"""Custom exceptions for the file processor.

This module defines domain-specific error types.
"""


class FileProcessorError(Exception):
    """Base exception for file processor errors."""


class FileNotFoundError(FileProcessorError):
    """Raised when a file cannot be found."""


class DirectoryNotFoundError(FileProcessorError):
    """Raised when a directory cannot be found."""


class InvalidSnapshotError(FileProcessorError):
    """Raised when a snapshot is invalid."""


class BackupError(FileProcessorError):
    """Raised when a backup operation fails."""
