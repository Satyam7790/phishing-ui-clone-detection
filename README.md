# Phishing-ui-clone-detection  (AI/ML-Based Phishing Domain Detection System)

## 1. Project Overview

Phishing attacks are one of the most common methods used to compromise users through malicious websites that imitate legitimate services.

Attackers often register domains that resemble genuine websites and create webpages that copy their **look, structure, content, and login interfaces**.

For example:

```text
Legitimate:
paypal.com

Potential phishing domains:
paypa1.com
paypal-login.com
paypal-security.com
```

The objective of this project is to build an **intelligent AI/ML-based system that analyzes newly registered or suspicious domains and estimates the probability that they are phishing websites**.

The system combines multiple signals rather than relying on a single rule:

* Domain-name similarity
* Domain registration information
* URL characteristics
* HTML/content similarity
* Webpage structure
* Screenshot/visual similarity
* Machine-learning classification

The final system produces a **phishing probability score** along with an explanation of the factors contributing to the score.

---

# 2. Problem Statement

> Create an intelligent system using AI/ML to detect phishing domains which imitate the look and feel of genuine domains.

Phishing domains are frequently created to impersonate legitimate organizations. These domains may host fake login pages designed to steal credentials or may deliver malicious content.

The system should be capable of analyzing newly registered domains using publicly available domain information and webpage characteristics.

The main objective is to determine:

1. Whether a domain is likely to be phishing.
2. Which legitimate domain or brand it may be impersonating.
3. How similar the suspicious website is to the genuine website.
4. A probability/risk score indicating the likelihood of phishing.
5. The result in a simple and understandable format.

---

# 3. Core Idea

The fundamental idea is:

> **Instead of trying to directly "recognize" a phishing website, convert the website into measurable features and use those features to determine how suspicious it is.**

A website can be represented using several types of information:

```text
                    WEBSITE
                       |
        +--------------+--------------+
        |              |              |
      DOMAIN          HTML         SCREENSHOT
        |              |              |
        v              v              v
   URL Features   Structure/Data   Visual Features
        |              |              |
        +--------------+--------------+
                       |
                       v
                FEATURE VECTOR
                       |
                       v
                ML CLASSIFIER
                       |
                       v
             PHISHING PROBABILITY
                       |
                       v
                 RISK REPORT
```

This makes the system explainable and modular.

---

# 4. Why Multiple Signals?

A newly registered domain is not necessarily malicious.

For example:

```text
mynewstartup.com
```

may have been registered yesterday and still be completely legitimate.

Therefore, domain age alone cannot determine whether a website is phishing.

Instead, several signals should be combined.

For example:

```text
Domain age = 2 days
Domain similarity to paypal.com = 94%
HTML similarity = 87%
Visual similarity = 92%
Contains login form = Yes
```

Together, these signals provide much stronger evidence of potential impersonation.

The system therefore follows the principle:

```text
Weak individual signals
        +
Multiple correlated signals
        ↓
Stronger overall decision
```

---

# 5. System Architecture

The proposed architecture is:

```text
                         USER
                          |
                          v
                    Enter Domain
                          |
                          v
                 +----------------+
                 |  FastAPI/API   |
                 +-------+--------+
                         |
             +-----------+-----------+
             |                       |
             v                       v
      Domain Analyzer          Website Analyzer
             |                       |
             |                 +-----+-----+
             |                 |           |
             v                 v           v
        WHOIS/RDAP           HTML      Screenshot
             |                 |           |
             v                 v           v
       Domain Features    HTML Features  Visual Features
             |                 |           |
             +-----------------+-----------+
                               |
                               v
                       Feature Engineering
                               |
                               v
                       ML Classification
                               |
                               v
                    Phishing Probability
                               |
                               v
                       Risk Explanation
                               |
                               v
                         Web Dashboard
```

---

# 6. Major Components

## 6.1 Domain Analysis

The first layer analyzes the domain name itself.

Example:

```text
paypa1-login-security.com
```

Possible features include:

```text
domain_length
number_of_digits
number_of_hyphens
number_of_dots
number_of_special_characters
subdomain_count
TLD
domain_entropy
```

These features can help identify unusual or suspicious domain patterns.

---

# 7. Domain Similarity

One of the most important concepts is determining whether a suspicious domain resembles a known legitimate domain.

For example:

```text
paypal.com
paypa1.com
```

The domains differ by only one character.

A simple method for measuring this is **Levenshtein distance**, which measures the number of character edits required to transform one string into another.

The distance can be converted into a normalized similarity score:

```text
similarity =
1 - distance / max(length(domain1), length(domain2))
```

A high similarity indicates that the domains are structurally close.

Other examples include:

```text
google.com
g00gle-login.com

microsoft.com
microsoft-security-login.com

amazon.com
amaz0n-support.com
```

Domain similarity becomes one of the features provided to the ML model.

---

# 8. Legitimate Domain / Brand Matching

There is an important second problem:

> If a domain is suspicious, which legitimate website is it trying to imitate?

The system can maintain a database of known legitimate domains.

Example:

```json
{
    "paypal": "https://paypal.com",
    "google": "https://google.com",
    "amazon": "https://amazon.com",
    "microsoft": "https://microsoft.com"
}
```

For a suspicious domain:

```text
paypa1-login.com
```

the system can determine:

```text
Closest legitimate domain:
paypal.com
```

The suspicious domain can then be compared against the genuine website.

---

# 9. WHOIS / Domain Registration Analysis

Newly registered domains can provide useful metadata.

Possible information includes:

```text
registration date
domain age
expiration date
registrar
name servers
```

For example:

```text
Domain: paypal-security-login.com
Age: 2 days
```

A very recently registered domain that also strongly resembles a known brand may deserve additional scrutiny.

However:

> **Newly registered does not mean phishing.**

Domain age should therefore be treated as one feature rather than a final decision.

---

# 10. HTML / Backend Content Analysis

A phishing website may copy the structure and content of the legitimate website.

The system can inspect the webpage's HTML and extract features such as:

```text
number of forms
number of input fields
number of password fields
number of buttons
number of images
number of scripts
number of iframes
number of links
```

For example:

```text
Genuine website:

forms = 1
inputs = 2
password fields = 1
images = 8

Suspicious website:

forms = 1
inputs = 2
password fields = 1
images = 7
```

The structural similarity can therefore provide another signal.

---

# 11. HTML / Content Similarity

Raw HTML can also be converted into a representation suitable for comparison.

A lightweight approach is:

```text
HTML
  |
  v
Text / Tokens
  |
  v
TF-IDF
  |
  v
Vector Representation
  |
  v
Cosine Similarity
```

This allows the system to calculate how similar the content or structure of two webpages is.

For a college project, **TF-IDF + cosine similarity** provides a relatively simple and explainable starting point.

---

# 12. Screenshot / Visual Analysis

HTML similarity alone is not sufficient.

An attacker can create a visually similar website using completely different HTML.

Therefore, the system can also capture screenshots of webpages.

Conceptually:

```text
Genuine Website
      |
      v
 Screenshot
      |
      v
 Visual Representation


Suspicious Website
      |
      v
 Screenshot
      |
      v
 Visual Representation
```

The two representations can then be compared.

The system can analyze similarities in:

* Page layout
* Logos
* Buttons
* Forms
* Images
* Colors
* Overall structure
* Visual arrangement

---

# 13. Computer Vision / Image Embeddings

Instead of training a large computer-vision model from scratch, a pretrained vision model can be used.

The basic process is:

```text
Screenshot
     |
     v
Pretrained Vision Model
     |
     v
Feature Vector / Embedding
     |
     v
Cosine Similarity
     |
     v
Visual Similarity Score
```

For example:

```text
Genuine screenshot embedding
        ↓
[0.21, 0.73, 0.19, ...]

Suspicious screenshot embedding
        ↓
[0.22, 0.70, 0.20, ...]
```

A similarity metric can then determine how visually close the two webpages are.

This approach avoids the need to train a large neural network from scratch.

---

# 14. Feature Engineering

All the collected information is converted into numerical features.

Example feature vector:

```python
[
    domain_similarity,
    html_similarity,
    visual_similarity,
    domain_age,
    domain_length,
    digit_count,
    hyphen_count,
    subdomain_count,
    form_count,
    password_field_count
]
```

A larger implementation can contain 20–30 or more features.

The important categories are:

### URL Features

```text
url_length
domain_length
path_length
digit_count
hyphen_count
dot_count
special_character_count
subdomain_count
```

### Domain Features

```text
domain_age
TLD
brand_similarity
edit_distance
entropy
```

### HTML Features

```text
form_count
input_count
password_field_count
iframe_count
script_count
image_count
external_link_count
html_similarity
```

### Visual Features

```text
image_similarity
logo_similarity
screenshot_embedding_similarity
```

---

# 15. Machine Learning Model

Once the features have been extracted, they can be given to a machine-learning classifier.

For the initial implementation, a suitable model is:

```text
Random Forest
```

Other possible models include:

```text
XGBoost
Logistic Regression
Support Vector Machine
```

Random Forest is useful for this project because it is relatively simple, works well with mixed numerical features, and is easy to explain during a project presentation.

The model learns:

```text
Features
   |
   v
Phishing / Legitimate
```

During inference:

```text
Feature Vector
      |
      v
Random Forest
      |
      v
Phishing Probability
```

---

# 16. Probability Score

Instead of producing only:

```text
PHISHING
```

or:

```text
LEGITIMATE
```

the system should produce a probability/risk score.

For example:

```text
0.08  → Low Risk
0.42  → Suspicious
0.87  → High Risk
0.97  → Very High Risk
```

The score should be treated as an **estimated model probability**, not absolute proof.

A useful result could be:

```text
Phishing Probability: 93%
Risk Level: HIGH
```

---

# 17. Explainable Detection

The system should not only say:

```text
93% phishing
```

It should explain why.

Example:

```text
Domain:
    paypa1-login.com

Possible target:
    paypal.com

Phishing probability:
    93%

Signals:
    Domain similarity       94%
    HTML similarity         87%
    Visual similarity       92%
    Domain age              2 days
    Password field          Detected
```

This makes the system easier to understand and more useful than a simple black-box classifier.

---

# 18. Detecting Previously Unseen Domains

A major requirement is the ability to identify **new phishing domains**.

The system should not simply memorize known phishing URLs.

Instead, it learns general patterns.

For example, even if:

```text
paypa1-secure-login.xyz
```

was never present in the training dataset, the system can still analyze:

```text
Domain similarity
Domain age
URL characteristics
HTML similarity
Visual similarity
Login structure
```

and make a prediction.

Therefore:

```text
Known training URLs
        ↓
Learn phishing patterns
        ↓
New unseen domain
        ↓
Extract same features
        ↓
Model inference
        ↓
Risk score
```

This is the intended idea behind detecting newly created phishing domains.

---

# 19. Example End-to-End Flow

Suppose the user submits:

```text
https://paypa1-login-security.com
```

### Step 1 — Domain Analysis

```text
Domain length: 26
Digits: 1
Hyphens: 2
```

### Step 2 — Brand Matching

The system identifies:

```text
Possible target:
paypal.com
```

### Step 3 — Domain Similarity

```text
Similarity:
94%
```

### Step 4 — Registration Analysis

```text
Domain age:
3 days
```

### Step 5 — Webpage Analysis

```text
Login form:
Detected

Password field:
Detected
```

### Step 6 — HTML Similarity

```text
HTML similarity:
87%
```

### Step 7 — Screenshot Analysis

```text
Visual similarity:
92%
```

### Step 8 — ML Prediction

```text
Phishing probability:
93%
```

### Final Result

```text
HIGH RISK

Possible impersonated website:
paypal.com

Phishing Probability:
93%
```

---

# 20. Proposed Technology Stack

## Frontend

```text
HTML
CSS
JavaScript
```

## Backend

```text
Python
FastAPI
```

## Machine Learning

```text
scikit-learn
pandas
numpy
```

## Domain Analysis

```text
WHOIS / RDAP
tldextract
```

## HTML Analysis

```text
BeautifulSoup
```

## Screenshot Capture

```text
Playwright / Selenium
```

## Similarity

```text
TF-IDF
Cosine Similarity
Levenshtein Distance
```

## Computer Vision

```text
Pretrained vision model
```

## Database

```text
SQLite
```

The initial system can remain lightweight and run locally without requiring expensive infrastructure.

---

# 21. Proposed Project Structure

```text
phishing-domain-detector/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── main.py
│   ├── domain_analyzer.py
│   ├── html_analyzer.py
│   ├── screenshot_analyzer.py
│   ├── feature_engineering.py
│   └── predictor.py
│
├── ml/
│   ├── dataset.csv
│   ├── train.py
│   └── model.pkl
│
├── data/
│   └── legitimate_domains.json
│
├── requirements.txt
│
└── README.md
```

---

# 22. High-Level Development Plan

The project can be developed incrementally.

## Phase 1 — URL and Domain Analysis

Implement:

```text
URL parsing
Domain feature extraction
Domain similarity
Legitimate-domain database
```

---

## Phase 2 — Website Analysis

Implement:

```text
HTML downloading
HTML feature extraction
HTML/content similarity
```

---

## Phase 3 — Visual Analysis

Implement:

```text
Automated webpage screenshot
Image/embedding extraction
Visual similarity
```

---

## Phase 4 — Machine Learning

Create a dataset containing:

```text
Phishing examples
Legitimate examples
```

Extract features and train:

```text
Random Forest
```

Evaluate using:

```text
Accuracy
Precision
Recall
F1-score
Confusion Matrix
```

---

## Phase 5 — Backend

Expose the detector through an API:

```http
POST /analyze
```

Example input:

```json
{
    "url": "https://example.com"
}
```

Example output:

```json
{
    "phishing_probability": 0.91,
    "risk": "HIGH",
    "target_domain": "paypal.com",
    "domain_similarity": 0.94,
    "html_similarity": 0.87,
    "visual_similarity": 0.92
}
```

---

## Phase 6 — Dashboard

Create a simple web interface where a user can:

```text
Enter URL
     ↓
Click Analyze
     ↓
View Risk Score
     ↓
View Similarity Scores
     ↓
View Reasons
```

---

# 23. Expected User Interface

```text
┌──────────────────────────────────────────────┐
│          PHISHING DOMAIN DETECTOR            │
│                                              │
│ Enter website URL                            │
│                                              │
│ [ https://paypa1-login-security.com       ] │
│                                              │
│                 [ ANALYZE ]                  │
└──────────────────────────────────────────────┘
```

Result:

```text
┌──────────────────────────────────────────────┐
│ ANALYSIS RESULT                              │
│                                              │
│ Domain: paypa1-login-security.com            │
│                                              │
│ RISK: HIGH                                   │
│                                              │
│ Phishing Probability: 93%                    │
│                                              │
│ Possible Target: paypal.com                  │
│                                              │
│ Domain Similarity       94%                  │
│ HTML Similarity         87%                  │
│ Visual Similarity       92%                  │
│ Domain Age              3 days               │
│                                              │
│ Reasons:                                     │
│ • Highly similar domain name                 │
│ • Newly registered domain                    │
│ • Similar login page structure               │
│ • High visual similarity                     │
└──────────────────────────────────────────────┘
```

---

# 24. Mapping to the Problem Statement

| Requirement                    | Proposed Solution                                  |
| ------------------------------ | -------------------------------------------------- |
| Detect phishing domains        | Machine-learning classifier                        |
| Newly registered domains       | WHOIS/RDAP/domain-age features                     |
| Open-source domain information | Public domain registration data                    |
| Backend/code similarity        | HTML and content similarity                        |
| Webpage image analysis         | Screenshot and visual similarity                   |
| Probability score              | ML prediction probability                          |
| Detect new phishing domains    | Feature-based inference on unseen domains          |
| Reasonable detection time      | Lightweight feature extraction + pretrained models |
| Ease of use                    | Web dashboard                                      |
| Flexible output                | JSON API + dashboard                               |

---

# 25. Design Philosophy

The project is based on four principles:

### 1. Multi-signal detection

No single feature should determine whether a website is malicious.

```text
Domain
+
Registration
+
HTML
+
Visual
+
URL
        ↓
Combined Decision
```

### 2. Similarity-based reasoning

Phishing websites often succeed by impersonating something that already exists.

Therefore, comparing suspicious websites against known legitimate websites is central to the system.

### 3. Explainability

The system should show the factors contributing to the risk score rather than returning an unexplained prediction.

### 4. Lightweight implementation

The goal is to demonstrate the complete intelligent detection pipeline without building a massive internet-wide cybersecurity infrastructure.

---

# 26. Core Pipeline

The complete project can ultimately be summarized as:

```text
                  NEW DOMAIN
                       |
                       v
              DOMAIN ANALYSIS
                       |
        +--------------+--------------+
        |              |              |
       URL           WHOIS         BRAND
     Features        Data        Similarity
        |              |              |
        +--------------+--------------+
                       |
                       v
                 WEBSITE CRAWLER
                       |
              +--------+--------+
              |                 |
              v                 v
             HTML          SCREENSHOT
              |                 |
              v                 v
       HTML Similarity    Visual Similarity
              |                 |
              +--------+--------+
                       |
                       v
                FEATURE VECTOR
                       |
                       v
                ML CLASSIFIER
                       |
                       v
             PHISHING PROBABILITY
                       |
                       v
                RISK EXPLANATION
                       |
                       v
                  DASHBOARD
```

---

# 27. Final Objective

The final system should allow a user to provide a newly registered or suspicious domain and receive an intelligent assessment:

```text
Domain
     ↓
Who/what does it resemble?
     ↓
How similar is the domain?
     ↓
How similar is the HTML?
     ↓
How similar is the webpage visually?
     ↓
How recently was it registered?
     ↓
What does the ML model predict?
     ↓
What is the phishing probability?
```

The core output is therefore not simply:

```text
Phishing / Not Phishing
```

but:

```text
┌───────────────────────────────┐
│       PHISHING ANALYSIS       │
├───────────────────────────────┤
│ Domain: suspicious-domain.com  │
│                               │
│ Target: example.com            │
│                               │
│ Phishing Probability: 91%     │
│ Risk: HIGH                    │
│                               │
│ Domain Similarity: 89%        │
│ HTML Similarity: 84%          │
│ Visual Similarity: 93%        │
│ Domain Age: 4 days            │
└───────────────────────────────┘
```

This provides an interpretable, multi-layered approach to detecting phishing domains that attempt to imitate legitimate websites.
