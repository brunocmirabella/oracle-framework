# autoDream — Memory Consolidation System

autoDream is Oracle's memory maintenance engine. It runs automatically at the end of every Claude Code session, keeping your memory files healthy and preparing context for the next session.

Inspired by the autoDream feature discovered in Claude Code's source (via leaked sourcemaps, March 2026).

---

## What it does

autoDream runs four phases silently in the background after each session:

```
Session ends
     │
     ▼
┌─────────────────────────────────────────────┐
│  Phase 1: ORIENT                             │
│  Scan all memory files. Note sizes.          │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  Phase 2: GATHER SIGNAL                      │
│  Read session transcript. Find [DECISION]    │
│  markers. Check today's session note.        │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  Phase 3: CONSOLIDATE                        │
│  Write autodream_journal.md with what        │
│  needs attention next session.               │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  Phase 4: PRUNE                              │
│  Trim any memory file > 200 lines to 180.    │
│  Preserves frontmatter header.               │
└─────────────────────────────────────────────┘
```

---

## Setup

### 1. Copy the script

```bash
cp scripts/autodream.py ~/oracle-workspace/autodream.py
```

Edit the two config paths at the top of the file:
- `MEMORY_DIR` — your Claude Code project memory directory
- `VAULT` — your Obsidian vault path

### 2. Add as Stop hook

In `~/.claude/settings.json`, add to the `Stop` hooks array:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [{
          "type": "command",
          "command": "PYTHONIOENCODING=utf-8 py -3.11 \"/path/to/autodream.py\"",
          "timeout": 15,
          "async": true,
          "statusMessage": "autoDream: consolidating memory..."
        }]
      }
    ]
  }
}
```

### 3. Add to CLAUDE.md

Add this section to your dynamic boundary area in `CLAUDE.md`:

```markdown
### autoDream (automatic — Stop hook)
At session start: if `second-brain/autodream_journal.md` exists and has
entries for today, read it and act on any listed actions before proceeding.
```

---

## Dream Journal format

autoDream writes to `[VAULT]/autodream_journal.md`. Example output:

```markdown
## Dream 2026-04-01 09:15

### Memory files to consolidate:
- `user_profile.md` — 215 lines (8.3 KB)

> Next session: review this file and reduce to ~180 lines,
> keeping recent and high-value entries.

### Memory status: 4 files, 12.1 KB
```

At the start of your next session, Oracle reads this file and consolidates
as needed — no manual intervention required for the pruning phase.

---

## Decision tracking integration

During a session, mark important decisions in your output with `[DECISION]`:

```
[DECISION] migrated Oracle from OpenClaw to Claude Code — local inference no longer needed
```

autoDream picks up these markers from the session transcript and adds them
to the dream journal for logging in the next session.

For manual decision logging, use `brain.py`:

```bash
py brain.py save-decision "we chose X because Y"
```

Output: `second-brain/decisions/YYYY-MM-DD.md` (append-only, timestamped).

---

## Pruning behavior

- Files **under 200 lines**: untouched
- Files **over 200 lines**: trimmed to 180 lines
  - Frontmatter (YAML between `---`) is always preserved
  - Most recent content is kept (tail, not head)
  - A pruning comment is inserted: `<!-- autoDream pruned N lines on DATE -->`

The 200/180 line threshold matches the MEMORY.md index limit used by Claude Code's own memory system.

---

## Differences from Claude Code's autoDream

| Feature | Claude Code autoDream | Oracle autoDream |
|---------|----------------------|-----------------|
| Trigger | 24h interval + 5 sessions + lock | Every session (lightweight) |
| Consolidation | LLM-powered rewrites | Prepares signals, human-in-loop |
| Prune | Smart summarization | Mechanical tail-trim |
| Decision extraction | Implicit | Explicit `[DECISION]` markers |

Oracle's version is intentionally simpler: it prepares the work and lets
Claude do the intelligent consolidation at session start, rather than
running an LLM call in the background at session end.
