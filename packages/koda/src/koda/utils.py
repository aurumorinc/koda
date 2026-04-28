"""Utilities for image and text processing."""

from __future__ import annotations

import io
import asyncio
from typing import Dict, Any

from PIL import Image, ImageChops
from bs4 import BeautifulSoup
from markdownify import markdownify as md

__all__ = ["images_are_identical", "extract_metadata", "html_to_markdown"]

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

def extract_metadata(html_content: str) -> Dict[str, Any]:
    """Extract metadata (title, description, open graph) from HTML.
    
    Args:
        html_content: The raw HTML content.
        
    Returns:
        A dictionary containing extracted metadata.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    metadata: Dict[str, Any] = {}
    
    # Extract title
    title_tag = soup.find('title')
    if title_tag and title_tag.string:
        metadata['title'] = title_tag.string.strip()
        
    # Extract meta tags
    for meta in soup.find_all('meta'):
        name = meta.get('name') or meta.get('property')
        content = meta.get('content')
        if name and content:
            metadata[name] = content.strip()
            
    return metadata

def html_to_markdown(html_content: str, only_main_content: bool = True) -> str:
    """Convert HTML content to clean Markdown.
    
    Args:
        html_content: The raw HTML string to convert.
        only_main_content: If True, attempts to extract only the main content
            by removing headers, footers, navs, and sidebars before conversion.
            
    Returns:
        The extracted and converted Markdown text.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    if only_main_content:
        # Strip out common noise elements
        for element in soup.find_all(['nav', 'header', 'footer', 'aside', 'script', 'style', 'noscript']):
            element.decompose()
            
        # Try to find main content block
        main_block = soup.find('main') or soup.find(id='main-content') or soup.find(class_='main-content')
        if main_block:
            soup = main_block
            
    return md(str(soup), heading_style="ATX", strip=['a', 'img']).strip()
