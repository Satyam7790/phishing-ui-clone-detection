from backend.analyzers.brand_matcher import find_brand_match
def test_lookalike_brand_match():
    match = find_brand_match("paypa1-login.com")
    assert match["target_brand"] == "PayPal" and match["brand_similarity"] > .8
def test_unrelated_domain_has_no_forced_match():
    assert find_brand_match("randomstudentproject.com")["target_brand"] is None
