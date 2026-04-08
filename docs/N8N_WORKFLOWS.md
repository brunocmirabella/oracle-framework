# n8n Workflows — Oracle Automation Infrastructure

n8n (port 5678, self-hosted) is Oracle's automation backbone. It handles scheduled triggers, external publishing, and multi-step workflows that Oracle cannot run directly during a Claude Code session.

This document describes the core workflow set — one group per Oracle agent, plus the general infrastructure workflows.

---

## How Oracle communicates with n8n

Oracle does not call n8n APIs directly. The integration works through two patterns:

**Pattern A — File drop:**
Oracle writes a JSON file to a watched folder. n8n detects the new file and processes it.
```
Oracle → writes /oracle-out/[type]/payload.json → n8n watches folder → executes workflow
```

**Pattern B — Webhook:**
Oracle calls a local webhook URL via Bash.
```bash
curl -s -X POST http://localhost:5678/webhook/[endpoint] \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

Both patterns keep Oracle and n8n loosely coupled — Oracle doesn't need to know n8n's internal state.

---

## Chief of Staff workflows

The chief-of-staff agent handles communication triage. These n8n workflows extend it into scheduled and event-driven automation.

### 1. Email triage — morning digest

**Schedule:** every day at 07:00

**What it does:**
1. Queries Gmail for unread emails since last run
2. Writes a JSON file to `/oracle-out/email/unread.json` with sender, subject, snippet, labels
3. Triggers chief-of-staff subagent via Claude Code CLI
4. Chief of staff classifies each email into: skip / info_only / meeting_info / action_required
5. Sends formatted Telegram digest

**n8n nodes:**
```
Schedule Trigger (07:00)
  → Gmail: Search Messages (is:unread after:[yesterday])
  → Code: format messages as JSON array
  → Write Binary File: /oracle-out/email/unread.json
  → Execute Command: claude -p "run chief-of-staff on /oracle-out/email/unread.json"
  → Telegram: Send Message (chat_id from env)
```

**Telegram output format:**
```
Email triage — 8 Apr

URGENT (2):
  Marco Rossi — Partnership Q2 [draft ready]
  Fattura #2041 — scadenza domani [task aggiunto]

INFO (3): newsletter AI, conferma prenotazione, aggiornamento tool

SKIP (5): —
```

**File: `/oracle-out/email/unread.json` schema:**
```json
[
  {
    "id": "msg_id",
    "from": "sender@example.com",
    "subject": "Subject line",
    "snippet": "First 100 chars of body",
    "date": "2026-04-08T09:32:00Z",
    "labels": ["INBOX", "UNREAD"]
  }
]
```

---

### 2. Priority sender alert — real-time

**Schedule:** every 15 minutes, 08:00–20:00

**What it does:**
1. Checks Gmail for emails from senders defined as priority in HEARTBEAT.md
2. If new email found: immediate Telegram notification
3. Marks as "alerted" to avoid duplicate notifications

**n8n nodes:**
```
Schedule Trigger (every 15 min)
  → Gmail: Search Messages (is:unread from:[priority_senders])
  → IF: new messages found
    → Telegram: Send Message (immediate alert)
    → Gmail: Modify Message (add label ORACLE_ALERTED)
  → ELSE: no action
```

**Telegram output:**
```
New email from [PRIORITY] Marco Rossi
Subject: Risposta alla proposta
Received: 14:32
```

**Priority senders list:** defined in HEARTBEAT.md, read by n8n at workflow start via `Read Binary File` node or environment variable.

---

### 3. Calendar briefing + reminders

**Schedule A:** daily at 07:30 (morning briefing)
**Schedule B:** every 15 minutes (event reminders)

**Morning briefing (Schedule A):**
1. Queries Google Calendar for today and tomorrow
2. Formats event list with time, title, location/link, attendees
3. Sends to Telegram

**Telegram output:**
```
Today — Tue 8 Apr

09:00  Standup (30 min) — meet.google.com/xxx
11:30  Call Marco — +39 02 xxx
14:00  Deep work (2h)

Tomorrow: Board review 10:00 — prepare Q1 report
```

**Event reminders (Schedule B):**
1. Queries next 90 minutes of calendar
2. Sends reminder at 1 day / 1 hour / 15 minutes before each event

**n8n nodes (Schedule B):**
```
Schedule Trigger (every 15 min)
  → Google Calendar: Get Events (timeMin: now, timeMax: now+90min)
  → Code: calculate reminder tier per event
  → IF: reminder needed (not already sent)
    → Telegram: Send Message
    → Set: mark event as reminded (in static data)
```

---

## Stratega workflows

The stratega agent runs system self-audits. These workflows automate periodic health checks and surface issues before they become problems.

### 4. Weekly system audit

**Schedule:** every Monday at 09:00

**What it does:**
1. Triggers the stratega subagent via Claude Code CLI
2. Stratega reads AGENTS.md, TOOLS.md, HEARTBEAT.md, MEMORY.md
3. Produces a gap report
4. Sends summary to Telegram; full report saved to `/oracle-out/audit/[date].md`

**n8n nodes:**
```
Schedule Trigger (Monday 09:00)
  → Execute Command: claude -p "stratega — weekly audit — save report to /oracle-out/audit/$(date +%F).md"
  → Read Binary File: /oracle-out/audit/[date].md
  → Code: extract "Priority actions" section
  → Telegram: Send Message (priority actions only)
```

**Telegram output:**
```
Oracle system audit — 6 Apr

Priority actions this week:
1. meeting-reporter skill not configured — install + test
2. NotebookLM hook returning empty — check patchright
3. CONTACTS.md has 4 entries with no last-contact date

Full report: /oracle-out/audit/2026-04-06.md
```

---

### 5. Memory health check

**Schedule:** every Friday at 18:00

**What it does:**
1. Reads all files in `~/.claude/projects/[project]/memory/`
2. Checks for files over 200 lines (autodream threshold)
3. Checks for stale project memories (last-modified > 30 days with no session link)
4. Sends brief status to Telegram

**n8n nodes:**
```
Schedule Trigger (Friday 18:00)
  → Execute Command: python scripts/autodream.py --dry-run
  → Code: parse output for warnings
  → IF: issues found
    → Telegram: Send Message (list of issues)
  → ELSE: Telegram: Send Message ("Memory health OK")
```

---

## Planner workflows

The planner agent is mostly on-demand, but these workflows make it available via Telegram and capture plans automatically.

### 6. Plan request via Telegram

**Trigger:** Telegram message containing "planner:" or "plan:"

**What it does:**
1. n8n receives incoming Telegram message via webhook
2. Detects "planner:" prefix
3. Extracts the task description
4. Triggers planner subagent via Claude Code CLI with the task
5. Sends the plan back to Telegram
6. Saves plan to `/oracle-out/plans/[date]-[task-slug].md`

**n8n nodes:**
```
Telegram Trigger (webhook, incoming messages)
  → IF: message starts with "planner:" or "plan:"
    → Code: extract task description
    → Execute Command: claude -p "planner — [task]"
    → Read Binary File: /oracle-out/plans/latest.md
    → Telegram: Send Message (formatted plan)
  → ELSE: pass to Oracle (standard processing)
```

**Usage from Telegram:**
```
planner: set up the email alert workflow in n8n from scratch
```

Oracle responds with the full structured plan.

---

### 7. Plan archive + Obsidian sync

**Trigger:** file created in `/oracle-out/plans/`

**What it does:**
1. Reads the new plan file
2. Appends it to today's Obsidian session note under "## Plans"
3. Adds a task to the kanban board for the first step

**n8n nodes:**
```
Watch Folder: /oracle-out/plans/
  → Read Binary File: [new file]
  → Execute Command: python scripts/brain.py append sessioni/[today] "## Plan\n[content]"
  → Execute Command: python scripts/brain.py kanban-add "in-corso" "[first step from plan]"
```

---

## Infrastructure workflows

General-purpose automations that support all three agents and Oracle's day-to-day operation.

### 8. Social publishing

**Trigger:** file created in `/oracle-out/social/`

**What it does:**
1. Reads post JSON (platform, text, media path, schedule time)
2. Routes to correct platform
3. Posts immediately or schedules

**File schema:**
```json
{
  "platform": "linkedin",
  "text": "Post content here...",
  "media": "/oracle-out/media/image.jpg",
  "schedule": "2026-04-09T10:00:00"
}
```

**n8n nodes:**
```
Watch Folder: /oracle-out/social/
  → Read Binary File: [new file]
  → Code: parse JSON
  → Switch: by platform
    → LinkedIn: HTTP Request (LinkedIn API)
    → Instagram: HTTP Request (Instagram Graph API via n8n node)
    → Facebook: HTTP Request (Meta Graph API)
  → Telegram: Send Message ("Posted: [platform] — [title]")
```

---

### 9. WhatsApp monitoring

**Schedule:** every 10 minutes, 08:00–22:00

**What it does:**
1. Reads new WhatsApp messages via bridge (whatsapp-web.js local API)
2. Classifies by sender (priority / normal / group)
3. Groups → ignored
4. Priority senders → immediate Telegram notification
5. Normal → added to morning digest batch

**n8n nodes:**
```
Schedule Trigger (every 10 min)
  → HTTP Request: GET http://localhost:3000/messages/unread (WhatsApp bridge)
  → Code: filter out groups, classify senders
  → IF: priority sender
    → Telegram: Send Message (immediate)
  → ELSE:
    → Write Binary File: append to /oracle-out/whatsapp/batch.json
```

**Rule enforced in n8n:** the workflow never calls WhatsApp send endpoints. It is read-only by design — outgoing messages require a separate, manually triggered workflow with explicit confirmation.

---

### 10. Obsidian session backup

**Schedule:** every 2 hours during working hours (09:00–19:00)

**What it does:**
1. Runs `git commit` on the Obsidian vault
2. Ensures session notes are versioned even if autodream doesn't run

**n8n nodes:**
```
Schedule Trigger (every 2h)
  → Execute Command: python scripts/brain.py git-backup "auto-backup"
  → IF: success
    → no notification (silent)
  → IF: error
    → Telegram: Send Message ("Vault backup failed — check git status")
```

---

## Oracle builds its own n8n workflows

The workflows described in this document don't need to be built manually. Oracle can create them programmatically — you install n8n, ask Oracle to build a workflow, and Oracle does the rest via the n8n REST API.

**How it works:**

n8n exposes a full REST API at `http://localhost:5678/api/v1/`. Oracle calls it via Bash to create, activate, and test workflows without you opening the n8n UI.

**Step 1 — Enable n8n API:**
In n8n Settings → API → create an API key. Add it to your CLAUDE.md or as an environment variable:
```
N8N_API_KEY=your-api-key-here
N8N_BASE_URL=http://localhost:5678
```

**Step 2 — Ask Oracle to build a workflow:**
```
Build the email triage workflow in n8n
```

Oracle will:
1. Query n8n for existing workflows (to avoid duplicates)
2. Compose the workflow JSON (nodes, connections, credentials)
3. POST it to n8n API to create it
4. Activate it
5. Confirm on Telegram

**Oracle's workflow creation pattern:**
```bash
# Create workflow
curl -s -X POST $N8N_BASE_URL/api/v1/workflows \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '[workflow JSON]'

# Activate it
curl -s -X POST $N8N_BASE_URL/api/v1/workflows/[id]/activate \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

**What Oracle needs to build a workflow:**
- n8n running locally (`n8n start`)
- API key configured
- Credential IDs for Gmail, Telegram, Google Calendar (created once in n8n UI, then reusable by Oracle)

**Getting credential IDs (one-time manual step):**
```bash
curl -s $N8N_BASE_URL/api/v1/credentials \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq '.data[] | {id, name, type}'
```
Give Oracle the credential IDs and it will wire them into every workflow automatically.

**Trigger phrase:** say `"build the [workflow name] n8n workflow"` and Oracle will compose and deploy it.

**Self-improvement loop:**
```
You: "the email triage is missing priority sender detection"
Oracle: reads current workflow → patches nodes → redeploys → confirms
```

Oracle can also list, disable, update, and delete workflows — the full n8n API is available.

---

## Setup checklist

Before enabling these workflows:

- [ ] n8n installed and running at `localhost:5678`
- [ ] Create output directories: `mkdir -p oracle-out/{email,social,plans,audit,media,whatsapp}`
- [ ] Gmail credentials configured in n8n (OAuth2)
- [ ] Google Calendar credentials configured in n8n
- [ ] Telegram bot token added to n8n credentials
- [ ] chat_id stored in n8n environment variables
- [ ] Priority senders list defined in HEARTBEAT.md
- [ ] WhatsApp bridge running (if using workflow 9)
- [ ] `claude` CLI accessible from n8n Execute Command nodes (check PATH)

---

## Folder structure

```
oracle-out/                    # n8n watches these folders
├── email/
│   └── unread.json            # daily email batch
├── social/
│   └── [post].json            # one file per post to publish
├── plans/
│   └── [date]-[task].md       # plans generated by planner agent
├── audit/
│   └── [date].md              # weekly stratega reports
├── media/
│   └── [image/video files]    # media to attach to social posts
└── whatsapp/
    └── batch.json             # WA messages for morning digest
```

---

## Environment variables (n8n)

Set these in n8n Settings → Variables:

| Variable | Value |
|----------|-------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | Your personal chat ID |
| `ORACLE_OUT_DIR` | Absolute path to `oracle-out/` folder |
| `ORACLE_VAULT_DIR` | Absolute path to Obsidian vault |
| `ORACLE_SCRIPTS_DIR` | Absolute path to `scripts/` folder |
| `PRIORITY_SENDERS` | Comma-separated email list |
