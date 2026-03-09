"""Shared constants for the cowork platform."""

from typing import Final

# --- Error Codes ---
# Machine-readable codes used in ErrorResponse across all services.


class ErrorCode:
    INVALID_REQUEST: Final = "INVALID_REQUEST"
    UNAUTHORIZED: Final = "UNAUTHORIZED"
    SESSION_NOT_FOUND: Final = "SESSION_NOT_FOUND"
    SESSION_EXPIRED: Final = "SESSION_EXPIRED"
    POLICY_BUNDLE_INVALID: Final = "POLICY_BUNDLE_INVALID"
    POLICY_EXPIRED: Final = "POLICY_EXPIRED"
    CAPABILITY_DENIED: Final = "CAPABILITY_DENIED"
    APPROVAL_REQUIRED: Final = "APPROVAL_REQUIRED"
    APPROVAL_DENIED: Final = "APPROVAL_DENIED"
    TOOL_NOT_FOUND: Final = "TOOL_NOT_FOUND"
    TOOL_EXECUTION_FAILED: Final = "TOOL_EXECUTION_FAILED"
    TOOL_EXECUTION_TIMEOUT: Final = "TOOL_EXECUTION_TIMEOUT"
    FILE_NOT_FOUND: Final = "FILE_NOT_FOUND"
    FILE_TOO_LARGE: Final = "FILE_TOO_LARGE"
    PERMISSION_DENIED: Final = "PERMISSION_DENIED"
    LLM_GUARDRAIL_BLOCKED: Final = "LLM_GUARDRAIL_BLOCKED"
    LLM_BUDGET_EXCEEDED: Final = "LLM_BUDGET_EXCEEDED"
    WORKSPACE_UPLOAD_FAILED: Final = "WORKSPACE_UPLOAD_FAILED"
    RATE_LIMITED: Final = "RATE_LIMITED"
    INTERNAL_ERROR: Final = "INTERNAL_ERROR"
    CODE_EXECUTION_TIMEOUT: Final = "CODE_EXECUTION_TIMEOUT"
    TEAM_MODE_DISABLED: Final = "TEAM_MODE_DISABLED"
    TEAM_WORKSPACE_INVALID: Final = "TEAM_WORKSPACE_INVALID"
    TEAMMATE_BUDGET_EXCEEDED: Final = "TEAMMATE_BUDGET_EXCEEDED"
    TEAMMATE_LIMIT_EXCEEDED: Final = "TEAMMATE_LIMIT_EXCEEDED"
    TASK_DEPENDENCY_CYCLE: Final = "TASK_DEPENDENCY_CYCLE"


# --- Retryable Error Codes ---
# Errors where the client should retry with backoff.

RETRYABLE_ERROR_CODES: Final[frozenset[str]] = frozenset(
    {
        ErrorCode.RATE_LIMITED,
        ErrorCode.INTERNAL_ERROR,
        ErrorCode.WORKSPACE_UPLOAD_FAILED,
    }
)


# --- Capability Names ---


class CapabilityName:
    FILE_READ: Final = "File.Read"
    FILE_WRITE: Final = "File.Write"
    FILE_DELETE: Final = "File.Delete"
    SHELL_EXEC: Final = "Shell.Exec"
    NETWORK_HTTP: Final = "Network.Http"
    WORKSPACE_UPLOAD: Final = "Workspace.Upload"
    BACKEND_TOOL_INVOKE: Final = "BackendTool.Invoke"
    LLM_CALL: Final = "LLM.Call"
    SEARCH_WEB: Final = "Search.Web"
    CODE_EXECUTE: Final = "Code.Execute"


# --- Event Types ---


class EventType:
    SESSION_CREATED: Final = "session_created"
    SESSION_STARTED: Final = "session_started"
    STEP_STARTED: Final = "step_started"
    STEP_COMPLETED: Final = "step_completed"
    STEP_LIMIT_APPROACHING: Final = "step_limit_approaching"
    TEXT_CHUNK: Final = "text_chunk"
    LLM_REQUEST_STARTED: Final = "llm_request_started"
    LLM_REQUEST_COMPLETED: Final = "llm_request_completed"
    TOOL_REQUESTED: Final = "tool_requested"
    TOOL_COMPLETED: Final = "tool_completed"
    APPROVAL_REQUESTED: Final = "approval_requested"
    APPROVAL_RESOLVED: Final = "approval_resolved"
    POLICY_EXPIRED: Final = "policy_expired"
    TASK_STARTED: Final = "task_started"
    TASK_COMPLETED: Final = "task_completed"
    TASK_FAILED: Final = "task_failed"
    TASK_CANCELLED: Final = "task_cancelled"
    LLM_RETRY: Final = "llm_retry"
    CONTEXT_COMPACTED: Final = "context_compacted"
    SESSION_COMPLETED: Final = "session_completed"
    SESSION_FAILED: Final = "session_failed"
    CHECKPOINT_SAVED: Final = "checkpoint_saved"
    CHECKPOINT_RESTORED: Final = "checkpoint_restored"
    CHECKPOINT_FAILED: Final = "checkpoint_failed"
    WORKSPACE_SYNC_COMPLETED: Final = "workspace_sync_completed"
    WORKSPACE_SYNC_FAILED: Final = "workspace_sync_failed"
    PLAN_MODE_CHANGED: Final = "plan_mode_changed"
    VERIFICATION_STARTED: Final = "verification_started"
    VERIFICATION_COMPLETED: Final = "verification_completed"
    PLAN_UPDATED: Final = "plan_updated"


# --- Component Names ---


class Component:
    DESKTOP_APP: Final = "DesktopApp"
    LOCAL_AGENT_HOST: Final = "LocalAgentHost"
    LOCAL_TOOL_RUNTIME: Final = "LocalToolRuntime"
    LOCAL_POLICY_ENFORCER: Final = "LocalPolicyEnforcer"
    LOCAL_APPROVAL_UI: Final = "LocalApprovalUI"
    SESSION_SERVICE: Final = "SessionService"
    LLM_GATEWAY: Final = "LLMGateway"
    POLICY_SERVICE: Final = "PolicyService"
    APPROVAL_SERVICE: Final = "ApprovalService"
    WORKSPACE_SERVICE: Final = "WorkspaceService"
    AUDIT_SERVICE: Final = "AuditService"
    TELEMETRY_SERVICE: Final = "TelemetryService"
    BACKEND_TOOL_SERVICE: Final = "BackendToolService"


# --- Session Status ---


class SessionStatus:
    CREATED: Final = "SESSION_CREATED"
    RUNNING: Final = "SESSION_RUNNING"
    WAITING_FOR_LLM: Final = "WAITING_FOR_LLM"
    WAITING_FOR_TOOL: Final = "WAITING_FOR_TOOL"
    WAITING_FOR_APPROVAL: Final = "WAITING_FOR_APPROVAL"
    PAUSED: Final = "SESSION_PAUSED"
    COMPLETED: Final = "SESSION_COMPLETED"
    FAILED: Final = "SESSION_FAILED"
    CANCELLED: Final = "SESSION_CANCELLED"


# --- Task Status ---


class TaskStatus:
    RUNNING: Final = "running"
    COMPLETED: Final = "completed"
    FAILED: Final = "failed"
    CANCELLED: Final = "cancelled"


# --- Risk Levels ---


class RiskLevel:
    LOW: Final = "low"
    MEDIUM: Final = "medium"
    HIGH: Final = "high"


# --- Tool Timeouts (seconds) ---


class ToolTimeout:
    FILE: Final = 30
    SHELL: Final = 300
    NETWORK: Final = 60
    REMOTE: Final = 120
    CODE: Final = 120
