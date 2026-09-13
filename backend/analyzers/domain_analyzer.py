from .url_analyzer import extract_url_features

def analyze_domain(url: str) -> dict:
    """Compatibility wrapper for domain-oriented lexical analysis."""
    return extract_url_features(url)
