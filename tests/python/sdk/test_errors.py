"""Tests for the error hierarchy and serialization."""

import pytest
from cowork_platform_sdk.constants import ErrorCode
from cowork_platform_sdk.errors import (
    CapabilityDeniedError,
    CoworkAPIError,
    InternalError,
    InvalidRequestError,
    RateLimitedError,
    SessionNotFoundError,
    ToolExecutionError,
    WorkspaceUploadError,
)


@pytest.mark.unit
class TestCoworkAPIError:
    def test_base_error_creation(self) -> None:
        err = CoworkAPIError(code="TEST_CODE", message="test message", retryable=False)
        assert err.code == "TEST_CODE"
        assert err.message == "test message"
        assert err.retryable is False
        assert err.details == {}

    def test_to_dict(self) -> None:
        err = CoworkAPIError(
            code="CAPABILITY_DENIED",
            message="Shell.Exec not allowed",
            retryable=False,
            details={"capability": "Shell.Exec"},
        )
        d = err.to_dict()
        assert d == {
            "code": "CAPABILITY_DENIED",
            "message": "Shell.Exec not allowed",
            "retryable": False,
            "details": {"capability": "Shell.Exec"},
        }

    def test_to_dict_without_details(self) -> None:
        err = CoworkAPIError(code="TEST", message="test", retryable=True)
        d = err.to_dict()
        assert "details" not in d

    def test_from_dict_maps_to_subclass(self) -> None:
        data = {
            "code": "SESSION_NOT_FOUND",
            "message": "Session sess_123 not found",
            "retryable": False,
        }
        err = CoworkAPIError.from_dict(data)
        assert isinstance(err, SessionNotFoundError)
        assert err.code == ErrorCode.SESSION_NOT_FOUND
        assert err.message == "Session sess_123 not found"

    def test_from_dict_unknown_code(self) -> None:
        data = {"code": "UNKNOWN_CODE", "message": "something", "retryable": False}
        err = CoworkAPIError.from_dict(data)
        assert isinstance(err, CoworkAPIError)
        assert not isinstance(err, SessionNotFoundError)
        assert err.code == "UNKNOWN_CODE"

    def test_from_dict_with_details(self) -> None:
        data = {
            "code": "CAPABILITY_DENIED",
            "message": "denied",
            "retryable": False,
            "details": {"capability": "Shell.Exec", "sessionId": "sess_1"},
        }
        err = CoworkAPIError.from_dict(data)
        assert isinstance(err, CapabilityDeniedError)
        assert err.details == {"capability": "Shell.Exec", "sessionId": "sess_1"}

    def test_repr(self) -> None:
        err = SessionNotFoundError(message="not found")
        assert "SessionNotFoundError" in repr(err)
        assert "SESSION_NOT_FOUND" in repr(err)

    def test_is_exception(self) -> None:
        err = ToolExecutionError(message="tool failed")
        assert isinstance(err, Exception)
        assert isinstance(err, CoworkAPIError)


@pytest.mark.unit
class TestRetryableErrors:
    def test_retryable_by_default(self) -> None:
        assert RateLimitedError().retryable is True
        assert InternalError().retryable is True
        assert WorkspaceUploadError().retryable is True

    def test_not_retryable_by_default(self) -> None:
        assert InvalidRequestError().retryable is False
        assert SessionNotFoundError().retryable is False
        assert CapabilityDeniedError().retryable is False
        assert ToolExecutionError().retryable is False

    def test_retryable_override_via_from_dict(self) -> None:
        """Subclasses hardcode retryable; override happens via from_dict or direct assignment."""
        data = {"code": "INTERNAL_ERROR", "message": "test", "retryable": False}
        err = CoworkAPIError.from_dict(data)
        assert isinstance(err, InternalError)
        assert err.retryable is False  # overridden from default True

    def test_retryable_override_via_attribute(self) -> None:
        err = InternalError(message="test")
        assert err.retryable is True  # default
        err.retryable = False
        assert err.retryable is False


@pytest.mark.unit
class TestRoundTrip:
    """Verify serialize → deserialize roundtrip preserves all fields."""

    def test_full_roundtrip(self) -> None:
        original = CapabilityDeniedError(
            message="Shell.Exec not allowed",
            details={"capability": "Shell.Exec"},
        )
        serialized = original.to_dict()
        restored = CoworkAPIError.from_dict(serialized)

        assert isinstance(restored, CapabilityDeniedError)
        assert restored.code == original.code
        assert restored.message == original.message
        assert restored.retryable == original.retryable
        assert restored.details == original.details
