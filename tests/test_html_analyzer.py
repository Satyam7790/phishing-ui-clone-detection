from backend.analyzers.html_analyzer import analyze_html
def test_html_signals():
    result = analyze_html('<form><input type="email"><input type="password"><button>Sign in</button></form>', "https://example.com")
    assert result["form_count"] == 1 and result["password_field_count"] == 1 and "sign in" in result["login_terms"]
