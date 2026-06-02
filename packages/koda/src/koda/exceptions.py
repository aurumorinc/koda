"""Exceptions for Koda."""

class KodaError(Exception):
    """Base exception class for all errors raised by the koda module."""
    pass

class ScrapeError(KodaError):
    """Exception raised when an error occurs during scraping."""
    pass

class SessionExhaustedError(KodaError):
    """Exception raised when no usable sessions are available for a provider."""
    pass
