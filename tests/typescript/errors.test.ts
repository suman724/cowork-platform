import { describe, it, expect } from "vitest";
import {
  CoworkAPIError,
  CapabilityDeniedError,
  InternalError,
  InvalidRequestError,
  RateLimitedError,
  SessionNotFoundError,
  ToolExecutionError,
  WorkspaceUploadError,
} from "../../sdk/typescript/src/errors.js";
import { ErrorCode } from "../../sdk/typescript/src/constants.js";

describe("CoworkAPIError", () => {
  it("creates a base error with all fields", () => {
    const err = new CoworkAPIError("TEST_CODE", "test message", {
      retryable: false,
      details: { key: "val" },
    });
    expect(err.code).toBe("TEST_CODE");
    expect(err.message).toBe("test message");
    expect(err.retryable).toBe(false);
    expect(err.details).toEqual({ key: "val" });
    expect(err).toBeInstanceOf(Error);
  });

  it("serializes to JSON", () => {
    const err = new CoworkAPIError("CAPABILITY_DENIED", "Shell.Exec not allowed", {
      retryable: false,
      details: { capability: "Shell.Exec" },
    });
    expect(err.toJSON()).toEqual({
      code: "CAPABILITY_DENIED",
      message: "Shell.Exec not allowed",
      retryable: false,
      details: { capability: "Shell.Exec" },
    });
  });

  it("omits details when empty", () => {
    const err = new CoworkAPIError("TEST", "test", { retryable: true });
    const json = err.toJSON();
    expect(json.details).toBeUndefined();
  });

  it("deserializes from JSON to specific subclass", () => {
    const data = {
      code: "SESSION_NOT_FOUND",
      message: "Session sess_123 not found",
      retryable: false,
    };
    const err = CoworkAPIError.fromJSON(data);
    expect(err).toBeInstanceOf(CoworkAPIError);
    expect(err.code).toBe(ErrorCode.SESSION_NOT_FOUND);
    expect(err.message).toBe("Session sess_123 not found");
  });

  it("deserializes unknown code as base CoworkAPIError", () => {
    const data = { code: "UNKNOWN_CODE", message: "something", retryable: false };
    const err = CoworkAPIError.fromJSON(data);
    expect(err).toBeInstanceOf(CoworkAPIError);
    expect(err.code).toBe("UNKNOWN_CODE");
  });

  it("deserializes with details", () => {
    const data = {
      code: "CAPABILITY_DENIED",
      message: "denied",
      retryable: false,
      details: { capability: "Shell.Exec", sessionId: "sess_1" },
    };
    const err = CoworkAPIError.fromJSON(data);
    expect(err.details).toEqual({ capability: "Shell.Exec", sessionId: "sess_1" });
  });
});

describe("retryable defaults", () => {
  it("marks retryable errors as retryable by default", () => {
    expect(new RateLimitedError().retryable).toBe(true);
    expect(new InternalError().retryable).toBe(true);
    expect(new WorkspaceUploadError().retryable).toBe(true);
  });

  it("marks non-retryable errors as not retryable by default", () => {
    expect(new InvalidRequestError().retryable).toBe(false);
    expect(new SessionNotFoundError().retryable).toBe(false);
    expect(new CapabilityDeniedError().retryable).toBe(false);
    expect(new ToolExecutionError().retryable).toBe(false);
  });

  it("allows retryable override via fromJSON", () => {
    const data = { code: "INTERNAL_ERROR", message: "test", retryable: false };
    const err = CoworkAPIError.fromJSON(data);
    expect(err.retryable).toBe(false);
  });
});

describe("roundtrip", () => {
  it("serializes and deserializes correctly", () => {
    const original = new CapabilityDeniedError("Shell.Exec not allowed", {
      details: { capability: "Shell.Exec" },
    });
    const json = original.toJSON();
    const restored = CoworkAPIError.fromJSON(json);

    expect(restored.code).toBe(original.code);
    expect(restored.message).toBe(original.message);
    expect(restored.retryable).toBe(original.retryable);
    expect(restored.details).toEqual(original.details);
  });
});
