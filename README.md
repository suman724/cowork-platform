# cowork-platform

Shared contracts, generated bindings, and SDK helpers for the cowork project. This is the single source of truth for all API shapes — every other repo depends on this package.

## What's Inside

```
contracts/schemas/     JSON Schema definitions (21 schemas)
contracts/enums/       Shared enums (error codes, event types, etc.)
contracts/jsonrpc/     JSON-RPC method specs (Desktop ↔ Agent Host)
generated/python/      Pydantic v2 models (auto-generated, do not hand-edit)
generated/typescript/  TypeScript interfaces (auto-generated, do not hand-edit)
sdk/python/            Python SDK: error classes, HTTP client, event builder
sdk/typescript/        TypeScript SDK: error classes, constants, event builder
```

## Setup

```bash
# Install everything
make install

# Or individually:
pip install -e ".[sdk,dev]"     # Python
npm install                      # TypeScript
```

Requires Python 3.12+ and Node 22+.

## Development Workflow

### Modifying a Schema

1. Edit the JSON Schema file in `contracts/schemas/`
2. Run codegen: `make codegen`
3. Run tests: `make test`
4. Commit the schema change **and** the regenerated code together

### Running Tests

```bash
make test          # All tests (Python + TypeScript)
make test-py       # Python only (27 tests)
make test-ts       # TypeScript only (22 tests)
```

### Linting & Type Checking

```bash
make check         # Full CI gate: validate + codegen check + lint + typecheck + test
make lint          # Lint both languages
make typecheck     # mypy + tsc --noEmit
```

### Codegen

```bash
make codegen           # Regenerate all bindings
make codegen-python    # Python only (datamodel-code-generator)
make codegen-ts        # TypeScript only (json-schema-to-typescript)
make validate          # Validate schemas against JSON Schema draft-2020-12
make check-codegen     # CI check: regenerate and verify no diff
```

## Key Schemas

| Schema | Purpose |
|--------|---------|
| `ToolRequest` / `ToolResult` | Agent Host ↔ Tool Runtime communication |
| `ToolDefinition` | Tool metadata sent to LLM |
| `PolicyBundle` | Governance: capabilities, LLM limits, approval rules |
| `Session` / `SessionCreate*` | Session lifecycle |
| `ConversationMessage` | Chat history stored as workspace artifacts |
| `ApprovalRequest` / `ApprovalDecision` | Human-in-the-loop approval flow |
| `EventEnvelope` | Standard event wrapper for audit/telemetry |
| `ErrorResponse` | Shared error shape (20 standard codes) |
| `Workspace` / `Artifact` | Artifact and workspace management |
| `TraceSpan` | Distributed tracing spans |

## SDK Usage

### Python

```python
from cowork_platform_sdk import (
    CoworkAPIError, CapabilityDeniedError, ErrorCode,
    build_event, EventType, Component,
    create_http_client, raise_for_status,
)

# Create an error
err = CapabilityDeniedError(
    message="Shell.Exec not allowed",
    details={"capability": "Shell.Exec"},
)

# Deserialize an error response
err = CoworkAPIError.from_dict(response_json)
if err.retryable:
    # retry logic

# Build an event envelope
event = build_event(
    event_type=EventType.TOOL_COMPLETED,
    tenant_id="tenant_abc",
    user_id="user_123",
    session_id="sess_789",
    component=Component.LOCAL_AGENT_HOST,
    payload={"toolName": "ReadFile", "durationMs": 42},
)

# Create a configured HTTP client
client = create_http_client(base_url="https://api.example.com")
```

### TypeScript

```typescript
import {
  CoworkAPIError, CapabilityDeniedError, ErrorCode,
  buildEvent, EventType, Component,
} from "@cowork/platform/sdk/typescript/src";

// Create an error
const err = new CapabilityDeniedError("Shell.Exec not allowed", {
  details: { capability: "Shell.Exec" },
});

// Deserialize an error response
const restored = CoworkAPIError.fromJSON(responseJson);

// Build an event envelope
const event = buildEvent({
  eventType: EventType.TOOL_COMPLETED,
  tenantId: "tenant_abc",
  userId: "user_123",
  sessionId: "sess_789",
  component: Component.LOCAL_AGENT_HOST,
  payload: { toolName: "ReadFile", durationMs: 42 },
});
```

## Versioning

- **Schemas**: CalVer within the schema files (e.g., `"schemaVersion": "2026.02.1"`)
- **Python package**: SemVer (`0.1.0`)
- **TypeScript package**: Mirrors Python version exactly
- Both packages are published atomically — CI publishes both or neither
