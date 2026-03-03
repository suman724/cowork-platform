"""Error hierarchy for the cowork platform.

All error responses across the system use the standard ErrorResponse shape:
    {"code": "...", "message": "...", "retryable": false, "details": {}}

This module provides typed exceptions that map to/from that shape.
"""

from __future__ import annotations

from typing import Any

from cowork_platform_sdk.constants import RETRYABLE_ERROR_CODES, ErrorCode


class CoworkAPIError(Exception):
    """Base exception for all cowork API errors.

    Maps directly to the ErrorResponse JSON schema.
    """

    def __init__(
        self,
        code: str,
        message: str,
        *,
        retryable: bool | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable if retryable is not None else (code in RETRYABLE_ERROR_CODES)
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Serialize to the standard error response shape."""
        result: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
            "retryable": self.retryable,
        }
        if self.details:
            result["details"] = self.details
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CoworkAPIError:
        """Deserialize from the standard error response shape."""
        code = data.get("code", ErrorCode.INTERNAL_ERROR)
        message = data.get("message", "Unknown error")
        retryable = data.get("retryable", False)
        details = data.get("details")

        # Map to specific subclass if available
        error_cls = _CODE_TO_CLASS.get(code, cls)
        if error_cls is cls:
            # No specific subclass — use base constructor
            return cls(code=code, message=message, retryable=retryable, details=details)
        # Subclasses hardcode their own code/retryable, so only pass message and details
        err = error_cls(message=message, details=details)  # type: ignore[call-arg]
        # Override retryable if the serialized value differs from the subclass default
        err.retryable = retryable
        return err

    def __repr__(self) -> str:
        return f"{type(self).__name__}(code={self.code!r}, message={self.message!r})"


# --- Specific Error Classes ---
# Each subclass hardcodes its error code and default retryable flag.
# The `details` parameter allows attaching structured context.


def _make_init(code: str, default_message: str, default_retryable: bool) -> Any:
    """Helper to avoid boilerplate in error subclass __init__ methods."""

    def _init(
        self: CoworkAPIError,
        message: str = default_message,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        CoworkAPIError.__init__(self, code, message, retryable=default_retryable, details=details)

    return _init


class InvalidRequestError(CoworkAPIError):
    """400 — The request was malformed or missing required fields."""

    __init__ = _make_init(ErrorCode.INVALID_REQUEST, "Invalid request", False)


class UnauthorizedError(CoworkAPIError):
    """401 — Authentication failed or credentials missing."""

    __init__ = _make_init(ErrorCode.UNAUTHORIZED, "Unauthorized", False)


class NotFoundError(CoworkAPIError):
    """404 — The requested resource was not found."""

    __init__ = _make_init(ErrorCode.SESSION_NOT_FOUND, "Not found", False)


class SessionNotFoundError(CoworkAPIError):
    """404 — Session not found."""

    __init__ = _make_init(ErrorCode.SESSION_NOT_FOUND, "Session not found", False)


class ToolNotFoundError(CoworkAPIError):
    """404 — Tool not found."""

    __init__ = _make_init(ErrorCode.TOOL_NOT_FOUND, "Tool not found", False)


class CoworkFileNotFoundError(CoworkAPIError):
    """404 — File not found."""

    __init__ = _make_init(ErrorCode.FILE_NOT_FOUND, "File not found", False)


class SessionExpiredError(CoworkAPIError):
    """410 — The session has expired."""

    __init__ = _make_init(ErrorCode.SESSION_EXPIRED, "Session expired", False)


class PolicyExpiredError(CoworkAPIError):
    """410 — The policy bundle has expired."""

    __init__ = _make_init(ErrorCode.POLICY_EXPIRED, "Policy expired", False)


class PolicyBundleInvalidError(CoworkAPIError):
    """400 — The policy bundle failed client-side validation."""

    __init__ = _make_init(ErrorCode.POLICY_BUNDLE_INVALID, "Policy bundle invalid", False)


class CapabilityDeniedError(CoworkAPIError):
    """403 — The requested capability is not granted by the policy."""

    __init__ = _make_init(ErrorCode.CAPABILITY_DENIED, "Capability denied", False)


class ApprovalRequiredError(CoworkAPIError):
    """403 — The action requires user approval."""

    __init__ = _make_init(ErrorCode.APPROVAL_REQUIRED, "Approval required", False)


class ApprovalDeniedError(CoworkAPIError):
    """403 — The user denied the approval request."""

    __init__ = _make_init(ErrorCode.APPROVAL_DENIED, "Approval denied", False)


class PermissionDeniedError(CoworkAPIError):
    """403 — Permission denied (path, command, or domain not allowed)."""

    __init__ = _make_init(ErrorCode.PERMISSION_DENIED, "Permission denied", False)


class ToolExecutionError(CoworkAPIError):
    """500 — A tool execution failed."""

    __init__ = _make_init(ErrorCode.TOOL_EXECUTION_FAILED, "Tool execution failed", False)


class ToolExecutionTimeoutError(CoworkAPIError):
    """504 — A tool execution timed out."""

    __init__ = _make_init(ErrorCode.TOOL_EXECUTION_TIMEOUT, "Tool execution timed out", False)


class FileTooLargeError(CoworkAPIError):
    """413 — The file exceeds the maximum allowed size."""

    __init__ = _make_init(ErrorCode.FILE_TOO_LARGE, "File too large", False)


class LlmGuardrailBlockedError(CoworkAPIError):
    """400 — The LLM guardrail blocked the request."""

    __init__ = _make_init(ErrorCode.LLM_GUARDRAIL_BLOCKED, "LLM guardrail blocked", False)


class LlmBudgetExceededError(CoworkAPIError):
    """429 — The session's token budget has been exceeded."""

    __init__ = _make_init(ErrorCode.LLM_BUDGET_EXCEEDED, "LLM budget exceeded", False)


class WorkspaceUploadError(CoworkAPIError):
    """502 — An artifact upload to the Workspace Service failed."""

    __init__ = _make_init(ErrorCode.WORKSPACE_UPLOAD_FAILED, "Workspace upload failed", True)


class RateLimitedError(CoworkAPIError):
    """429 — Rate limited."""

    __init__ = _make_init(ErrorCode.RATE_LIMITED, "Rate limited", True)


class InternalError(CoworkAPIError):
    """500 — An unexpected internal error occurred."""

    __init__ = _make_init(ErrorCode.INTERNAL_ERROR, "Internal error", True)


class CodeExecutionTimeoutError(CoworkAPIError):
    """504 — Code execution exceeded the allowed time limit."""

    __init__ = _make_init(ErrorCode.CODE_EXECUTION_TIMEOUT, "Code execution timed out", False)


# --- Code-to-class mapping ---

_CODE_TO_CLASS: dict[str, type[CoworkAPIError]] = {
    ErrorCode.INVALID_REQUEST: InvalidRequestError,
    ErrorCode.UNAUTHORIZED: UnauthorizedError,
    ErrorCode.SESSION_NOT_FOUND: SessionNotFoundError,
    ErrorCode.SESSION_EXPIRED: SessionExpiredError,
    ErrorCode.POLICY_BUNDLE_INVALID: PolicyBundleInvalidError,
    ErrorCode.POLICY_EXPIRED: PolicyExpiredError,
    ErrorCode.CAPABILITY_DENIED: CapabilityDeniedError,
    ErrorCode.APPROVAL_REQUIRED: ApprovalRequiredError,
    ErrorCode.APPROVAL_DENIED: ApprovalDeniedError,
    ErrorCode.TOOL_NOT_FOUND: ToolNotFoundError,
    ErrorCode.TOOL_EXECUTION_FAILED: ToolExecutionError,
    ErrorCode.TOOL_EXECUTION_TIMEOUT: ToolExecutionTimeoutError,
    ErrorCode.FILE_NOT_FOUND: CoworkFileNotFoundError,
    ErrorCode.FILE_TOO_LARGE: FileTooLargeError,
    ErrorCode.PERMISSION_DENIED: PermissionDeniedError,
    ErrorCode.LLM_GUARDRAIL_BLOCKED: LlmGuardrailBlockedError,
    ErrorCode.LLM_BUDGET_EXCEEDED: LlmBudgetExceededError,
    ErrorCode.WORKSPACE_UPLOAD_FAILED: WorkspaceUploadError,
    ErrorCode.RATE_LIMITED: RateLimitedError,
    ErrorCode.INTERNAL_ERROR: InternalError,
    ErrorCode.CODE_EXECUTION_TIMEOUT: CodeExecutionTimeoutError,
}
