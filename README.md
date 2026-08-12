# Customer Churn Prediction — MLOps Project

MAI201NAA.06381.2264 — full MLOps lifecycle for a customer-churn classifier:
data versioning, experiment tracking, pipeline automation, containerized
serving, CI/CD, and drift monitoring with automated retraining.

> **Note on the dataset:** `data/raw/churn.csv` is a synthetic dataset that
> mimics the structure of the public IBM/Kaggle "Telco Customer Churn"
> dataset. See [`docs/dataset_card.md`](docs/dataset_card.md) for details and
> for instructions on swapping in the real dataset.

## Data & model versioning (DVC)

`data/raw/churn.csv`, `data/processed/*.csv`, and `models/*.pkl` are **DVC-
tracked, not git-tracked**. Git only stores the small `.dvc` pointer files
(e.g. `data/raw/churn.csv.dvc`) and `dvc.lock`; the actual bytes live in a
local DVC remote at `../dvc-storage` (a sibling folder to this repo, included
in the delivered zip) so the project is reproducible without needing a cloud
storage account.

```bash
dvc pull      # fetch data/raw/churn.csv, processed splits, and the model
              # from ../dvc-storage into your working copy
```

If `../dvc-storage` isn't next to your clone (e.g. you only pushed the repo
to GitHub, not the storage folder), regenerate everything instead — the
dataset generator is deterministic:

```bash
python src/generate_dataset.py
dvc repro
```

This is also exactly what CI does (see `.github/workflows/ci-cd.yml`): it
never assumes the local remote is reachable, so every job regenerates the
data and model from scratch before running tests or building the Docker
image.

## Project structure
```
churn-mlops/
├── data/
│   ├── raw/churn.csv.dvc          # DVC pointer (actual .csv is DVC-tracked)
│   └── processed/                 # DVC-generated train/test splits (not in git)
├── src/                            # training/serving pipeline
│   ├── generate_dataset.py        # synthetic data generator
│   ├── prepare.py                 # DVC stage 1: clean, encode, split
│   ├── train.py                   # DVC stage 2: train + MLflow logging
│   ├── evaluate.py                # DVC stage 3: metrics + drift reference
│   └── app.py                     # FastAPI serving app
├── monitoring/                     # production monitoring, separate from the training pipeline
│   ├── simulate_production_traffic.py
│   ├── monitor.py                 # EvidentlyAI drift detection
│   └── retrain.py                 # retraining trigger
├── models/                        # trained model + encoders (DVC-tracked, not in git)
├── reports/                       # metrics, drift reports, MLflow comparison
├── docs/
│   ├── architecture.png           # system architecture diagram
│   ├── model_card.md
│   ├── dataset_card.md
│   ├── Project_Proposal.pdf       # Phase 0 deliverable
│   └── Phase2_Presentation.pptx   # Phase 2 deliverable
├── tests/
│   ├── test_api.py                # pytest suite for the FastAPI layer
│   └── test_pipeline.py           # pytest suite for prepare.py / train.py logic
├── .github/workflows/ci-cd.yml    # CI/CD pipeline
├── dvc.yaml / params.yaml / dvc.lock   # DVC pipeline definition
├── Dockerfile
└── requirements.txt
```

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run the ML pipeline (Phase 1)
```bash
dvc pull                             # fetch raw data from ../dvc-storage, if present
# — or, if you don't have ../dvc-storage —
python src/generate_dataset.py       # deterministically regenerate the raw CSV
dvc repro                            # runs prepare -> train -> evaluate
```
Change which model trains by editing `params.yaml` (`train.model`:
`logistic_regression` | `random_forest` | `gradient_boosting`) and re-running
`dvc repro` — each run is logged as a new MLflow experiment. All
hyperparameters and the random seed live in `params.yaml`; nothing in
`src/` hard-codes them.

Inspect experiments:
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

## Run the API locally (Phase 2)
```bash
uvicorn src.app:app --reload --port 8000
# then open http://localhost:8000/docs for interactive Swagger UI
```

## Run with Docker
```bash
# models/model.pkl must exist first (see "Run the ML pipeline" above) —
# Docker COPYs it in rather than training inside the image.
docker build -t churn-mlops-api .
docker run -p 8000:8000 churn-mlops-api
```

## Run tests & linting
```bash
python -m pytest tests/ -v
python -m flake8 src/ tests/ monitoring/
```
`tests/test_pipeline.py` unit-tests the pure data-transformation and
model-building functions in `prepare.py`/`train.py` directly (no files or
MLflow needed); `tests/test_api.py` exercises the FastAPI layer end to end
and needs `models/model.pkl` / `models/label_encoders.pkl` to exist first.

## Drift monitoring
```bash
python monitoring/simulate_production_traffic.py   # or point at real logged traffic
python monitoring/monitor.py                       # writes reports/drift_report.html
python monitoring/retrain.py                       # retrains if drift was flagged
```

## Deployment (Render)
See [`docs/deployment_guide.md`](docs/deployment_guide.md) for the full
step-by-step walkthrough of connecting this repo to Render and wiring up the
GitHub Actions secrets needed for automatic deploys.

## Deliverables checklist
- [x] Phase 0: `docs/Project_Proposal.pdf`
- [x] Phase 1: `docs/architecture.png`, `dvc.yaml`, MLflow experiments (baseline + 2)
- [x] Phase 2: FastAPI + Dockerfile, `.github/workflows/ci-cd.yml`, drift monitoring, `docs/model_card.md`, `docs/Phase2_Presentation.pptx`

