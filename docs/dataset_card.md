# Dataset Card — Synthetic Customer Churn Dataset

## Summary
`data/raw/churn.csv` is a **synthetically generated** dataset produced by
`src/generate_dataset.py`. It is designed to mimic the schema, size, and
statistical patterns of the well-known public **IBM/Kaggle "Telco Customer
Churn"** dataset, but the rows themselves are simulated — not scraped or
copied from any real dataset.

**Why synthetic:** this project was built in an environment without direct
internet access to Kaggle. If your instructor requires a real external
dataset, download the actual Telco Customer Churn CSV and drop it into
`data/raw/churn.csv` — the column names and pipeline code are unchanged, so
`dvc repro` will work identically on the real file.

## Source & generation method
- Script: `src/generate_dataset.py`, seeded (`np.random.seed(42)`) for
  reproducibility.
- Size: 7,043 rows × 21 columns (matches the real dataset's dimensions).
- Categorical features drawn from realistic marginal probabilities (e.g.
  ~55% month-to-month contracts, ~44% fiber optic internet).
- The `Churn` label is not random: it is generated from a logistic function
  of contract type, tenure, internet service, tech support, payment method,
  and monthly charges — the same drivers documented in telecom churn
  literature — so the resulting dataset has real, learnable signal for the
  pipeline to model, rather than being pure noise.

## Schema
| Column | Type | Description |
|---|---|---|
| customerID | string | Synthetic unique identifier |
| gender | categorical | Male / Female |
| SeniorCitizen | binary | 0 / 1 |
| Partner, Dependents | categorical | Yes / No |
| tenure | numeric | Months with the company (0–72) |
| PhoneService, MultipleLines | categorical | Phone service usage |
| InternetService | categorical | DSL / Fiber optic / No |
| OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies | categorical | Add-on services (conditioned on InternetService) |
| Contract | categorical | Month-to-month / One year / Two year |
| PaperlessBilling | categorical | Yes / No |
| PaymentMethod | categorical | 4 payment methods |
| MonthlyCharges, TotalCharges | numeric | Billing amounts (USD) |
| Churn | categorical (target) | Yes / No |

## Quality notes
- **Missing values:** in the real IBM/Kaggle dataset, exactly one column —
  `TotalCharges` — contains missing/blank values (11 rows, stored as an
  empty string because a few brand-new customers have 0 tenure). This
  generator does not inject any missing values, so `data/raw/churn.csv`
  currently has none. `src/prepare.py` still runs median imputation on
  `TotalCharges` defensively, so the pipeline behaves identically if you
  swap in the real CSV (which does have those 11 missing rows). No other
  column has missing values in either version.
- **Feature count:** the raw file is **7,043 rows × 21 columns**
  (`customerID` + 19 predictive features + the `Churn` label). After
  `src/prepare.py` drops `customerID` and separates out the `Churn` target,
  the model is trained on exactly **19 features** — this is the number
  referenced everywhere else in the project (MLflow runs, the FastAPI
  schema, and the drift monitoring report).
- Class balance: ~38.7% churn — comparable to the real dataset's ~26.5%,
  intentionally kept a bit higher to give the classifier more positive
  examples to learn from in a small course-project setting.
- **Known limitation:** because the label is generated from a fixed formula
  over a subset of features, the model can achieve a higher apparent ROC-AUC
  than it would on real, noisier customer behavior. Treat all reported
  metrics as demonstrating the *pipeline*, not as claims about real-world
  churn-prediction accuracy.
- **Categorical encoding limitation:** `src/prepare.py` uses label encoding
  (integer codes) for all categorical columns so a single encoder scheme
  works for every model in the registry. This is harmless for the
  tree-based models (Random Forest, Gradient Boosting), which split on
  thresholds rather than assuming order. For the Logistic Regression
  baseline, however, label encoding implicitly assumes a numeric ordering
  between categories (e.g. `Contract` values) that doesn't actually exist —
  a one-hot encoding would be the methodologically correct choice for a
  linear model. This is a deliberate simplification for this course
  project (one shared preprocessing path for all three models) and is
  flagged here rather than hidden.

## License / provenance
Fully synthetic — no license or attribution required. Structure inspired by
the publicly available Telco Customer Churn dataset (commonly distributed
under an open license on Kaggle/IBM's sample data repository).
