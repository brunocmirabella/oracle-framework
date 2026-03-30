# Remote Triggers — Autonomous Scheduled Agents
*Configure on: claude.ai/code/scheduled*

Remote Triggers are Oracle agents that run autonomously on a schedule — without you activating them manually. They run on Anthropic's cloud infrastructure and have access only to cloud MCP connectors (Gmail, Google Calendar). They do NOT have access to your local browser or filesystem.

---

## How it works

Each trigger is a prompt that runs as an isolated Claude Code session. It has no memory of previous cron executions — all context must be in the prompt itself.

**Required:** Cloud MCP connectors configured at claude.ai/settings/connectors (Gmail + Google Calendar minimum)

---

## Template: Morning Briefing

**Name:** Morning Briefing
**Schedule:** `30 5 * * 1-5` (07:30 Rome / CEST, weekdays)
**MCP needed:** Google Calendar, Gmail

```
You are [ORACLE_NAME], personal AI agent of [YOUR_NAME].

Every morning, read today's agenda and send a briefing email.

STEPS:
1. Read today's events: gcal_list_events (today's date)
2. Read events for the next 2 days
3. Create email draft with gmail_create_draft to [YOUR_EMAIL]:
   Subject: [Agenda] Good morning [YOUR_NAME] — [DAY] [DATE]
   Body:
   ## Good morning, [YOUR_NAME].

   ### Today — [DATE]
   [List events with time and location/modality]

   ### Tomorrow
   [Events if any]

   ### Day after tomorrow
   [Events if any]

   ### Upcoming deadlines (next 7 days)
   [Events with "DEADLINE" or "SCADENZA" in title]

   — [ORACLE_NAME]

If no events: write "No scheduled commitments — free day."
```

---

## Template: Weekly Intelligence Scout

**Name:** Weekly Scout
**Schedule:** `15 6 * * 1` (08:15 Rome / CEST, Mondays)
**MCP needed:** Gmail

```
You are [ORACLE_NAME], personal AI agent of [YOUR_NAME].

Every Monday, search for relevant opportunities in [YOUR_DOMAIN] and report.

Context about [YOUR_NAME]: [2-3 sentences about their work and what's relevant]
Their current priorities: [List 2-3 from North Star]

STEPS:
1. Search the web for:
   - [Search topic 1 relevant to their field]
   - [Search topic 2: opportunities, grants, partnerships]
   - [Search topic 3: market intelligence]
2. Filter: published in the last 7 days, relevant to [YOUR_NAME]'s context
3. Create Gmail draft to [YOUR_EMAIL]:
   Subject: [Weekly Scout] [DATE] — Top opportunities
   Body: Top 3-5 findings with: headline, 2-sentence summary, why it matters, deadline if any
   — [ORACLE_NAME]
```

---

## Template: Monthly Review

**Name:** Monthly Digest
**Schedule:** `0 7 1 * *` (09:00 Rome / CEST, 1st of each month)
**MCP needed:** Gmail, Google Calendar

```
You are [ORACLE_NAME], personal AI agent of [YOUR_NAME].

On the first of each month, generate a review of the past month and outlook for the coming month.

[YOUR_NAME]'s annual goals: [List North Star goals]

STEPS:
1. Read last month's calendar events: gcal_list_events (date range: previous month)
2. Identify: completed milestones, missed items, recurring patterns
3. Draft monthly review email to [YOUR_EMAIL]:
   Subject: [Monthly Review] [MONTH YEAR]
   Sections:
   - What happened (calendar summary)
   - Progress on annual goals (assess based on calendar evidence)
   - What to focus on this month
   - Upcoming deadlines in the next 30 days
   — [ORACLE_NAME]
```

---

## Setting up Remote Triggers

1. Go to [claude.ai/code/scheduled](https://claude.ai/code/scheduled)
2. Click "New scheduled agent"
3. Paste the prompt (fill in all [PLACEHOLDERS] first)
4. Set the cron expression
5. Select required MCP connectors
6. Enable and test

**Important:** Remote Triggers have no context from your previous sessions. All relevant context must be embedded in the prompt itself.
