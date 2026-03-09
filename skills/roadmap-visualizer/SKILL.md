---
name: roadmap-visualizer
description: Generates Gantt-style project roadmaps from Jira, Linear, or raw input data (tasks, epics, milestones, dependencies, timelines), outputting visual diagrams (Mermaid or ASCII) and markdown summaries.
tags: [roadmap, gantt, project-management, visualization, jira, linear]
author: Jose Quiñones
version: 1.0
license: MIT
---

# Roadmap Visualizer Skill

Generates Gantt-style project roadmaps from task data (Jira/Linear exports or raw input), producing visual diagrams and comprehensive markdown reports with timeline analysis.

## Instructions

Follow this step-by-step methodology to generate roadmap visualizations:

### Step 1: Read and Parse Input Data
Parse the provided input, which may be:
- **Jira export** (CSV, JSON, or copied table data)
- **Linear export** (task lists with dates and dependencies)
- **Raw text description** of tasks, epics, milestones
- **Project plan document** containing timeline information

Extract the following elements from input:
| Element | What to Look For | Example Values |
|---------|------------------|----------------|
| Tasks | Individual work items with owners | "Implement auth", "Write tests" |
| Epics/Layers | Groupings for related tasks | "Authentication", "User Profile" |
| Milestones | Key dates/deadlines | "Beta Launch", "Production Ready" |
| Dependencies | Task relationships | "Task B depends on Task A" |
| Start Dates | When work begins | "2024-03-01", "Week 1" |
| End Dates/Duration | Completion or length | "2024-03-15", "5 days" |
| Status | Current state | "Not Started", "In Progress" |

### Step 2: Normalize and Structure Data
Convert parsed data into a consistent timeline format:
- Resolve relative dates ("Week 1", "Next Monday") to absolute dates
- Calculate missing end dates from duration values
- Identify task owners and assignees
- Group related tasks under epics for layered visualization

### Step 3: Build Timeline Structure
Organize tasks chronologically:
1. Sort all tasks by start date
2. Identify the overall project timeline (earliest start to latest end)
3. Determine appropriate time unit for display:
   - **Days**: Projects < 30 days
   - **Weeks**: Projects 1-6 months
   - **Months**: Projects > 6 months

### Step 4: Detect Dependencies and Critical Path
Analyze task relationships to identify:
- **Dependency chains**: Tasks that must complete before others start
- **Critical path**: Sequence of tasks determining minimum project duration
- **Parallel work**: Tasks that can execute simultaneously
- **Bottlenecks**: Single points of failure in the timeline

Flag potential issues:
| Risk Type | Detection Criteria | Action |
|-----------|-------------------|--------|
| Overlaps | Multiple critical tasks same owner | Flag for resource conflict |
| Delays | Dependency chain extends timeline | Highlight on critical path |
| Gaps | Idle time between dependent tasks | Suggest buffer removal |

### Step 5: Generate Mermaid Gantt Diagram
Create a Mermaid.js-compatible Gantt chart using this structure:

```mermaid
gantt
    title [Project Name]
    dateFormat  YYYY-MM-DD
    axisFormat  %W

    section [Epic/Phase Name]
    Task Name          :a1, yyyy-mm-dd, yyy-mm-dd
    Another Task       :a2, after a1, 5d
    Milestone: Key Date :milestone, m1, yyyy-mm-dd, 0d

    %% Dependencies (optional)
    # a2 depends on a1 (implicit in "after" syntax or explicit links)
```

**Mermaid Gantt Best Practices:**
- Use `section` headers to group tasks by epic/phases
- Apply `milestone` marker for key dates/deadlines
- Use relative durations (`5d`, `2w`) when exact end date unknown
- Add comments for dependency notes (`# depends on previous task`)
- Include `dateFormat` and `axisFormat` for proper rendering

### Step 6: Generate Task List with Dates and Status
Create a structured table of all tasks:

| ID | Task Name | Epic/Phase | Owner | Start Date | End Date | Duration | Status | Dependencies |
|----|-----------|------------|-------|------------|----------|----------|--------|--------------|
| 1 | Implement authentication | Authentication | Jane D. | 2024-03-01 | 2024-03-08 | 7 days | In Progress | - |
| 2 | Write unit tests | Authentication | John S. | 2024-03-09 | 2024-03-15 | 6 days | Not Started | Task 1 completes |

### Step 7: Identify Risks and Constraints
Analyze the timeline for potential issues:

**Risk Categories:**
| Category | Indicators | Severity |
|----------|------------|----------|
| Resource Conflicts | Same owner assigned to overlapping tasks | High/Medium/Low |
| Timeline Compression | Tasks with < 2 days duration in sequence | Medium |
| Dependency Risk | Long chains without parallel work | High |
| Buffer不足 | No contingency time before milestones | Medium |

### Step 8: Generate Summary Report
Create a comprehensive markdown report including:
1. **Executive Summary**: Project name, overall timeline, key milestones
2. **Visual Diagram**: Mermaid Gantt chart (rendered or code block)
3. **Task Inventory**: Structured table with all tasks and metadata
4. **Dependency Map**: Critical path identification and relationships
5. **Risk Analysis**: Flagged issues with severity ratings
6. **Recommendations**: Suggested adjustments for improved feasibility

## Output Format Template

Your response should follow this structure:

```markdown
# Roadmap: [Project Name]

## Executive Summary
- **Timeline**: [Start Date] to [End Date] ([Total Duration])
- **Milestones**: [List of key dates with descriptions]
- **Total Tasks**: [Count], **In Progress**: [Count], **At Risk**: [Count]

## Visual Timeline (Mermaid Gantt)

```mermaid
gantt
    title [Project Name]
    dateFormat  YYYY-MM-DD
    axisFormat  %W

    section [Epic Name]
    Task 1       :a1, 2024-03-01, 5d
    Task 2       :a2, after a1, 7d

    section [Epic Name 2]
    Milestone: Launch :milestone, m1, 2024-03-20, 0d
```

## Task Inventory

| # | Task | Phase | Owner | Start | End | Duration | Status | Dependencies |
|---|------|-------|-------|-------|-----|----------|--------|--------------|
| 1 | ... | ... | ... | ... | ... | ... | ... | ... |

## Critical Path Analysis
**Critical Tasks**: [List of tasks on critical path]
**Total Critical Duration**: [X days/weeks]
**Bottlenecks Identified**: [Description of any constraints]

## Risk Assessment
| Risk | Task(s) Affected | Severity | Recommendation |
|------|------------------|----------|----------------|
| Resource Conflict | Task 3, Task 4 | High | Reassign one task or extend timeline |
| Timeline Risk | Milestone: Launch | Medium | Add buffer before launch date |

## Recommendations
1. [Priority action item with rationale]
2. [Secondary improvement suggestion]
3. [Optional refinement for optimization]
```

## Activation Phrases / When to Use

Use this skill when the user mentions any of these scenarios:
- "Generate roadmap from this Jira data"
- "Create Gantt chart for this project plan"
- "Visualize timeline from Linear tasks"
- "Build roadmap with dependencies and milestones"
- "Show Gantt view of these epics and stories"

## Usage Examples

### Example 1: Jira Epic Export
**Input**: User pastes Jira export table or provides CSV data
```
Key,Summary,Start Date,Due Date,Status,Epic,Assignee
PROJ-101,Implement auth,2024-03-01,2024-03-08,In Progress,Authentication,Jane D.
PROJ-102,Write tests,2024-03-09,2024-03-15,Not Started,Authentication,John S.
```

**Output**: Gantt chart with Authentication phase, task table, dependency analysis

### Example 2: Product Launch Plan
**Input**: "Create roadmap for Q2 product launch"
**Output**: Multi-phase roadmap covering development, testing, launch preparation

### Example 3: Linear Task List
**Input**: User provides Linear task export with dependencies
**Output**: Timeline visualization highlighting dependency chains and critical path

## Best Practices / Notes

### When This Skill Adds Value
- Converting raw task data into visual timelines
- Identifying timeline conflicts before they become problems
- Communicating project status to stakeholders visually
- Planning complex projects with multiple dependencies
- Preparing for sprint planning or milestone reviews

### Mermaid Diagram Guidelines
1. **Use sections** to group tasks by epic, phase, or team
2. **Mark milestones** explicitly for key dates/deadlines
3. **Keep labels concise** - long names break diagram readability
4. **Include dateFormat** for proper date parsing and rendering
5. **Test renderability** - ensure dates follow YYYY-MM-DD format

### Timeline Analysis Tips
- Always flag resource conflicts (same owner on overlapping tasks)
- Identify critical path to show minimum achievable duration
- Suggest buffer time before major milestones
- Highlight any gaps where dependent tasks wait idle
- Recommend parallel work opportunities when possible

### Input Handling
- Accept Jira CSV/JSON exports directly
- Parse Linear task list formats with dependencies
- Handle relative dates by converting to absolute dates
- Infer missing information from context or ask clarifying questions

## Dependencies

- **No external dependencies required** - works with text/Mermaid generation only
- **Optional**: Can integrate with Jira/Linear APIs for direct data fetch (if available)

## License

This skill is released under the MIT License. See [LICENSE](https://github.com/jalos33/Skill-Cauldron/blob/main/LICENSE) for details.

---

*Roadmap generation follows project management best practices from PMBOK and uses Mermaid.js for diagram rendering.*
