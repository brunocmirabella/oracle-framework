# Quick Start — Oracle in 30 minutes

Get Oracle running on Telegram, reading your emails, and answering in your voice — with zero local infrastructure. No Obsidian, NotebookLM, n8n, or local AI models required for this first setup.

You can add all of that later. This gets you to a working Oracle in one sitting.

---

## What you'll have at the end

- Oracle answers your Telegram messages
- Reads and drafts emails in your voice
- Knows your identity, priorities, and communication style
- Persists basic memory across sessions (memory cards)

**Time:** ~30 minutes
**Cost:** Claude Pro or Team plan (~$20/month)

---

## Prerequisites

- [ ] [Node.js 18+](https://nodejs.org) installed
- [ ] Anthropic account with Claude Pro or Team plan
- [ ] Telegram account
- [ ] Google account (for Gmail)

---

## Step 1 — Install Claude Code CLI (5 min)

```bash
npm install -g @anthropic/claude-code
claude --version
```

On first launch, Claude Code will open a browser for authentication. Log in with your Anthropic account.

Verify it works:
```bash
claude
# → Claude Code starts. Type "hello" and press Enter.
```

---

## Step 2 — Set up your Telegram bot (5 min)

**2a — Create a bot:**
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose a name and username (e.g. `MyOracleBot`)
4. BotFather gives you a **bot token** — save it

**2b — Get your chat ID:**
1. Start a conversation with your new bot (press Start)
2. Go to: `https://api.telegram.org/bot[YOUR_TOKEN]/getUpdates`
3. Find `"chat":{"id":XXXXXXX}` — that number is your chat ID

**2c — Install the Telegram plugin:**
```bash
bun --version   # if not installed: npm install -g bun
```

In a Claude Code session:
```
/telegram:configure
```

Follow the prompts and paste your bot token.

**Test:** send "hello" from Telegram to your bot. The message should appear in your Claude Code terminal.

---

## Step 3 — Fill in your identity (10 min)

This is the most important step. It's what makes Oracle sound like you.

```bash
cp CLAUDE.md.template ~/CLAUDE.md
```

Open `~/CLAUDE.md` and fill in:

- **Your name and Oracle's name** — what you want to call your AI
- **How Oracle speaks** — language, tone (direct/warm/technical), any specific style
- **Your priorities** — what matters most (project 1, project 2, etc.)
- **Telegram chat_id** — from Step 2b
- **Profile files path** — leave as placeholder for now

Minimum viable fill-in (everything else is optional for now):

```markdown
## Identity
You are [NAME], the personal AI of [YOUR NAME].
You speak in [language], [tone].

## Communication Channels
Primary: Telegram (chat_id: [YOUR_CHAT_ID])
Always reply with the reply tool — not text output.

## Priorities
1. [Your top priority]
2. [Second priority]
```

---

## Step 4 — Set up memory cards (3 min)

Memory cards give Oracle persistent context without Obsidian.

```bash
mkdir -p ~/.claude/projects/oracle/memory
cp memory/user_profile.md.template ~/.claude/projects/oracle/memory/user_profile.md
cp memory/MEMORY.md.template ~/.claude/projects/oracle/memory/MEMORY.md
```

Open `~/.claude/projects/oracle/memory/user_profile.md` and fill in your professional profile: role, current projects, key collaborators, communication preferences.

---

## Step 5 — Connect Gmail (3 min)

1. Go to [claude.ai/settings/connectors](https://claude.ai/settings/connectors)
2. Click **Connect** next to Gmail
3. Authorize with your Google account

That's it — no MCP install needed. Oracle can now search, read, and draft emails.

**Optional:** connect Google Calendar the same way for event management and reminders.

---

## Step 6 — First test (5 min)

Open a Claude Code session:
```bash
claude
```

From Telegram, send:
```
check my unread emails
```

Oracle should read your Gmail and summarize what needs attention.

Then try:
```
draft an email to [contact name] about [topic]
```

Check Gmail drafts — you should see the draft waiting for your review.

---

## You're live

Oracle is now running. Start using it for 1-2 weeks before adding anything else.

**Useful first commands from Telegram:**
- `check emails` — read and triage inbox
- `what's on my calendar today` — today's events
- `write a LinkedIn post about [topic]` — social content in your voice
- `remind me about [X] tomorrow at 9` — calendar event
- `research [topic]` — web research and summary

---

## What to add next

Once the basics feel natural, add layers in this order:

| Layer | What it adds | Guide |
|-------|-------------|-------|
| **Soul Document** | Oracle sounds deeply like you | [SOUL_INTERVIEW.md](SOUL_INTERVIEW.md) |
| **Obsidian hooks** | Oracle remembers across sessions | [HOOKS_GUIDE.md](HOOKS_GUIDE.md) |
| **Brave Search MCP** | Real-time web search | [MCP_GUIDE.md](MCP_GUIDE.md) |
| **Skills** | Specialized agents (email, calendar, research) | [skills/examples/](../skills/examples/) |
| **n8n** | Social publishing, automation | [N8N_WORKFLOWS.md](N8N_WORKFLOWS.md) |
| **NotebookLM** | Permanent knowledge base | [HOOKS_GUIDE.md](HOOKS_GUIDE.md) |
| **Remote Triggers** | Autonomous scheduled agents | [HEARTBEAT_GUIDE.md](HEARTBEAT_GUIDE.md) |

Full setup guide (2-3 hours): [SETUP.md](SETUP.md)
