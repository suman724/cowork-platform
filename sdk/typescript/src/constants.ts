/**
 * Shared constants for the cowork platform TypeScript SDK.
 */

// --- Error Codes ---

export const ErrorCode = {
  INVALID_REQUEST: "INVALID_REQUEST",
  UNAUTHORIZED: "UNAUTHORIZED",
  SESSION_NOT_FOUND: "SESSION_NOT_FOUND",
  SESSION_EXPIRED: "SESSION_EXPIRED",
  POLICY_BUNDLE_INVALID: "POLICY_BUNDLE_INVALID",
  POLICY_EXPIRED: "POLICY_EXPIRED",
  CAPABILITY_DENIED: "CAPABILITY_DENIED",
  APPROVAL_REQUIRED: "APPROVAL_REQUIRED",
  APPROVAL_DENIED: "APPROVAL_DENIED",
  TOOL_NOT_FOUND: "TOOL_NOT_FOUND",
  TOOL_EXECUTION_FAILED: "TOOL_EXECUTION_FAILED",
  TOOL_EXECUTION_TIMEOUT: "TOOL_EXECUTION_TIMEOUT",
  FILE_NOT_FOUND: "FILE_NOT_FOUND",
  FILE_TOO_LARGE: "FILE_TOO_LARGE",
  PERMISSION_DENIED: "PERMISSION_DENIED",
  LLM_GUARDRAIL_BLOCKED: "LLM_GUARDRAIL_BLOCKED",
  LLM_BUDGET_EXCEEDED: "LLM_BUDGET_EXCEEDED",
  WORKSPACE_UPLOAD_FAILED: "WORKSPACE_UPLOAD_FAILED",
  RATE_LIMITED: "RATE_LIMITED",
  INTERNAL_ERROR: "INTERNAL_ERROR",
} as const;

export type ErrorCodeValue = (typeof ErrorCode)[keyof typeof ErrorCode];

export const RETRYABLE_ERROR_CODES: ReadonlySet<string> = new Set([
  ErrorCode.RATE_LIMITED,
  ErrorCode.INTERNAL_ERROR,
  ErrorCode.WORKSPACE_UPLOAD_FAILED,
]);

// --- Capability Names ---

export const CapabilityName = {
  FILE_READ: "File.Read",
  FILE_WRITE: "File.Write",
  FILE_DELETE: "File.Delete",
  SHELL_EXEC: "Shell.Exec",
  NETWORK_HTTP: "Network.Http",
  WORKSPACE_UPLOAD: "Workspace.Upload",
  BACKEND_TOOL_INVOKE: "BackendTool.Invoke",
  LLM_CALL: "LLM.Call",
} as const;

// --- Event Types ---

export const EventType = {
  SESSION_CREATED: "session_created",
  SESSION_STARTED: "session_started",
  STEP_STARTED: "step_started",
  STEP_COMPLETED: "step_completed",
  STEP_LIMIT_APPROACHING: "step_limit_approaching",
  TEXT_CHUNK: "text_chunk",
  LLM_REQUEST_STARTED: "llm_request_started",
  LLM_REQUEST_COMPLETED: "llm_request_completed",
  TOOL_REQUESTED: "tool_requested",
  TOOL_COMPLETED: "tool_completed",
  APPROVAL_REQUESTED: "approval_requested",
  APPROVAL_RESOLVED: "approval_resolved",
  POLICY_EXPIRED: "policy_expired",
  TASK_COMPLETED: "task_completed",
  TASK_FAILED: "task_failed",
  LLM_RETRY: "llm_retry",
  SESSION_COMPLETED: "session_completed",
  SESSION_FAILED: "session_failed",
} as const;

export type EventTypeValue = (typeof EventType)[keyof typeof EventType];

// --- Components ---

export const Component = {
  DESKTOP_APP: "DesktopApp",
  LOCAL_AGENT_HOST: "LocalAgentHost",
  LOCAL_TOOL_RUNTIME: "LocalToolRuntime",
  LOCAL_POLICY_ENFORCER: "LocalPolicyEnforcer",
  LOCAL_APPROVAL_UI: "LocalApprovalUI",
  SESSION_SERVICE: "SessionService",
  LLM_GATEWAY: "LLMGateway",
  POLICY_SERVICE: "PolicyService",
  APPROVAL_SERVICE: "ApprovalService",
  WORKSPACE_SERVICE: "WorkspaceService",
  AUDIT_SERVICE: "AuditService",
  TELEMETRY_SERVICE: "TelemetryService",
  BACKEND_TOOL_SERVICE: "BackendToolService",
} as const;

// --- Session Status ---

export const SessionStatus = {
  CREATING: "creating",
  ACTIVE: "active",
  PAUSED: "paused",
  COMPLETED: "completed",
  FAILED: "failed",
  CANCELLED: "cancelled",
  EXPIRED: "expired",
} as const;

export type SessionStatusValue =
  (typeof SessionStatus)[keyof typeof SessionStatus];
