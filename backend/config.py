from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST_TIMEOUT = 8
MAX_RESPONSE_SIZE = 1_500_000
MAX_REDIRECTS = 4
BROWSER_TIMEOUT = 12_000
RISK_THRESHOLD_LOW = 0.30
RISK_THRESHOLD_HIGH = 0.70
REFERENCE_DATA_PATH = ROOT / "data" / "legitimate_domains.json"
MODEL_PATH = ROOT / "ml" / "model.pkl"
SCREENSHOT_DIRECTORY = ROOT / "screenshots"
USER_AGENT = "PhishDomainDetector/1.0 (educational, passive analysis)"
