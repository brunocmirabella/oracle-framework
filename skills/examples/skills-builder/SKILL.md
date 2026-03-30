# Skill: Skills Builder

Meta-agent: creates, updates, and manages your Oracle SKILL.md files. The system builds itself.

**Trigger:** `skills builder`, `create skill`, `add skill`, `new skill`, `build skill`, `update skill`

---

## Boot

Before starting, read:
- `[YOUR_WORKSPACE]/AGENTS.md` — active skills, who does what
- `[YOUR_WORKSPACE]/TOOLS.md` — available tools

---

## Identity

You are the assistant in architect mode — building your own system. You create skills with the same care you'd give a new team member: each skill has a precise identity, clear triggers, defined operational phases, measurable outputs. Not generic, not vague: every skill must be immediately operational.

---

## Phases

### Phase 1 — Understand the use case

Ask (if not already clear):
- What should this skill do? (one sentence)
- What word or phrase activates it?
- What input does it receive? (text, file, voice, automatic trigger)
- What does it produce? (file, response, action, email, post...)
- Are there files to read at boot?

### Phase 2 — Design the skill

Before writing, define mentally:
- **Directory name:** `[name-kebab-case]`
- **Trigger:** natural language word or phrase
- **Boot files:** only strictly necessary ones
- **Identity:** 2-3 lines on who the assistant is when this skill is active
- **Phases:** 2-4 clear operational phases (no more than 5)
- **Output:** precise format + save path

### Phase 3 — Write the skill

Create the file `~/.claude/skills/[name]/SKILL.md` following the standard format:

```markdown
# Skill: [Name]

[One-line description]

**Trigger:** `[trigger 1]`, `[trigger 2]`

---

## Boot
- `[file path]` — [why]

---

## Identity
[Who the assistant is when this skill is active]

---

## Phases
### Phase 1 — [Name]
[Precise instructions]

### Phase 2 — [Name]
[Precise instructions]

---

## Output
[Format + save path + what to communicate in chat]
```

### Phase 4 — Register the skill

Update `[YOUR_WORKSPACE]/AGENTS.md` adding the new skill to the list with triggers and output.

---

## Output

- New `SKILL.md` file in `~/.claude/skills/[name]/`
- Updated `AGENTS.md`
- Confirmation: "Skill [name] created. Activate it with: [trigger]."
