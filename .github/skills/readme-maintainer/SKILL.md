---
name: readme-maintainer
description: "Use when you need to update, review, or refresh the project README.md so it stays accurate, concise, and aligned with the current codebase."
---

# README Maintainer

Use this skill when the project README needs to be updated, audited, or rewritten for accuracy and maintainability.

## When to use this skill

- A feature, command, or dependency changed.
- The project structure or startup flow changed.
- The README is outdated or inconsistent with the current code.
- A release, handoff, or onboarding update is needed.

## Workflow

1. Gather the source of truth
   - Read the current README.
   - Inspect the repository files that define behavior, such as the entry point, dependency files, and package configuration.
   - Note actual commands, ports, environment variables, and supported features.

2. Compare the README with reality
   - Verify that setup steps match the current dependency installation flow.
   - Confirm that run instructions match the real entry point and startup command.
   - Check that referenced files, folders, and modules still exist.
   - Make sure claims about features, ports, and behavior are still true.

3. Update the README structure
   - Keep sections focused and practical: overview, setup, run instructions, project structure, and maintenance notes.
   - Prefer short bullets and copy-paste-ready commands.
   - Remove stale content instead of preserving outdated examples.

4. Improve clarity for maintainers and contributors
   - Explain the purpose of the project in plain language.
   - Highlight the most important setup and run steps first.
   - Keep troubleshooting and maintenance notes actionable.

5. Validate before finishing
   - Ensure there is no contradictory or outdated information.
   - Check that commands are accurate and easy to follow.
   - If possible, verify the documented steps with a local run or a quick inspection of the relevant files.

## Quality checklist

- The README reflects the current repository structure.
- Setup and run instructions are accurate.
- File names, commands, and ports are current.
- The document is concise and easy to scan.
- The content is useful for onboarding and future maintenance.

## Expected output

Produce either:
- an updated README draft, or
- a brief summary of the changes made, including what was corrected and why.

## Example prompts

- Update the README so it matches the current project structure and startup flow.
- Review the README for stale setup instructions and fix them.
- Rewrite the README to make onboarding clearer for new contributors.
