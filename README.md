# Skill-Cauldron – Collection of Claude Code Skills

Open-source skills for Claude Code agents. Each skill lives in its own folder under `/skills/`.

## What is This Repo?

This repository contains a collection of reusable **Claude Code skills** - specialized instructions that help Claude assist with specific development tasks like documentation generation, backend architecture design, and more.

## Structure

```
Skill-Cauldron/
├── README.md              # This file
├── LICENSE                # MIT License
├── SECURITY.md            # Security policy
├── .gitignore             # Git ignore patterns
└── skills/                # All skill folders
    ├── documentation-generator/   # Auto-generate project docs
    │   ├── SKILL.md       # Skill instructions (for Claude)
    │   └── README.md      # User-facing documentation
    └── backend-architect/     # Backend architecture guidance
        ├── SKILL.md       # Skill instructions (for Claude)
        └── README.md      # User-facing documentation
```

## How to Use

1. **Clone this repository:**
   ```bash
   git clone https://github.com/jalos33/Skill-Cauldron.git
   ```

2. **Copy desired skill folders** to your Claude Code skills directory:
   ```bash
   # Copy a single skill
   cp -r skills/documentation-generator ~/.claude/skills/

   # Or copy all skills
   cp -r skills/* ~/.claude/skills/
   ```

3. **Use the skills with Claude Code** by invoking phrases like:
   - `"Update README"` (Documentation Generator)
   - `"Design microservices for this app"` (Backend Architect)

## Available Skills

| Skill | Description |
|-------|-------------|
| [Documentation Generator](skills/documentation-generator/) | Auto-generate and update project documentation based on code changes |
| [Backend Architect](skills/backend-architect/) | Guidance on microservices, API versioning, and database migrations |

## Contributing

Contributions welcome! Feel free to add your own skills:

1. Fork this repository
2. Create a new folder under `skills/` with your skill
3. Include both `SKILL.md` (instructions) and `README.md` (documentation)
4. Submit a pull request

## License

MIT - See [LICENSE](LICENSE) for details.

---

Part of the Claude Code ecosystem. Built with ❤️ by [MdAlchemy.ai](https://mdalchemy.ai)
