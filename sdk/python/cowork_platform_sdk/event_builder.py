"""Builder for constructing standard event envelopes.

All audit and telemetry events share the EventEnvelope schema.
This module provides a fluent builder to construct valid envelopes.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any


def build_event(
    *,
    event_type: str,
    component: str,
    tenant_id: str,
    user_id: str,
    session_id: str,
    workspace_id: str | None = None,
    task_id: str | None = None,
    bounded_context: str | None = None,
    severity: str = "info",
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a standard event envelope.

    Args:
        event_type: One of the standard event type names.
        component: The component emitting this event.
        tenant_id: Tenant context.
        user_id: User context.
        session_id: Session context.
        workspace_id: Workspace context (optional).
        task_id: Task context (optional).
        bounded_context: Bounded context of the emitting component.
        severity: Event severity (debug, info, warning, error, critical).
        payload: Event-specific payload data.

    Returns:
        A dict matching the EventEnvelope schema.
    """
    envelope: dict[str, Any] = {
        "eventId": str(uuid.uuid4()),
        "eventType": event_type,
        "timestamp": datetime.now(UTC).isoformat(),
        "tenantId": tenant_id,
        "userId": user_id,
        "sessionId": session_id,
        "component": component,
        "payload": payload or {},
    }

    if workspace_id is not None:
        envelope["workspaceId"] = workspace_id
    if task_id is not None:
        envelope["taskId"] = task_id
    if bounded_context is not None:
        envelope["boundedContext"] = bounded_context
    if severity != "info":
        envelope["severity"] = severity

    return envelope
