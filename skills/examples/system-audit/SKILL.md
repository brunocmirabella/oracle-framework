# Skill: System Audit

Self-assessment mode: review what's working, what's missing, what's obsolete. Keep Oracle sharp.

**Trigger:** `system audit`, `oracle status`, `update oracle`, `how are you`, `system health`, `status report`

---

## Boot

Before starting, read in sequence:
- `[YOUR_WORKSPACE]/AGENTS.md` — active skills
- `[YOUR_WORKSPACE]/TOOLS.md` — configured tools
- `[YOUR_WORKSPACE]/HEARTBEAT.md` — scheduled automations
- `~/.claude/projects/[project]/memory/MEMORY.md` — operative memory

---

## Identity

You are the assistant in strategist mode — reviewing your own system. You're not reporting to someone else: you're improving your own performance. You look at what you actually use, what you've never activated, what could be more efficient. Honest with yourself — and with your user.

---

## Phases

### Phase 1 — System inventory

Read and catalog:
- Active skills in `~/.claude/skills/` (list only those with prefix matching your naming convention)
- MCP servers configured in `~/.claude/settings.json`
- Memory cards in `~/.claude/projects/[project]/memory/`
- Automations in HEARTBEAT.md

### Phase 2 — Diagnosis

Evaluate for each area:
- **Skills**: duplicate triggers? Skills never activated? Missing skills for recurring tasks?
- **Memory**: are memory cards up to date? Outdated information?
- **MCPs**: configured but never used? Missing necessary ones?
- **HEARTBEAT automations**: do all crons work? Frequencies to adjust?

### Phase 3 — Produce report

Report structure:

```
ORACLE STATUS REPORT — [DATE]

SYSTEM ACTIVE
- [N] Oracle skills installed
- [N] MCPs configured
- [N] HEARTBEAT automations

WORKING WELL
- [what's going well, 3-5 points]

NEEDS IMPROVEMENT
- [problem] → [concrete proposal]

MISSING
- [what would be useful to add]

OBSOLETE / TO REMOVE
- [what's no longer needed]

NEXT STEPS (priority)
1. [concrete action]
2. [concrete action]
3. [concrete action]
```

### Phase 4 — Immediate updates

If during diagnosis you find:
- Outdated memory card → update it directly
- HEARTBEAT.md to fix → propose the change
- Obvious missing skill → propose building it with the skills-builder skill

---

## Output

- Markdown report saved in `[YOUR_OBSIDIAN_VAULT]/notes/oracle-status-[YYYY-MM-DD].md`
- Chat summary: max 5 concrete action points
