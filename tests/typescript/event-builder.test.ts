import { describe, it, expect } from "vitest";
import { buildEvent } from "../../sdk/typescript/src/event-builder.js";
import { EventType, Component } from "../../sdk/typescript/src/constants.js";

describe("buildEvent", () => {
  const baseParams = {
    eventType: EventType.TOOL_COMPLETED,
    tenantId: "tenant_abc",
    userId: "user_123",
    sessionId: "sess_789",
    component: Component.LOCAL_AGENT_HOST,
    payload: { toolName: "ReadFile", durationMs: 42 },
  };

  it("includes all required fields", () => {
    const event = buildEvent(baseParams);
    expect(event.eventId).toBeDefined();
    expect(event.timestamp).toBeDefined();
    expect(event.eventType).toBe("tool_completed");
    expect(event.tenantId).toBe("tenant_abc");
    expect(event.userId).toBe("user_123");
    expect(event.sessionId).toBe("sess_789");
    expect(event.component).toBe("LocalAgentHost");
    expect(event.payload).toEqual({ toolName: "ReadFile", durationMs: 42 });
  });

  it("generates valid UUID for eventId", () => {
    const event = buildEvent(baseParams);
    const uuidRegex =
      /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
    expect(event.eventId).toMatch(uuidRegex);
  });

  it("generates ISO timestamp", () => {
    const event = buildEvent(baseParams);
    const parsed = new Date(event.timestamp);
    expect(parsed.toISOString()).toBe(event.timestamp);
  });

  it("includes optional fields when provided", () => {
    const event = buildEvent({
      ...baseParams,
      taskId: "task_001",
      stepId: "step_001",
      workspaceId: "ws_001",
    });
    expect(event.taskId).toBe("task_001");
    expect(event.stepId).toBe("step_001");
    expect(event.workspaceId).toBe("ws_001");
  });

  it("omits optional fields when not provided", () => {
    const event = buildEvent(baseParams);
    expect("taskId" in event).toBe(false);
    expect("stepId" in event).toBe(false);
    expect("workspaceId" in event).toBe(false);
  });

  it("generates unique event IDs", () => {
    const ids = new Set(
      Array.from({ length: 100 }, () => buildEvent(baseParams).eventId),
    );
    expect(ids.size).toBe(100);
  });
});
