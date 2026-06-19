import re
from urllib.parse import urlparse, urlunparse

def sanitize_url(url: str) -> str:
    """Removes query parameters (like utm_source) from a URL."""
    try:
        parsed_url = urlparse(url)
        # Keep scheme, netloc, path. Drop params, query, fragment to ensure clean URL
        sanitized = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
        return sanitized
    except Exception:
        return url

def extract_and_clean_urls(text: str) -> list[str]:
    """Finds URLs in text and returns a list of sanitized URLs."""
    url_pattern = re.compile(r'https?://\S+')
    urls = url_pattern.findall(text)
    return [sanitize_url(url) for url in urls]

def clean_text(text: str) -> str:
    """Removes odd characters, zero-width spaces, and trims text."""
    text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)
    return text.strip()
