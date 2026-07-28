# ADR-001: Monorepo Architecture for AegisOps

## Status
Approved

## Context
AegisOps is a multi-component DevOps platform consisting of a Python (FastAPI) backend, a React (TypeScript) frontend, infrastructure configuration code (Terraform, Docker Compose, Kubernetes manifests), and technical manuals/runbooks.
Historically, development of component layers across distinct repositories has led to API contract drift, dependency synchronization overhead, and complex local developer onboarding scripts.

## Decision
We will organize the AegisOps project as a **Monorepo** using a single version-controlled repository.

### Key Details:
- **Root Level**: Stores shared project rules, formatting/linting definitions, CI/CD scripts (`.github/workflows`), and overall system documentation.
- **Backend Directory (`/backend`)**: Governs the core FastAPI application using its own Poetry dependency context.
- **Frontend Directory (`/frontend`)**: Manages the React application utilizing Node/NPM.
- **Deployment Manifests (`/deployments`)**: Isolates Docker Compose, Kubernetes Helm charts, and OpenTofu/Terraform modules.

## Consequences
### Positive:
- **Atomic Commits**: Full features (spanning schema models, backend REST controllers, frontend stores, and deployment configs) are reviewable and mergeable in single Git changesets.
- **Unified Tooling**: Global tooling rules (like linting and code formatting) are synchronized.
- **Simplified Dependency Locking**: API changes immediately notify corresponding frontend and infrastructure layers.

### Negative:
- **Build Speeds**: CI build tasks must employ path filtering (`paths-ignore` or intelligent changed-file checks) to prevent full-repository rebuilds on narrow doc updates.
- **Repository Size**: Local clones retrieve full histories of all systems (can be mitigated with Git sparse checkout configurations if required).
