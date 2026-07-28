# AegisOps: Technical Architecture & Project Foundation
## Phase 2 — Technical Blueprint
### Technical Stack: Python (FastAPI) + React (TypeScript) + PostgreSQL + TimescaleDB

---

## 1. Repository Architecture

AegisOps adopts an enterprise **Monorepo** pattern to house all backend code, frontend interfaces, infrastructure scripts, and documentation under a single version-controlled repository.

### 1.1. Monorepo Philosophy & Justification
*   **Single Source of Truth**: All core services, frontend assets, configurations, and documentation versions are locked in lockstep, preventing API drift and synchronization issues.
*   **Shared Contract & Type Safety**: API schemas (Pydantic models) can be shared or compiled into TypeScript types directly within the monorepo, guaranteeing immediate frontend/backend synchronization.
*   **Atomic Commits**: Features affecting both frontend and backend (e.g., adding a new AI provider parameter) can be reviewed, merged, and reverted in a single pull request.
*   **Dependency Management**: Shared tooling configurations (linting, formatting, testing pipelines) are defined at the root level, avoiding configuration duplication across services.

### 1.2. Complete Directory Tree
```text
/aegisops (Root)
├── .github/                       # CI/CD pipelines (workflows)
├── .vscode/                       # Shared VSCode workspace settings & extensions
├── docs/                          # Project documentation
│   ├── architecture/              # High-level architecture docs
│   ├── api/                       # API documentation (OpenAPI specs)
│   ├── runbooks/                  # Incident response runbooks
│   └── decisions/                 # Architecture Decision Records (ADRs)
│       ├── ADR-001-monorepo.md
│       ├── ADR-002-fastapi-backend.md
│       ├── ADR-003-react-vite-frontend.md
│       └── ADR-004-ai-hub-abstraction.md
├── backend/                       # Python FastAPI codebase
│   ├── app/                       # Main application core
│   │   ├── api/                   # API version routing, controllers, schemas
│   │   ├── core/                  # Clean Architecture Layers (Domain & Use Cases)
│   │   ├── services/              # External service integrations (K8s, Monitoring)
│   │   ├── providers/             # AI Provider Hub implementations
│   │   ├── infrastructure/        # Framework drivers (databases, caches, logging)
│   │   └── main.py                # FastAPI entry point
│   ├── tests/                     # Test suite (Unit, Integration, Chaos)
│   ├── poetry.lock                # Python dependency lockfile
│   └── pyproject.toml             # Poetry project config
├── frontend/                      # React / TypeScript / Vite codebase
│   ├── src/                       # Application source
│   │   ├── assets/                # Styling variables, image assets
│   │   ├── components/            # Shared presentation UI components
│   │   ├── features/              # Feature modules (Monitoring, Incident, Healing)
│   │   ├── hooks/                 # Custom global React hooks
│   │   ├── providers/             # Context Providers (Auth, Theme, Socket)
│   │   ├── services/              # API clients, logging adapters
│   │   ├── store/                 # State management (Zustand)
│   │   └── types/                 # TypeScript interfaces and shared types
│   ├── package.json               # NPM package manifest
│   ├── tsconfig.json              # TypeScript compilation rules
│   └── vite.config.ts             # Vite configuration
├── deployments/                   # Deployment manifests
│   ├── docker/                    # Dockerfiles and docker-compose templates
│   ├── helm/                      # Helm charts for Kubernetes deployments
│   └── terraform/                 # Infrastructure as Code templates (OpenTofu)
├── Makefile                       # Shared root build instructions
├── pyproject.toml                 # Root linter (Ruff, Black) rules
└── README.md                      # Monorepo onboarding guide
```

### 1.3. Folder Descriptions
*   `docs/decisions/`: Stores Architectural Decision Records (ADRs) tracking significant technical compromises and pivots.
*   `backend/app/core/`: Separates clean architecture layers (domain entities and business use cases) from framework implementations.
*   `frontend/src/features/`: Groups related UI, logic, and state into cohesive functional modules (e.g., `features/self-healing`, `features/k8s-manager`) to facilitate horizontal scale.
*   `deployments/`: Contains isolated environments (Docker/K8s/Terraform) to maintain strict separation between business logic and deployment mechanisms.

---

## 2. Backend Architecture (FastAPI & Clean Architecture)

The backend utilizes **FastAPI** to build a high-performance, asynchronous REST and WebSocket API. The design complies strictly with Clean Architecture and Domain-Driven Design (DDD) principles.

```
+-----------------------------------------------------------------------------------+
|                            FRAMEWORKS & DRIVERS                                   |
|   (FastAPI routes, HTTP middlewares, TortoiseORM/SQLAlchemy, Redis, NATS, Vault)  |
+-----------------------------------------------------------------------------------+
                                         ||
                                         \/
+-----------------------------------------------------------------------------------+
|                            INTERFACE ADAPTERS                                     |
|    (Pydantic Schemas, Controller routes, Database repositories, SDK Clients)       |
+-----------------------------------------------------------------------------------+
                                         ||
                                         \/
+-----------------------------------------------------------------------------------+
|                            APPLICATION BUSINESS RULES                             |
|      (Use cases: ExecuteSelfHealing, CorrelateMetrics, AnalyzeIncident)           |
+-----------------------------------------------------------------------------------+
                                         ||
                                         \/
+-----------------------------------------------------------------------------------+
|                            ENTERPRISE BUSINESS RULES                              |
|          (Domain models: Incident, AIProvider, Runbook, Cluster entity)           |
+-----------------------------------------------------------------------------------+
```

### 2.1. Layer Responsibilities

#### 2.1.1. Bounded Context Directories
*   `backend/app/core/domain/`: Defines entities, value objects, and repository interfaces. Completely pure Python (no SQLAlchemy, no FastAPI, no third-party imports).
*   `backend/app/core/usecases/`: Coordinates specific application tasks (e.g., invoking the AI incident analysis pipeline, resolving alerts). Depends only on domain interfaces.
*   `backend/app/api/v1/`: HTTP endpoints. Defines path variables, returns responses matching JSON schema contracts, and validates structures using Pydantic models.
*   `backend/app/infrastructure/`: Implementations of database persistence (SQLAlchemy ORM models, repository patterns, migration tables), redis configurations, NATS workers, and logging providers.

#### 2.1.2. Specific Engine Modules
*   **Monitoring Engine (`services/monitoring`)**: Connects to external Prometheus/OpenTelemetry agents, issues downsampling commands, and stores telemetry blocks.
*   **Incident Engine (`services/incidents`)**: Periodically reads metric partitions, runs static threshold tests, and evaluates machine learning anomalies.
*   **Healing Engine (`services/healing`)**: Translates triggers to automated executions, establishes SSH connections, calls Kubernetes rollouts, and records logs.
*   **AI Engine (`providers/ai`)**: Implements the provider abstraction factory, translating generic prompts into OpenAI, Bedrock, or Ollama completions.

### 2.2. Dependency Injection
FastAPI's native dependency injection engine (`Depends`) is utilized to resolve interfaces at runtime. 
```python
# Example interface injection inside endpoints
@router.post("/incidents/{incident_id}/analyze")
async def analyze_incident(
    incident_id: str,
    use_case: AnalyzeIncidentUseCase = Depends(get_analyze_incident_use_case)
):
    return await use_case.execute(incident_id)
```
The helper dependency resolution functions (e.g., `get_analyze_incident_use_case`) reside within `backend/app/api/dependencies.py` to decouple controller routes from active database configurations.

---

## 3. Frontend Architecture (React, TypeScript & Vite)

The frontend is structured to be feature-modular rather than file-type modular, preventing long directory listings and keeping related views, hooks, and components localized.

### 3.1. Detailed Frontend Layout
*   `src/components/`: Reusable, layout-agnostic atomic design structures (e.g., `Button`, `Modal`, `Table`, `Card`).
*   `src/features/`: Contains self-contained application modules. Each folder contains its own page structures, sub-components, zustand slice stores, and custom feature hooks.
    ```text
    src/features/self-healing/
    ├── components/         # Feature-specific sub-components (e.g., RunbookVisualizer)
    ├── hooks/              # Custom hooks for fetching healing logs
    ├── store/              # Zustand slice store for active runbooks
    ├── views/              # Pages/tabs for self-healing configurations
    └── index.ts            # Public entry point exposing the view components
    ```
*   `src/providers/`: Houses application wrapper contexts, including:
    *   `AuthProvider`: Tracks OAuth JWT tokens, refresh routines, and user profile permissions.
    *   `ThemeProvider`: Interchanges root level CSS custom variables to handle styling transitions.
    *   `SocketProvider`: Connects to background server WebSockets to receive real-time incident event updates.
*   `src/store/`: Central state store utilizing **Zustand**. Manages global state configurations, workspace mappings, and navigation layouts.

---

## 4. Configuration Strategy

AegisOps applies a multi-level, priority-driven configuration engine to manage parameters across development, testing, staging, and production environments.

### 4.1. Core Design Parameters
*   **Twelve-Factor Alignment**: All configuration variables are extracted from environment variables. No credentials, endpoints, or keys are hardcoded in the codebase.
*   **Configuration Priority Logic**:
    ```
    (Highest) 1. Kubernetes Secret / Env Override
              2. Vault Secret Injection
              3. Local System Environment Variables
              4. .env Configuration File
    (Lowest)  5. Default Pydantic Settings
    ```

### 4.2. Environment-Specific Config Matrix
*   **Development**: Loads from local `.env.development` file. Caching uses in-memory mock structures instead of local Redis clusters.
*   **Testing**: Configured to run database queries against isolated SQLite schemas or dockerized testcontainers. Instantiates mock AI adapters to prevent API costs.
*   **Production / Cloud**: Vault configurations are injected as environment variables inside pod definitions via Kubernetes sidecar agents. Enforces strict SSL configuration checks.

### 4.3. Feature Flags
AegisOps manages feature rollouts using a local configuration file parsed at runtime, which checks user roles before enabling beta features (e.g., AI auto-remediation triggers). This provides safe progression paths before code is fully promoted.

---

## 5. Development Environment

To eliminate "works on my machine" inconsistencies, the engineering team adopts fixed environment variables and dependencies across all workstations.

### 5.1. Version Recommendations

| Component | Target Version | Selection Rationale |
| :--- | :--- | :--- |
| **Python** | `3.11.x` | High runtime optimization over previous versions, solid compatibility with data science packages and standard ASGI engines. |
| **Node.js** | `20.x LTS` | Active Long-Term Support version, featuring stable execution paths and standard performance metrics. |
| **Docker** | `24.0.x+` | Compatibility with advanced compose schemas, buildkit features, and standard container lifecycle systems. |
| **Kubernetes** | `1.28.x+` | Standard target cluster version. Matches current cloud providers (EKS, GKE, AKS) standard baseline specs. |
| **OpenTofu / Terraform** | `1.6.x+` | Focuses on open-source infrastructure management engines, eliminating commercial licensing risks. |
| **Git** | `2.40.x+` | Supports advanced branch switching pipelines and robust hook integrations. |

### 5.2. Tooling & Extensions
*   **IDE**: Microsoft VSCode / Cursor.
*   **Extensions**: Ruff (Python Linting), Pytest Runner, ESLint, Prettier, Postman/Thunder Client, HashiCorp Terraform.
*   **Linters & Formatters**:
    *   *Backend*: **Ruff** for super-fast linting and format enforcement (replaces flake8, black, isort).
    *   *Frontend*: **ESLint** for code analysis, **Prettier** for structure format rules.
*   **API Testing**: Local Swagger UI endpoint (`/docs`) generated natively by FastAPI, or shared Bruno configuration structures.

---

## 6. Package Management Strategy

AegisOps strictly enforces locked dependency schemas using lockfiles to guarantee build reproducibility across CI environments and target deploy nodes.

```
       +---------------------------------------------+
       |             Monorepo Root Level             |
       |  - Shared configs, Ruff rules, Makefiles    |
       +----------------------++---------------------+
                              ||
             +----------------+----------------+
             |                                 |
             \/                                \/
+--------------------------+      +--------------------------+
|      backend/            |      |      frontend/           |
|  - Dependency: Poetry    |      |  - Dependency: NPM/PNPM  |
|  - pyproject.toml        |      |  - package.json          |
|  - poetry.lock           |      |  - package-lock.json     |
+--------------------------+      +--------------------------+
```

### 6.1. Dependency Abstraction

#### 6.1.1. Backend Dependencies (`backend/pyproject.toml`)
*   **Package Tool**: **Poetry**. Poetry manages clean virtual environments, generates deterministic lockfiles (`poetry.lock`), and cleanly separates developer utilities from core execution components.
*   **Version Pinning Strategy**:
    *   All external packages are strictly pinned to exact patch versions (e.g., `fastapi = "0.109.2"`, `pydantic = "2.6.1"`).
    *   Updating dependencies requires executing `poetry update <package>` on a local branch, running the test suite, and committing the modified `poetry.lock`.

#### 6.1.2. Frontend Dependencies (`frontend/package.json`)
*   **Package Tool**: **NPM** (or **PNPM** for optimized caching).
*   **Strategy**: All packages are configured without wildcard ranges (`package-lock.json` must be committed) to protect builds from dependency vulnerabilities.

---

## 7. Git Strategy

AegisOps utilizes **Trunk-Based Development** paired with strict commit conventions to maintain a clean git history and enable automated changelog generation.

### 7.1. Workflow Lifecycle
1.  **Branch Names**: Developers cut branches from `main` using descriptive naming patterns:
    *   `feat/` for new operational features.
    *   `fix/` for bug resolution paths.
    *   `docs/` for writing manuals and ADRs.
    *   `refactor/` for modifying structures without functional changes.
2.  **Conventional Commits**: Commit messages must adhere to the structured syntax: `<type>(<scope>): <description>`.
    *   *Example*: `feat(ai): add retry logic to anthropic client wrapper`
    *   *Example*: `fix(healing): check pod readiness status before rolling restart completion`
3.  **Merge Mechanics**:
    *   Direct commits to `main` are blocked.
    *   Merging requires a Pull Request (PR) passing all CI lint/test pipelines.
    *   Pull Requests require a peer review approval.
    *   **Squash and Merge** is enforced. This turns development branches into single clean commits on `main`, ensuring readability of the central git history.

---

## 8. Documentation Strategy

To maintain operational efficiency, technical documentation is written in markdown and co-located with the codebase inside the `/docs` directory.

### 8.1. Document Directory Mapping

| Document Target | Location | Purpose |
| :--- | :--- | :--- |
| **Monorepo Onboarding** | `README.md` (Root) | Explains repository structure, local prerequisites, and initialization commands (`make install`). |
| **Architecture Decisions** | `docs/decisions/` | Architectural Decision Records (ADRs) tracking engineering compromises and tech stack changes. |
| **API Manual** | `docs/api/` | Complete OpenAPI schema diagrams and websocket event specifications. |
| **Operator Runbooks** | `docs/runbooks/` | Execution guides for human operations during critical incident situations. |
| **Security Controls** | `docs/SECURITY.md` | Detailing vulnerability report patterns, encryption keys rotation, and compliance matrices. |

---

## 9. Coding Standards

Every engineer must adhere to the coding style regulations defined below to ensure high code readability and maintainability.

### 9.1. Python (Backend PEP-8 & Modern Standards)
*   **Type Hinting**: All function parameters and return structures must feature explicit type hints.
    ```python
    async def get_incident_status(self, incident_id: uuid.UUID) -> IncidentStatus:
    ```
*   **Async/Await**: I/O bound operations (database calls, AI completions, network requests) must be handled asynchronously using Python's `asyncio` loop.
*   **Variable/Folder Naming**:
    *   Folders and Files: Snake case (`self_healing/`, `incident_engine.py`).
    *   Variables and Functions: Snake case (`active_nodes`, `calculate_latency_avg()`).
    *   Classes: CamelCase (`KubernetesClusterRepository`).

### 9.2. TypeScript / React Standards
*   **Component Structure**: React components must be written as functional components using hook patterns. Avoid class-based components.
*   **Type Guarding**: Do not use the `any` keyword. All interfaces and variables must resolve to strict TypeScript types.
*   **File Naming**:
    *   Presentation Components: CamelCase with `.tsx` suffix (`IncidentDashboard.tsx`).
    *   Hooks and helpers: CamelCase with `.ts` suffix (`useIncidentLogs.ts`).

---

## 10. Logging Strategy

AegisOps implements structured JSON logging to output telemetry in formats easily parsed by Grafana Loki, Elasticsearch, or OpenSearch.

### 10.1. Logging Format Structure
Logs are written to standard output (`stdout`) as single-line JSON records containing consistent context keys:
```json
{
  "timestamp": "2026-07-26T20:57:51.045Z",
  "level": "INFO",
  "trace_id": "tr-92837190-2819",
  "span_id": "sp-83710-18",
  "user_id": "usr-8391",
  "module": "self_healing",
  "msg": "Runbook execution initiated for target deployment",
  "context": {
    "deployment_name": "auth-service",
    "namespace": "production",
    "runbook_id": "rb-restart-pod-9"
  }
}
```

### 10.2. Log Levels & Scopes
*   `DEBUG`: Highly verbose variables outputs, query statements (disabled by default in production).
*   `INFO`: Standard operational changes, user logons, alert clearances.
*   `WARNING`: Recoverable errors (e.g., AI API returned a timeout, retrying request).
*   `ERROR`: Unhandled operational issues (e.g., self-healing action failed verification loop).
*   `CRITICAL`: System-wide failures (e.g., primary PostgreSQL connection lost, NATS broker down).

---

## 11. Error Handling Strategy

AegisOps designs a consistent error catching and translation layer. Errors are modeled as structured domain exceptions and mapped to client responses in the adapter layer.

```
       +---------------------------------------------+
       |             Infrastructure Layer            |
       |  - Catch low-level PostgreSQL connection err|
       +----------------------++---------------------+
                              ||
                              \/
       +---------------------------------------------+
       |                 Domain Layer                |
       |  - Raise typed domain exception             |
       |    (e.g., DatabaseUnreachableError)         |
       +----------------------++---------------------+
                              ||
                              \/
       +---------------------------------------------+
       |                 Adapter Layer               |
       |  - FastAPI Exception Handler converts error |
       |  - Returns consistent error payload to API  |
       +---------------------------------------------+
```

### 11.1. Client Response Payload
When an API route fails, the server responds with a standard error envelope:
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested cluster instance does not exist or has been cordoned.",
    "trace_id": "tr-92837190-2819",
    "details": {
      "cluster_id": "cl-prod-east-1"
    }
  }
}
```

### 11.2. Specific Error Types
*   **Validation Errors**: Returns HTTP 422. Outlines exactly which field failed schema checks.
*   **Authentication / Authorization Errors**: Returns HTTP 401 (Invalid signature/Expired token) or HTTP 403 (Insufficient permissions).
*   **AI Provider Failures**: Catches API timeouts and issues fallbacks without failing the parent incident context.

---

## 12. Testing Strategy

To guarantee the reliability of autonomous operations, AegisOps implements a rigorous testing pyramid containing automated static checks, functional tests, and runtime chaos scenarios.

```
                  / \
                 /   \
                / E2E \  <-- UI Scenarios (Playwright)
               /-------\
              /  Chaos  \  <-- Network splits & pod failures
             /-----------\
            / Integration \  <-- Docker Testcontainers / DB schemas
           /---------------\
          /      Unit       \  <-- Core domain logic testing (Pytest)
         /-------------------\
```

### 12.1. Testing Hierarchy
*   **Unit Tests**: Written using `pytest` and `pytest-asyncio`. Aims for >85% code coverage on core domain services (`backend/app/core/`). Utilizes unittest mock utilities to isolate dependencies.
*   **Integration Tests**: Validates repository implementations and database query scripts against real postgres containers using `testcontainers-python`.
*   **E2E Testing**: UI workflow testing using Playwright to verify dashboard features, logins, and settings screens.
*   **Chaos Testing**: Emulates network splits, high disk usage, and container termination loops to verify the self-healing and alert engine responses.

---

## 13. Security Foundation

AegisOps applies a Zero Trust model to verify identity, credentials, and network paths at every execution step.

### 13.1. Authentication Framework
*   **JWT Token Handshake**: Keycloak issues RSA-256 signed JSON Web Tokens. The API Gateway caches Keycloak's public keys to verify signatures locally without executing network calls.
*   **Role-Based Access Control (RBAC)**: All routes are protected by a role assertion decorator. Inside modules, access is parsed using fine-grained scopes:
    ```python
    @router.post("/runbooks/execute", dependencies=[Depends(RequirePermission("runbook:write"))])
    async def trigger_runbook(req: RunbookTriggerRequest):
        ...
    ```

### 13.2. Vault Integration
Configuration templates reference Vault path keys. At startup, the infrastructure manager connects to Vault using local service account credentials, fetches the decrypted secrets, and maps them to application memory. Secret keys are never stored on persistent storage disks.

---

## 14. Project Roadmap (Milestones)

The engineering timeline splits the 12-month development cycle into measurable execution gates.

### Milestone 1: Workspace & Core AI Abstraction (Months 1–3)
*   **Goal**: Establish the local monorepo directory, configure code formatting engines, and build the AI Provider Hub interfaces.
*   **Deliverables**: Main directory structures, Keycloak SSO integration templates, Pydantic configuration schemas, and unit tested OpenAI/Ollama factory clients.
*   **Success Criteria**: Running API server returning health check stats and processing test LLM requests.

### Milestone 2: observability & Detection (Months 4–5)
*   **Goal**: Connect metric streams and define alert criteria.
*   **Deliverables**: TimescaleDB partitioning setup, OpenTelemetry gRPC receiver endpoints, and static rule evaluations.
*   **Success Criteria**: Local test instances pushing real-time container metrics that successfully trigger critical incident states in the database.

### Milestone 3: Self-Healing & Kubernetes manager (Months 6–7)
*   **Goal**: Enable automation loops and cluster control features.
*   **Deliverables**: Secure WebSocket log streaming proxy, SSH script runner modules, and self-healing verification loops.
*   **Success Criteria**: AI-driven analysis generating a pod restart operation in response to a simulated `CrashLoopBackOff` incident.

---

## 15. Risk Assessment

| Risk Domain | Risk Event | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Operational** | AI engine runs incorrect self-healing actions, causing cascading container outages. | High | Enforce namespace isolation boundaries; require SRE confirmation on high-risk runbooks (e.g., node drain). |
| **Performance** | Telemetry ingestion locks database partitions during system spikes. | Medium | Implement memory-backed buffering inside collectors; configure downsampling intervals in TimescaleDB. |
| **Security** | Hardcoded developer credentials committed to public code branches. | High | Enforce githooks running Gitleaks audits on every developer commit action. |
| **Architectural** | Core packages (FastAPI/Pydantic) undergo major breaking syntax updates. | Medium | Pin all libraries to exact patch versions; restrict direct library usage outside of the infrastructure layer. |
