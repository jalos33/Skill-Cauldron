# Database Migration Planner Skill

A Claude Code skill for generating safe, reversible database schema migration scripts with comprehensive rollback plans, forward/backward compatibility checks, and test suggestions.

## Description

The Database Migration Planner skill provides a systematic approach to database schema changes that minimizes risk and ensures reversibility. Instead of manually writing migration scripts, it analyzes the current schema, identifies potential breaking changes, generates both forward and rollback SQL scripts, and includes pre/post-migration validation checks. This reduces deployment failures and data loss risks during schema updates.

## Purpose

Database migrations often fail or cause production issues when:
- Migrations lack tested rollback procedures
- Breaking changes (column drops, type changes) are not properly handled
- Pre-migration conditions (locks, active transactions) are not checked
- Post-migration validation is missing to confirm success
- Migration scripts are not idempotent (can't be run multiple times safely)

This skill addresses these challenges by providing:
- Automatic generation of forward migration scripts with safety checks
- Tested rollback procedures for every schema change
- Pre-migration condition validation (disk space, locks, transactions)
- Post-migration verification queries to confirm success
- Breaking change detection with mitigation strategies
- Idempotency checks to prevent errors on re-runs

## Features

- **Schema Analysis**: Reads current database structure from SQL dumps, migration history, or ORM models
- **Risk Classification**: Categorizes changes by impact level (Low/Medium/High/Critical)
- **Forward Migration Generation**: Creates production-ready SQL scripts with transactions and idempotency checks
- **Rollback Script Creation**: Generates tested rollback procedures for every change
- **Pre-Migration Checks**: Validates disk space, locks, active transactions before deployment
- **Post-Migration Verification**: Includes validation queries to confirm successful execution
- **Breaking Change Detection**: Identifies data loss risks and provides mitigation strategies
- **Test Suggestions**: Provides unit and integration test cases for migration validation
- **Risk Assessment Matrix**: Documents potential issues with severity levels and mitigations

## How to Use

### Activation Phrases

Use these phrases to invoke the Database Migration Planner skill:
- "Plan database migration for new schema"
- "Generate safe migration script for adding column"
- "Create reversible migration for table rename"
- "Plan migration with rollback for this schema change"
- "Audit migration safety for this ALTER TABLE"

### Usage Examples

```bash
# Plan migration for adding user_roles column to users table
Plan migration for adding user_roles column to users table

# Generate forward + rollback scripts for renaming table customers to clients
Generate forward + rollback scripts for renaming table customers to clients

# Create safe migration for changing email column from varchar(100) to varchar(255)
Create safe migration for changing email column from varchar(100) to varchar(255)

# Plan migration for adding foreign key constraint
Plan migration for adding foreign key constraint
```

## Examples

### Example 1: Adding New Column with Array Type

**Input:** "Plan migration for adding user_roles column to users table"

**Output:** Migration plan showing:
- Forward script with idempotency check (skip if column exists)
- Rollback script that safely drops column and index
- Pre-migration checks for disk space, locks, active transactions
- Post-migration verification queries
- Risk assessment: MEDIUM severity for NOT NULL constraint on existing data

### Example 2: Table Rename Migration

**Input:** "Generate forward + rollback scripts for renaming table customers to clients"

**Output:** Comprehensive migration including:
- Forward: RENAME TABLE customers TO clients
- Rollback: RENAME TABLE clients TO customers
- Dependency handling: Update foreign keys, views, triggers referencing table
- Application code update checklist
- Downtime estimation and maintenance window recommendations

### Example 3: Column Type Change

**Input:** "Create safe migration for changing email column from varchar(100) to varchar(255)"

**Output:** Safe type change with:
- Forward: ALTER TABLE users ALTER COLUMN email TYPE VARCHAR(255)
- Idempotency check (skip if already correct size)
- Data validation query before migration
- Rollback plan (can't easily revert, document implications)
- Warning about potential application compatibility issues

## License

MIT License - see [SKILL.md](./SKILL.md) for full license text.

## Repository

Source: https://github.com/jalos33/Skill-Cauldron/tree/main/skills/database-migration-planner
