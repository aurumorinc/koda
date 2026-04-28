"""Tests for utility functions."""

from bs4 import BeautifulSoup
from PIL import Image
import io

from koda.utils import html_to_markdown, extract_metadata, images_are_identical

def test_html_to_markdown_basic():
    """Test basic HTML to Markdown conversion."""
    html = "<h1>Hello</h1><p>World</p>"
    md = html_to_markdown(html, only_main_content=False)
    assert "# Hello" in md
    assert "World" in md

def test_html_to_markdown_main_content():
    """Test main content extraction filtering."""
    html = """
    <html>
        <head><title>Test</title></head>
        <body>
            <header>Header Info</header>
            <nav>Nav Info</nav>
            <main>
                <h2>Main Section</h2>
                <p>This is the core content.</p>
            </main>
            <footer>Footer Info</footer>
        </body>
    </html>
    """
    md = html_to_markdown(html, only_main_content=True)
    assert "Main Section" in md
    assert "This is the core content." in md
    assert "Header Info" not in md
    assert "Nav Info" not in md
    assert "Footer Info" not in md

def test_extract_metadata():
    """Test extracting metadata from HTML."""
    html = """
    <html>
        <head>
            <title>My Page</title>
            <meta name="description" content="A simple test page.">
            <meta property="og:title" content="My OG Title">
        </head>
    </html>
    """
    meta = extract_metadata(html)
    assert meta.get("title") == "My Page"
    assert meta.get("description") == "A simple test page."
    assert meta.get("og:title") == "My OG Title"

def test_images_are_identical():
    """Test image comparison logic."""
    img1 = Image.new("RGB", (100, 100), color="red")
    img2 = Image.new("RGB", (100, 100), color="red")
    img3 = Image.new("RGB", (100, 100), color="blue")
    img4 = Image.new("RGB", (50, 50), color="red")
    
    assert images_are_identical(img1, img2) is True
    assert images_are_identical(img1, img3) is False
    assert images_are_identical(img1, img4) is False
