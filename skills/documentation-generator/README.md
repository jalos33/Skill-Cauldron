# Documentation Generator Skill

Automatically generates or updates README.md, CLAUDE.md, or custom documentation based on code changes and repository structure.

## Purpose

Keeps documentation current without manual effort. Ideal for solo developers, teams, and open-source maintainers who want to ensure their project docs stay in sync with the codebase.

## Features

- **Git Change Detection** - Analyzes recent commits to identify what needs documentation
- **Code Structure Extraction** - Scans source files to understand project layout and APIs
- **Auto-Generated Sections** - Creates Overview, Installation, Usage, API Reference, Changelog, and Contributing sections
- **Smart Merge** - Preserves manually written content while updating auto-generated sections
- **Custom Templates** - Supports different templates based on project type (CLI, Web API, Library, Full-stack)

## How to Use

1. Copy this skill folder to `~/.claude/skills/`
2. Invoke with natural language phrases:

| Phrase | What it does |
|--------|--------------|
| `"Update README"` | Analyzes recent changes and updates README.md |
| `"Generate docs for this project"` | Creates comprehensive documentation from scratch |
| `"Add changelog from last 10 commits"` | Extracts git history into CHANGELOG.md format |
| `"Refresh CLAUDE.md"` | Updates Claude Code configuration documentation |

## Example Output

**Before:** README.md with outdated or missing sections

```markdown
# My Project

A simple Node.js API.
```

**After (generated):**

```markdown
# My Project

A simple Node.js REST API built with Express for managing user data.

## Installation

```bash
npm install
```

## Usage

Start the server:

```bash
node index.js
```

## API Reference

### GET `/api/users`
Retrieve all users. Returns JSON array.

### POST `/api/users`
Create a new user. Expects JSON body with `name` and `email`.

## Contributing

Contributions welcome! Please read our contributing guidelines before submitting PRs.
```

## Dependencies

- **git** - For commit history analysis and change detection

## License

MIT

## Author

Joe Quiñones / MdAlchemy.ai

---

Part of [Skill Cauldron](https://github.com/jalos33/Skill_cauldron-) – Collection of Claude Code Skills
