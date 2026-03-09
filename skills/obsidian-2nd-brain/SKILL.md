---
name: obsidian-2nd-brain
description: Captures, organizes, and retrieves personal knowledge, notes, ideas, and insights in Obsidian-style markdown format, acting as a persistent second brain for tech, games, places, learning, and daily reflections.
tags: [obsidian, second-brain, knowledge-management, notes, productivity]
author: Jose Quiñones
version: 1.0
license: MIT
---

# Obsidian / 2nd Brain Skill

Captures, organizes, and retrieves personal knowledge, notes, ideas, and insights in Obsidian-style markdown format, acting as a persistent second brain for tech, games, places, learning, and daily reflections.

## Purpose

Individuals accumulate vast amounts of knowledge across different domains—technical learnings, game strategies, travel experiences, productivity insights—but struggle to organize and retrieve this information systematically. Without a structured vault, valuable notes become scattered and difficult to connect. This skill helps by:
- **Structured storage**: Maintains a local markdown vault with consistent organization
- **YAML frontmatter**: Adds metadata (date, tags, aliases) for easy filtering and search
- **Bidirectional linking**: Creates connections between related notes using `[[note-title]]` syntax
- **Categorized folders**: Organizes knowledge into logical groups (tech, games, places, personal, work)
- **Smart retrieval**: Searches by keyword, tag, date range with ranked results
- **Connection suggestions**: Identifies potential backlinks and thematic relationships
- **Summarization**: Generates daily/weekly summaries revealing patterns and themes

Ideal for knowledge workers, developers, gamers, travelers, and lifelong learners using Obsidian or similar tools.

## Instructions

### Step 1: Initialize Your Vault

**Vault Structure:**
```
vault/
├── tech/           # Technical learnings (code, tools, frameworks)
├── games/          # Game strategies, reviews, walkthroughs
├── places/         # Travel notes, restaurants, locations visited
├── personal/       # Daily reflections, habits, life events
├── work/           # Professional activities, meetings, projects
└── templates/      # Note templates for consistent formatting
    ├── standard.md
    └── quick.md
```

**Initial Setup:**
Create a root `_index.md` or `vault-summary.md`:
```markdown
# My Second Brain Vault

## Folders
- [[tech]] - Technical knowledge and learnings
- [[games]] - Game strategies and reviews
- [[places]] - Travel experiences and recommendations
- [[personal]] - Daily reflections and habits
- [[work]] - Professional activities

## Recent Notes
<!-- Auto-populated by skill -->

## Active Connections
<!-- Suggested links appear here -->
```

### Step 2: Accept New Note Input

Parse user input for note content:

**Input Patterns to Recognize:**

| Pattern | Example | Extracted Data |
|---------|---------|----------------|
| Learning capture | "Today I learned X about Y" | Type=learning, topic extracted |
| Tech insight | "Figured out how Z works" | Type=tech, concept identified |
| Game strategy | "Best way to beat boss is..." | Type=strategy, game named |
| Place recommendation | "Best coffee in [city]" | Type=place, location tagged |
| Daily reflection | "Today I felt..." | Type=reflection, emotion noted |
| Quick capture | "Quick: [idea]" | Type=quick note, minimal format |

**Auto-Detection Rules:**
- If entry mentions code, programming, tools → **tech folder**
- If entry discusses games, bosses, strategies → **games folder**
- If entry references locations, restaurants, travel → **places folder**
- If entry is personal feeling or habit → **personal folder**
- If entry relates to work tasks or meetings → **work folder**

### Step 3: Create Note with Frontmatter

Generate YAML frontmatter at top of note:

```yaml
---
title: "Note Title Here"
date: 2026-03-08
time: 14:32:15
tags: [tag1, tag2, tag3]
aliases: ["Alternative Name", "Synonym"]
category: tech|games|places|personal|work
related: []
---
```

**Frontmatter Guidelines:**
- **title**: Clear descriptive title (sentence case)
- **date**: ISO 8601 date (YYYY-MM-DD)
- **time**: Optional time component (HH:MM:SS)
- **tags**: 3-7 relevant tags for categorization
- **aliases**: Alternative names for search flexibility
- **category**: Primary folder classification
- **related**: Array of `[[linked-note-names]]` (populated later)

### Step 4: Write Note Content

Structure the note body:

```markdown
## Summary

[One-sentence overview of what this note is about]

## Details

[Main content - use bullet points, numbered lists, or paragraphs as appropriate]

### Key Points
- Important insight 1
- Important insight 2
- Important insight 3

## Takeaways

[Actionable insights or lessons learned]

## Related Notes
- [[related-note-1]]
- [[related-note-2]]
```

**Content Best Practices:**
- Use `[[note-title]]` syntax for internal links to other notes
- Keep atomic: one idea/concept per note file
- Use bullet points for readability
- Include specific examples when possible
- Add quotes or references for attributed content

### Step 5: Create Backlinks and Connections

Search existing vault for potential connections:

**Connection Methods:**

1. **Tag Overlap Search:**
   - Find notes sharing 2+ tags with current note
   - Suggest as "Related knowledge from your vault"

2. **Keyword Matching:**
   - Search for common terms in titles and content
   - Example: Note mentions "Python" → link to existing Python notes

3. **Temporal Proximity:**
   - Show notes created within same week/month
   - Helpful for tracking evolving understanding

4. **Semantic Similarity:**
   - Compare conceptual themes even without exact keyword matches
   - Example: "Git rebase" connects to "version control strategies"

**Output Format:**
```markdown
### Suggested Connections

🔗 [[Efficient Git Workflows]] - You mentioned similar optimization goals last month
🔗 [[Version Control Best Practices]] - Context for this choice
```

### Step 6: Update Vault Index

Refresh the vault summary to include new note:

**Update `_index.md`:**
- Add entry to "Recent Notes" section with date and brief description
- Update tag cloud with new tags encountered
- Refresh connection suggestions based on new links

Example update:
```markdown
## Recent Notes (Last 7 Days)
- **2026-03-08**: [Efficient Git Rebase Workflow](./tech/efficient-git-rebase-workflow.md)
- **2026-03-05**: [Debugging Race Conditions in APIs](./tech/debugging-race-conditions.md)
- **2026-03-01**: [Best Coffee Shops in Denver](./places/best-coffee-shops-denver.md)

## Tag Cloud
#git (5), #productivity (8), #debugging (4), #python (12), #coffee (3)
```

### Step 7: Search and Retrieve Notes

Enable powerful search capabilities:

**Search Query Types:**

| Query Type | Syntax Example | Returns |
|------------|----------------|---------|
| Keyword search | `search:"Python decorators"` | All notes containing phrase |
| Tag filter | `tag:git` or `#git` | Notes with specific tag |
| Date range | `date:2026-03-01..2026-03-08` | Notes within window |
| Folder search | `folder:tech` | All tech notes |
| Combined query | `tag:python AND date:2026-03` | Tag + date combination |

**Search Algorithm:**
1. Parse query for operators (:, AND, OR, ..)
2. Extract filters (tags, dates, folders, keywords)
3. Scan vault notes matching all criteria
4. Rank results by relevance (tag match count, recency, content depth)
5. Display top 10 matches with excerpts

**Result Format:**
```markdown
### 🔍 Search Results: "debugging"

Found **8 notes** matching your search.

#### 1. Debugging Race Conditions in APIs
**Date:** March 5, 2026 | **Tags:** #debugging, #concurrency, #backend
> Investigated intermittent failures caused by race conditions...
**Links:** [[API Design]], [[Thread Safety]]

#### 2. GDB Basics for Linux Debugging
**Date:** February 28, 2026 | **Tags:** #debugging, #tools, #linux
> Set up breakpoints and examined stack traces using gdb...
```

### Step 8: Generate Summaries

Create periodic summaries identifying patterns:

**Daily Summary Template:**
```markdown
## Daily Knowledge Summary - March 8, 2026

### Notes Added Today (3)
1. [[Efficient Git Rebase Workflow]] - tech/productivity
2. [[Morning Routine Optimization]] - personal/habits
3. [[Best Coffee Denver]] - places/travel

### Themes Explored
- **Version Control**: Deepened understanding of rebase vs merge
- **Productivity Systems**: Morning routine optimization techniques
- **Local Discovery**: Coffee shop recommendations for remote work

### Connections Made
- Linked Git note to existing version control documentation
```

**Weekly Summary Template:**
```markdown
## Weekly Knowledge Summary - Week 10 (March 2-8, 2026)

### Activity Overview
- **Total Notes Added:** 12
- **Most Active Category:** tech (7 notes)
- **Top Tags:** #python, #debugging, #productivity

### Recurring Themes
**Python Development**: You explored decorators, async/await patterns, and testing strategies. Key insight: "Type hints significantly improve code maintainability."

**Debugging Practices**: Multiple sessions on systematic debugging approaches. Pattern: You invest time in understanding root causes before applying fixes.

### Notable Connections Formed
- Connected Python testing notes to earlier documentation review
- Linked productivity habits across personal and work domains

### Questions for Next Week
- What testing framework should I standardize on?
- How can I better track debugging patterns?
```

### Step 9: Suggest Cross-Links

Proactively suggest linking opportunities:

**Link Suggestions:**
```markdown
### 📎 Potential Connections

Based on your note content, consider linking to:

1. [[Python Best Practices]] - This Python tip relates to broader guidelines you've documented
2. [[Code Review Checklist]] - Your testing approach aligns with review criteria
3. [[Debugging Methodology]] - Systematic approach matches your established framework
```

**When to Suggest:**
- Note contains specific concepts already covered elsewhere
- Multiple notes reference same underlying principle
- User has documented general guidelines that apply here

### Step 10: Ensure Privacy and Security

Protect personal knowledge vault:

| Practice | Implementation |
|----------|----------------|
| Local storage only | Vault stays on user's device, never synced by default |
| Optional encryption | For sensitive notes, use encrypted metadata or separate vault |
| Access control | File permissions set to private (600 on Unix systems) |
| No telemetry | Skill does not collect usage data or send content externally |
| Backup recommendation | User responsible for own backup strategy (git sync, cloud backup) |

**Encryption Option:**
For sensitive notes, wrap in encrypted block:
```markdown
<!-- ENCRYPTED:start -->
Use this section for private thoughts that shouldn't be read casually.
<!-- ENCRYPTED:end -->
```

## Output Format Templates

### New Note Creation Response
```markdown
✅ **Note added to your vault**

**Title:** Efficient Git Rebase Workflow
**Date:** March 8, 2026 at 14:32
**Folder:** tech/
**Tags:** #git, #productivity, #workflow

> Learn efficient git rebase practices for cleaner feature branches and better commit history.

### Suggested Connections

🔗 [[Git Configuration Tips]] - You mentioned similar optimization goals last month
🔗 [[Version Control Best Practices]] - Context for this choice

---
*Vault updated at ./vault/_index.md*
```

### Search Results Response
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

### Summary Response
```markdown
## 📊 Weekly Knowledge Summary - Week 10 (March 2-8, 2026)

### Activity Overview
- **Total Notes Added:** 12 notes
- **Most Active Category:** tech (7 notes), personal (3 notes)
- **Top Tags:** #python, #debugging, #productivity

### Recurring Themes

#### Python Development
You've explored: decorators, async/await patterns, and testing strategies. Key insight: "Type hints significantly improve code maintainability."

#### Debugging Practices
Multiple sessions on systematic debugging approaches. Pattern: You invest time in understanding root causes before applying fixes.

### Notable Connections Formed
- Connected Python testing notes to earlier documentation review
- Linked productivity habits across personal and work domains

---
*View full summary: [vault/weekly-summary-2026-03-08.md](./vault/weekly-summary-2026-03-08.md)*
```

## Activation Phrases / When to Use

Use this skill when the user mentions:
- "Add note to my 2nd brain: today I learned..."
- "Search my Obsidian vault for Python tips"
- "Summarize my notes on game design from last month"
- "Capture this insight about productivity"
- "Link this new travel note to existing places"

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
- Use `git log --oneline --graph` to visualize branch structure

### Key Points
1. Interactive rebase (`git rebase -i`) allows commit squashing
2. Always update remote after force-push: `git push --force-with-lease`
3. Don't rebase published commits shared with teammates

## Takeaways
Rebasing keeps project history linear and makes code reviews cleaner.

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

#### 3. Python pdb Interactive Debugger
**February 15, 2026** | **Tags:** #debugging, #python, #tools
> Learned to use pdb for step-through debugging of Python scripts...

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

### Suggested Connections
🔗 [[Morning Routine Optimization]] - Complements your productivity planning
🔗 [[Deep Work Strategies]] - Related to focus techniques discussed

---
*View full summary: [vault/productivity-summary.md](./vault/productivity-summary.md)*
```

## Best Practices / Notes

### When This Skill Adds Value

- **Daily knowledge capture**: End-of-day reflection on what was learned
- **Post-learning documentation**: Capture insights after tutorials, courses, or experiments
- **Game strategy tracking**: Document strategies, boss patterns, walkthrough steps
- **Travel journaling**: Record place recommendations, routes, experiences
- **Weekly review sessions**: Pattern recognition and theme identification
- **Building interconnected knowledge**: Linking related concepts over time

### Note Writing Guidelines

**Do:**
- Use atomic notes (one idea/concept per file)
- Add 3-7 descriptive tags per note for categorization
- Create internal links liberally using `[[note-title]]` syntax
- Include specific examples and concrete details
- Review weekly to identify connection opportunities
- Keep consistent folder structure

**Don't:**
- Create overly long notes covering multiple topics (split into separate notes)
- Use vague tags like "misc" or "random" without specificity
- Skip linking related concepts (build the graph over time)
- Store sensitive personal information without encryption mode
- Let the vault become disorganized (maintain folder structure)

### Folder Organization Strategy

| Folder | Contents Examples | Tag Patterns |
|--------|-------------------|--------------|
| `tech/` | Programming, tools, frameworks, tutorials | #python, #git, #linux, #webdev |
| `games/` | Game strategies, reviews, walkthroughs | #gaming, #strategy, #[game-name] |
| `places/` | Travel notes, restaurants, locations | #travel, #coffee, #[city], #food |
| `personal/` | Daily reflections, habits, life events | #habits, #reflection, #health |
| `work/` | Professional activities, meetings, projects | #work, #meetings, #projects |

### Linking Best Practices

**Effective linking creates a knowledge graph:**
- Link from specific to general: [[Git rebase]] → [[Version control best practices]]
- Link from concept to example: [[Python decorators]] → [[Decorator implementation examples]]
- Link temporally: [[Q1 2026 goals]] → [[January progress review]]

### Recommended Review Cadence

| Frequency | Purpose | Suggested Action |
|-----------|---------|------------------|
| **Daily** | Knowledge capture | Add notes on what was learned, reflect on day |
| **Weekly** | Pattern recognition | Review week's notes, create summary, identify connections |
| **Monthly** | Theme evolution | Compare monthly themes, update topic maps |
| **Quarterly** | Strategic review | Assess knowledge gaps, plan learning priorities |

### Privacy Considerations

- Vault file is stored locally by default on user's device
- Never sync sensitive vaults to unencrypted cloud storage without consideration
- For highly sensitive content, use encrypted notes or separate encrypted vault
- Regular backups recommended (weekly at minimum via git or other means)
- Skill does not collect usage data or send content externally

## Dependencies

**Required:**
- Local file system access for markdown files
- None external - fully functional with text input alone

**Optional Enhancements:**
- Git integration for vault versioning and backup
- Obsidian application for graph visualization (if vault is in Obsidian format)
- Search indexing for faster retrieval in large vaults (100+ notes)
- Calendar integration for date-based queries

## License

This skill is released under the MIT License. See [LICENSE](https://github.com/jalos33/Skill-Cauldron/blob/main/LICENSE) for details.

---

*Obsidian-style knowledge management inspired by "Building a Second Brain" by Tiago Forte, Zettelkasten methodology, and Obsidian community best practices.*
