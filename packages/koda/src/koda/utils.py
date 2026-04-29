"""Utilities for image and text processing."""

from __future__ import annotations

import re
from PIL import Image, ImageChops

__all__ = ["images_are_identical", "sanitize_filename"]

def images_are_identical(img1: Image.Image, img2: Image.Image) -> bool:
    """Compare two PIL Images to see if they are identical.
    
    Args:
        img1: The first image to compare.
        img2: The second image to compare.
        
    Returns:
        True if the images have the same size and identical pixel data, False otherwise.
    """
    if img1.size != img2.size:
        return False
    diff = ImageChops.difference(img1, img2)
    if diff.getbbox() is None:
        return True
    return False

def sanitize_filename(url: str) -> str:
    """Sanitize a URL into a safe filename string.
    
    Args:
        url: The URL to sanitize.
        
    Returns:
        A sanitized string suitable for use as a filename or S3 key.
    """
    sanitized_name = re.sub(r"^https?://", "", url)
    sanitized_name = re.sub(r"[^a-zA-Z0-9]", "_", sanitized_name)
    return sanitized_name[:200]
