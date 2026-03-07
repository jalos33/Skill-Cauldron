---
name: documentation-generator
description: This skill should be used when the user asks to "generate README", "update documentation", "add changelog", "write CLAUDE.md", or needs help creating/updating project documentation based on code changes and repo structure. Use for README generation, documentation updates from git history, and custom doc creation.
tags: [documentation, git, maintenance, open-source]
author: Jose Quiñones
version: 1.0
license: MIT
---

# Documentation Generator

Automatically generates or updates README.md, CLAUDE.md, CHANGELOG.md, or custom documentation based on code changes and repository structure.

## Instructions

### Step-by-Step Process

When invoked, this skill performs the following steps:

**1. Detect Changes**
   - Run `git diff HEAD~5` to identify recently modified files
   - Check for new files that lack documentation coverage
   - Identify deleted or renamed files that may need doc updates
   - Parse commit messages from recent history for context

**2. Extract Information**
   - Read package.json, setup.py, requirements.txt for project metadata (name, description, version, dependencies)
   - Scan source files for:
     - Public functions and classes (via function/class declarations)
     - API routes and endpoints (e.g., `app.get()`, `router.post()`)
     - Configuration options and environment variables
     - JSDoc/Docstring comments for inline documentation
   - Extract project structure from directory tree

**3. Generate Sections**
   Based on detected content, generate appropriate sections:

   | Section | Source | When Generated |
   |---------|--------|----------------|
   | Overview | Project metadata + main entry point | Always (for new docs) |
   | Installation | Dependencies file + README requirements | If install instructions needed |
   | Usage | Code examples, test files | If usage patterns detected |
   | API Reference | Route handlers, exported functions | For projects with APIs/libraries |
   | Changelog | `git log` output | When updating existing docs |
   | Contributing | CONTRIBUTING.md templates | Optional, based on project type |

**4. Smart Merge**
   - Check if target file (README.md, etc.) already exists
   - Preserve manually written sections not covered by auto-generation
   - Update existing sections with new information
   - Append new sections at appropriate locations
   - Flag conflicts for manual review

**5. Write and Commit**
   - Write the generated/merged documentation to file
   - Suggest commit message: `docs: update [file] based on code changes`
   - Recommend reviewing before pushing

## Activation Phrases / When to Use

Use this skill when you see or type these phrases:

| Phrase | Effect |
|--------|--------|
| `"Update README"` | Analyzes recent changes and updates README.md |
| `"Generate docs for this project"` | Creates comprehensive documentation from scratch |
| `"Add changelog from recent commits"` | Extracts git history into CHANGELOG.md format |
| `"Refresh CLAUDE.md"` | Updates Claude Code configuration documentation |
| `"Document new endpoint in api/routes"` | Focuses on API route documentation only |

## Usage Examples

### Update README after adding new endpoint

```
user: "Update README after adding new endpoint"
skill: Documentation Generator will analyze the new API endpoints and update README.md with relevant documentation sections.
```

**What happens:**
1. Scans `api/routes/` for new or modified route files
2. Extracts endpoint paths, methods (GET/POST/etc.), and descriptions
3. Updates or creates "API Reference" section in README.md
4. Preserves existing manual content

### Generate initial README for this repo

```
user: "Generate initial README for this repo"
skill: Creates a comprehensive README.md including project description, installation instructions, usage examples, and project structure based on code analysis.
```

**What happens:**
1. Reads package.json or equivalent for metadata
2. Scans directory structure to map out project layout
3. Identifies main entry point and key modules
4. Generates complete README with all standard sections
5. Creates file if it doesn't exist

### Add changelog section from last 5 commits

```
user: "Add changelog from last 5 commits"
skill: Extracts commit messages and creates a CHANGELOG.md or updates existing changelog with recent changes organized by commit type (feat, fix, chore, etc.).
```

**What happens:**
1. Runs `git log --oneline -n 20` to get recent history
2. Parses conventional commits (feat:, fix:, breaking!:)
3. Groups entries by category
4. Creates or appends to CHANGELOG.md with proper formatting
5. Suggests version bump if breaking changes detected

## How It Works

### Technical Implementation

**1. Git Integration**
```bash
# Detect recent changes
git diff --name-only HEAD~5
git log --oneline -n 20

# Parse commit types
feat: new feature
fix: bug fix
docs: documentation change
style: formatting
refactor: code restructuring
test: adding tests
chore: maintenance
```

**2. Code Structure Scanning**
- **JavaScript/TypeScript**: Parses function declarations, class definitions, route handlers (express, fastify)
- **Python**: Reads docstrings, identifies public APIs from `__init__.py` exports or main module
- **General pattern matching**: Looks for common structures regardless of language

**3. Template System**
Uses predefined templates based on project type:

| Project Type | Template Applied |
|--------------|------------------|
| Node.js CLI | Installation + Usage with examples |
| Web API | Overview + API Reference with endpoint docs |
| Library/Module | Documentation of exports and usage patterns |
| Full-stack app | Architecture overview + deployment instructions |

**4. Smart Merge Algorithm**
- Loads existing file if present
- Identifies section boundaries by heading markers (`##`)
- Maps generated sections to existing ones by title similarity
- Keeps manual content when confidence is low
- Adds `<!-- AUTOGENERATED -->` markers for easy regeneration

### File Output Locations

| Requested Doc | Target Path | Notes |
|---------------|-------------|-------|
| README | `./README.md` | Default, most common |
| CHANGELOG | `./CHANGELOG.md` or `./HISTORY.md` | Detects existing convention |
| CLAUDE.md | `.claude/CLAUDE.md` or `./CLAUDE.md` | For Claude Code config docs |
| CONTRIBUTING | `./CONTRIBUTING.md` | Optional, community projects |
| Custom | User-specified | Any valid filename |

## Dependencies

### Required
- **git** - For commit history analysis and change detection
- **Read/Grep tools** - For scanning codebase structure
- **Write tool** - For creating/upending documentation files

### Optional (Enhanced Parsing)
- **tree-sitter** - For precise AST-based code parsing (if available)
- **Package parsers** - For specific language metadata extraction

## Best Practices / Notes

### Before Generating
- Always commit generated docs separately for review
- Review AI-generated content before pushing to shared branches
- Check for sensitive information exposure in auto-docs

### When Writing README.md
- Start with a clear project description from package metadata
- Include installation steps before usage examples
- Add section links (table of contents) for longer documents
- Keep API documentation concise but complete
- Update automatically after significant changes

### When Extracting Changelog
- Group commits by type (feat, fix, refactor, etc.)
- Use conventional commit format when possible
- Link to relevant issues or PRs when available
- Include breaking changes prominently with warning markers
- Consider semantic version impact of detected changes

### For CLAUDE.md Configuration
- Document project-specific conventions
- Explain build and test workflows
- Note any special development patterns
- Reference key files and their purposes

### Conflict Resolution
- If auto-generated content conflicts with manual edits, prefer manual
- Use `<!-- AUTOGENERATED -->` comments to mark machine-written sections
- Allow users to specify which sections should never be overwritten

## Error Handling

The skill handles common scenarios gracefully:

| Scenario | Behavior |
|----------|----------|
| Empty repository | Generates basic template structure with placeholders |
| No git history | Creates static documentation without changelog section |
| Missing metadata | Infers project type from file patterns (package.json, main.py, etc.) |
| Permission issues | Reports clearly and suggests manual alternative |
| Parse failures | Falls back to pattern matching, logs warnings |
| Large codebase | Processes in chunks, focuses on top-level structure first |

## Integration with Workflow

This skill integrates naturally into development workflows:

- **After major feature completion**: Regenerate README to document new functionality
- **Before releases**: Update changelog from accumulated commits
- **When onboarding new contributors**: Ensure docs are current and comprehensive
- **Periodic audits**: Run documentation checks before PR merges

### Suggested Commit Workflow

```bash
# After generating docs
git add README.md CHANGELOG.md
git commit -m "docs: update documentation based on recent changes"
git push origin main
```

## Tests

Run these test scenarios to verify functionality:

### Test 1: Update README with latest changes
**Command**: `"Update README with latest changes"`
**Expected**: Analyzes git diff, updates relevant sections in README.md

### Test 2: Generate initial README for this repo
**Command**: `"Generate initial README for this repo"`
**Expected**: Creates comprehensive README.md from project analysis

### Test 3: Add changelog from last 5 commits
**Command**: `"Add changelog from last 5 commits"`
**Expected**: Creates or updates CHANGELOG.md with recent commit history
