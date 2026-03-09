# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

`cowork-platform` is the shared contracts and SDK repo. It holds the source-of-truth JSON Schema definitions and generates typed bindings for both Python and TypeScript consumers. Every other repo depends on this one — no other repo dependencies are allowed here.

## Architecture

```
contracts/
  schemas/      ← JSON Schema files (ToolRequest, ToolResult, PolicyBundle, event envelope, etc.)
  enums/        ← Shared enums (event names, error codes, session states)
  jsonrpc/      ← JSON-RPC method specs (CreateSession, StartTask, etc.)
generated/
  python/       ← Pydantic models (published as pip package via datamodel-code-generator)
  typescript/   ← TypeScript interfaces (published as npm package via json-schema-to-typescript)
sdk/
  python/       ← Python helpers (event envelope builders, retry, HTTP clients)
  typescript/   ← TypeScript helpers (JSON-RPC client, event listener)
```

## Key Conventions

- **JSON Schema is the source of truth.** Never hand-write Pydantic models or TypeScript interfaces that duplicate a schema — always generate them.
- **Codegen pipeline:** Schema change → run codegen → publish updated pip/npm packages → consumers import the new version.
- Python bindings use `datamodel-code-generator` to produce Pydantic models.
- TypeScript bindings use `json-schema-to-typescript` to produce interfaces.
- `contracts/` must NOT import any service or application repo.

## Key Schemas

| Schema | Used By |
|--------|---------|
| `ToolRequest` / `ToolResult` | Agent Host ↔ Tool Runtime |
| `ToolDefinition` | Tool Runtime → LLM (via Agent Host) |
| `PolicyBundle` | Policy Service → Session Service → Agent Host (includes optional `TeamPolicy`) |
| `ConversationMessage` | Agent Host → Workspace Service (session_history artifact) |
| `ApprovalRequest` | Agent Host → Desktop App (approval modal) |
| Event envelope | All components → Audit/Telemetry Services |

## Shared Error Shape

All error responses across the system use one shape:
```json
{ "code": "...", "message": "...", "retryable": false, "details": {} }
```

Standard codes: `INVALID_REQUEST`, `UNAUTHORIZED`, `SESSION_NOT_FOUND`, `SESSION_EXPIRED`, `POLICY_BUNDLE_INVALID`, `POLICY_EXPIRED`, `CAPABILITY_DENIED`, `APPROVAL_REQUIRED`, `APPROVAL_DENIED`, `TOOL_NOT_FOUND`, `TOOL_EXECUTION_FAILED`, `TOOL_EXECUTION_TIMEOUT`, `FILE_NOT_FOUND`, `FILE_TOO_LARGE`, `PERMISSION_DENIED`, `LLM_GUARDRAIL_BLOCKED`, `LLM_BUDGET_EXCEEDED`, `WORKSPACE_UPLOAD_FAILED`, `RATE_LIMITED`, `INTERNAL_ERROR`, `CODE_EXECUTION_TIMEOUT`, `TEAM_MODE_DISABLED`, `TEAM_WORKSPACE_INVALID`, `TEAMMATE_BUDGET_EXCEEDED`, `TEAMMATE_LIMIT_EXCEEDED`, `TASK_DEPENDENCY_CYCLE`

## Shared Enums

Event names: `session_created`, `session_started`, `step_started`, `step_completed`, `step_limit_approaching`, `text_chunk`, `llm_request_started`, `llm_request_completed`, `tool_requested`, `tool_completed`, `approval_requested`, `approval_resolved`, `policy_expired`, `task_completed`, `task_failed`, `session_completed`, `session_failed`

Component values: `DesktopApp`, `LocalAgentHost`, `LocalToolRuntime`, `LocalPolicyEnforcer`, `LocalApprovalUI`, `SessionService`, `LLMGateway`, `PolicyService`, `ApprovalService`, `WorkspaceService`, `AuditService`, `TelemetryService`, `BackendToolService`

## JSON-RPC Methods

Desktop App → Local Agent Host: `CreateSession`, `StartTask`, `CancelTask`, `ResumeSession`, `GetSessionState`, `GetPatchPreview`, `ApproveAction`, `Shutdown`

Local Agent Host → Desktop App (notifications): `SessionEvent`, `team/*` (6 team notification methods)

## Agent Teams Contracts

The `PolicyBundle` schema includes an optional `teamPolicy` section (`TeamPolicy` type) that controls team behavior:
- `maxTeammates` (int, 1–20): Maximum concurrent teammates
- `teammateBudget` (int, ≥1): Default token budget per teammate
- `allowedRoles` (string[]): Optional role allowlist (empty = all permitted)

When `teamPolicy` is absent, team creation is disabled. Team error codes: `TEAM_MODE_DISABLED`, `TEAM_WORKSPACE_INVALID`, `TEAMMATE_BUDGET_EXCEEDED`, `TEAMMATE_LIMIT_EXCEEDED`, `TASK_DEPENDENCY_CYCLE`.

Team JSON-RPC notifications bypass the `SessionEvent` envelope and use `team/*` method names: `team/created`, `team/teammate_created`, `team/teammate_removed`, `team/task_updated`, `team/message`, `team/teammate_output`.

---

## Engineering Standards

### Project Structure

```
cowork-platform/
  CLAUDE.md
  README.md
  Makefile
  pyproject.toml              # Generated Python package
  package.json                # Generated TypeScript package
  .python-version             # 3.12
  .nvmrc                      # 22
  contracts/
    schemas/                  # JSON Schema draft-2020-12 files
    enums/                    # Shared enum definitions
    jsonrpc/                  # JSON-RPC method specs
  generated/
    python/
      cowork_platform/
        __init__.py
        models.py             # Generated Pydantic v2 models
    typescript/
      src/
        index.ts
        models.ts             # Generated TypeScript interfaces
  sdk/
    python/
      cowork_platform_sdk/
        __init__.py
        retry.py              # Retry helpers (tenacity wrappers)
        http_client.py        # Async HTTP client factory
        event_builder.py      # Event envelope construction
      pyproject.toml
      tests/
    typescript/
      src/
        jsonrpc-client.ts
        event-listener.ts
      package.json
      tests/
  codegen/
    generate_python.sh
    generate_typescript.sh
    validate_schemas.sh
```

### Codegen Pipeline

```
contracts/schemas/*.json
    ↓ validate (JSON Schema draft-2020-12)
    ↓ datamodel-code-generator → generated/python/ (Pydantic v2 BaseModel)
    ↓ json-schema-to-typescript → generated/typescript/ (TypeScript interfaces)
    ↓ check-codegen (git diff --exit-code generated/)
```

**Rule:** Never hand-edit files in `generated/`. Always modify the schema and re-run codegen.

### Python Tooling

- **Python**: 3.12+
- **Linting/formatting**: `ruff` (replaces flake8, isort, black)
  - Enable rule sets: `E`, `F`, `W`, `I`, `N`, `UP`, `S`, `B`, `A`, `C4`, `SIM`, `TCH`, `RUF`
  - Line length: 100
- **Type checking**: `mypy --strict`
- **Testing**: `pytest` with `pytest-asyncio` for async SDK helpers
- **Coverage**: 90% minimum for SDK code

### TypeScript Tooling

- **Node**: 22 LTS
- **TypeScript**: 5.7+ with `strict: true`
- **Linting**: ESLint 9 flat config with `typescript-eslint/strict`
- **Formatting**: Prettier (single quotes, trailing commas, 100 print width)
- **Testing**: Vitest for SDK helpers

### Versioning

- Schema versions: CalVer within the schema (`"schemaVersion": "2026.02.1"`)
- Python package: SemVer (`0.1.0`, `1.0.0`)
- TypeScript package: mirrors Python package version exactly
- Breaking schema changes → major version bump for both packages
- Both packages published atomically (CI publishes both or neither)

### Makefile Targets

```
make help              # Show all targets
make install           # Install Python + Node dependencies
make validate          # Validate all JSON Schema files
make codegen           # Run all codegen (Python + TypeScript)
make codegen-python    # Generate Pydantic models only
make codegen-ts        # Generate TypeScript interfaces only
make check-codegen     # Verify generated code matches schemas (CI)
make lint              # Lint Python + TypeScript
make format            # Format Python + TypeScript
make format-check      # Check formatting without modifying
make typecheck         # Typecheck Python (mypy) + TypeScript (tsc)
make test              # Run all tests (Python + TypeScript)
make test-py           # Python SDK tests only
make test-ts           # TypeScript SDK tests only
make build             # Build distributable packages
make check             # CI gate: validate + check-codegen + lint + typecheck + test
make clean             # Remove generated artifacts and caches
```

### Error Handling (SDK)

The Python SDK should provide:
- `CoworkAPIError` base exception with `code`, `message`, `retryable`, `details` fields matching the shared error shape
- Subclasses: `NotFoundError`, `UnauthorizedError`, `RateLimitedError`, `InternalError`
- HTTP client helpers that parse error responses into typed exceptions
- Retry helpers that only retry when `retryable=True`

### Testing

- **Schema validation tests**: Verify all schemas are valid JSON Schema draft-2020-12
- **Codegen round-trip tests**: Generate models, instantiate them with sample data, serialize back to JSON, validate against schema
- **SDK unit tests**: Test retry logic, HTTP client error parsing, event envelope building
- Pytest markers: `@pytest.mark.unit` for all Python tests
