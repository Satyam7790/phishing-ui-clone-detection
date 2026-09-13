"""Best-effort free RDAP lookup; failure is a normal unavailable signal."""
from datetime import datetime, timezone
import httpx

def analyze_registration(domain: str) -> dict:
    result = {"registration_date": None, "domain_age_days": None, "registrar": None, "registration_available": False}
    try:
        response = httpx.get(f"https://rdap.org/domain/{domain}", timeout=5, headers={"Accept": "application/rdap+json"})
        response.raise_for_status(); payload = response.json()
        event = next((x for x in payload.get("events", []) if x.get("eventAction") == "registration"), None)
        if event and event.get("eventDate"):
            date = datetime.fromisoformat(event["eventDate"].replace("Z", "+00:00"))
            result["registration_date"] = date.date().isoformat()
            result["domain_age_days"] = max(0, (datetime.now(timezone.utc) - date).days)
        entities = payload.get("entities", [])
        registrar = next((x for x in entities if "registrar" in x.get("roles", [])), None)
        if registrar:
            result["registrar"] = registrar.get("vcardArray", [None, []])[1][1][3] if len(registrar.get("vcardArray", [])) > 1 and len(registrar["vcardArray"][1]) > 1 else None
        result["registration_available"] = result["registration_date"] is not None
    except (httpx.HTTPError, ValueError, KeyError, IndexError, TypeError):
        pass
    return result
