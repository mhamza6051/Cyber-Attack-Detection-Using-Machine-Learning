# Cyber Attack Detection Using Machine Learning — Network Intrusion Detection on CICIDS2017

A network intrusion-detection system trained on the **CICIDS2017** dataset (Canadian Institute for Cybersecurity): **2.83 million network flows** cleaned and engineered down to 38 features, with the severe class imbalance handled explicitly — because the first model looked perfect and wasn't.

> **The honest headline:** a Random Forest on the raw data scored **99.85% accuracy but only 0.84 macro F1** — it was ignoring rare attack types. After undersampling to a balanced 12-class dataset, the tuned XGBoost reaches **94.4% accuracy with 0.94 macro F1**: slightly lower accuracy, far more trustworthy detection. That model powers the Streamlit app.

## Results

**Final balanced evaluation** (7,824 flows, 12 classes × 652)

| Model | Accuracy | Macro F1 |
|---|---|---|
| **XGBoost (tuned) — deployed** | **0.9438** | **0.94** |
| Random Forest (tuned) | 0.9419 | 0.94 |
| Random Forest | 0.9393 | 0.94 |
| XGBoost | 0.9278 | 0.93 |

**Before balancing** (full imbalanced data, 50,000-flow test): accuracy 0.9985, **macro F1 0.84** — rare classes effectively undetected.

Full numbers: [docs/RESULTS.md](docs/RESULTS.md)

## Pipeline

1. **Merge & clean** — all 8 CICIDS2017 day files combined (2,830,743 rows × 79 columns); infinities → NaN, missing values and **307,078 duplicate rows** removed → 2,520,798 clean flows
2. **Feature reduction** — constant features removed (79 → 71), then features correlated > 0.9 removed → **38 features**
3. **The imbalance problem** — BENIGN traffic dominates; several attack classes have only a handful of flows. Extremely small classes were removed and the rest balanced by random undersampling → **7,824 flows, 12 classes × 652**
4. **Modelling** — Random Forest vs. XGBoost, then RandomizedSearchCV tuning of both; tuned XGBoost won and is the deployed model
5. **App** — Streamlit "AI Network Security Threat Detection": enter flow features → BENIGN/attack verdict with class-specific mitigation guidance

## Detected classes (12)

BENIGN · DDoS · PortScan · Bot · FTP-Patator · SSH-Patator · DoS Hulk · DoS GoldenEye · DoS slowloris · DoS Slowhttptest · Web Attack – Brute Force · Web Attack – XSS

## Run the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Repository structure

```
app.py                         Streamlit threat-detection app
notebooks/                     Full pipeline: cleaning → feature reduction → balancing → tuning
models/                        Tuned XGBoost model, scaler, label encoder, feature columns
data/README.md                 Dataset source & download instructions (data not stored in Git)
docs/RESULTS.md                Complete verified metrics
```

## Dataset

CICIDS2017 is a public benchmark from the Canadian Institute for Cybersecurity (University of New Brunswick). The raw CSVs total ~885 MB and several files exceed GitHub's 100 MB per-file limit, so they are **not stored in this repository** — see `data/README.md` for the official download and the expected folder layout.

## Limitations

- Balancing by undersampling discards most BENIGN flows and drops the rarest attack classes entirely (e.g. Heartbleed, SQL Injection) — the honest trade-off of a 652-per-class cap, documented in the notebook.
- Benchmark performance on CICIDS2017 does not equal performance on live enterprise traffic.

## Author

**Muhammad Hamza** — Data Scientist · [GitHub @mhamza6051](https://github.com/mhamza6051)
