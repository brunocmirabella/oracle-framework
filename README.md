# Oracle Framework

> **Your personal AI operating system.** Thinks like you, speaks like you, acts with your strategy.

Oracle is not a chatbot. It's not a generic assistant. It's the operational version of yourself — an AI agent that knows your projects, your priorities, your communication style, and acts on them autonomously.

Built on **Claude Code CLI**, Oracle operates through Telegram on your phone, reads your emails, manages your calendar, produces content in your voice, and remembers everything you've told it — across sessions.

---

## What it looks like in practice

You message your bot on Telegram:
> *"funding scout"*

Oracle searches open grants, VC rounds, and public tenders relevant to your business. It saves a report, creates a draft email with the top 3 opportunities, and adds calendar reminders for key deadlines. All without you opening a browser.

Or:
> *"write a follow-up to Marco about the partnership"*

Oracle reads your previous email thread, drafts the follow-up in your tone, and saves it as a Gmail draft — ready for your review.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│                    YOU                       │
│              (Telegram mobile)               │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│             ORACLE CORE                      │
│         Claude Code CLI (Sonnet)             │
│                                              │
│  CLAUDE.md ──── Identity + Rules             │
│  Soul Document ─ Your cognitive profile      │
│  Skills ──────── Agent capabilities          │
└──┬───────────────┬───────────────┬───────────┘
   │               │               │
┌──▼───┐      ┌────▼────┐    ┌─────▼──────┐
│ RAM  │      │   HD    │    │    MCP     │
│Obsid-│      │Notebook │    │  Servers   │
│ ian  │      │   LM    │    │Gmail/Cal/  │
│      │      │         │    │Playwright/ │
└──────┘      └─────────┘    └────────────┘
```

**Three memory layers:**
- **Memory cards** — immediate context (always loaded)
- **Obsidian** — session RAM (updated every conversation)
- **NotebookLM** — permanent HD (structured knowledge, citeable)

**Skills** — modular agents activated by natural language triggers. Each skill is a `SKILL.md` file that tells Oracle who to become, what to read, how to act, and what to produce.

**MCP Servers** — direct connections to Gmail, Google Calendar, Playwright (browser automation), Brave Search, Telegram, and more.

**n8n** — local automation hub running on port 5678. Connects Oracle's outputs to social platforms (Instagram, LinkedIn, Facebook), CRM tools, and any webhook endpoint. Unlike cloud automation tools (Zapier, Make), n8n runs entirely on your machine — no data leaves your infrastructure.

**Remote Triggers (Cron)** — agents that run autonomously on a schedule. Morning briefing at 07:30. Funding scout every Monday. News digest every weekday. All without manual activation.

---

## The Soul Document

The Soul Document is what separates Oracle from a generic AI assistant. It's a personal cognitive constitution — loaded as a master context — with 5 sections:

1. **Identity** — Who you are, how you describe yourself, what legacy you want to leave
2. **Decision Framework** — How you decide under pressure, what questions you ask, what blocks you
3. **Communication DNA** — Your tone with collaborators, clients, in moments of crisis
4. **Cognitive Triggers** — What energizes you, what drains you, what to avoid
5. **North Star** — Your 3-5 annual goals as a permanent filter for every action

Oracle reads this before acting. It produces outputs that sound like you — not like a generic AI.

---

## Quick Start

1. Install Claude Code CLI: `npm install -g @anthropic/claude-code`
2. Authenticate with GitHub: `gh auth login` (required to push your own fork)
3. Copy `CLAUDE.md.template` to `~/CLAUDE.md` and fill in your identity
4. Fill in your Soul Document (`soul-document/SOUL_DOCUMENT.md.template`)
5. Copy workspace templates: `cp -r workspace-template/ ~/oracle-workspace/`
6. Copy memory templates to `~/.claude/projects/[project]/memory/`
7. Install MCP servers (see `docs/MCP_GUIDE.md`)
8. Copy skills to `~/.claude/skills/`
9. Set up hooks (see `docs/HOOKS_GUIDE.md`)
10. Set up Telegram plugin (`/telegram:configure`)
11. Configure heartbeats on `claude.ai/code/scheduled` (see `docs/HEARTBEAT_GUIDE.md`)
12. Set up autoDream memory consolidation (see `docs/AUTODREAM.md`)

Full setup guide: [docs/SETUP.md](docs/SETUP.md)

---

## What's included

```
oracle-framework/
├── CLAUDE.md.template              # Core identity + rules (fill this first)
├── soul-document/
│   └── SOUL_DOCUMENT.md.template   # Your cognitive profile
├── workspace-template/             # Operational workspace files (copy to ~/oracle-workspace/)
│   ├── USER.md.template            # Your professional profile
│   ├── VOICE.md.template           # Your communication style + real examples
│   ├── CONTACTS.md.template        # Key contacts with context and tone calibration
│   ├── HEARTBEAT.md.template       # Autonomous automation config (topics, KPIs, tasks)
│   ├── AGENTS.md.template          # Registry of active skills
│   └── TOOLS.md.template           # Available MCPs, connectors, local services
├── memory/
│   ├── MEMORY.md.template          # Memory index
│   ├── user_profile.md.template    # Your profile for Oracle
│   └── reference_knowledge.md.template  # Paths, services, external resources
├── skills/
│   ├── SKILL.md.template           # Build your own skill
│   └── examples/
│       ├── email-agent/            # Draft emails in your voice
│       ├── calendar-agent/         # Manage calendar + reminders
│       ├── news-agent/             # Daily briefings
│       ├── research-agent/         # Web research on demand
│       ├── meeting-reporter/       # Audio/notes → structured minutes + action items
│       ├── skills-builder/         # Meta-agent: Oracle builds its own skills
│       └── system-audit/           # Self-diagnosis: what works, what's missing
├── scripts/
│   ├── autodream.py                # Memory consolidation Stop hook (4-phase: orient/gather/consolidate/prune)
│   └── brain.py                    # Second brain CLI: sessions, decisions, project notes
├── cron/
│   └── REMOTE_TRIGGERS.md          # Autonomous scheduled agents
└── docs/
    ├── SETUP.md                    # Step-by-step installation
    ├── ARCHITECTURE.md             # How Oracle works (memory, agents, self-improvement)
    ├── HOOKS_GUIDE.md              # How automatic context injection works (NotebookLM + Obsidian)
    ├── HEARTBEAT_GUIDE.md          # Scheduled automations: morning briefing, funding scout, etc.
    ├── AUTODREAM.md                # Memory consolidation: autoDream setup and behavior
    ├── SOUL_INTERVIEW.md           # How to write your Soul Document
    └── MCP_GUIDE.md                # MCPs, local AI stack, Telegram, desktop control
```

---

## Connectors & Integrations

A full Oracle deployment connects to these layers:

### MCP Servers (local — `~/.claude/settings.json`)

| Server | Install | Purpose |
|--------|---------|---------|
| **Playwright** | `claude mcp add playwright -- npx @playwright/mcp@latest` | Browser automation — any web UI |
| **Brave Search** | `claude mcp add brave-search -- npx -y @modelcontextprotocol/server-brave-search` | Web search (2000 req/month free) |
| **Sequential Thinking** | `claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking` | Multi-step reasoning |
| **GitHub** | `claude mcp add github -- npx -y @modelcontextprotocol/server-github` | Repos, issues, PRs |
| **Notion** | `claude mcp add notion -- npx -y @notionhq/notion-mcp-server` | Notes and project tracking |
| **Filesystem** | `claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /path` | Local file access |
| **Telegram** | via `claude-plugins-official` | Mobile interface for Oracle |

### Cloud Connectors (`claude.ai/settings/connectors`)

| Connector | Purpose |
|-----------|---------|
| **Gmail** | Read, search, draft emails |
| **Google Calendar** | Events, reminders, availability |
| **Canva** | Generate graphics and social posts |
| **Gamma** | AI slide decks from text |
| **Notion** | Cloud knowledge base (alt to local MCP) |
| **Hugging Face** | ML model research |
| **Indeed** | Job market data |
| **Replicate** | Image/video generation via API |

### n8n — Local Automation Hub

n8n (port 5678, self-hosted) handles everything Oracle cannot do directly — mainly **publishing to social platforms** and **webhook integrations**.

Typical Oracle → n8n flow:
```
Oracle writes content → saves to file → triggers n8n webhook
→ n8n posts to Instagram / LinkedIn / Facebook / WhatsApp
```

Key n8n workflows for Oracle:
- **Social publish**: Oracle drafts post → n8n distributes to 3+ platforms
- **CRM sync**: Oracle logs contacts → n8n updates your CRM
- **Notification routing**: Oracle sends summaries → n8n pushes to Slack/WhatsApp
- **Content calendar**: Oracle plans → n8n schedules and publishes

Install n8n: [docs.n8n.io/hosting/installation/npm](https://docs.n8n.io/hosting/installation/npm/)

---

## Contributing

PRs welcome. Open an issue first for major changes.

If you build your own Oracle instance, share it — open a PR to add it to the `examples/` directory.

## Local AI stack

Oracle integrates with local AI models — no API cost, no data sent to cloud:

| Tool | Port | Purpose |
|------|------|---------|
| **Ollama** | 11434 | Run Llama, Mistral, Gemma locally |
| **ComfyUI** | 8188 | Stable Diffusion image generation |
| **Whisper** | — | Local audio transcription (meetings, voice notes) |

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for setup details.

---

## Community

[Twitter/X](https://x.com/brunocmirabella) · [LinkedIn](https://linkedin.com/in/brunomirabella)

## License

MIT — free to use, fork, and build on. If you build something interesting, open a PR or tag me.

---

## Built by

This framework was built by [Bruno Mirabella](https://linkedin.com/in/brunomirabella) — AI trainer (600+ professionals), screenwriter, and director.

Oracle has been running in production on his own life and work since early 2026. Two additional instances — Lucius (freelance developer / CTO profile) and Alfred (manager profile) — are deployed on different professional contexts.

If you want Oracle configured for your organization: [contact](mailto:brunocmirabella@gmail.com)
