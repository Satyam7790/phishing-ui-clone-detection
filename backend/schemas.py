from typing import Any
from pydantic import BaseModel, HttpUrl

class AnalyzeRequest(BaseModel):
    url: HttpUrl

class AnalyzeResponse(BaseModel):
    url: str
    domain: str
    risk_level: str
    phishing_probability: float
    target_brand: str | None = None
    target_domain: str | None = None
    features: dict[str, Any]
    reasons: list[str]
    pipeline: dict[str, str]
    screenshots: dict[str, str | None]
    warnings: list[str] = []
