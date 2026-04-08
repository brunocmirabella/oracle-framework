# MCP Guide — Which servers to install and why

MCP (Model Context Protocol) servers connect Oracle to external services. This guide explains which ones matter, what they do, and how to install them.

---

## Essential (install these first)

### Gmail
Lets Oracle read, search, and draft emails.

**Setup:** Go to [claude.ai/settings/connectors](https://claude.ai/settings/connectors) → Connect Gmail
**What Oracle can do:** Search threads, read emails, create drafts, list labels
**What Oracle cannot do without your confirmation:** Send emails

### Google Calendar
Lets Oracle read and create calendar events.

**Setup:** [claude.ai/settings/connectors](https://claude.ai/settings/connectors) → Connect Google Calendar
**What Oracle can do:** List events, create events, find free time, set reminders
**Required for:** Remote Triggers (cron agents need this to send morning briefings)

---

## Recommended

### Playwright (browser automation)
Lets Oracle control a real browser — navigate websites, fill forms, take screenshots, click elements.

```bash
claude mcp add playwright -- npx @playwright/mcp@latest
```

**Use cases:**
- Automate tasks on web platforms (your CRM, project management tools, etc.)
- Extract data from websites that don't have APIs
- Run workflows in apps that don't have MCP connectors yet

**Note:** Playwright works on your local machine. Remote Triggers (cloud cron) cannot use Playwright.

### Brave Search
Web search with privacy focus. No tracking, good results for research.

```bash
claude mcp add brave-search -- npx -y @modelcontextprotocol/server-brave-search
```

Get your free API key at [brave.com/search/api](https://brave.com/search/api/) (2000 queries/month free).

Add to `~/.claude/settings.json`:
```json
{
  "env": {
    "BRAVE_API_KEY": "your-key-here"
  }
}
```

### Sequential Thinking
Helps Oracle reason through complex multi-step problems more reliably.

```bash
claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking
```

**Use when:** The task has multiple interdependent steps, or when precision matters more than speed.

---

## Optional (domain-specific)

### GitHub
For developers. Lets Oracle interact with your repos, issues, and PRs.

```bash
claude mcp add github -- npx -y @modelcontextprotocol/server-github
```

Requires `GITHUB_TOKEN` environment variable.

### Notion
If you use Notion as a knowledge base or project tracker.

```bash
claude mcp add notion -- npx -y @notionhq/notion-mcp-server
```

Requires `NOTION_API_KEY`.

### Filesystem
Direct access to your local files. Oracle already has file access via built-in tools, but this MCP allows more granular path configuration.

```bash
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /path/to/your/workspace
```

### MCPControl (Desktop automation)
Lets Oracle control your mouse, keyboard, and screen — take screenshots, click elements, type text, read clipboard. Enables full desktop automation for apps that don't have APIs or web interfaces.

**Install:** See [github.com/Anthropic-Community/mcp-control](https://github.com/Anthropic-Community/mcp-control) or search for `mcp-control` in your MCP registry.

**What Oracle can do:**
- Take screenshots and analyze what's on screen
- Click, type, scroll in any application
- Read/write clipboard content
- Control any desktop app (CRM, design tools, legacy software)

**Use cases:**
- Automate tasks in apps without APIs
- Screen recording and monitoring
- UI testing and demonstration
- Control tools that only exist as desktop apps

**Note:** Only available in local sessions. Remote Triggers (cloud cron) cannot control your desktop.

---

## Cloud connectors (claude.ai/settings/connectors)

Beyond local MCP servers, Claude Code integrates with cloud services:

| Service | Use case |
|---------|----------|
| Canva | Generate and edit graphics, social posts, presentations |
| Gamma | AI-generated slide decks from text |
| Notion | Cloud access (alternative to local MCP) |
| Hugging Face | Search ML models and research papers |
| Indeed | Job market research |

These connectors are available to both local sessions and Remote Triggers.

---

## n8n — Local Automation Hub

n8n is the missing piece between Oracle and the outside world. While MCP servers let Oracle *read and draft*, n8n lets Oracle *publish and trigger* — across social platforms, CRMs, webhooks, and more.

**Install:**
```bash
npm install -g n8n
n8n start
# runs at http://localhost:5678
```

**How Oracle uses n8n:**

Oracle doesn't talk to n8n directly — it outputs files or calls webhooks, and n8n picks them up:

```
Oracle writes post → saves JSON → n8n watches folder → posts to Instagram + LinkedIn
Oracle finishes briefing → triggers webhook → n8n sends WhatsApp summary
Oracle logs contact → n8n syncs to HubSpot / Notion CRM
```

**Recommended n8n workflows:**

| Workflow | Trigger | Output |
|----------|---------|--------|
| Social publish | File created in /oracle-out/social/ | Post to IG + LI + FB |
| WhatsApp summary | Webhook from Oracle | Send formatted summary |
| CRM contact sync | Webhook | Update HubSpot / Notion DB |
| Content calendar | Schedule (n8n cron) | Pull from Notion → post |
| Email alert | New Gmail label | Notify Oracle via file |

**Why n8n over Zapier/Make:**
- Runs locally — your data never leaves your machine
- Unlimited workflows (no plan limits)
- Full code nodes (JavaScript) for custom logic
- Direct integration with local files and webhooks

---

## Full connector map

A complete Oracle installation:

```
Oracle Core (Claude Code CLI)
│
├── MCP Local (installed via claude mcp add)
│   ├── Playwright          — browser automation
│   ├── Brave Search        — web research
│   ├── Sequential Thinking — complex reasoning
│   ├── GitHub              — code repos
│   ├── Notion              — knowledge base
│   ├── Filesystem          — local files
│   └── Telegram plugin     — mobile interface
│
├── Cloud Connectors (claude.ai/settings/connectors)
│   ├── Gmail               — email
│   ├── Google Calendar     — calendar
│   ├── Canva               — graphics
│   ├── Gamma               — slide decks
│   ├── Notion              — cloud KB
│   ├── Hugging Face        — ML research
│   ├── Indeed              — job market
│   └── Replicate           — image/video generation
│
├── Memory Layer
│   ├── Memory cards        — immediate context (files)
│   ├── Obsidian            — session RAM (vault)
│   └── NotebookLM          — permanent HD (structured docs)
│
└── n8n (localhost:5678)
    ├── Social publishing   — IG, LinkedIn, Facebook
    ├── CRM sync            — HubSpot, Notion DB
    ├── Messaging           — WhatsApp, Slack
    └── Webhook routing     — any HTTP endpoint
```

---

## Power tier — Full computer control

These integrations unlock Oracle's most powerful capabilities: native control of your PC and voice interaction.

### MCPControl (computer takeover)

Gives Oracle eyes and hands on your desktop. It can move the mouse, click, type, take screenshots, read what's on screen — and act on any app that doesn't have an API.

```bash
npm install -g mcp-control
claude mcp add mcp-control -- npx mcp-control
```

**What Oracle can do:**
- Take screenshots and "see" what's on screen
- Click buttons and fill forms in any desktop app
- Type into any window (terminal, email client, design tool)
- Automate workflows across apps that don't have APIs
- Control Premiere Pro, Photoshop, any local software

**Use cases:**
- Automate repetitive tasks in legacy tools
- Watch a screen and react to what appears
- Control creative tools (video editors, DAWs) via natural language

### Voice transcription (local Whisper)

Oracle can transcribe audio files locally — no cloud, no API cost.

```bash
pip install openai-whisper
```

**Usage:**
```bash
python -c "import whisper; m=whisper.load_model('base'); r=m.transcribe('file.mp3', language='en'); print(r['text'])"
```

**Models:** `tiny` (fast), `base` (balanced), `medium`/`large` (accurate for noisy audio)

**Use cases:**
- Transcribe meeting recordings → meeting-reporter skill
- Process voice messages from Telegram
- Convert spoken notes to text

### Voice reply — Telegram voice messages (edge-tts)

Oracle can respond with voice messages on Telegram — not just text. Useful for conversational interactions, mobile briefings, or any context where listening is more natural than reading.

**Install:**
```bash
pip install edge-tts
# Also requires ffmpeg (system install — must be in PATH)
```

**Script:** `scripts/oracle_tts.py` — converts text to OGG Opus, the format Telegram uses for voice messages.

**Usage from CLAUDE.md:**
```python
import subprocess
result = subprocess.run(
    ["python", "/path/to/scripts/oracle_tts.py", "Text to speak"],
    capture_output=True, text=True
)
ogg_path = result.stdout.strip()
# then attach to Telegram reply: reply(..., files=[ogg_path])
```

**Voice selection:** Edit `DEFAULT_VOICE` in `oracle_tts.py`. Full list: `edge-tts --list-voices`
- English: `en-US-AriaNeural`, `en-GB-SoniaNeural`
- Italian: `it-IT-IsabellaNeural`
- Spanish: `es-ES-ElviraNeural`
- French: `fr-FR-DeniseNeural`

**Trigger in CLAUDE.md:** When the user sends a voice message or requests a voice reply, generate the audio and attach it to the Telegram reply via `files: [ogg_path]`.

**Cost:** Free — uses Microsoft Edge TTS network endpoint. No API key required. Requires internet and ffmpeg for MP3 to OGG Opus conversion.

### WhatsApp bridge

Oracle can monitor WhatsApp messages via a local bridge and summarize or route them — but never replies autonomously.

**How it works:**
1. Bridge script connects to WhatsApp Web and exposes a local interface
2. Oracle reads incoming messages via file polling or local webhook
3. Oracle summarizes and routes — but never sends without explicit confirmation

**Non-negotiable rules (must be in CLAUDE.md):**
- Never reply in group chats
- Never reply autonomously — only draft responses for review
- Only send with explicit confirmation from you
- Priority contacts trigger immediate notifications to you (via Telegram), not to them

**Use cases:**
- Morning briefing: Oracle scans overnight messages and summarizes action items
- Priority alerts: specific senders → instant Telegram notification to you
- Batch processing: Oracle drafts replies for your review in bulk

**Implementation options:**
- [whatsapp-web.js](https://github.com/pedroslopez/whatsapp-web.js) — Node.js, widely used
- [WPPConnect](https://github.com/wppconnect-team/wppconnect) — alternative with more features
- n8n WhatsApp node — if you prefer GUI-based workflow management

**Note:** WhatsApp Web bridges operate in a grey zone of WhatsApp ToS. Use responsibly and only on accounts you own.

### Desktop control script

Beyond MCPControl (full mouse/keyboard access), you can expose a predefined set of OS-level commands through a simple local script. Safer for system operations like sleep, shutdown, or starting local services.

**Pattern (Linux/Mac):**
```bash
#!/bin/bash
# oracle-commands.sh
case "$1" in
  sleep)        pmset sleepnow ;;
  shutdown)     sudo shutdown -h now ;;
  restart)      sudo shutdown -r now ;;
  start-n8n)    n8n start & ;;
  start-ollama) ollama serve & ;;
  start-all)    n8n start & ollama serve & ;;
  *)            echo "Unknown command: $1"; exit 1 ;;
esac
```

On Windows, use a `.bat` file with `if "%1"=="sleep" ...` branching.

**In CLAUDE.md:**
```
PC Control script: /path/to/oracle-commands.sh [command]
Commands: sleep, shutdown, restart, start-n8n, start-ollama, start-all
Requires confirmation before: shutdown, restart, sleep
No confirmation needed for: starting services
```

**Why this over MCPControl for system ops:**
- Predefined, auditable set of allowed actions
- Oracle cannot trigger arbitrary system operations
- Works without MCPControl installed
- Easy to audit, extend, and version-control

### Email alerts via Telegram

Oracle watches your inbox and pushes Telegram notifications for unread emails — filtering by sender, subject keywords, or labels.

**How it works:**
1. A Remote Trigger runs on a schedule (e.g., every 30 min)
2. Oracle queries Gmail for unread messages matching your filter rules
3. Matching emails → formatted Telegram notification
4. Oracle never replies — only reads and notifies

**Filter rules (define in HEARTBEAT.md):**
```yaml
email_alerts:
  - senders: [boss@company.com, client@example.com]
    keywords: [urgent, invoice, deadline]
    notify: immediately
  - senders: []        # all senders
    keywords: []       # all subjects
    notify: morning_digest
```

**Telegram notification format:**
```
Email from Marco Rossi
Subject: Partnership proposal — Q2 review
[first 2 lines of the email]
```

**Setup:** Configure as a Remote Trigger at `claude.ai/code/scheduled` with Gmail connector active. See `cron/REMOTE_TRIGGERS.md`.

### Calendar reminders via Telegram

Oracle checks your calendar and sends Telegram reminders before events — with context (attendees, location, prep notes).

**Reminder tiers (configure in HEARTBEAT.md):**
```
15 min before  → "Starting soon: [Event] with [People]"
1 hour before  → "[Event] in 1h — [location / dial-in link]"
1 day before   → "Tomorrow: [Event] — [preparation notes]"
```

**Morning briefing format (sent at 07:30):**
```
Today — Tuesday Apr 8

09:00  Team standup (30 min) — Google Meet
11:30  Client call with Marco
14:00  Deep work block (2h)

Tomorrow: Board review at 10:00 — prepare Q1 report
```

**Setup:** Morning briefing → Remote Trigger at 07:30. Individual reminders → Remote Trigger every 15 min. See `cron/REMOTE_TRIGGERS.md`.

---

## Updated full connector map

```
Oracle Core (Claude Code CLI)
│
├── MCP Local (installed via claude mcp add)
│   ├── Playwright          — browser automation (navigate, click, extract)
│   ├── Brave Search        — web research (2000 req/month free)
│   ├── Sequential Thinking — complex multi-step reasoning
│   ├── GitHub              — code repos, issues, PRs
│   ├── Notion              — knowledge base
│   ├── Filesystem          — local files with path control
│   ├── MCPControl          — full desktop control (mouse, keyboard, screen)
│   └── Telegram plugin     — mobile interface (send/receive)
│
├── Cloud Connectors (claude.ai/settings/connectors)
│   ├── Gmail               — email read/draft + unread alerts
│   ├── Google Calendar     — events, scheduling, reminders
│   ├── Canva               — graphics generation
│   ├── Gamma               — AI slide decks
│   ├── Notion              — cloud knowledge base
│   ├── Hugging Face        — ML model search
│   ├── Indeed              — job market research
│   └── Replicate           — image/video AI generation
│
├── Local tools (scripts + CLI)
│   ├── oracle_tts.py       — voice reply (edge-tts, OGG Opus for Telegram)
│   ├── Whisper             — local audio transcription
│   ├── oracle-commands.sh  — OS control (sleep, shutdown, start services)
│   ├── WhatsApp bridge     — message monitoring (read-only by default)
│   ├── gcloud / clasp      — Google Workspace deep integration
│   └── n8n                 — local automation hub (port 5678)
│
├── Memory Layer
│   ├── Memory cards        — immediate context (CLAUDE.md files)
│   ├── Obsidian vault      — session RAM (live notes)
│   └── NotebookLM          — permanent HD (structured knowledge)
│
├── Remote Triggers (claude.ai/code/scheduled)
│   ├── Morning briefing    — 07:30 daily (calendar + email digest)
│   ├── Email alerts        — every 30 min (priority senders)
│   ├── Calendar reminders  — 15 min, 1h, 1 day before events
│   ├── Funding scout       — Monday weekly
│   └── News digest         — weekdays
│
└── n8n Workflows (localhost:5678)
    ├── Social publishing   — IG, LinkedIn, Facebook, X
    ├── CRM sync            — HubSpot, Notion DB
    ├── Messaging           — WhatsApp, Slack, Telegram
    └── Webhook routing     — any HTTP endpoint
```

---

## Verifying your setup

In a Claude Code session, run:
```
claude mcp list
```

You should see all your installed local MCP servers with their status.

For cloud connectors, check [claude.ai/settings/connectors](https://claude.ai/settings/connectors).

For n8n, open [http://localhost:5678](http://localhost:5678) in your browser.
