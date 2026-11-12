# Full Results — Cyber Attack Detection (CICIDS2017)

All figures are taken verbatim from the project notebook outputs.

## Data processing ledger

| Step | Shape |
|---|---|
| 8 day files merged | 2,830,743 × 79 |
| After cleaning (inf→NaN, dropna, **307,078 duplicates removed**) | 2,520,798 × 79 |
| Constant features removed | 2,520,798 × 71 |
| Correlated features (> 0.9) removed | 2,520,798 × 39 (38 features + label) |

Per-file sizes: Monday 529,918 · Tuesday 445,909 · Wednesday 692,703 · Thursday AM 170,366 · Thursday PM 288,602 · Friday AM 191,033 · Friday DDoS 225,745 · Friday PortScan 286,467.

## Experiment 1 — imbalanced data (the misleading model)

Random Forest, 50,000-flow test set from the raw distribution:

- **Accuracy 0.9985** — but **macro avg F1 = 0.84** (weighted F1 1.00)
- Precision ill-defined warnings for rare classes: the model barely predicts them at all

Conclusion recorded in the notebook: accuracy is the wrong metric here; balancing is required.

## Experiment 2 — balanced data (7,824 flows, 12 classes × 652)

| Model | Accuracy | Macro P / R / F1 |
|---|---|---|
| Random Forest | 0.9393 | 0.94 / 0.94 / 0.94 |
| XGBoost | 0.9278 | 0.93 / 0.93 / 0.93 |
| Random Forest (tuned) | 0.9419 | 0.94 / 0.94 / 0.94 |
| **XGBoost (tuned) — deployed** | **0.9438** | **0.95 / 0.94 / 0.94** |

- Tuned RF best params: `n_estimators=200, max_depth=30, max_features='log2', min_samples_split=2, min_samples_leaf=1`; best CV score 0.9316 (RandomizedSearchCV, 20 candidates × 3 folds)
- Tuned XGBoost best params: `n_estimators=100, max_depth=4, learning_rate=0.1, subsample=1.0, colsample_bytree=1.0`
- Notebook note: *"Initial experiments showed Random Forest outperforming XGBoost. However, after hyperparameter tuning, XGBoost achieved superior performance."*

## Final balanced class distribution (652 each)

BENIGN, DDoS, PortScan, Bot, FTP-Patator, SSH-Patator, DoS Hulk, DoS GoldenEye, DoS slowloris, DoS Slowhttptest, Web Attack – Brute Force, Web Attack – XSS.
