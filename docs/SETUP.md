# Oracle Framework — Setup Guide

Complete installation guide. Expected time: 2-3 hours for a full setup.

---

## Prerequisites

Before starting, you need:
- [ ] **Node.js 18+** — [nodejs.org](https://nodejs.org)
- [ ] **Anthropic account** with Claude Pro or Team plan
- [ ] **Telegram account** + a bot created via [@BotFather](https://t.me/BotFather)
- [ ] **Google account** (for Gmail + Calendar integration)
- [ ] `bun` runtime (for Telegram plugin): `npm install -g bun`

Optional (for advanced features):
- [ ] Python 3.10+ (for Obsidian integration scripts)
- [ ] Brave Search API key (for web search MCP)

---

## Step 1 — Install Claude Code CLI

```bash
npm install -g @anthropic/claude-code
claude --version
```

On first launch, follow the login link. Use your Anthropic account with a Pro or Team plan.

---

## Step 2 — Create your directory structure

```bash
mkdir -p ~/.claude/projects/oracle/memory
mkdir -p ~/.claude/skills
```

---

## Step 3 — Configure your identity (CLAUDE.md)

This is the most important step. Copy and fill in the template:

```bash
cp CLAUDE.md.template ~/CLAUDE.md
```

Open `~/CLAUDE.md` and fill in every section. Replace all `[PLACEHOLDERS]` with real information about yourself. The more specific, the better Oracle works.

---

## Step 4 — Write your Soul Document

```bash
cp soul-document/SOUL_DOCUMENT.md.template ~/oracle-workspace/SOUL_DOCUMENT.md
```

Set aside 1-2 hours to fill this in seriously. This is what makes Oracle sound like you.

If you want help: see [docs/SOUL_INTERVIEW.md](SOUL_INTERVIEW.md) for a guided process.

---

## Step 5 — Set up your workspace

Copy the workspace templates to your working directory:

```bash
mkdir -p ~/oracle-workspace
cp -r workspace-template/* ~/oracle-workspace/
```

Fill in the files in this order:
1. `USER.md` — your professional profile
2. `VOICE.md` — your communication style (include real email examples)
3. `CONTACTS.md` — key people Oracle should know
4. `HEARTBEAT.md` — topics, KPIs, and recurring tasks for autonomous agents
5. `AGENTS.md` and `TOOLS.md` — update after configuring MCPs and skills

---

## Step 5b — Set up memory cards

```bash
cp memory/user_profile.md.template ~/.claude/projects/oracle/memory/user_profile.md
cp memory/MEMORY.md.template ~/.claude/projects/oracle/memory/MEMORY.md
```

Fill in `user_profile.md` with your professional context.

---

## Step 6 — Install skills

```bash
cp -r skills/examples/* ~/.claude/skills/
```

Fill in all `[PLACEHOLDERS]` in each `SKILL.md`. Or write your own skills using `skills/SKILL.md.template`.

---

## Step 7 — Install MCP servers

Install the MCP servers Oracle needs:

```bash
# Browser automation (for Playwright-based tasks)
claude mcp add playwright -- npx @playwright/mcp@latest

# Web search
claude mcp add brave-search -- npx -y @modelcontextprotocol/server-brave-search
# (requires BRAVE_API_KEY in your environment)

# Sequential reasoning (for complex tasks)
claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking
```

Add your API keys to `~/.claude/settings.json`:
```json
{
  "env": {
    "BRAVE_API_KEY": "your-key-here"
  }
}
```

---

## Step 8 — Configure cloud MCP connectors

Go to [claude.ai/settings/connectors](https://claude.ai/settings/connectors) and connect:
- **Gmail** — for email drafting and reading
- **Google Calendar** — for scheduling and cron agents

These are required for Remote Triggers (cron agents) to work.

---

## Step 8b — Set up hooks (automatic context injection)

Hooks are what make Oracle proactively know your context. Without them, Oracle only knows what you explicitly tell it.

```bash
mkdir -p ~/.claude/hooks
```

Create `~/.claude/hooks/consult_nb_hook.py` and `~/.claude/hooks/consult_obsidian_hook.py` (see `docs/HOOKS_GUIDE.md` for templates and setup).

Add to `~/.claude/settings.json`:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {"type": "command", "command": "python ~/.claude/hooks/consult_nb_hook.py"},
          {"type": "command", "command": "python ~/.claude/hooks/consult_obsidian_hook.py"}
        ]
      }
    ]
  }
}
```

Full guide: [docs/HOOKS_GUIDE.md](HOOKS_GUIDE.md)

---

## Step 9 — Set up Telegram

In your Claude Code terminal, run:
```
/telegram:configure
```

Follow the prompts. You'll need:
- Your bot token from BotFather
- `bun` installed

Test it: open Telegram and send a message to your bot. It should appear as a `<channel source="telegram">` tag in your Claude Code session.

---

## Step 10 — Configure Remote Triggers (optional)

For autonomous scheduled agents:
1. Go to [claude.ai/code/scheduled](https://claude.ai/code/scheduled)
2. Use templates from `cron/REMOTE_TRIGGERS.md`
3. Fill in all placeholders
4. Select required MCP connectors
5. Set your cron schedule

---

## Step 11 — First run

Open a terminal and run:
```bash
claude
```

Say hello to Oracle. Test a skill trigger. Check that Telegram is working.

---

## Troubleshooting

**Telegram not receiving messages:**
- Check that the plugin is active in `~/.claude/settings.json`
- Verify `bun` is installed: `bun --version`
- Restart the Claude Code session

**MCP not connecting:**
- Check `claude mcp list` to see installed servers
- Verify API keys are set correctly in settings.json
- Some MCPs need the Node version cache cleared: `npx clear-npx-cache`

**Skills not activating:**
- Skills must be in `~/.claude/skills/[skill-name]/SKILL.md`
- The trigger phrase must be in the CLAUDE.md or the SKILL.md itself
- Check spelling of trigger phrases

---

## Next steps

Once everything is running:
1. Use Oracle for a full week before tweaking anything
2. Update your Soul Document after 30 days (you'll know more about what you want)
3. Add domain-specific skills for your work
4. Set up NotebookLM as your permanent knowledge base and link it to Oracle
