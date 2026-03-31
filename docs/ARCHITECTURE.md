# Oracle Architecture — How It Works

## The core loop

Every time you send a message (Telegram, terminal, or web), Oracle runs this loop:

```
1. LOAD CONTEXT
   ├── CLAUDE.md  (identity, rules, MCP declarations)
   ├── Soul Document  (who you are, how you decide)
   ├── Memory cards  (immediate reference knowledge)
   └── Obsidian session note  (today's RAM)

2. QUERY KNOWLEDGE (if hook configured)
   └── NotebookLM  (permanent HD — documents, processes, history)

3. ACTIVATE SKILL (if trigger phrase detected)
   └── Load SKILL.md  (specialized identity + phases + output format)

4. SPAWN AGENTS (if task is complex)
   ├── Research agent  → web search, doc retrieval
   ├── Writing agent   → draft production
   ├── Planning agent  → task decomposition
   └── Coordinator     → synthesize, deliver

5. ACT
   ├── Read/write local files
   ├── Browse the web (Playwright)
   ├── Draft emails (Gmail MCP)
   ├── Create calendar events
   ├── Update Obsidian notes
   └── Trigger n8n webhook → social / CRM / messaging

6. DELIVER
   ├── Response in terminal or chat
   ├── Message via Telegram
   └── Update session memory (Obsidian)
```

---

## Memory architecture

Oracle uses three memory layers with different scopes:

### Layer 1 — Memory cards (immediate, always loaded)
Files in `~/.claude/projects/[project]/memory/`

Loaded as system context via CLAUDE.md. Available from the first token of every response. Contains:
- Your profile (USER.md or user_profile.md)
- Reference maps (paths, services, contacts)
- Persistent feedback and preferences

**Scope:** permanent, hand-curated
**Access:** instant (already in context window)
**Update:** manual

### Layer 2 — Obsidian vault (session RAM)
A local Markdown vault connected via REST API (port 27123) or direct file access.

Oracle reads and writes notes during sessions. Each day gets a new session note. Contains:
- Current work-in-progress
- Decisions made today
- Open tasks and blockers
- Ephemeral notes

**Scope:** session-level, updated in real time
**Access:** via hook (injected at prompt submit) or explicit read
**Update:** automatic (Oracle writes during conversation)

### Layer 3 — NotebookLM (permanent HD)
Google NotebookLM notebooks containing your documents, processes, past sessions.

Queried automatically via a hook before each response. Returns relevant excerpts and citations.

**Scope:** permanent, grows over time
**Access:** natural language query
**Update:** you upload documents; Oracle doesn't write here

---

## Skills system

A skill is a Markdown file (`SKILL.md`) that transforms Oracle into a specialized agent:

```
~/.claude/skills/
└── [skill-name]/
    └── SKILL.md
```

Each skill defines:
- **Trigger phrase** — natural language that activates it
- **Boot files** — what to read before starting
- **Identity** — who Oracle becomes when this skill is active
- **Phases** — step-by-step operational workflow
- **Output** — format, destination, what to report in chat

Skills are activated when Oracle detects the trigger phrase in your message. Multiple skills can chain: meeting-reporter → action items → calendar events.

**Building new skills:** Use the `skills-builder` skill. Oracle designs and writes its own SKILL.md files. It then registers itself in AGENTS.md. The system grows by building itself.

---

## Multi-agent orchestration

For complex tasks, Oracle decomposes work into parallel subagents:

```
User: "Manage the launch of our new project"
         │
         ▼
    Oracle (coordinator)
    ├── Agent 1: Market research
    │   └── Brave Search + web scraping
    ├── Agent 2: Competitive analysis
    │   └── GitHub + web research
    ├── Agent 3: Draft production
    │   └── Writes emails, posts, briefs in your voice
    └── Coordinator synthesizes → delivers report
```

Each agent runs with isolated context. The coordinator merges results and produces the final deliverable. This is handled natively by Claude Code's agent spawning — no extra infrastructure needed.

---

## Self-improvement loop

Oracle can improve its own system:

```
oracle-stratega (audit)
    → identifies missing skill
    → proposes design
    → oracle-skills-builder creates SKILL.md
    → AGENTS.md updated
    → new skill active immediately
```

This loop runs whenever you trigger a system audit. Oracle reviews its own capabilities, identifies gaps, and builds new tools for itself.

---

## Local AI stack

Oracle integrates with local AI models for offline/private workflows:

### Ollama (local LLMs, port 11434)
Run open-source models (Llama, Mistral, Gemma, Phi) locally. Oracle can route lightweight tasks to Ollama to preserve Claude API credits.

```bash
ollama serve
ollama pull llama3.2
```

Use cases: local summarization, classification, draft iteration.

### ComfyUI (local image generation, port 8188)
Stable Diffusion via node-based GUI. Oracle can trigger image generation workflows via the ComfyUI API.

```bash
# In your ComfyUI directory
python main.py --listen
```

Use cases: social post visuals, concept art, product mockups.

### Whisper (local audio transcription)
OpenAI Whisper running locally — no API cost, no data sent to cloud.

```bash
pip install openai-whisper
```

Use cases: meeting audio → minutes, voice messages → text tasks.

---

## n8n integration

n8n (port 5678) is Oracle's publishing and automation bridge — handling everything that requires external API calls Oracle cannot make directly.

**How Oracle triggers n8n:**
1. Oracle writes a JSON file to a watched folder, OR
2. Oracle calls a local webhook endpoint

**n8n picks up the trigger and:**
- Posts to Instagram / LinkedIn / Facebook / X
- Sends WhatsApp or Slack messages
- Syncs contacts to CRM (HubSpot, Notion)
- Fires any external HTTP webhook

**Why local n8n over Zapier/Make:**
- No subscription fees
- Unlimited workflows and executions
- Full JavaScript nodes for custom logic
- Your data never leaves your machine
- Direct access to local files and services

---

## Deployment patterns

### Single instance (personal)
One CLAUDE.md, one Soul Document, one Telegram bot, one person.

### Multi-instance (team or multiple roles)
Multiple CLAUDE.md configurations with different Soul Documents. Each instance has its own Telegram bot, different skill sets, different memory domains.

Examples:
- **Personal assistant** — creative work, personal ops
- **Developer / CTO** — code, architecture, PR reviews, technical research
- **Manager** — team ops, client communication, project tracking

Same infrastructure. Different identity. Different Telegram chat.
