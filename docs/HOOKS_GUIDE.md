# Hooks Guide — Automatic Context Injection

Hooks are Oracle's nervous system. They fire automatically before and after your messages, injecting live context without you doing anything.

---

## What hooks do

Without hooks, Oracle only knows what you tell it in the current message.

With hooks, Oracle automatically knows:
- What you're working on today (from Obsidian)
- Relevant knowledge from your permanent archive (from NotebookLM)
- ...before it says a single word

This is how Oracle answers questions with context you never explicitly provided.

---

## Hook types

Claude Code supports two hook types relevant to Oracle:

| Type | When it fires | Use case |
|------|--------------|---------|
| `UserPromptSubmit` | Before each message you send | Inject Obsidian session + NotebookLM context |
| `PostToolUse` | After a tool runs | Auto-update Obsidian, format output |

---

## Setting up hooks

Hooks are configured in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/hooks/consult_nb_hook.py"
          },
          {
            "type": "command",
            "command": "python ~/.claude/hooks/consult_obsidian_hook.py"
          }
        ]
      }
    ]
  }
}
```

The `matcher` is empty — hooks fire on every message.

---

## The NotebookLM hook

**File:** `~/.claude/hooks/consult_nb_hook.py`

**What it does:**
1. Takes your message as input (passed via stdin)
2. Calls `ask_question.py` with your message as a query
3. NotebookLM searches your notebooks and returns relevant excerpts
4. The hook injects the result as a system message before your prompt

**Setup requirements:**
- NotebookLM notebook URL configured in your hook script
- `patchright` installed: `pip install patchright`
- Ask question script: `~/.claude/skills/notebooklm/scripts/ask_question.py`

**How NotebookLM integration works:**

```
Your message → hook script → ask_question.py → Chrome (headless)
    → NotebookLM API → relevant excerpts
    → injected as [NotebookLM context] before your prompt
```

This means every time you ask Oracle something, it has already searched your knowledge base.

---

## The Obsidian hook

**File:** `~/.claude/hooks/consult_obsidian_hook.py`

**What it does:**
1. Reads today's session note from your Obsidian vault
2. Injects it as context: what you've done today, open tasks, decisions made

**Setup requirements:**
- Obsidian vault path configured in the script
- Either direct file access or Obsidian REST API (port 27123)

**Session note format Oracle writes:**

```markdown
---
date: 2026-01-15
tags: [sessione]
---

# Session 2026-01-15

## What we did
- Drafted email to Marco re: partnership
- Researched Q1 funding rounds

## Decisions made
- Postpone product launch to March
- Focus on Series A preparation

## Next steps
- Follow up with Marco
- Prepare pitch deck

## Oracle notes
[Oracle updates this section during the session]
```

---

## Writing session notes

Oracle updates Obsidian during sessions. You can trigger this with:
- `save note: [content]`
- `update obsidian: [content]`
- Any instruction involving "ricorda" or "salva"

**Via REST API (if Obsidian is running):**
```python
# ~/.claude/scripts/obsidian_api.py
import requests

def save_note(content, vault_path, note_name):
    url = f"http://localhost:27123/vault/{note_name}"
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    requests.put(url, data=content, headers=headers)
```

**Via direct file write (always works):**
```python
from pathlib import Path

vault = Path("/path/to/your/obsidian/vault")
today = "2026-01-15"
note_path = vault / "sessions" / f"{today}.md"
note_path.write_text(content)
```

---

## Hook output format

Hooks inject context in this format (visible in your terminal):

```
[NotebookLM context]
---
From your knowledge base (query: "Marco partnership"):

In the meeting notes from December, Marco expressed interest in a revenue-share model...
---

[Obsidian — Your live memory (RAM)]
=== Today's session ===
...
[End Obsidian]
```

Oracle reads this before formulating its response.

---

## Troubleshooting

**Hook not firing:**
- Check `~/.claude/settings.json` syntax (must be valid JSON)
- Verify script path is absolute
- Test the script manually: `echo "test query" | python ~/.claude/hooks/consult_nb_hook.py`

**NotebookLM context empty:**
- Verify the notebook URL in the script
- Check that `patchright` is installed
- On Windows: ensure no console window issues (see `ask_question.py` preamble)

**Obsidian context not loading:**
- Check vault path in the hook script
- If using REST API: verify Obsidian is running and the plugin is active
- Fall back to direct file read if API is unavailable

---

## Advanced: chaining hooks

You can stack multiple hooks. They run sequentially and all inject context:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {"type": "command", "command": "python ~/.claude/hooks/consult_nb_hook.py"},
          {"type": "command", "command": "python ~/.claude/hooks/consult_obsidian_hook.py"},
          {"type": "command", "command": "python ~/.claude/hooks/inject_contacts.py"}
        ]
      }
    ]
  }
}
```

Each hook adds its context block. Oracle sees all of them.

---

## PostToolUse hook example

Auto-update Obsidian after Oracle writes a file:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {"type": "command", "command": "python ~/.claude/hooks/log_file_write.py"}
        ]
      }
    ]
  }
}
```

This logs every file Oracle creates or edits to your session note automatically.
