"""Exceptions for Koda."""

class Error(Exception):
    """Base exception class for all errors raised by the koda module."""
    pass

class ScrapeError(Error):
    """Exception raised when an error occurs during scraping."""
    pass

class SessionExhaustedError(Error):
    """Exception raised when no usable sessions are available for a provider."""
    pass

class TimeoutError(Error):
    """Exception raised when an execution limit is exceeded."""
    pass

class BrowserLaunchError(Error):
    """Exception raised when a browser crashes or fails to launch."""
    pass
