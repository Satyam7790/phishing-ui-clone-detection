"""Safe URL parsing and lexical feature extraction."""
from ipaddress import ip_address
from urllib.parse import urlparse
import re

def validate_public_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Enter a complete http:// or https:// website URL.")
    host = parsed.hostname.lower().rstrip(".")
    if host in {"localhost"} or host.endswith(".local"):
        raise ValueError("Local network addresses cannot be analyzed.")
    try:
        address = ip_address(host)
        if address.is_private or address.is_loopback or address.is_link_local or address.is_reserved:
            raise ValueError("Private network addresses cannot be analyzed.")
    except ValueError as error:
        if "cannot be analyzed" in str(error):
            raise

def extract_url_features(url: str) -> dict:
    validate_public_url(url)
    parsed = urlparse(url)
    host = parsed.hostname.lower().rstrip(".")
    labels = host.split(".")
    try:
        ip_address(host)
        is_ip = True
    except ValueError:
        is_ip = False
    domain = host if is_ip else ".".join(labels[-2:]) if len(labels) >= 2 else host
    specials = len(re.findall(r"[^A-Za-z0-9./?=&_%:-]", url))
    return {
        "domain": domain, "hostname": host, "tld": "" if is_ip else labels[-1],
        "url_length": len(url), "domain_length": len(domain), "path_length": len(parsed.path),
        "query_length": len(parsed.query), "digit_count": sum(c.isdigit() for c in host),
        "hyphen_count": host.count("-"), "dot_count": host.count("."),
        "special_character_count": specials, "subdomain_count": max(0, len(labels) - 2),
        "has_https": int(parsed.scheme == "https"), "has_punycode": int("xn--" in host),
        "has_unicode_lookalike": int(any(ord(c) > 127 for c in host)), "is_ip_address": int(is_ip),
        "excessive_subdomains": int(len(labels) > 4),
        "suspicious_structure": int(len(url) > 100 or host.count("-") >= 3 or "@" in url),
    }
