import json
from pathlib import Path
from backend.config import REFERENCE_DATA_PATH

SUBSTITUTIONS = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t"})

def _distance(left: str, right: str) -> int:
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, 1):
        current = [i]
        for j, b in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (a != b)))
        previous = current
    return previous[-1]

def _normalize(value: str) -> str:
    return "".join(c for c in value.lower().translate(SUBSTITUTIONS) if c.isalnum())

def find_brand_match(domain: str, reference_path: Path = REFERENCE_DATA_PATH) -> dict:
    references = json.loads(reference_path.read_text())
    label = domain.split(".")[0]
    candidate = _normalize(label)
    best = {"target_brand": None, "target_domain": None, "brand_similarity": 0.0, "reference_url": None}
    for brand, item in references.items():
        target = _normalize(item["domain"].split(".")[0])
        similarity = 1 - _distance(candidate, target) / max(len(candidate), len(target), 1)
        # A brand token combined with extra login/security wording is more indicative
        # than raw whole-label edit distance alone.
        if target in candidate and candidate != target:
            similarity = max(similarity, min(0.95, 0.82 + (len(target) / max(len(candidate), 1)) * 0.10))
        if similarity > best["brand_similarity"]:
            best = {"target_brand": brand, "target_domain": item["domain"], "brand_similarity": round(similarity, 4), "reference_url": item["url"]}
    return best if best["brand_similarity"] >= 0.58 else {"target_brand": None, "target_domain": None, "brand_similarity": 0.0, "reference_url": None}
