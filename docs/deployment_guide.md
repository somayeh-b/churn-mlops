# Deployment guide — Render

Render offers a free tier that works well for a course project. This walks
through connecting this repo so GitHub Actions can auto-deploy on every push.

## 1. Push this repo to GitHub
```bash
git remote add origin https://github.com/<your-username>/churn-mlops.git
git branch -M main
git push -u origin main
```

## 2. Create the Render Web Service
1. Go to https://dashboard.render.com and sign up / log in (free, no credit card
   required for the free tier).
2. Click **New +** → **Web Service**.
3. Connect your GitHub account and select the `churn-mlops` repo.
4. Configure:
   - **Environment:** Docker
   - **Region:** closest to you
   - **Instance type:** Free
   - Render will auto-detect the `Dockerfile` at the repo root.
5. Click **Create Web Service**. Render builds and deploys once manually —
   this gives you your public URL, e.g. `https://churn-mlops-api.onrender.com`.

## 3. Get the deploy hook URL (for GitHub Actions auto-deploy)
1. In the Render dashboard, open your service → **Settings** → **Deploy Hook**.
2. Copy the URL (looks like `https://api.render.com/deploy/srv-xxxxxxxx?key=yyyy`).

## 4. Add secrets to GitHub Actions
In your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**.
Add:
| Secret name | Value |
|---|---|
| `RENDER_DEPLOY_HOOK_URL` | the deploy hook URL from step 3 |
| `DOCKERHUB_USERNAME` | your Docker Hub username (if using the build-and-push job) |
| `DOCKERHUB_TOKEN` | a Docker Hub access token (Account Settings → Security → New Access Token) |

## 5. Push to main
```bash
git add .
git commit -m "Phase 2: FastAPI + Docker + CI/CD + monitoring"
git push
```
GitHub Actions will lint, test, build the Docker image, push it, and hit the
Render deploy hook automatically. Watch progress under the **Actions** tab.

## 6. Verify
```bash
curl https://<your-app>.onrender.com/health
```
You should see `{"status":"ok","model_loaded":true}`.

**Note on the free tier:** Render's free web services spin down after 15
minutes of inactivity and take ~30–60 seconds to wake up on the next request
— mention this if your live demo's first request is slow.

## How the retraining → redeploy loop actually works
The `monitor-and-retrain` job runs on a daily schedule (06:00 UTC) or manually
via `workflow_dispatch`. If EvidentlyAI flags drift:
1. `monitoring/retrain.py` re-runs the DVC pipeline and overwrites `models/model.pkl`
   (a DVC-tracked, not git-tracked, artifact — see the README's "Data & model
   versioning" section).
2. The job commits `dvc.lock` and the updated report files **directly to
   `main`** (no `[skip ci]` — this is intentional, so the push flows into
   the jobs below). The model file itself isn't committed to git; it's
   DVC-tracked.
3. A separate `redeploy-after-retrain` job (gated on
   `needs.monitor-and-retrain.outputs.retrained == 'true'`) regenerates the
   data and model (`python src/generate_dataset.py && dvc repro`), rebuilds
   the Docker image with it, and hits the Render deploy hook again.

This means a drift-triggered retrain reaches production automatically,
without needing a human to manually rebuild or redeploy. If no drift is
detected, `retrain.py` exits early and neither the commit nor the redeploy
job runs.

## Using a real cloud DVC remote instead of the local one

This project ships with a **local** DVC remote (`../dvc-storage`, a sibling
folder to the repo) so it's fully reproducible without any cloud account.
If you want proper multi-machine DVC storage (e.g. so GitHub Actions could
`dvc pull` instead of regenerating data from scratch), swap in a real
remote — for example a free [DagsHub](https://dagshub.com) repo or a Google
Drive folder:

```bash
dvc remote add -d storage gdrive://<your-folder-id>
# or: dvc remote add -d storage https://dagshub.com/<user>/<repo>.dvc
dvc push
```

Then add the resulting credentials as GitHub Actions secrets and add a
`dvc pull` step (authenticated via those secrets) in place of the
`generate_dataset.py && dvc repro` steps in `.github/workflows/ci-cd.yml`.
This project intentionally avoids requiring that setup, since it assumes no
cloud storage account is available.
