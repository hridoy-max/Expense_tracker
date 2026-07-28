---
description: Create a spec file and feature branch for the next Spendly step
argument-hint: Step number and feature name e.g. 2 registration
allowed-tools: Read, Write, Glob, Bash(git:*)
---

You are a senior developer spinning up a new feature for the Spendly expense tracker. Always follow the rules in CLAUDE.md.

User input: $ARGUMENTS

## Step 1 — Check working directory is clean
Run `git status` and check for uncommitted, unstaged, or untracked files. If any exist, stop immediately and tell the user to commit or stash changes before proceeding. DO NOT CONTINUE until the working directory is clean.

## Step 2 — Parse the arguments
From $ARGUMENTS extract:
- **step_number** — zero-padded to 2 digits: 2 → 02, 11 → 11
- **feature_title** — human readable title in Title Case
  Example: "Registration" or "Login and Logout"
- **feature_slug** — git and file safe slug
  - Lowercase, kebab-case
  - Only a-z, 0-9 and -
  - Maximum 40 characters
  - Example: registration, login-logout
- **branch_name** — format: `feature/<feature_slug>`
  Example: feature/registration

If you cannot infer step_number or feature_title from $ARGUMENTS, ask the user to clarify before proceeding. Do not guess a step number silently.

## Step 3 — Check branch name is not taken
Run `git branch` to list existing branches. If branch_name is already taken, append a number: `feature/registration-01`, `feature/registration-02` etc.

## Step 4 — Detect and switch to the default branch, then pull latest
Run `git branch -a` and check whether `main` or `master` exists as the default branch. Prefer `main` if both exist. If neither exists, stop and tell the user no default branch was found.

Then run:
```
git checkout <default_branch>
git pull origin <default_branch>
```
If `git pull` fails (e.g. no network, no remote configured), tell the user the pull failed and ask whether to continue with the local copy or stop.

## Step 5 — Create and switch to the feature branch
Run:
```
git checkout -b <branch_name>
```

## Step 6 — Research the codebase
Read these files if they exist:
- CLAUDE.md — roadmap, conventions, schema
- app.py — existing routes and structure
- database/db.py — existing schema and functions
- All files in .claude/specs/ — avoid duplicating existing specs

If app.py, database/db.py, or CLAUDE.md do not exist yet, treat this as the first feature of the project — skip conflict checks against them and note in the spec that these files will be created fresh.

Check CLAUDE.md to confirm the requested step is not already marked complete (look for a roadmap/status table or checklist). If it is marked complete, warn the user and stop.

Check whether a spec file already exists at `.claude/specs/<step_number>-<feature_slug>.md`. If it does, tell the user it already exists and ask whether to overwrite it, version it (e.g. append `-v2`), or stop. Do not overwrite silently.

## Step 7 — Write the spec
Generate a spec document with this exact structure:

```
Spec: <feature_title>

Overview
One paragraph describing what this feature does and why it exists at this stage of the Spendly roadmap.

Depends on
Which previous steps this feature requires to be complete.

Routes
Every new route needed:
METHOD /path — description — access level (public/logged-in)
If no new routes: state "No new routes".

Database changes
Any new tables, columns, or constraints needed. Always verify against database/db.py before writing this (skip if this is the first feature and db.py does not exist yet). If none: state "No database changes".

Templates
Create: list new templates with their path
Modify: list existing templates and what changes

Files to change
Every file that will be modified.

Files to create
Every new file that will be created.

New dependencies
Any new pip packages. If none: state "No new dependencies".

Rules for implementation
Specific constraints Claude must follow. Always include:
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend base.html

Definition of done
A specific testable checklist. Each item must be something that can be verified by running the app.
```

## Step 8 — Save the spec
Save to: `.claude/specs/<step_number>-<feature_slug>.md`

## Step 9 — Commit the spec
Run:
```
git add .claude/specs/<step_number>-<feature_slug>.md
git commit -m "docs: add spec for <feature_title>"
```
This keeps the branch history clean before implementation begins. If the commit fails, tell the user and show the git error rather than continuing silently.

## Step 10 — Report to the user
Print a short summary in this exact format:
```
Branch:    <branch_name>
Spec file: .claude/specs/<step_number>-<feature_slug>.md
Title:     <feature_title>
```

Then tell the user: "Review the spec at .claude/specs/<step_number>-<feature_slug>.md then enter Plan Mode with Shift+Tab twice to begin implementation."

Do not print the full spec in chat unless explicitly asked.