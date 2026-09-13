# Phishing Domain Detector

A free, local React + Node.js college-project prototype for estimating whether a URL shows phishing or brand-impersonation characteristics. It performs passive analysis only: it never submits forms, collects credentials, downloads files, or uses API keys.

## How it works

```text
React dashboard → POST /api/analyze → Express server
  → URL feature extraction → brand similarity → basic webpage analysis
  → transparent Risk Scoring Engine → result dashboard
```

The score is an estimate from a transparent prototype risk model, not an AI claim or a definitive security verdict. The design keeps `riskAnalyzer.js` isolated so a trained classifier can replace it later.

## Features

- React dashboard with real loading, errors, risk cards, feature cards, and dynamic explanations.
- Express API (`POST /api/analyze`, `GET /api/health`).
- Understandable URL features: length, digits, hyphens, dots, subdomains, special characters, HTTPS, IP address use, punycode, and unusual structure.
- Levenshtein-based comparison against an editable local reference-brand database.
- Basic passive HTML inspection: forms, inputs, password inputs, buttons, links, images, scripts, and login terms.
- Graceful webpage-fetch failure: the domain-level result still returns.

## Install

Requires Node.js 18+.

```bash
npm install
npm install --prefix server
npm install --prefix client
```

## Run

Run both applications together:

```bash
npm run dev
```

Open `http://localhost:5173`. The Express API runs on `http://localhost:5000` and Vite proxies `/api` requests to it.

To run separately:

```bash
npm run dev --prefix server
npm run dev --prefix client
```

## API example

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

The response contains `phishingProbability`, `riskLevel`, closest reference-brand match, extracted features, and reasons created from the actual signals.

## Tests and build

```bash
npm test
npm run build --prefix client
```

## Safety and limitations

Only `http` and `https` URLs are permitted. Local/private network targets are rejected, page retrieval is time-limited, and only the submitted page is inspected. Some sites block automated requests or render content with JavaScript, so webpage signals may be unavailable. The reference list is deliberately small, and this prototype score is not a production phishing decision.

## Future improvements

Future versions could add RDAP, larger labelled phishing datasets, a properly trained local ML classifier, advanced HTML comparison, screenshot comparison, threat-intelligence feeds, or a browser extension. These are intentionally outside this simple, viva-friendly version.
