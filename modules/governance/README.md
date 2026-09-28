# 🏛️ Bharat360 — Governance, Finance & Mobility Module (Member 4)

Part of the **Bharat360** unified citizen services platform.

---

## 📌 Module Overview

The **Governance, Finance & Mobility** module provides Indian citizens with a centralized, transparent platform to:
1. **Discover Public Welfare Schemes:** Central & state government schemes with rule-based matching based on age, occupation, and preferences.
2. **Access Financial Inclusion Awareness:** Educational resources on zero-balance banking (BSBDA/PMJDY), financial literacy, UPI digital payment safety, Mudra microcredit, and micro-insurance (PMSBY/PMJJBY).
3. **Explore Municipal Transit & Mobility:** State & city-level transit networks (city bus routes, regional rail lines) with an interactive geographic hub visualizer.
4. **Personalized Recommendations:** Transparent, explainable rule-based recommendation engine showing exact matching rationale for every suggestion.
5. **Real-time Analytics:** Interactive Plotly charts dynamically reflecting actual dataset distribution across welfare sectors, financial focus areas, and urban transit modes.

---

## 🛠️ Code Structure

```
modules/
└── governance/
    ├── __init__.py          # Exposes render_governance_module() and utility loaders
    ├── governance.py        # Streamlit UI, visual layout, Hero, Profile, and Tab views
    ├── data_loader.py       # Safe, dynamic data loader with multi-path resolution and caching
    ├── recommender.py       # Explainable rule-based matching engine
    └── README.md            # Module documentation & integration guide
```

---

## 🚀 Integration Guide for Unified Bharat360 `app.py`

Any teammate or team lead can integrate this module with two simple lines:

```python
import streamlit as st
from modules.governance import render_governance_module

# Inside your main app or navigation dispatcher:
render_governance_module()
```

---

## 🧪 Testing

Run the automated test suite:

```bash
python -m unittest tests/test_governance.py
```

Run standalone Streamlit preview:

```bash
streamlit run modules/governance/governance.py
```

---

## 🛡️ Safety & Compliance Disclaimers

1. **Government Schemes:** Informational prototype only. Eligibility must always be verified through official nodal government portals (`india.gov.in`, `pmkisan.gov.in`, etc.).
2. **Financial Literacy:** Strictly educational awareness. Does not provide personalized financial, legal, or investment advice.
