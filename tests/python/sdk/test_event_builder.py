"""Tests for the event envelope builder."""

import uuid

import pytest
from cowork_platform_sdk.constants import Component, EventType
from cowork_platform_sdk.event_builder import build_event


@pytest.mark.unit
class TestBuildEvent:
    def test_required_fields_present(self) -> None:
        event = build_event(
            event_type=EventType.SESSION_CREATED,
            component=Component.SESSION_SERVICE,
            tenant_id="tenant_abc",
            user_id="user_123",
            session_id="sess_789",
        )

        assert "eventId" in event
        assert event["eventType"] == "session_created"
        assert event["component"] == "SessionService"
        assert event["tenantId"] == "tenant_abc"
        assert event["userId"] == "user_123"
        assert event["sessionId"] == "sess_789"
        assert "timestamp" in event
        assert event["payload"] == {}

    def test_event_id_is_valid_uuid(self) -> None:
        event = build_event(
            event_type=EventType.TOOL_COMPLETED,
            component=Component.LOCAL_AGENT_HOST,
            tenant_id="t",
            user_id="u",
            session_id="s",
        )
        # Should not raise
        uuid.UUID(event["eventId"])

    def test_optional_fields(self) -> None:
        event = build_event(
            event_type=EventType.TOOL_COMPLETED,
            component=Component.LOCAL_AGENT_HOST,
            tenant_id="t",
            user_id="u",
            session_id="s",
            workspace_id="ws_456",
            task_id="task_001",
            bounded_context="AgentExecution",
            severity="warning",
            payload={"toolName": "ReadFile", "durationMs": 42},
        )

        assert event["workspaceId"] == "ws_456"
        assert event["taskId"] == "task_001"
        assert event["boundedContext"] == "AgentExecution"
        assert event["severity"] == "warning"
        assert event["payload"]["toolName"] == "ReadFile"

    def test_optional_fields_omitted_when_none(self) -> None:
        event = build_event(
            event_type=EventType.SESSION_CREATED,
            component=Component.SESSION_SERVICE,
            tenant_id="t",
            user_id="u",
            session_id="s",
        )

        assert "workspaceId" not in event
        assert "taskId" not in event
        assert "boundedContext" not in event
        # severity defaults to "info" and is omitted
        assert "severity" not in event

    def test_unique_event_ids(self) -> None:
        events = [
            build_event(
                event_type=EventType.STEP_STARTED,
                component=Component.LOCAL_AGENT_HOST,
                tenant_id="t",
                user_id="u",
                session_id="s",
            )
            for _ in range(10)
        ]
        event_ids = [e["eventId"] for e in events]
        assert len(set(event_ids)) == 10, "Event IDs should be unique"
