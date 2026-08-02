---
description: Push current feature branch, create and merge a GitHub PR, sync main, and clean up merged feature branch.
allowed-tools: Bash(git:*), mcp__github__*
---

You are completing the current Git feature branch workflow.

Execute the following steps **in order**:

1. Determine the current Git branch.
2. If the current branch is `main`, stop immediately and inform the user that this command must be run from a feature branch.
3. Push the current branch and all latest commits to `origin`.
4. Using the GitHub MCP server, create a Pull Request from the current branch into `main`.
5. If repository permissions and branch protection rules allow, automatically review (if permitted) and merge the Pull Request.
6. If the merge is not possible because of required reviews, failed checks, merge conflicts, or insufficient permissions, stop immediately, explain the reason, and wait for the user's instructions.
7. After a successful merge:
   - Delete the remote feature branch if it still exists.
   - Switch to the local `main` branch.
   - Pull the latest changes from `origin/main`.
   - Delete the local feature branch using a safe delete (`git branch -d`).

Safety rules:

- Never delete the `main` branch.
- Never force delete a local branch (`git branch -D`) unless the user explicitly requests it.
- Never force push.
- Verify that the branch being deleted is not `main`.
- Stop immediately if any Git or GitHub operation fails and explain the reason before continuing.
- Report the result of each completed step.