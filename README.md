# AI/ML Phishing Domain Detector

A free, local college-project prototype that estimates whether a website could be a phishing or lookalike domain. It uses a FastAPI backend, a Random Forest classifier, passive webpage analysis, local reference-domain matching, and optional local screenshot comparison. No API key or paid service is required.

## Architecture

```text
URL → URL/domain features + brand match + best-effort RDAP
    → passive HTML analysis → optional Playwright screenshots
    → feature vector → local Random Forest → risk estimate + explanation → dashboard
```

## Features

- Safe HTTP/HTTPS validation; local/private network targets are rejected.
- URL/domain features: length, digits, hyphens, subdomains, punycode, Unicode, and URL structure.
- Levenshtein-based lookalike matching against the editable `data/legitimate_domains.json` reference database.
- Best-effort free RDAP registration lookup; unavailable data remains unavailable rather than being invented.
- Passive HTML feature extraction, TF-IDF/cosine HTML comparison, and optional Playwright screenshot capture.
- Local Pillow/NumPy visual comparison when both screenshots are available.
- A local scikit-learn `RandomForestClassifier` with `predict_proba` and a dynamic, evidence-based explanation.
- Responsive dashboard with real API calls, pipeline state, and JSON download.

## Installation

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ml/train.py
```

Windows:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python ml/train.py
```

Screenshot comparison is optional. To enable it after installing requirements:

```bash
playwright install chromium
```

## Run

```bash
python run.py
```

Open `http://127.0.0.1:8000`. Alternatively use `uvicorn backend.main:app --reload`.

## API

- `GET /health` — server and model status.
- `POST /analyze` — accepts `{"url":"https://example.com"}`.

The response includes a probability estimate, risk level, possible impersonation target, features, available similarity values, pipeline statuses, warnings, and evidence-based reasons. Missing page, registration, or screenshot data is returned as `null`/`unavailable`, never fabricated.

## Dataset and ML

`ml/dataset.csv` is **DEMO DATA**, deliberately small and synthetic. Run `python ml/train.py` to train and save `ml/model.pkl`; it prints accuracy, precision, recall, F1, and a confusion matrix on a reproducible held-out demo split. Those are demonstration metrics, not real-world performance. Replace the demo file with a suitably licensed public phishing dataset, retaining the documented feature columns and `label` (0 legitimate, 1 phishing), before drawing real-world performance conclusions.

## Security and privacy

The analyzer is passive: it does not execute downloads, submit forms, or accept credentials. It enforces HTTP(S), timeouts, redirect and response limits, and rejects local/private IP targets. URLs are analyzed by the local backend; no commercial AI service is used.

## Limitations

This is an educational prototype, not a production security product. Websites can block automated access, many pages require JavaScript, RDAP can be unavailable, and the reference-domain set is intentionally small. Screenshot capture requires a local browser installation. Visual similarity and a probability score are supporting signals, not proof of malicious intent. A larger, independently validated dataset and stronger SSRF protections (including DNS-resolution checks) are recommended for deployment.

## Next step

Add a carefully curated, labelled public dataset and evaluate the model against a separate real-world test set before expanding the reference-brand database or deploying it beyond a controlled environment.
