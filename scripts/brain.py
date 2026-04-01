#!/usr/bin/env python3
"""
brain.py — Oracle second brain CLI.
Interface between Oracle (Claude Code) and your Obsidian vault.

Usage:
  py brain.py read sessioni/2026-03-21
  py brain.py write note/idea "# Title\n\nContent"
  py brain.py append sessioni/2026-03-21 "## Update\n- new thing"
  py brain.py list sessioni
  py brain.py search "keyword"
  py brain.py oggi                            # read/create today's session
  py brain.py save-session "text"             # Oracle updates its own section
  py brain.py save-claude "text"              # Claude Code updates its section
  py brain.py save-decision "we chose X because Y"   # log a decision
  py brain.py progetto <name>                 # read/create a project note

Decision tracking:
  Decisions are distinct from actions.
  Not "I updated CONTACTS.md" but "we decided to migrate Oracle to Claude Code
  because Ollama was unreliable and we no longer needed local inference."
  Use save-decision for: architectural choices, tool migrations, project pivots,
  dismissals, strategic calls. NOT for: completed tasks, file updates, routine ops.

  Output: second-brain/decisions/YYYY-MM-DD.md (append-only, timestamped)

Setup:
  1. Copy to your oracle-workspace/
  2. Update VAULT path below to your Obsidian vault
  3. Add to CLAUDE.md:
       py "path/to/brain.py" save-decision "text"
       py "path/to/brain.py" save-claude "text"
"""

import sys
from pathlib import Path
from datetime import date, datetime

# ---------------------------------------------------------------------------
# Config — update this path
# ---------------------------------------------------------------------------

VAULT = Path("[YOUR-VAULT-PATH]")  # e.g. ~/oracle-workspace/second-brain
TODAY = date.today().isoformat()

SESSION_TEMPLATE = """\
---
date: {date}
tags: [session]
agents: [claude-code]
---

# Session {date}

## What we did
-

## Decisions made
-

## Next steps
-

## Oracle notes
<!-- Oracle updates this section -->

## Claude Code notes
<!-- Claude Code updates this section -->
"""

# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_read(args):
    if not args:
        print("Usage: brain.py read <note-path>"); return
    p = _resolve(args[0])
    if not p.exists():
        print(f"Note not found: {p}"); return
    print(p.read_text(encoding="utf-8"))

def cmd_write(args):
    if len(args) < 2:
        print("Usage: brain.py write <path> <content>"); return
    p = _resolve(args[0])
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(args[1].replace("\\n", "\n"), encoding="utf-8")
    print(f"[OK] Written: {p.relative_to(VAULT)}")

def cmd_append(args):
    if len(args) < 2:
        print("Usage: brain.py append <path> <text>"); return
    p = _resolve(args[0])
    if not p.exists():
        print(f"Note not found: {p}"); return
    existing = p.read_text(encoding="utf-8")
    p.write_text(existing + "\n" + args[1].replace("\\n", "\n"), encoding="utf-8")
    print(f"[OK] Updated: {p.relative_to(VAULT)}")

def cmd_list(args):
    folder = VAULT / (args[0] if args else "")
    if not folder.exists():
        print(f"Folder not found: {folder}"); return
    files = sorted(folder.rglob("*.md"))
    for f in files:
        print(f"  {str(f.relative_to(VAULT)):50s}  {f.stat().st_size:6d} bytes")
    print(f"\n{len(files)} notes found")

def cmd_search(args):
    if not args:
        print("Usage: brain.py search <keyword>"); return
    keyword = " ".join(args).lower()
    results = []
    for f in VAULT.rglob("*.md"):
        content = f.read_text(encoding="utf-8", errors="ignore")
        if keyword in content.lower():
            lines = [l.strip() for l in content.split("\n") if keyword in l.lower()]
            results.append((f.relative_to(VAULT), lines[:2]))
    if not results:
        print(f"No results for: {keyword}"); return
    for path, lines in results:
        print(f"\n[note] {path}")
        for l in lines:
            print(f"   {l[:100]}")
    print(f"\n{len(results)} notes found")

def cmd_oggi(args):
    p = VAULT / "sessions" / f"{TODAY}.md"
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(SESSION_TEMPLATE.format(date=TODAY), encoding="utf-8")
        print(f"[OK] Created: {p.name}")
    print(p.read_text(encoding="utf-8"))

def cmd_save_session(args, section="## Oracle notes"):
    if not args:
        print("Usage: brain.py save-session <text>"); return
    text = " ".join(args).replace("\\n", "\n")
    p = VAULT / "sessions" / f"{TODAY}.md"
    if not p.exists():
        cmd_oggi([])
    content = p.read_text(encoding="utf-8")
    if section in content:
        parts = content.split(section)
        after = parts[1]
        next_section = after.find("\n## ")
        if next_section == -1:
            new_after = f"\n{text}\n"
        else:
            new_after = f"\n{text}\n" + after[next_section:]
        content = parts[0] + section + new_after
    else:
        content += f"\n{section}\n{text}\n"
    p.write_text(content, encoding="utf-8")
    print(f"[OK] {section.strip()} updated in sessions/{TODAY}.md")

def cmd_save_claude(args):
    cmd_save_session(args, section="## Claude Code notes")

def cmd_save_decision(args):
    """Log a decision to decisions/YYYY-MM-DD.md (append-only).

    Decisions are WHAT and WHY, not WHAT was done.
    Example: "migrated Oracle from OpenClaw/Ollama to Claude Code because
              Ollama was unreliable and local inference no longer needed"
    """
    if not args:
        print("Usage: brain.py save-decision \"we chose X because Y\""); return
    text = " ".join(args).replace("\\n", "\n")
    p = VAULT / "decisions" / f"{TODAY}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(f"# Decisions {TODAY}\n\n", encoding="utf-8")
    ts = datetime.now().strftime("%H:%M")
    entry = f"- [{ts}] {text}\n"
    with open(p, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"[OK] Decision logged in decisions/{TODAY}.md")

def cmd_progetto(args):
    if not args:
        print("Usage: brain.py progetto <name>"); return
    name = args[0].lower().replace(" ", "-")
    p = VAULT / "projects" / f"{name}.md"
    if p.exists():
        print(p.read_text(encoding="utf-8"))
    else:
        content = f"# {name}\n\n## Status\n-\n\n## Notes\n-\n"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        print(f"[OK] Created project: {p.name}")
        print(content)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve(path_str: str) -> Path:
    p = VAULT / path_str
    if not p.suffix:
        p = p.with_suffix(".md")
    return p

# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

COMMANDS = {
    "read":          cmd_read,
    "write":         cmd_write,
    "append":        cmd_append,
    "list":          cmd_list,
    "search":        cmd_search,
    "oggi":          cmd_oggi,
    "save-session":  cmd_save_session,
    "save-claude":   cmd_save_claude,
    "save-decision": cmd_save_decision,
    "progetto":      cmd_progetto,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(0)
    COMMANDS[sys.argv[1]](sys.argv[2:])
