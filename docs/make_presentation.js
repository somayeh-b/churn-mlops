const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.author = "Customer Churn Prediction — MLOps Project";
pres.company = "MAI201NAA.06381.2264";

// ---------- Design tokens ----------
const NAVY = "16241F";
const TEAL = "0F6E56";
const TEAL_DARK = "0A4F3E";
const TEAL_DEEP = "072F26";
const CORAL = "D2572B";
const GOLD = "C08A28";
const WHITE = "FFFFFF";
const GRAY_DARK = "26312C";
const GRAY_MED = "5C6660";
const GRAY_SOFT = "8B948E";
const BG_TEAL_TINT = "E7F5EF";
const BG_GOLD_TINT = "FBF1DD";
const BG_CORAL_TINT = "FBEAE2";
const BG_PAPER = "FAFAF7";

const PAGE_W = 13.33;
const PAGE_H = 7.5;
const MARGIN = 0.75;

let pageCounter = 0;

function footer(slide, sectionLabel) {
  pageCounter += 1;
  slide.addShape(pres.ShapeType.line, {
    x: MARGIN, y: 7.08, w: PAGE_W - MARGIN * 2, h: 0,
    line: { color: "DEDCD3", width: 0.75 },
  });
  slide.addText(sectionLabel || "Customer Churn Prediction", {
    x: MARGIN, y: 7.14, w: 7, h: 0.3, fontSize: 9.5, color: GRAY_SOFT, fontFace: "Arial",
  });
  slide.addText("MAI201NAA.06381.2264", {
    x: PAGE_W - MARGIN - 3.2, y: 7.14, w: 2.4, h: 0.3, fontSize: 9.5, color: GRAY_SOFT, fontFace: "Arial", align: "right",
  });
  slide.addText(String(pageCounter), {
    x: PAGE_W - MARGIN - 0.6, y: 7.14, w: 0.6, h: 0.3, fontSize: 9.5, color: GRAY_SOFT, fontFace: "Arial", align: "right",
  });
}

function sectionHeader(kicker, title) {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 0.18, h: PAGE_H, fill: { color: TEAL } });
  s.addText(kicker.toUpperCase(), {
    x: MARGIN, y: 0.5, w: 8, h: 0.35, fontSize: 12, color: GOLD, fontFace: "Arial", charSpacing: 2, bold: true,
  });
  s.addText(title, { x: MARGIN, y: 0.82, w: 11.0, h: 0.75, fontSize: 28, color: NAVY, fontFace: "Arial" });
  s.addShape(pres.ShapeType.rect, { x: MARGIN, y: 1.58, w: 1.5, h: 0.045, fill: { color: TEAL } });
  return s;
}

function bulletList(slide, items, opts) {
  const o = Object.assign({ x: MARGIN, y: 1.95, w: 5.6, h: 4.3, fontSize: 15 }, opts || {});
  const arr = items.map((t, i) => ({
    text: t,
    options: {
      bullet: { code: "2022", color: TEAL },
      breakLine: i < items.length - 1,
      color: GRAY_DARK,
      fontSize: o.fontSize,
      paraSpaceAfter: o.paraSpaceAfter !== undefined ? o.paraSpaceAfter : 11,
    },
  }));
  slide.addText(arr, { x: o.x, y: o.y, w: o.w, h: o.h, fontFace: "Arial", valign: "top", lineSpacingMultiple: 1.08 });
}

function statCard(slide, x, y, w, h, value, label, opts) {
  const o = Object.assign({ bg: BG_TEAL_TINT, valColor: TEAL }, opts || {});
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.1, fill: { color: o.bg }, line: { color: o.bg } });
  slide.addText(value, { x: x + 0.25, y: y + 0.18, w: w - 0.5, h: h * 0.55, fontSize: 30, color: o.valColor, fontFace: "Arial", bold: true });
  slide.addText(label, { x: x + 0.25, y: y + h * 0.62, w: w - 0.5, h: h * 0.35, fontSize: 12, color: GRAY_MED, fontFace: "Arial" });
}

// =====================================================================
// 1. TITLE SLIDE
// =====================================================================
(function titleSlide() {
  const s = pres.addSlide();
  s.background = { color: TEAL_DEEP };
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: PAGE_W, h: PAGE_H, fill: { color: TEAL_DEEP } });
  s.addShape(pres.ShapeType.rect, { x: -2, y: 4.6, w: 18, h: 5, fill: { color: TEAL_DARK }, rotate: -6 });
  s.addShape(pres.ShapeType.rect, { x: -2, y: 5.7, w: 18, h: 3, fill: { color: TEAL }, rotate: -6 });
  s.addShape(pres.ShapeType.ellipse, { x: 10.6, y: -1.4, w: 4.2, h: 4.2, fill: { color: "0D5C48" }, line: { color: "0D5C48" } });
  s.addShape(pres.ShapeType.ellipse, { x: 11.6, y: -0.6, w: 2.0, h: 2.0, fill: { color: GOLD }, line: { color: GOLD } });

  s.addText("MLOPS FINAL PROJECT  \u00b7  PHASE 2", {
    x: 0.9, y: 1.5, w: 9, h: 0.4, fontSize: 13, color: "9FE1CB", fontFace: "Arial", charSpacing: 3, bold: true,
  });
  s.addText("Customer Churn\nPrediction", {
    x: 0.85, y: 2.0, w: 10.5, h: 1.9, fontSize: 46, color: WHITE, fontFace: "Arial", lineSpacingMultiple: 1.02,
  });
  s.addText("An end-to-end MLOps pipeline \u2014 from raw data to a deployed,\nmonitored, self-retraining model in production.", {
    x: 0.9, y: 4.0, w: 9.2, h: 0.8, fontSize: 16, color: "CFF0E3", fontFace: "Arial", lineSpacingMultiple: 1.15,
  });

  s.addShape(pres.ShapeType.line, { x: 0.9, y: 6.35, w: 2.0, h: 0, line: { color: GOLD, width: 2 } });
  s.addText("MAI201NAA.06381.2264", { x: 0.9, y: 6.5, w: 6, h: 0.35, fontSize: 12.5, color: "BFE7D9", fontFace: "Arial" });
  s.addText("Final presentation  \u00b7  Solo submission  \u00b7  August 2026", { x: 0.9, y: 6.82, w: 8, h: 0.35, fontSize: 11.5, color: "8FCDB8", fontFace: "Arial" });
})();

// =====================================================================
// 2. AGENDA
// =====================================================================
(function agenda() {
  const s = sectionHeader("Overview", "What we'll cover");
  const items = [
    ["01", "Problem & objective", "Why churn prediction, and what the course project demonstrates"],
    ["02", "Dataset", "Synthetic data, schema, and why it was generated this way"],
    ["03", "System architecture", "How every MLOps component connects end to end"],
    ["04", "Experiment tracking", "Baseline vs. two experiments in MLflow, and model selection"],
    ["05", "Serving, CI/CD & monitoring", "FastAPI, Docker, GitHub Actions, and drift-triggered retraining"],
    ["06", "Model card, limitations & demo", "Honest assessment, and the live system"],
  ];
  const colW = 5.85, gap = 0.3, rowH = 1.55;
  items.forEach((it, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = MARGIN + col * (colW + gap);
    const y = 1.95 + row * (rowH + 0.18);
    s.addShape(pres.ShapeType.roundRect, { x, y, w: colW, h: rowH, rectRadius: 0.08, fill: { color: row % 2 === 0 ? BG_TEAL_TINT : BG_GOLD_TINT }, line: { color: row % 2 === 0 ? BG_TEAL_TINT : BG_GOLD_TINT } });
    s.addText(it[0], { x: x + 0.2, y: y + 0.15, w: 1.0, h: 0.6, fontSize: 26, color: row % 2 === 0 ? TEAL : GOLD, fontFace: "Arial", bold: true });
    s.addText(it[1], { x: x + 1.15, y: y + 0.16, w: colW - 1.35, h: 0.45, fontSize: 15.5, color: NAVY, fontFace: "Arial", bold: true });
    s.addText(it[2], { x: x + 1.15, y: y + 0.62, w: colW - 1.35, h: 0.8, fontSize: 11.5, color: GRAY_MED, fontFace: "Arial", lineSpacingMultiple: 1.1 });
  });
  footer(s, "Overview");
})();

// =====================================================================
// 3. PROBLEM & OBJECTIVE
// =====================================================================
(function problem() {
  const s = sectionHeader("The business problem", "Problem & objective");
  bulletList(s, [
    "Telecom companies lose recurring revenue every time a customer churns \u2014 retention teams need to know who is at risk before they leave, not after.",
    "Objective: predict each customer's churn probability from account, billing, and service-usage data so retention efforts can be prioritized.",
    "Course objective: build the full MLOps lifecycle around this model \u2014 data versioning, experiment tracking, containerized serving, CI/CD, and automated drift monitoring \u2014 not just a notebook that trains once.",
  ], { w: 6.9, y: 2.05, h: 4.4, fontSize: 14.5, paraSpaceAfter: 16 });

  statCard(s, 8.2, 2.05, 4.3, 1.55, "38.7%", "baseline churn rate in the training data", { bg: BG_TEAL_TINT, valColor: TEAL });
  statCard(s, 8.2, 3.8, 4.3, 1.55, "7,043", "customer records used to train and evaluate the model", { bg: BG_GOLD_TINT, valColor: GOLD });
  statCard(s, 8.2, 5.55, 4.3, 1.15, "3 phases", "team formation -> pipeline -> deployment & monitoring", { bg: BG_CORAL_TINT, valColor: CORAL });
  footer(s, "Problem & objective");
})();

// =====================================================================
// 4. DATASET
// =====================================================================
(function dataset() {
  const s = sectionHeader("Data foundation", "Dataset");
  bulletList(s, [
    "Synthetic dataset mimicking IBM/Kaggle \"Telco Customer Churn\" \u2014 generated because this build environment has no direct internet access to Kaggle. Same schema, same size (7,043 rows x 21 columns).",
    "21 columns = customerID + 19 predictive features + the Churn label. After dropping the ID and separating the label, the model trains on exactly 19 features \u2014 the number referenced everywhere else in this project (MLflow, the API schema, drift monitoring).",
    "The Churn label is not random noise: it's generated from a logistic function over realistic churn drivers (contract type, tenure, internet service, tech support, payment method, monthly charges), so the pipeline has genuine signal to learn.",
    "80/20 stratified train/test split. Label encoding for categoricals (documented ordinal-assumption limitation for the Logistic Regression baseline). Median imputation on TotalCharges \u2014 the one column with missing values in the real dataset (11 rows); this synthetic version has none, but the step runs regardless for compatibility.",
  ], { w: 11.6, y: 1.95, h: 4.6, fontSize: 14, paraSpaceAfter: 14 });
  footer(s, "Dataset");
})();

// =====================================================================
// 5. SYSTEM ARCHITECTURE
// =====================================================================
(function architecture() {
  const s = sectionHeader("How it all connects", "System architecture");
  s.addShape(pres.ShapeType.roundRect, { x: 0.75, y: 1.95, w: 3.3, h: 4.6, rectRadius: 0.08, fill: { color: BG_PAPER }, line: { color: "EAE8DF" } });
  const flow = ["Data (DVC)", "Pipeline (prepare/train/evaluate)", "MLflow tracking", "FastAPI + Docker", "CI/CD", "Cloud (Render)", "Drift monitoring", "Retrain -> auto-redeploy"];
  let fy = 2.15;
  flow.forEach((step, i) => {
    s.addShape(pres.ShapeType.ellipse, { x: 0.98, y: fy, w: 0.14, h: 0.14, fill: { color: TEAL }, line: { color: TEAL } });
    s.addText(step, { x: 1.25, y: fy - 0.1, w: 2.65, h: 0.35, fontSize: 11, color: GRAY_DARK, fontFace: "Arial" });
    if (i < flow.length - 1) {
      s.addShape(pres.ShapeType.line, { x: 1.04, y: fy + 0.14, w: 0, h: 0.36, line: { color: "CFE4DB", width: 1 } });
    }
    fy += 0.56;
  });
  const diagH = 5.15, diagW = diagH * (657 / 1256);
  const diagX = 4.3 + (8.3 - diagW) / 2;
  s.addImage({ path: "docs/architecture.png", x: diagX, y: 1.75, h: diagH, w: diagW });
  footer(s, "System architecture");
})();

// =====================================================================
// 6. EXPERIMENT TRACKING
// =====================================================================
(function experiments() {
  const s = sectionHeader("Model selection", "Experiment tracking (MLflow)");
  s.addImage({ path: "reports/mlflow_experiment_comparison.png", x: 0.55, y: 1.75, w: 12.25, h: 12.25 * (699 / 2839) });
  s.addShape(pres.ShapeType.roundRect, { x: 0.75, y: 4.55, w: 11.85, h: 0.55, rectRadius: 0.08, fill: { color: BG_TEAL_TINT }, line: { color: BG_TEAL_TINT } });
  s.addText([
    { text: "Selected: ", options: { color: GRAY_DARK } },
    { text: "Gradient Boosting  (n_estimators=150, learning_rate=0.05, max_depth=3) \u2014 highest ROC-AUC (0.838)", options: { color: TEAL, bold: true } },
  ], { x: 0.95, y: 4.62, w: 11.5, h: 0.42, fontSize: 14, fontFace: "Arial", valign: "middle" });
  bulletList(s, [
    "All 5 metrics computed at decision threshold = 0.5. ROC-AUC (threshold-independent) is the model-selection metric because the retention team ranks customers by risk rather than acting on a fixed cutoff.",
    "Recall is tracked alongside precision because missing an actual churner (false negative) costs more than one unnecessary retention call (false positive) \u2014 a production system could lower the threshold below 0.5 to trade precision for recall without changing which model wins on ROC-AUC.",
  ], { w: 11.6, y: 5.3, h: 1.6, fontSize: 12.5, paraSpaceAfter: 8 });
  footer(s, "Experiment tracking");
})();

// =====================================================================
// 7. SERVING & DEPLOYMENT
// =====================================================================
(function serving() {
  const s = sectionHeader("From model to endpoint", "Serving & deployment");
  bulletList(s, [
    "Model served through a FastAPI app exposing /predict, /health, and /model-info.",
    "A Pydantic model validates the full request against all 19 required fields (types, allowed categories, numeric ranges) before prediction \u2014 the JSON shown here is truncated for slide space, not what the API actually accepts.",
    "Packaged into a Docker image (python:3.11-slim base, health-checked).",
    "Deployed to Render, triggered automatically by GitHub Actions on every push to main.",
    "5 automated pytest tests cover valid predictions, input validation, and health checks.",
  ], { w: 6.55, y: 1.95, h: 4.7, fontSize: 13.5, paraSpaceAfter: 13 });

  s.addShape(pres.ShapeType.roundRect, { x: 7.75, y: 1.95, w: 4.85, h: 4.9, rectRadius: 0.1, fill: { color: NAVY }, line: { color: NAVY } });
  s.addText("POST /predict   (all 19 fields required)", { x: 8.0, y: 2.1, w: 4.4, h: 0.35, fontSize: 11.5, color: "8FE0BD", fontFace: "Courier New" });
  s.addText(
    '{\n  "gender": "Female", "SeniorCitizen": 0,\n  "Partner": "No", "Dependents": "No",\n  "tenure": 5, "PhoneService": "Yes",\n  "MultipleLines": "No",\n  "InternetService": "Fiber optic",\n  "OnlineSecurity": "No", "OnlineBackup": "No",\n  "DeviceProtection": "No", "TechSupport": "No",\n  "StreamingTV": "No", "StreamingMovies": "No",\n  "Contract": "Month-to-month",\n  "PaperlessBilling": "Yes",\n  "PaymentMethod": "Electronic check",\n  "MonthlyCharges": 85.0, "TotalCharges": 425.0\n}',
    { x: 8.0, y: 2.5, w: 4.4, h: 2.85, fontSize: 8.7, color: "E3E7E4", fontFace: "Courier New", lineSpacingMultiple: 1.08 }
  );
  s.addText("Response", { x: 8.0, y: 5.35, w: 4.1, h: 0.3, fontSize: 11.5, color: "F0B08C", fontFace: "Courier New" });
  s.addText('{ "churn_prediction": "Yes", "churn_probability": 0.932,\n  "model_version": "gradient_boosting_v1" }', {
    x: 8.0, y: 5.65, w: 4.4, h: 1.05, fontSize: 8.7, color: "E3E7E4", fontFace: "Courier New",
  });
  footer(s, "Serving & deployment");
})();

// =====================================================================
// 8. CI/CD PIPELINE
// =====================================================================
(function cicd() {
  const s = sectionHeader("Automation", "CI/CD pipeline (GitHub Actions)");
  const steps = [
    ["1", "Lint & test", "flake8 + pytest on every push/PR", BG_TEAL_TINT, TEAL],
    ["2", "Build & push", "Docker image built and pushed to registry", BG_GOLD_TINT, GOLD],
    ["3", "Deploy", "Render deploy hook triggered automatically", BG_TEAL_TINT, TEAL],
    ["4", "Monitor & retrain", "Daily drift check; if triggered, commits new model and redeploys automatically (separate job, no manual step)", BG_CORAL_TINT, CORAL],
  ];
  steps.forEach((step, i) => {
    const x = MARGIN + i * 2.98;
    s.addShape(pres.ShapeType.roundRect, { x, y: 2.05, w: 2.7, h: 2.35, rectRadius: 0.1, fill: { color: step[3] }, line: { color: step[3] } });
    s.addText(step[0], { x: x + 0.18, y: 2.2, w: 0.7, h: 0.5, fontSize: 20, color: step[4], fontFace: "Arial", bold: true });
    s.addText(step[1], { x: x + 0.18, y: 2.72, w: 2.35, h: 0.45, fontSize: 14.5, color: NAVY, fontFace: "Arial", bold: true });
    s.addText(step[2], { x: x + 0.18, y: 3.2, w: 2.35, h: 1.1, fontSize: 10.5, color: GRAY_MED, fontFace: "Arial", lineSpacingMultiple: 1.1 });
    if (i < steps.length - 1) {
      s.addText("\u2192", { x: x + 2.73, y: 2.95, w: 0.26, h: 0.4, fontSize: 18, color: GRAY_SOFT, fontFace: "Arial", align: "center", valign: "middle", wrap: false });
    }
  });
  bulletList(s, [
    "Workflow file: .github/workflows/ci-cd.yml \u2014 triggers on push to main, pull requests, and a daily 06:00 UTC schedule.",
    "If drift is detected, retrain.py's commit is deliberately NOT tagged [skip ci] \u2014 it flows into a redeploy-after-retrain job that rebuilds the image and re-hits the Render deploy hook automatically.",
  ], { w: 11.6, y: 4.75, h: 1.7, fontSize: 13, paraSpaceAfter: 10 });
  footer(s, "CI/CD pipeline");
})();

// =====================================================================
// 9. MONITORING & DRIFT
// =====================================================================
(function monitoring() {
  const s = sectionHeader("Staying accurate in production", "Monitoring & drift detection");
  bulletList(s, [
    "EvidentlyAI compares live production data against the training-time reference distribution, feature by feature.",
    "Simulated a realistic drift scenario for the demo: a marketing push shifted new sign-ups toward shorter tenure and higher monthly charges.",
    "Result: 3 of 19 features drifted (15.8% drift share) \u2014 exceeded the 15% threshold, so retraining was flagged automatically.",
    "monitoring/retrain.py backs up the current model, then re-runs the DVC pipeline to produce a fresh one; the CI/CD pipeline then redeploys it (see previous slide).",
  ], { w: 6.9, y: 2.0, h: 4.4, fontSize: 14, paraSpaceAfter: 14 });

  statCard(s, 8.2, 2.0, 4.3, 1.4, "3 / 19", "features drifted in the simulated batch", { bg: BG_CORAL_TINT, valColor: CORAL });
  statCard(s, 8.2, 3.6, 4.3, 1.4, "15.8%", "drift share \u2014 above the 15% retrain threshold", { bg: BG_GOLD_TINT, valColor: GOLD });
  statCard(s, 8.2, 5.2, 4.3, 1.15, "Auto", "retraining + redeploy, no manual intervention", { bg: BG_TEAL_TINT, valColor: TEAL });
  footer(s, "Monitoring & drift detection");
})();

// =====================================================================
// 10. MODEL CARD & LIMITATIONS
// =====================================================================
(function modelCard() {
  const s = sectionHeader("Honest assessment", "Model card & limitations");
  bulletList(s, [
    "Gradient Boosting @ threshold=0.5 \u2014 Accuracy 0.762, Precision 0.720, Recall 0.632, F1 0.673, ROC-AUC 0.838 on held-out test data.",
    "Selected on ROC-AUC (ranking quality) because the model ranks customers by risk for a capacity-limited retention team; precision/recall/F1 are reported at the standard 0.5 threshold for interpretability.",
  ], { w: 11.6, y: 1.95, h: 1.7, fontSize: 14, paraSpaceAfter: 10 });

  s.addText("Known limitations", { x: MARGIN, y: 3.7, w: 6, h: 0.35, fontSize: 14, color: NAVY, fontFace: "Arial", bold: true });
  bulletList(s, [
    "Trained on synthetic data \u2014 never seen real customer behavior.",
    "No fairness/bias audit across demographic groups yet.",
    "Label encoding creates an ordinal assumption for the Logistic Regression baseline (documented, not hidden).",
    "Class imbalance (38.7% churn) affects recall on the minority class.",
  ], { w: 11.6, y: 4.1, h: 2.5, fontSize: 13, paraSpaceAfter: 9 });
  footer(s, "Model card & limitations");
})();

// =====================================================================
// 11. CLOSING / DEMO
// =====================================================================
(function closing() {
  const s = pres.addSlide();
  s.background = { color: TEAL_DEEP };
  s.addShape(pres.ShapeType.rect, { x: -2, y: -1, w: 18, h: 4, fill: { color: TEAL_DARK }, rotate: 8 });
  s.addText("LIVE DEMO & REPOSITORY", { x: 0.9, y: 1.0, w: 9, h: 0.4, fontSize: 13, color: "9FE1CB", fontFace: "Arial", charSpacing: 3, bold: true });
  s.addText("Let's see it running", { x: 0.85, y: 1.4, w: 10, h: 0.9, fontSize: 34, color: WHITE, fontFace: "Arial" });

  const demo = [
    ["Live API", "[public Render URL after deployment]"],
    ["GitHub repository", "[repo URL]"],
    ["Demo flow", "submit a customer profile to /predict -> inspect response -> show MLflow UI -> show drift report"],
  ];
  let dy = 2.8;
  demo.forEach((row) => {
    s.addShape(pres.ShapeType.ellipse, { x: 0.9, y: dy + 0.06, w: 0.12, h: 0.12, fill: { color: GOLD }, line: { color: GOLD } });
    s.addText(row[0], { x: 1.2, y: dy - 0.08, w: 2.6, h: 0.4, fontSize: 14, color: "CFF0E3", fontFace: "Arial", bold: true });
    s.addText(row[1], { x: 3.9, y: dy - 0.08, w: 8.4, h: 0.5, fontSize: 14, color: WHITE, fontFace: "Arial" });
    dy += 0.55;
  });

  s.addShape(pres.ShapeType.line, { x: 0.9, y: 5.6, w: 2.0, h: 0, line: { color: GOLD, width: 2 } });
  s.addText("Thank you \u2014 questions welcome.", { x: 0.9, y: 5.85, w: 8, h: 0.6, fontSize: 22, color: WHITE, fontFace: "Arial" });
  s.addText("MAI201NAA.06381.2264  \u00b7  Project Phase 2 final presentation", { x: 0.9, y: 6.9, w: 8, h: 0.35, fontSize: 11, color: "8FCDB8", fontFace: "Arial" });
})();

pres.writeFile({ fileName: "docs/Phase2_Presentation.pptx" }).then(() => console.log("done"));
