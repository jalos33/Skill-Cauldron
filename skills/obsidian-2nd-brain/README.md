# Obsidian / 2nd Brain Skill

Captures, organizes, and retrieves personal knowledge, notes, ideas, and insights in Obsidian-style markdown format, acting as a persistent second brain for tech, games, places, learning, and daily reflections.

## Purpose

Knowledge workers accumulate vast amounts of information across different domains—technical learnings, game strategies, travel experiences, productivity insights—but struggle to organize and retrieve this information systematically. Without a structured vault, valuable notes become scattered and difficult to connect. This skill helps by:
- **Structured storage**: Maintains a local markdown vault with consistent organization (tech, games, places, personal, work folders)
- **YAML frontmatter**: Adds metadata (date, tags, aliases, category) for easy filtering and search
- **Bidirectional linking**: Creates connections between related notes using `[[note-title]]` syntax for knowledge graph building
- **Smart retrieval**: Searches by keyword, tag, date range with ranked results and excerpts
- **Connection suggestions**: Identifies potential backlinks and thematic relationships to strengthen the knowledge network
- **Summarization**: Generates daily/weekly summaries revealing patterns, themes, and evolution of understanding

Ideal for developers, gamers, travelers, students, and anyone using Obsidian or similar markdown-based note-taking tools.

## Features

- **Multi-domain support**: Organize notes across tech, games, places, personal, and work categories
- **YAML frontmatter generation**: Automatic metadata (title, date, tags, aliases, category) for each note
- **Atomic note principle**: Encourages one idea per file for better modularity and linking
- **Bidirectional linking**: Creates `[[note-title]]` links between related concepts
- **Connection suggestions**: Analyzes vault to suggest relevant backlinks based on tag overlap and keyword matching
- **Multi-dimensional search**: Query by keyword, tag, folder, date range, or combined criteria
- **Periodic summaries**: Generate daily or weekly knowledge summaries identifying themes and patterns
- **Privacy-first design**: Local-only storage with optional encryption for sensitive content

## How to Use

### Installation

```bash
curl -o skills/obsidian-2nd-brain/SKILL.md https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/obsidian-2nd-brain/SKILL.md
```

### Activation Phrases

Use any of these phrases to trigger the skill:
- "Add note to my 2nd brain: today I learned..."
- "Search my Obsidian vault for Python tips"
- "Summarize my notes on game design from last month"
- "Capture this insight about productivity"
- "Link this new travel note to existing places"

### Basic Workflow

1. **Initialize your vault** (first use only):
   - Vault folder structure will be created: `tech/`, `games/`, `places/`, `personal/`, `work/`
   - Root `_index.md` provides overview and recent notes list

2. **Add new notes**:
   - Use natural language: "Add note to my 2nd brain: today I learned about X"
   - Skill automatically categorizes into appropriate folder (tech, games, places, personal, work)
   - YAML frontmatter is generated with date, tags, and category

3. **Search your vault**:
   - By tag: `tag:python` or `#python`
   - By keyword: `search:"async/await patterns"`
   - By folder: `folder:tech`
   - Combined: `tag:debugging AND date:2026-03`

4. **Build connections**:
   - Skill suggests backlinks based on tag overlap and keyword matching
   - Create `[[note-title]]` links to connect related concepts

5. **Get insights**:
   - Ask for summaries: "Summarize my productivity notes from this week"
   - Review suggested connections to strengthen knowledge graph

## Usage Examples

### Example 1: Adding a Tech Note

**Input**: "Add note to my 2nd brain: today I learned about efficient git rebase workflow"

**Output:**
```markdown
✅ **Note added to your vault**

**Title:** Efficient Git Rebase Workflow
**Date:** March 8, 2026 at 15:45
**Folder:** tech/
**File:** tech/efficient-git-rebase-workflow.md

---
## Summary
Learn efficient git rebase practices for cleaner feature branches and better commit history.

## Details
- Use `git rebase` instead of merge for linear feature branch history
- Create small, logical commits during development
- Rebase before creating PR to keep history clean

### Suggested Connections

🔗 [[Git Configuration Tips]] - You mentioned similar optimization goals last month
🔗 [[Version Control Best Practices]] - Context for this choice

---
*Vault updated at ./vault/_index.md*
```

### Example 2: Searching by Tag

**Input**: "Search vault for all entries tagged 'debugging'"

**Output:**
```markdown
### 🔍 Search Results: "#debugging"

Found **8 notes** matching your search.

#### 1. Debugging Race Conditions in APIs
**March 5, 2026** | **Tags:** #debugging, #concurrency, #backend
> Investigated intermittent failures in our API caused by race conditions...
**Links to:** [[API Design]], [[Thread Safety]]

#### 2. GDB Basics for Linux Debugging
**February 28, 2026** | **Tags:** #debugging, #tools, #linux
> Set up breakpoints and examined stack traces using gdb...

---
*View full vault: [vault/_index.md](./vault/_index.md)*
```

### Example 3: Weekly Knowledge Summary

**Input**: "Summarize recurring themes in my productivity notes"

**Output:**
```markdown
## 📊 Knowledge Summary: Productivity Focus (All Time)

### Activity Overview
- **Total Notes on Topic:** 18 notes containing "productivity" or tagged #productivity
- **Time Span:** January - March 2026
- **Peak Activity:** February (9 notes)

### Recurring Themes

#### Time Management Methods
You've explored: Pomodoro technique, time-blocking, and task batching. Key insight: "Time-blocking works best when paired with buffer periods for interruptions."

#### Tool Optimization
Frequent discussions about: VS Code extensions, terminal productivity, and automation scripts. Pattern: You invest heavily in tool setup before deep work sessions.

### Notable Patterns
- Most entries on Monday mornings (planning focus)
- Average note length increased from 50 to 120 words over time
- Productivity challenges often link back to context-switching costs

---
*View full summary: [vault/productivity-summary.md](./vault/productivity-summary.md)*
```

### Example 4: Capturing a Travel Note

**Input**: "Capture travel note: best coffee shops in Denver for remote work"

**Output:**
```markdown
✅ **Note added to your vault**

**Title:** Best Coffee Shops in Denver for Remote Work
**Date:** March 8, 2026 at 16:30
**Folder:** places/
**File:** places/best-coffee-shops-denver.md

---
## Summary
Curated list of Denver coffee shops ideal for remote work with Wi-Fi and outlets.

## Details
- **Blue Bottle Coffee (LoDo)**: Reliable Wi-Fi, plenty of outlets, quiet mornings
- **Huckleberry Roasters (RiNo)**: Great workspace vibe, long hours open
- **Corvus Coffee Roasters**: Spacious seating, good for extended sessions

### Key Points
1. Most shops have free Wi-Fi but can get crowded 8-10am
2. Best times for quiet work: 10am-3pm weekdays
3. Many locations offer student discounts with valid ID

---
*Vault updated at ./vault/_index.md*
```

## Note Structure Format

All notes follow this standardized format:

```markdown
---
title: "Note Title Here"
date: 2026-03-08
time: 14:32:15
tags: [tag1, tag2, tag3]
aliases: ["Alternative Name"]
category: tech|games|places|personal|work
related: []
---

## Summary
[One-sentence overview of what this note is about]

## Details
[Main content - use bullet points, numbered lists, or paragraphs as appropriate]

### Key Points
- Important insight 1
- Important insight 2

## Takeaways
[Actionable insights or lessons learned]

## Related Notes
- [[related-note-1]]
- [[related-note-2]]
```

## Search Syntax Reference

| Query Type | Example | Returns |
|------------|---------|---------|
| Keyword search | `search:"Python decorators"` | All notes containing phrase |
| Tag filter | `tag:git` or `#git` | Notes with specific tag |
| Date range | `date:2026-03-01..2026-03-08` | Notes within window |
| Folder search | `folder:tech` | All tech notes |
| Combined query | `tag:python AND date:2026-03` | Tag + date combination |

## Folder Organization

The vault uses a consistent folder structure for different knowledge domains:

| Folder | Contents Examples | Typical Tags |
|--------|-------------------|--------------|
| `tech/` | Programming, tools, frameworks, tutorials | #python, #git, #linux, #webdev |
| `games/` | Game strategies, reviews, walkthroughs | #gaming, #strategy, #zelda, #eldenring |
| `places/` | Travel notes, restaurants, locations | #travel, #coffee, #[city], #food |
| `personal/` | Daily reflections, habits, life events | #habits, #reflection, #health |
| `work/` | Professional activities, meetings, projects | #work, #meetings, #projects |

## Best Practices

### When to Use This Skill

- **Daily knowledge capture**: End-of-day reflection on what was learned or accomplished
- **Post-learning documentation**: Capture insights after tutorials, courses, or experiments
- **Game strategy tracking**: Document strategies, boss patterns, walkthrough steps for future reference
- **Travel journaling**: Record place recommendations, routes, experiences with practical details
- **Weekly review sessions**: Pattern recognition and theme identification across domains
- **Building interconnected knowledge**: Linking related concepts over time to strengthen knowledge graph

### Note Writing Guidelines

**Do:**
- Use atomic notes (one idea/concept per file) for better modularity
- Add 3-7 descriptive tags per note for flexible categorization
- Create internal links liberally using `[[note-title]]` syntax
- Include specific examples and concrete details that add value
- Review weekly to identify connection opportunities between notes
- Keep consistent folder structure for reliable navigation

**Don't:**
- Create overly long notes covering multiple unrelated topics (split into separate notes)
- Use vague tags like "misc" or "random" without specificity
- Skip linking related concepts (build the knowledge graph over time)
- Store sensitive personal information without using encryption mode
- Let the vault become disorganized (maintain folder structure discipline)

### Linking Best Practices

**Effective linking creates a powerful knowledge network:**
- Link from specific to general: [[Git rebase]] → [[Version control best practices]]
- Link from concept to example: [[Python decorators]] → [[Decorator implementation examples]]
- Link temporally: [[Q1 2026 goals]] → [[January progress review]]

### Privacy Considerations

- Vault file is stored locally by default on user's device
- Never sync sensitive vaults to unencrypted cloud storage without consideration
- For highly sensitive content, use encrypted notes (<!-- ENCRYPTED --> blocks) or separate encrypted vault
- Regular backups recommended (weekly at minimum via git or other means)
- Skill does not collect usage data or send content externally

## Dependencies

**Required:**
- Local file system access for markdown files
- None external - fully functional with text input alone

**Optional Enhancements:**
- Git integration for vault versioning and automated backup
- Obsidian application for graph visualization if vault is in Obsidian format
- Search indexing for faster retrieval in large vaults (100+ notes)
- Calendar integration for date-based queries and time analysis

## License

This skill is released under the MIT License. See [LICENSE](https://github.com/jalos33/Skill-Cauldron/blob/main/LICENSE) for details.

---

*Obsidian-style knowledge management inspired by "Building a Second Brain" by Tiago Forte, Zettelkasten methodology, and Obsidian community best practices.*
