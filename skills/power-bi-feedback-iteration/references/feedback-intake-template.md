# Feedback Intake Template

Before classifying and routing feedback, gather enough detail to act. Use this checklist for every feedback item.

## Questions to Ask the User

### Core questions (always)
```
□ What exactly is wrong, missing, or desired?
   - Specific page name? ____________________
   - Specific visual? ______________________
   - Specific measure or field? ____________

□ What is the expected behavior or result?
   - What should the number / chart / page show? ____________

□ How do we reproduce it?
   - Steps? ________________________________
   - Filters applied at the time? __________
   - User role / RLS role? _________________
```

### Impact questions (for prioritization)
```
□ Who reported it? (name, role, frequency of use)
□ How many users are affected?
□ What is the business impact if not fixed?
□ Is there a workaround?
□ Is this blocking a specific decision or report cycle?
```

### Evidence (when available)
```
□ Screenshot / screen recording
□ Exact filter state at the time
□ Date / time of occurrence
□ Workspace and report version
□ Expected value vs actual value (with source for expected)
```

## One-item, one-template

If the user describes multiple issues in one message, **create one intake record per item**. Do not merge distinct problems.

## Intake record format

Store each intake as a single structured record:

```markdown
## Feedback #<id>
- **Reporter:** <name, role>
- **Reported:** <date>
- **Symptom:** <one sentence>
- **Expected:** <one sentence>
- **Reproduce:** <steps or filter state>
- **Evidence:** <link / screenshot>
- **Users affected:** <count or scope>
- **Business impact:** <Critical | High | Medium | Low>
- **Workaround:** <yes/no — describe>

## Classification
- **Category:** <1-12 from classification.md>
- **Severity:** <Critical | High | Medium | Low>

## Prioritization
- **Business impact:** <High | Low>
- **Effort:** <Low < 1h | High > 1h>
- **Quadrant:** <★★★★★ | ★★★★ | ★★★ | ★★>

## Routing
- **Destination phase:** <Phase 1 | 2 | 3 | 4a | 4b | 4c | Perf>
- **Skill:** <skill name>
- **Owner:** <assignee>
```

## Interview discipline

- Ask **one question at a time** when the user is providing verbal feedback
- Don't propose solutions during intake — capture the problem first
- If a user says "make it better" with no specifics, ask: *"What would make it obviously better — can you give one concrete example?"*
- If a user says "it's broken", ask: *"Which specific visual or number looks wrong, and what would be correct?"*

## Red flags during intake

| User statement | Likely underlying issue | Probe |
|---|---|---|
| "The report is wrong" | Unclear scope | Which page? Which visual? |
| "The numbers don't match" | Source-of-truth mismatch | Match against what? Which report or system? |
| "It's too slow" | Perf classification needed | Which page / interaction? How slow? |
| "It doesn't look professional" | Cosmetic category | What specifically — colors, spacing, fonts? |
| "Users are complaining" | Aggregated feedback | Can we talk to 1-2 users directly? |
