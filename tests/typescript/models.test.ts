import { describe, it, expect } from "vitest";
import type {
  ToolRequest,
  ToolResult,
  PolicyBundle,
  ErrorResponse,
  EventEnvelope,
  ConversationMessage,
} from "../../generated/typescript/src/models.js";

/**
 * Tests that generated TypeScript interfaces accept valid data shapes.
 * Since interfaces are erased at runtime, these tests validate that
 * objects conforming to the interfaces pass type checking and have
 * the expected structure.
 */
describe("generated models", () => {
  it("ToolRequest matches expected shape", () => {
    const req: ToolRequest = {
      toolName: "ReadFile",
      arguments: { path: "/tmp/test.py" },
      sessionId: "sess_001",
      taskId: "task_001",
      stepId: "step_001",
    };
    expect(req.toolName).toBe("ReadFile");
    expect(req.sessionId).toBe("sess_001");
    expect(req.arguments).toEqual({ path: "/tmp/test.py" });
  });

  it("ToolResult matches expected shape", () => {
    const res: ToolResult = {
      toolName: "ReadFile",
      sessionId: "sess_001",
      taskId: "task_001",
      stepId: "step_001",
      status: "succeeded",
      outputText: "file contents here",
    };
    expect(res.status).toBe("succeeded");
    expect(res.outputText).toBe("file contents here");
  });

  it("PolicyBundle matches expected shape", () => {
    const bundle: PolicyBundle = {
      policyBundleVersion: "2026-02-28.1",
      schemaVersion: "1.0",
      tenantId: "tenant_abc",
      userId: "user_123",
      sessionId: "sess_789",
      expiresAt: "2026-02-28T18:30:00Z",
      capabilities: [
        {
          name: "File.Read",
          allowedPaths: ["/Users/test/project"],
          requiresApproval: false,
        },
      ],
      llmPolicy: {
        allowedModels: ["claude-sonnet-4-6"],
        maxInputTokens: 64000,
        maxOutputTokens: 4000,
        maxSessionTokens: 250000,
      },
      approvalRules: [],
    };
    expect(bundle.tenantId).toBe("tenant_abc");
    expect(bundle.llmPolicy.maxSessionTokens).toBe(250000);
    expect(bundle.capabilities).toHaveLength(1);
    expect(bundle.capabilities[0].name).toBe("File.Read");
  });

  it("ErrorResponse matches expected shape", () => {
    const err: ErrorResponse = {
      code: "CAPABILITY_DENIED",
      message: "Shell.Exec is not allowed",
      retryable: false,
    };
    expect(err.code).toBe("CAPABILITY_DENIED");
    expect(err.retryable).toBe(false);
  });

  it("EventEnvelope matches expected shape", () => {
    const envelope: EventEnvelope = {
      eventId: "550e8400-e29b-41d4-a716-446655440000",
      eventType: "tool_completed",
      timestamp: "2026-02-28T15:09:00Z",
      tenantId: "tenant_abc",
      userId: "user_123",
      sessionId: "sess_789",
      component: "LocalAgentHost",
      payload: { toolName: "ReadFile", durationMs: 42 },
    };
    expect(envelope.eventType).toBe("tool_completed");
    expect(envelope.component).toBe("LocalAgentHost");
  });

  it("ConversationMessage matches expected shape", () => {
    const msg: ConversationMessage = {
      messageId: "msg_001",
      sessionId: "sess_789",
      role: "user",
      content: "Refactor the API client",
      timestamp: "2026-02-28T14:01:00Z",
    };
    expect(msg.role).toBe("user");
    expect(msg.content).toBe("Refactor the API client");
  });
});
