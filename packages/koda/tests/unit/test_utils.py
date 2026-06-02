"""Tests for utility functions."""

from koda.utils import images_are_identical, sanitize_filename
from PIL import Image

def test_images_are_identical():
    """Test image comparison logic."""
    img1 = Image.new("RGB", (100, 100), color="red")
    img2 = Image.new("RGB", (100, 100), color="red")
    img3 = Image.new("RGB", (100, 100), color="blue")
    img4 = Image.new("RGB", (50, 50), color="red")
    
    assert images_are_identical(img1, img2) is True
    assert images_are_identical(img1, img3) is False
    assert images_are_identical(img1, img4) is False

def test_sanitize_filename():
    """Test URL to filename sanitization."""
    assert sanitize_filename("https://example.com/path?query=1") == "example_com_path_query_1"
    assert sanitize_filename("http://test.org/!@#$%^&*()") == "test_org___________"
