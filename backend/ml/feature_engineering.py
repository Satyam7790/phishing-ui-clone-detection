FEATURE_COLUMNS = ["url_length", "domain_length", "path_length", "digit_count", "hyphen_count", "dot_count", "special_character_count", "subdomain_count", "has_https", "has_punycode", "has_unicode_lookalike", "domain_age_days", "brand_similarity", "form_count", "input_count", "password_field_count", "email_field_count", "button_count", "image_count", "script_count", "iframe_count", "external_link_count", "html_similarity", "visual_similarity"]

def build_feature_vector(*sources: dict) -> dict:
    merged = {key: value for source in sources for key, value in source.items()}
    # Missing signals stay explicit; the model pipeline imputes them from training data.
    return {column: merged.get(column) for column in FEATURE_COLUMNS}
