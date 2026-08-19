"""Custom exceptions for PyFlow.

This module defines domain-specific error types.
"""


class PyFlowError(Exception):
    """Base exception for PyFlow errors."""


class FileDiscoveryError(PyFlowError):
    """Raised when file discovery fails."""


class ProcessingError(PyFlowError):
    """Raised when file processing fails."""


class CacheError(PyFlowError):
    """Raised when cache operations fail."""


class SchedulerError(PyFlowError):
    """Raised when scheduler operations fail."""


class SnapshotError(PyFlowError):
    """Raised when snapshot operations fail."""
