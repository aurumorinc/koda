"""Tests for page extraction logic."""

from koda.services.page import _to_markdown, _extract_metadata
from koda.schemas.page import ScrapeRequest

def test_html_to_markdown_basic():
    """Test basic HTML to Markdown conversion."""
    html = "<h1>Hello</h1><p>World</p>"
    md = _to_markdown(html, only_main_content=False)
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
    md = _to_markdown(html, only_main_content=True)
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
    meta = _extract_metadata(html)
    assert meta.get("title") == "My Page"
    assert meta.get("description") == "A simple test page."
    assert meta.get("og:title") == "My OG Title"
