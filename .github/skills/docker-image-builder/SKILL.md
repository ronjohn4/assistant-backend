---
name: docker-image-builder
description: "Use when you need to build, verify, or troubleshoot a Docker image for this repository."
---

# Docker Image Builder

Use this skill when you need to build the container image for the assistant backend or troubleshoot a failed Docker build.

## When to use this skill

- You want to build the project image locally.
- The Dockerfile or dependencies changed and need a fresh build.
- The image build is failing and needs a guided troubleshooting pass.

## Prerequisites

- Docker is installed and running.
- You are in the repository root.
- The project has a valid Dockerfile and dependency metadata.

## Workflow

1. Confirm the build context
   - Make sure you are in the repository root.
   - Review the Dockerfile to confirm the intended base image, exposed port, and startup command.

2. Build the image
   - Run:
     - `docker build -t ronjohn4/assistant-backend .`
   - Use a more verbose build if you need detailed output:
     - `docker build --progress=plain -t ronjohn4/assistant-backend .`

3. Verify the build
   - Confirm the build completed successfully with exit code 0.
   - If the build fails, inspect the failing step and fix the underlying issue before retrying.

4. Optionally run the container
   - Start the image locally with:
     - `docker run --rm -p 5010:5010 --env-file .env ronjohn4/assistant-backend`
   - Check that the app starts correctly and that the health endpoint responds.

5. Troubleshoot common issues
   - Dependency install failures: verify `pyproject.toml` and the base image compatibility.
   - Network-related failures: retry the build with a stable network connection.
   - Startup errors: confirm required environment variables are present and the container port matches the app configuration.

## Quality checklist

- The Docker image builds successfully.
- The container starts without crashing.
- The application is reachable on the expected port.
- Any environment or dependency issues are documented or resolved.

## Expected output

Provide either:
- a successful image build confirmation with the image tag, or
- a concise summary of the build issue and the fix applied.

## Example prompts

- Build the Docker image for this project.
- Rebuild the container after changing dependencies.
- Troubleshoot the Docker build for this repository.
