# Heartbeat Guide — Oracle's Autonomous Rhythms

A Heartbeat is a scheduled agent that runs automatically, without you triggering it. It's Oracle's autonomy in time — not just in response to your requests.

---

## What heartbeats are

Every morning Oracle knows what's on your calendar, what emails need attention, and what opportunities appeared overnight. Not because you asked — because it checked on schedule.

This is the difference between a reactive assistant and an autonomous operating system.

---

## How heartbeats work

Oracle uses **Remote Triggers** — scheduled agents running on `claude.ai/code/scheduled`. These are separate from your local session: they run in the cloud, even if your machine is off.

```
claude.ai/code/scheduled
    ├── 07:30 daily    → Morning briefing
    ├── Monday 08:00   → Weekly planning
    ├── Every weekday  → News digest
    └── Custom         → Your domain-specific automations
```

---

## Core heartbeats

### Morning Briefing — 07:30 daily

Reads your calendar, email, and any overnight updates. Sends you a structured message (Telegram or email) with:
- Today's agenda
- Emails that need action
- Open tasks from yesterday
- Priority focus for the day

**Requires:** Gmail connector, Google Calendar connector, Telegram bot

### Weekly Planning — Monday 08:00

Reviews last week's progress. Proposes focus areas for the week. Checks your goals (North Star) and asks: are you on track?

**Requires:** Gmail connector, Google Calendar connector, Obsidian vault (for session history)

### Funding Scout — Monday 10:00 (optional)

Searches open grants, VC rounds, and public tenders relevant to your sector. Saves report and sends top 3 opportunities to Telegram.

**Requires:** Brave Search MCP, Gmail connector (for draft creation)

### News Digest — Weekdays 08:00 (optional)

Aggregates news relevant to your domain (configurable topics). Delivers a curated brief.

**Requires:** Brave Search MCP, Telegram bot

---

## Setting up heartbeats

### Step 1 — Configure your HEARTBEAT.md

Create `~/oracle-workspace/HEARTBEAT.md` from the template:

```bash
cp workspace-template/HEARTBEAT.md.template ~/oracle-workspace/HEARTBEAT.md
```

Fill in your topics, contacts, sectors to monitor.

### Step 2 — Configure Remote Triggers

Go to `claude.ai/code/scheduled` and create a new trigger.

Use the templates from `cron/REMOTE_TRIGGERS.md`. For each trigger:

1. **Name** — e.g., "Morning Briefing"
2. **Schedule** — cron syntax: `30 7 * * *` (07:30 daily)
3. **Prompt** — the instruction Oracle executes (see templates below)
4. **MCPs** — select which connectors to enable
5. **CLAUDE.md** — load your identity from the cloud version

### Step 3 — Test manually

Before scheduling, test the trigger manually from the Remote Triggers interface. Verify the output is what you expect.

---

## Trigger prompt templates

### Morning briefing
```
Morning briefing. Today is [DATE].

Read:
1. Google Calendar — events for today
2. Gmail — unread emails from last 12 hours, flag those needing action
3. ~/oracle-workspace/HEARTBEAT.md — open tasks and focus areas

Produce a structured brief and send it to my Telegram (chat_id: [YOUR_CHAT_ID]):

FORMAT:
📅 TODAY: [2-3 key events]
📧 EMAIL: [flagged emails with 1-line action per item]
🎯 FOCUS: [single most important thing today]
📋 OPEN: [top 3 pending tasks]

Keep it under 300 words. Actionable, not informational.
```

### Weekly planning
```
Weekly planning. Week of [DATE].

Read:
1. Google Calendar — events this week
2. Gmail — pending threads from last 7 days
3. ~/oracle-workspace/SOUL_DOCUMENT.md section "North Star" — annual goals

Evaluate: what happened last week vs. what was planned? What needs to move?

Send to Telegram (chat_id: [YOUR_CHAT_ID]):
- Week summary (3 bullet points)
- This week's priorities (3 max)
- One thing I should stop doing
- One thing I should start
```

### Funding scout
```
Funding scout. Today is [DATE].

Search for:
- Open grants relevant to [YOUR_SECTOR]
- Public tenders in [YOUR_REGION/COUNTRY]
- VC rounds open for applications in [YOUR_STAGE]

For each opportunity found (max 5):
- Name and amount
- Deadline
- Relevance to [YOUR_BUSINESS_DESCRIPTION]
- Application link

Save report to ~/oracle-workspace/reports/funding-[DATE].md
Draft Gmail email with top 3 opportunities, subject "Funding Scout [DATE]"
Send Telegram message (chat_id: [YOUR_CHAT_ID]): "Funding scout done. [N] opportunities found. Top one: [NAME] — deadline [DATE]."
```

---

## The HEARTBEAT.md file

Your HEARTBEAT.md is the configuration file for Oracle's autonomous behavior. It tells Oracle:
- What topics to monitor
- What contacts to watch
- What KPIs matter
- What recurring tasks to check

```markdown
# Heartbeat Configuration

## Topics to monitor
- [YOUR_SECTOR]: trends, news, opportunities
- [YOUR_COMPETITORS]: product updates, funding news
- [YOUR_TECHNOLOGY]: new tools, research

## Contacts to track
- [NAME] — [relationship, what to monitor]
- [NAME] — [relationship, what to monitor]

## Weekly KPIs
- [METRIC_1]: current [VALUE], target [TARGET]
- [METRIC_2]: current [VALUE], target [TARGET]

## Recurring tasks
- [ ] [WEEKLY_TASK_1] — every Monday
- [ ] [MONTHLY_TASK_1] — first of the month

## Sectors to scout for funding
- [SECTOR_1]
- [SECTOR_2]

## North Star check-in
Goals I want Oracle to evaluate weekly:
1. [GOAL_1]
2. [GOAL_2]
3. [GOAL_3]
```

---

## Local vs. cloud heartbeats

| Type | Where runs | Requires machine on | Can use Playwright |
|------|-----------|--------------------|--------------------|
| Remote Triggers | claude.ai cloud | No | No |
| Local cron (crontab) | Your machine | Yes | Yes |

**For maximum coverage:** use Remote Triggers for briefings/research (cloud-native), local cron for tasks that need browser automation or local file access.

**Local cron example (Mac/Linux):**
```bash
# ~/.claude/cron/morning-briefing.sh
#!/bin/bash
cd ~/oracle-workspace
claude --headless --print "Morning briefing. [paste your trigger prompt]"
```

Add to crontab:
```
30 7 * * * /bin/bash ~/.claude/cron/morning-briefing.sh >> ~/.claude/logs/heartbeat.log 2>&1
```

---

## Notification routing

Heartbeat outputs should reach you where you are:

- **Telegram** — primary (instant, mobile)
- **Gmail draft** — for content that needs review before sending
- **Obsidian note** — for reports and logs that feed future sessions
- **Local file** — for structured data that triggers n8n workflows

Configure your preferred channel in each heartbeat prompt.

---

## Troubleshooting

**Trigger not running:**
- Check cron syntax at [crontab.guru](https://crontab.guru)
- Verify MCPs are selected in the Remote Triggers interface
- Gmail/Calendar connectors must be connected at claude.ai/settings/connectors

**Empty output:**
- Test the prompt manually in a Claude Code session first
- Verify your HEARTBEAT.md paths are correct
- Check that Telegram chat_id is correct

**Oracle not sounding like you:**
- Make sure your CLAUDE.md is loaded as context for the trigger
- For Remote Triggers, you may need to paste a condensed identity section into the trigger prompt itself
