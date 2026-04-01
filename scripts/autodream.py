#!/usr/bin/env python3
"""
autoDream — Oracle memory consolidation system.
Inspired by the autoDream feature found in Claude Code's leaked source.

Runs as a Stop hook after every Claude Code session.
No LLM calls needed — prepares signals for the next session to act on.

Four phases:
  1. ORIENT    — scan memory files, detect sizes
  2. GATHER    — collect signals from the just-closed session
  3. CONSOLIDATE — write autodream_journal.md with what needs attention
  4. PRUNE     — trim memory files over MAX_LINES to PRUNE_TO lines

Trigger: every session (lightweight when nothing to do).
Lock: .autodream.lock prevents concurrent runs.

Setup:
  1. Copy this file to your oracle-workspace/ directory
  2. Add as Stop hook in ~/.claude/settings.json:

     "Stop": [{
       "hooks": [{
         "type": "command",
         "command": "PYTHONIOENCODING=utf-8 py -3.11 \"/path/to/autodream.py\"",
         "timeout": 15,
         "async": true,
         "statusMessage": "autoDream: consolidating memory..."
       }]
     }]

  3. Add to CLAUDE.md:
     At session start, check autodream_journal.md in your vault if it exists.
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, date

# ---------------------------------------------------------------------------
# Config — update these paths for your setup
# ---------------------------------------------------------------------------

MEMORY_DIR  = Path.home() / ".claude" / "projects" / "[YOUR-PROJECT]" / "memory"
VAULT       = Path("[YOUR-VAULT-PATH]")       # e.g. ~/oracle-workspace/second-brain
DREAM_FILE  = VAULT / "autodream_journal.md"
LOCK_FILE   = MEMORY_DIR / ".autodream.lock"
MAX_LINES   = 200
PRUNE_TO    = 180
TODAY       = date.today().isoformat()
NOW         = datetime.now().strftime("%H:%M")

# ---------------------------------------------------------------------------
# Lock — prevents concurrent runs
# ---------------------------------------------------------------------------

def acquire_lock() -> bool:
    if LOCK_FILE.exists():
        try:
            ts = float(LOCK_FILE.read_text().strip())
            if datetime.now().timestamp() - ts > 600:  # stale after 10 min
                LOCK_FILE.unlink()
            else:
                return False
        except Exception:
            LOCK_FILE.unlink(missing_ok=True)
    LOCK_FILE.write_text(str(datetime.now().timestamp()))
    return True

def release_lock():
    LOCK_FILE.unlink(missing_ok=True)

# ---------------------------------------------------------------------------
# Phase 1: ORIENT — scan memory files
# ---------------------------------------------------------------------------

def orient() -> dict:
    result = {"files": [], "oversized": []}
    if not MEMORY_DIR.exists():
        return result
    for f in MEMORY_DIR.glob("*.md"):
        lines = len(f.read_text(encoding="utf-8", errors="ignore").splitlines())
        size_kb = round(f.stat().st_size / 1024, 1)
        entry = {"path": f, "name": f.name, "lines": lines, "size_kb": size_kb}
        result["files"].append(entry)
        if lines > MAX_LINES:
            result["oversized"].append(entry)
    return result

# ---------------------------------------------------------------------------
# Phase 2: GATHER SIGNAL — extract signals from session transcript
# ---------------------------------------------------------------------------

def gather(transcript_path: str | None) -> dict:
    signals = {"decisions": [], "session_date": TODAY}

    if transcript_path and Path(transcript_path).exists():
        try:
            with open(transcript_path, encoding="utf-8", errors="ignore") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        content = ""
                        if entry.get("type") == "assistant":
                            for block in entry.get("message", {}).get("content", []):
                                if isinstance(block, dict) and block.get("type") == "text":
                                    content += block.get("text", "")
                        # Look for [DECISION] markers in assistant output
                        if "[DECISION]" in content:
                            matches = re.findall(r'\[DECISION\]\s*(.+?)(?:\n|$)', content)
                            signals["decisions"].extend(m.strip() for m in matches)
                    except Exception:
                        continue
        except Exception:
            pass

    return signals

# ---------------------------------------------------------------------------
# Phase 3: CONSOLIDATE — prepare dream journal for next session
# ---------------------------------------------------------------------------

def consolidate(orient_data: dict, signals: dict):
    DREAM_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = DREAM_FILE.read_text(encoding="utf-8") if DREAM_FILE.exists() else ""

    entry_lines = [f"\n## Dream {TODAY} {NOW}"]

    if orient_data["oversized"]:
        entry_lines.append("\n### Memory files to consolidate:")
        for f in orient_data["oversized"]:
            entry_lines.append(f"- `{f['name']}` — {f['lines']} lines ({f['size_kb']} KB)")
        entry_lines.append(
            "\n> Next session: review these files and reduce to ~180 lines,"
            " keeping recent and high-value entries."
        )

    if signals["decisions"]:
        entry_lines.append("\n### Decisions to log:")
        for d in signals["decisions"]:
            entry_lines.append(f"- {d}")
        entry_lines.append(
            "\n> Add these to your decision log:"
            " `py brain.py save-decision \"text\"`"
        )

    total_files = len(orient_data["files"])
    total_kb = round(sum(f["size_kb"] for f in orient_data["files"]), 1)
    entry_lines.append(f"\n### Memory status: {total_files} files, {total_kb} KB")

    if not orient_data["oversized"] and not signals["decisions"]:
        entry_lines.append("All clean — no action required.")

    entry = "\n".join(entry_lines) + "\n"

    # Keep journal under 300 lines
    lines = existing.splitlines()
    if len(lines) > 300:
        existing = "\n".join(lines[-250:]) + "\n"

    if f"## Dream {TODAY}" in existing:
        existing = re.sub(
            rf"\n## Dream {TODAY}.*?(?=\n## Dream |\Z)",
            entry,
            existing,
            flags=re.DOTALL
        )
    else:
        existing += entry

    DREAM_FILE.write_text(existing, encoding="utf-8")

# ---------------------------------------------------------------------------
# Phase 4: PRUNE — trim oversized memory files
# ---------------------------------------------------------------------------

def prune(orient_data: dict) -> list[str]:
    pruned = []
    for entry in orient_data["oversized"]:
        f: Path = entry["path"]
        try:
            lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()

            # Preserve frontmatter header (--- ... ---)
            header_end = 0
            if lines and lines[0].strip() == "---":
                for i, line in enumerate(lines[1:], 1):
                    if line.strip() == "---":
                        header_end = i + 1
                        break
            header = lines[:header_end]
            body = lines[header_end:]

            keep = max(50, PRUNE_TO - len(header))
            if len(body) > keep:
                note = f"<!-- autoDream pruned {len(body) - keep} lines on {TODAY} -->"
                new_content = "\n".join(header + [note] + body[-keep:]) + "\n"
                f.write_text(new_content, encoding="utf-8")
                pruned.append(f"{f.name} ({len(lines)} → {len(header) + keep + 1} lines)")
        except Exception as e:
            pruned.append(f"ERROR on {f.name}: {e}")
    return pruned

# ---------------------------------------------------------------------------
# Main — Stop hook entry point
# ---------------------------------------------------------------------------

def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}

    transcript_path = data.get("transcript_path")

    if not acquire_lock():
        print(json.dumps({"continue": True}))
        return

    try:
        orient_data = orient()
        signals = gather(transcript_path)
        consolidate(orient_data, signals)
        pruned = prune(orient_data)

        parts = []
        if pruned:
            parts.append(f"Pruned: {', '.join(pruned)}")
        if signals["decisions"]:
            parts.append(f"Decisions found: {len(signals['decisions'])}")
        if parts:
            print(f"[autoDream] {' | '.join(parts)}", file=sys.stderr)

    finally:
        release_lock()

    print(json.dumps({"continue": True}))


if __name__ == "__main__":
    main()
