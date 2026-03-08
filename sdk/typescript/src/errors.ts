/**
 * Error hierarchy for the cowork platform TypeScript SDK.
 *
 * All error responses across the system use the standard ErrorResponse shape:
 *   { "code": "...", "message": "...", "retryable": false, "details": {} }
 *
 * This module provides typed error classes that map to/from that shape.
 */

import { ErrorCode, RETRYABLE_ERROR_CODES } from "./constants.js";

export interface ErrorResponseData {
  code: string;
  message: string;
  retryable: boolean;
  details?: Record<string, unknown>;
}

export class CoworkAPIError extends Error {
  readonly code: string;
  retryable: boolean;
  readonly details: Record<string, unknown>;

  constructor(
    code: string,
    message: string,
    options?: { retryable?: boolean; details?: Record<string, unknown> },
  ) {
    super(message);
    this.name = "CoworkAPIError";
    this.code = code;
    this.retryable = options?.retryable ?? RETRYABLE_ERROR_CODES.has(code);
    this.details = options?.details ?? {};
  }

  toJSON(): ErrorResponseData {
    const result: ErrorResponseData = {
      code: this.code,
      message: this.message,
      retryable: this.retryable,
    };
    if (Object.keys(this.details).length > 0) {
      result.details = this.details;
    }
    return result;
  }

  static fromJSON(data: ErrorResponseData): CoworkAPIError {
    const code = data.code ?? ErrorCode.INTERNAL_ERROR;
    const message = data.message ?? "Unknown error";
    const retryable = data.retryable ?? false;
    const details = data.details;

    const SubErrorClass = CODE_TO_CLASS.get(code);
    if (SubErrorClass) {
      const err = new SubErrorClass(message, { details });
      err.retryable = retryable;
      return err;
    }
    return new CoworkAPIError(code, message, { retryable, details });
  }
}

// --- Specific Error Classes ---

interface CoworkSubErrorConstructor {
  new (
    message?: string,
    options?: { details?: Record<string, unknown> },
  ): CoworkAPIError;
}

function defineError(
  name: string,
  code: string,
  defaultMessage: string,
  defaultRetryable: boolean,
): CoworkSubErrorConstructor {
  const cls = class extends CoworkAPIError {
    constructor(
      message: string = defaultMessage,
      options?: { details?: Record<string, unknown> },
    ) {
      super(code, message, {
        retryable: defaultRetryable,
        details: options?.details,
      });
      this.name = name;
    }
  };
  Object.defineProperty(cls, "name", { value: name });
  return cls;
}

export const InvalidRequestError = defineError(
  "InvalidRequestError",
  ErrorCode.INVALID_REQUEST,
  "Invalid request",
  false,
);
export const UnauthorizedError = defineError(
  "UnauthorizedError",
  ErrorCode.UNAUTHORIZED,
  "Unauthorized",
  false,
);
export const SessionNotFoundError = defineError(
  "SessionNotFoundError",
  ErrorCode.SESSION_NOT_FOUND,
  "Session not found",
  false,
);
export const SessionExpiredError = defineError(
  "SessionExpiredError",
  ErrorCode.SESSION_EXPIRED,
  "Session expired",
  false,
);
export const PolicyBundleInvalidError = defineError(
  "PolicyBundleInvalidError",
  ErrorCode.POLICY_BUNDLE_INVALID,
  "Policy bundle invalid",
  false,
);
export const PolicyExpiredError = defineError(
  "PolicyExpiredError",
  ErrorCode.POLICY_EXPIRED,
  "Policy expired",
  false,
);
export const CapabilityDeniedError = defineError(
  "CapabilityDeniedError",
  ErrorCode.CAPABILITY_DENIED,
  "Capability denied",
  false,
);
export const ApprovalRequiredError = defineError(
  "ApprovalRequiredError",
  ErrorCode.APPROVAL_REQUIRED,
  "Approval required",
  false,
);
export const ApprovalDeniedError = defineError(
  "ApprovalDeniedError",
  ErrorCode.APPROVAL_DENIED,
  "Approval denied",
  false,
);
export const ToolNotFoundError = defineError(
  "ToolNotFoundError",
  ErrorCode.TOOL_NOT_FOUND,
  "Tool not found",
  false,
);
export const ToolExecutionError = defineError(
  "ToolExecutionError",
  ErrorCode.TOOL_EXECUTION_FAILED,
  "Tool execution failed",
  false,
);
export const ToolExecutionTimeoutError = defineError(
  "ToolExecutionTimeoutError",
  ErrorCode.TOOL_EXECUTION_TIMEOUT,
  "Tool execution timed out",
  false,
);
export const FileNotFoundError = defineError(
  "FileNotFoundError",
  ErrorCode.FILE_NOT_FOUND,
  "File not found",
  false,
);
export const FileTooLargeError = defineError(
  "FileTooLargeError",
  ErrorCode.FILE_TOO_LARGE,
  "File too large",
  false,
);
export const PermissionDeniedError = defineError(
  "PermissionDeniedError",
  ErrorCode.PERMISSION_DENIED,
  "Permission denied",
  false,
);
export const LlmGuardrailBlockedError = defineError(
  "LlmGuardrailBlockedError",
  ErrorCode.LLM_GUARDRAIL_BLOCKED,
  "LLM guardrail blocked",
  false,
);
export const LlmBudgetExceededError = defineError(
  "LlmBudgetExceededError",
  ErrorCode.LLM_BUDGET_EXCEEDED,
  "LLM budget exceeded",
  false,
);
export const WorkspaceUploadError = defineError(
  "WorkspaceUploadError",
  ErrorCode.WORKSPACE_UPLOAD_FAILED,
  "Workspace upload failed",
  true,
);
export const RateLimitedError = defineError(
  "RateLimitedError",
  ErrorCode.RATE_LIMITED,
  "Rate limited",
  true,
);
export const InternalError = defineError(
  "InternalError",
  ErrorCode.INTERNAL_ERROR,
  "Internal error",
  true,
);
export const CodeExecutionTimeoutError = defineError(
  "CodeExecutionTimeoutError",
  ErrorCode.CODE_EXECUTION_TIMEOUT,
  "Code execution timed out",
  false,
);
export const TeamModeDisabledError = defineError(
  "TeamModeDisabledError",
  ErrorCode.TEAM_MODE_DISABLED,
  "Team mode disabled",
  false,
);
export const TeamWorkspaceInvalidError = defineError(
  "TeamWorkspaceInvalidError",
  ErrorCode.TEAM_WORKSPACE_INVALID,
  "Team workspace invalid",
  false,
);
export const TeammateBudgetExceededError = defineError(
  "TeammateBudgetExceededError",
  ErrorCode.TEAMMATE_BUDGET_EXCEEDED,
  "Teammate budget exceeded",
  false,
);
export const TeammateLimitExceededError = defineError(
  "TeammateLimitExceededError",
  ErrorCode.TEAMMATE_LIMIT_EXCEEDED,
  "Teammate limit exceeded",
  false,
);
export const TaskDependencyCycleError = defineError(
  "TaskDependencyCycleError",
  ErrorCode.TASK_DEPENDENCY_CYCLE,
  "Task dependency cycle",
  false,
);

// --- Code-to-class mapping ---

const CODE_TO_CLASS = new Map<string, CoworkSubErrorConstructor>([
  [ErrorCode.INVALID_REQUEST, InvalidRequestError],
  [ErrorCode.UNAUTHORIZED, UnauthorizedError],
  [ErrorCode.SESSION_NOT_FOUND, SessionNotFoundError],
  [ErrorCode.SESSION_EXPIRED, SessionExpiredError],
  [ErrorCode.POLICY_BUNDLE_INVALID, PolicyBundleInvalidError],
  [ErrorCode.POLICY_EXPIRED, PolicyExpiredError],
  [ErrorCode.CAPABILITY_DENIED, CapabilityDeniedError],
  [ErrorCode.APPROVAL_REQUIRED, ApprovalRequiredError],
  [ErrorCode.APPROVAL_DENIED, ApprovalDeniedError],
  [ErrorCode.TOOL_NOT_FOUND, ToolNotFoundError],
  [ErrorCode.TOOL_EXECUTION_FAILED, ToolExecutionError],
  [ErrorCode.TOOL_EXECUTION_TIMEOUT, ToolExecutionTimeoutError],
  [ErrorCode.FILE_NOT_FOUND, FileNotFoundError],
  [ErrorCode.FILE_TOO_LARGE, FileTooLargeError],
  [ErrorCode.PERMISSION_DENIED, PermissionDeniedError],
  [ErrorCode.LLM_GUARDRAIL_BLOCKED, LlmGuardrailBlockedError],
  [ErrorCode.LLM_BUDGET_EXCEEDED, LlmBudgetExceededError],
  [ErrorCode.WORKSPACE_UPLOAD_FAILED, WorkspaceUploadError],
  [ErrorCode.RATE_LIMITED, RateLimitedError],
  [ErrorCode.INTERNAL_ERROR, InternalError],
  [ErrorCode.CODE_EXECUTION_TIMEOUT, CodeExecutionTimeoutError],
  [ErrorCode.TEAM_MODE_DISABLED, TeamModeDisabledError],
  [ErrorCode.TEAM_WORKSPACE_INVALID, TeamWorkspaceInvalidError],
  [ErrorCode.TEAMMATE_BUDGET_EXCEEDED, TeammateBudgetExceededError],
  [ErrorCode.TEAMMATE_LIMIT_EXCEEDED, TeammateLimitExceededError],
  [ErrorCode.TASK_DEPENDENCY_CYCLE, TaskDependencyCycleError],
]);
