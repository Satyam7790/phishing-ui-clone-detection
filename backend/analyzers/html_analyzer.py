from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import httpx
from backend.config import MAX_RESPONSE_SIZE, REQUEST_TIMEOUT, USER_AGENT

def fetch_html(url: str) -> tuple[str | None, str | None]:
    try:
        with httpx.Client(timeout=REQUEST_TIMEOUT, follow_redirects=True, max_redirects=4, headers={"User-Agent": USER_AGENT}) as client:
            response = client.get(url)
            response.raise_for_status()
            if "html" not in response.headers.get("content-type", "").lower(): return None, "The address did not return an HTML page."
            body = response.content[:MAX_RESPONSE_SIZE]
            return body.decode(response.encoding or "utf-8", errors="replace"), None
    except httpx.HTTPError:
        return None, "The website could not be retrieved; domain-level analysis is still available."

def analyze_html(html: str, page_url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    links = [a.get("href", "") for a in soup.find_all("a")]
    host = urlparse(page_url).hostname
    external = sum(bool(urlparse(urljoin(page_url, link)).hostname not in {None, host}) for link in links)
    inputs = soup.find_all("input")
    visible = soup.get_text(" ", strip=True)[:12000]
    lowered = visible.lower()
    tokens = [word for word in ("login", "sign in", "password", "verify", "account", "secure", "authentication") if word in lowered]
    return {"form_count": len(soup.find_all("form")), "input_count": len(inputs), "password_field_count": sum(x.get("type", "").lower() == "password" for x in inputs), "email_field_count": sum(x.get("type", "").lower() == "email" for x in inputs), "button_count": len(soup.find_all("button")), "link_count": len(links), "image_count": len(soup.find_all("img")), "script_count": len(soup.find_all("script")), "iframe_count": len(soup.find_all("iframe")), "external_link_count": external, "login_terms": tokens, "normalized": normalize_html(soup)}

def normalize_html(soup: BeautifulSoup) -> str:
    tags = " ".join(node.name for node in soup.find_all(["form", "input", "button", "img", "a", "script", "iframe", "label", "h1", "h2"]))
    text = soup.get_text(" ", strip=True)[:5000]
    return f"{tags} {text}"

def html_similarity(first: str, second: str) -> float | None:
    if not first or not second: return None
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    matrix = TfidfVectorizer(stop_words="english").fit_transform([first, second])
    return round(float(cosine_similarity(matrix[0], matrix[1])[0, 0]), 4)
