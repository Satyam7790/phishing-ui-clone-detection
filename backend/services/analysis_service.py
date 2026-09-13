import logging
from pathlib import Path
from backend.analyzers.url_analyzer import extract_url_features
from backend.analyzers.brand_matcher import find_brand_match
from backend.analyzers.registration_analyzer import analyze_registration
from backend.analyzers.html_analyzer import fetch_html, analyze_html, html_similarity
from backend.analyzers.screenshot_analyzer import capture_screenshot
from backend.analyzers.visual_similarity import compare_screenshots
from backend.ml.feature_engineering import build_feature_vector
from backend.ml.predictor import predict_probability
from backend.config import RISK_THRESHOLD_LOW, RISK_THRESHOLD_HIGH

log = logging.getLogger(__name__)

def _risk(probability: float) -> str:
    return "LOW" if probability < RISK_THRESHOLD_LOW else "SUSPICIOUS" if probability < RISK_THRESHOLD_HIGH else "HIGH"

def _reasons(domain: dict, brand: dict, registration: dict, html: dict, features: dict) -> list[str]:
    reasons = []
    if brand["brand_similarity"] >= .85: reasons.append("The domain closely resembles a known reference domain.")
    elif brand["brand_similarity"] >= .65: reasons.append("The domain has a moderate similarity to a known reference domain.")
    if domain["has_punycode"] or domain["has_unicode_lookalike"]: reasons.append("The domain uses an encoded or Unicode lookalike character pattern.")
    if domain["suspicious_structure"] or domain["excessive_subdomains"]: reasons.append("The URL has an unusually complex structure.")
    if registration.get("domain_age_days") is not None and registration["domain_age_days"] <= 30: reasons.append("The domain appears to have been registered recently.")
    if html.get("password_field_count", 0): reasons.append("A password input field was detected on the retrieved page.")
    if features.get("html_similarity") is not None and features["html_similarity"] >= .8: reasons.append("The page structure/content is highly similar to its reference website.")
    if features.get("visual_similarity") is not None and features["visual_similarity"] >= .8: reasons.append("The captured page has high visual similarity to its reference website.")
    return reasons or ["No strong impersonation signal was found in the available analysis data."]

def analyze_url(url: str) -> dict:
    log.info("Starting passive analysis for %s", url)
    domain = extract_url_features(url); brand = find_brand_match(domain["domain"]); registration = analyze_registration(domain["domain"])
    pipeline = {"domain_analysis": "complete", "brand_matching": "complete", "registration_analysis": "complete" if registration["registration_available"] else "unavailable", "html_analysis": "unavailable", "screenshot_analysis": "unavailable", "ml_classification": "pending"}
    warnings = []
    html, warning = fetch_html(url)
    submitted = reference = None
    webpage = {"form_count": 0, "input_count": 0, "password_field_count": 0, "email_field_count": 0, "button_count": 0, "link_count": 0, "image_count": 0, "script_count": 0, "iframe_count": 0, "external_link_count": 0, "login_terms": [], "normalized": ""}
    html_score = visual_score = None
    if html:
        webpage = analyze_html(html, url); pipeline["html_analysis"] = "complete"
        if brand["reference_url"]:
            reference_html, _ = fetch_html(brand["reference_url"])
            if reference_html: html_score = html_similarity(webpage["normalized"], analyze_html(reference_html, brand["reference_url"])["normalized"])
        submitted = capture_screenshot(url, "submitted")
        if brand["reference_url"]: reference = capture_screenshot(brand["reference_url"], "reference")
        visual_score = compare_screenshots(submitted, reference)
        pipeline["screenshot_analysis"] = "complete" if submitted else "unavailable"
    elif warning: warnings.append(warning)
    merged = {**domain, **registration, **webpage, "html_similarity": html_score, "visual_similarity": visual_score}
    features = build_feature_vector(merged, brand)
    probability = predict_probability(features); pipeline["ml_classification"] = "complete"
    return {"url": url, "domain": domain["domain"], "risk_level": _risk(probability), "phishing_probability": probability, "target_brand": brand["target_brand"], "target_domain": brand["target_domain"], "features": {**features, "tld": domain["tld"], "registration_date": registration["registration_date"], "registrar": registration["registrar"], "login_terms": webpage["login_terms"]}, "reasons": _reasons(domain, brand, registration, webpage, features), "pipeline": pipeline, "screenshots": {"submitted": f"/screenshots/{submitted.name}" if submitted else None, "reference": f"/screenshots/{reference.name}" if reference else None}, "warnings": warnings}
