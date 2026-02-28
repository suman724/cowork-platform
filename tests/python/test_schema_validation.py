"""Tests that all JSON schemas are valid and generated models work correctly."""

import json
from pathlib import Path

import pytest

SCHEMAS_DIR = Path(__file__).resolve().parent.parent.parent / "contracts" / "schemas"


@pytest.mark.unit
class TestSchemaFiles:
    """Verify all schema files are valid JSON."""

    def test_all_schemas_are_valid_json(self) -> None:
        schema_files = list(SCHEMAS_DIR.glob("*.json"))
        assert len(schema_files) > 0, "No schema files found"

        for sf in schema_files:
            data = json.loads(sf.read_text())
            assert "$schema" in data, f"{sf.name} missing $schema"
            assert "title" in data, f"{sf.name} missing title"

    def test_schema_count(self) -> None:
        """Ensure we have all expected schemas."""
        schema_files = list(SCHEMAS_DIR.glob("*.json"))
        # We expect at least 20 schema files
        assert len(schema_files) >= 20, f"Expected ≥20 schemas, got {len(schema_files)}"


@pytest.mark.unit
class TestGeneratedModels:
    """Verify generated Pydantic models can be imported and used."""

    def test_import_all_models(self) -> None:
        from cowork_platform import (  # noqa: F401
            ApprovalDecision,
            ApprovalRequest,
            Artifact,
            ArtifactUploadRequest,
            Capability,
            ConversationMessage,
            ErrorResponse,
            EventEnvelope,
            PolicyBundle,
            Session,
            SessionCancelRequest,
            SessionCreateRequest,
            SessionCreateResponse,
            SessionResumeRequest,
            ToolDefinition,
            ToolRequest,
            ToolResult,
            TraceSpan,
            Workspace,
            WorkspaceCreateRequest,
            WorkspaceCreateResponse,
        )

    def test_tool_request_roundtrip(self) -> None:
        from cowork_platform import ToolRequest

        data = {
            "toolName": "ReadFile",
            "arguments": {"path": "/tmp/test.py"},
            "sessionId": "sess_001",
            "taskId": "task_001",
            "stepId": "step_001",
        }
        model = ToolRequest.model_validate(data)
        assert model.toolName == "ReadFile"
        assert model.sessionId == "sess_001"

        serialized = json.loads(model.model_dump_json(exclude_none=True))
        assert serialized["toolName"] == "ReadFile"
        assert serialized["arguments"] == {"path": "/tmp/test.py"}

    def test_tool_result_roundtrip(self) -> None:
        from cowork_platform import ToolResult

        data = {
            "toolName": "ReadFile",
            "sessionId": "sess_001",
            "taskId": "task_001",
            "stepId": "step_001",
            "status": "succeeded",
            "outputText": "file contents here",
        }
        model = ToolResult.model_validate(data)
        assert model.status == "succeeded"
        assert model.outputText == "file contents here"

    def test_policy_bundle_roundtrip(self) -> None:
        from cowork_platform import PolicyBundle

        data = {
            "policyBundleVersion": "2026-02-28.1",
            "schemaVersion": "1.0",
            "tenantId": "tenant_abc",
            "userId": "user_123",
            "sessionId": "sess_789",
            "expiresAt": "2026-02-28T18:30:00Z",
            "capabilities": [
                {
                    "name": "File.Read",
                    "allowedPaths": ["/Users/test/project"],
                    "requiresApproval": False,
                }
            ],
            "llmPolicy": {
                "allowedModels": ["claude-sonnet-4-6"],
                "maxInputTokens": 64000,
                "maxOutputTokens": 4000,
                "maxSessionTokens": 250000,
            },
            "approvalRules": [],
        }
        model = PolicyBundle.model_validate(data)
        assert model.tenantId == "tenant_abc"
        assert model.llmPolicy.maxSessionTokens == 250000
        assert len(model.capabilities) == 1
        assert model.capabilities[0].name == "File.Read"

    def test_error_response_roundtrip(self) -> None:
        from cowork_platform import ErrorResponse

        data = {
            "code": "CAPABILITY_DENIED",
            "message": "Shell.Exec is not allowed",
            "retryable": False,
        }
        model = ErrorResponse.model_validate(data)
        assert model.code == "CAPABILITY_DENIED"
        assert model.retryable is False

    def test_event_envelope_roundtrip(self) -> None:
        from cowork_platform import EventEnvelope

        data = {
            "eventId": "550e8400-e29b-41d4-a716-446655440000",
            "eventType": "tool_completed",
            "timestamp": "2026-02-28T15:09:00Z",
            "tenantId": "tenant_abc",
            "userId": "user_123",
            "sessionId": "sess_789",
            "component": "LocalAgentHost",
            "payload": {"toolName": "ReadFile", "durationMs": 42},
        }
        model = EventEnvelope.model_validate(data)
        assert model.eventType == "tool_completed"
        assert model.component == "LocalAgentHost"

    def test_conversation_message_roundtrip(self) -> None:
        from cowork_platform import ConversationMessage

        data = {
            "messageId": "msg_001",
            "sessionId": "sess_789",
            "role": "user",
            "content": "Refactor the API client",
            "timestamp": "2026-02-28T14:01:00Z",
        }
        model = ConversationMessage.model_validate(data)
        assert model.role == "user"
        assert model.content == "Refactor the API client"
