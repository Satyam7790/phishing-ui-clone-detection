import pytest
from backend.analyzers.url_analyzer import extract_url_features

def test_url_features():
    result = extract_url_features("https://login.g00gle-security-example.com/path?q=7")
    assert result["digit_count"] == 2 and result["hyphen_count"] == 2 and result["subdomain_count"] == 1

def test_private_url_rejected():
    with pytest.raises(ValueError): extract_url_features("http://127.0.0.1/admin")
