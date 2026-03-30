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

---

## n8n — Local Automation Hub

n8n is the missing piece between Oracle and the outside world. While MCP servers let Oracle *read and draft*, n8n lets Oracle *publish and trigger* — across social platforms, CRMs, webhooks, and more.

**Install:**
```bash
npm install -g n8n
n8n start
# → runs at http://localhost:5678
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
| Social publish | File created in `/oracle-out/social/` | Post to IG + LI + FB |
| WhatsApp summary | Webhook from Oracle | Send formatted summary |
| CRM contact sync | Webhook | Update HubSpot / Notion DB |
| Content calendar | Schedule (n8n cron) | Pull from Notion → post |
| Email → Oracle | New Gmail label | Notify Oracle via file |

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

## Verifying your setup

In a Claude Code session, run:
```
claude mcp list
```

You should see all your installed local MCP servers with their status.

For cloud connectors, check [claude.ai/settings/connectors](https://claude.ai/settings/connectors).

For n8n, open [http://localhost:5678](http://localhost:5678) in your browser.
