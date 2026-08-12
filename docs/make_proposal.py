# -*- coding: utf-8 -*-
"""
make_proposal.py — builds docs/Project_Proposal.pdf: a long-form, formally
structured project proposal (cover page, real table of contents with page
numbers, numbered sections, header/footer on every content page, and the
architecture diagram embedded as a figure).
"""
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, NextPageTemplate, PageBreak,
    Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem, Image,
    KeepTogether,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as canvas_mod

PAGE_W, PAGE_H = letter

TEAL = colors.HexColor("#0F6E56")
TEAL_DARK = colors.HexColor("#0A4F3E")
TEAL_DEEP = colors.HexColor("#072F26")
NAVY = colors.HexColor("#16241F")
GOLD = colors.HexColor("#C08A28")
CORAL = colors.HexColor("#D2572B")
GRAY_MED = colors.HexColor("#5C6660")
GRAY_LIGHT = colors.HexColor("#F4F3EE")
GRAY_LINE = colors.HexColor("#DEDCD3")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="H1Num", fontSize=18, leading=22, spaceBefore=22, spaceAfter=10,
                           textColor=NAVY, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="H2Num", fontSize=13.5, leading=17, spaceBefore=14, spaceAfter=6,
                           textColor=TEAL_DARK, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="BodyText2", fontSize=10.3, leading=15.2, spaceAfter=8,
                           textColor=NAVY, fontName="Helvetica"))
styles.add(ParagraphStyle(name="BodyItalic", parent=styles["BodyText2"], fontName="Helvetica-Oblique",
                           textColor=GRAY_MED))
styles.add(ParagraphStyle(name="Caption", fontSize=9, leading=12, textColor=GRAY_MED,
                           fontName="Helvetica-Oblique", alignment=TA_CENTER, spaceBefore=4, spaceAfter=14))
styles.add(ParagraphStyle(name="TOCHeading", fontSize=13.5, leading=17, textColor=colors.white,
                           fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="TOC1", fontSize=11.5, leading=22, textColor=NAVY, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="TOC2", fontSize=10, leading=17, leftIndent=16, textColor=GRAY_MED,
                           fontName="Helvetica"))
styles.add(ParagraphStyle(name="CoverTitle", fontSize=34, leading=40, textColor=colors.white,
                           fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CoverSub", fontSize=14, leading=19, textColor=colors.HexColor("#CFF0E3"),
                           fontName="Helvetica"))
styles.add(ParagraphStyle(name="CoverKicker", fontSize=11, leading=14, textColor=colors.HexColor("#9FE1CB"),
                           fontName="Helvetica-Bold"))


def para_list(items, style="BodyText2", bullet_color=TEAL):
    return ListFlowable(
        [ListItem(Paragraph(t, styles[style]), bulletColor=bullet_color) for t in items],
        bulletType="bullet", start="\u2022", leftIndent=14, bulletFontSize=8,
    )


CELL_STYLE = ParagraphStyle(name="Cell", fontSize=9, leading=12.5, textColor=NAVY, fontName="Helvetica")
CELL_STYLE_HDR = ParagraphStyle(name="CellHdr", fontSize=9, leading=12.5, textColor=colors.white, fontName="Helvetica-Bold")


def _wrap_cell(val, is_header=False, font_size=9):
    if isinstance(val, str):
        style = ParagraphStyle(name="CellDyn", parent=CELL_STYLE_HDR if is_header else CELL_STYLE, fontSize=font_size, leading=font_size + 3.5)
        return Paragraph(val, style)
    return val


def styled_table(data, col_widths, header_bg=TEAL, zebra=GRAY_LIGHT, font_size=9):
    wrapped = []
    for r_idx, row in enumerate(data):
        wrapped.append([_wrap_cell(cell, is_header=(r_idx == 0), font_size=font_size) for cell in row])
    t = Table(wrapped, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY_LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, zebra]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


# ---------------------------------------------------------------------------
# Page templates: cover (no header/footer), TOC page (dark), content pages
# ---------------------------------------------------------------------------

def draw_cover(c: canvas_mod.Canvas, doc):
    c.saveState()
    c.setFillColor(TEAL_DEEP)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(TEAL_DARK)
    c.saveState()
    c.translate(-40, PAGE_H * 0.30)
    c.rotate(-5)
    c.rect(0, 0, PAGE_W + 100, PAGE_H * 0.55, fill=1, stroke=0)
    c.restoreState()
    c.setFillColor(TEAL)
    c.saveState()
    c.translate(-40, PAGE_H * 0.18)
    c.rotate(-5)
    c.rect(0, 0, PAGE_W + 100, PAGE_H * 0.30, fill=1, stroke=0)
    c.restoreState()
    c.setFillColor(colors.HexColor("#0D5C48"))
    c.circle(PAGE_W - 0.9 * inch, PAGE_H - 0.6 * inch, 1.55 * inch, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.circle(PAGE_W - 0.55 * inch, PAGE_H - 0.35 * inch, 0.55 * inch, fill=1, stroke=0)
    c.restoreState()


def draw_toc_bg(c: canvas_mod.Canvas, doc):
    c.saveState()
    c.setFillColor(colors.white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(TEAL_DEEP)
    c.rect(0, PAGE_H - 1.55 * inch, PAGE_W, 1.55 * inch, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.circle(PAGE_W - 0.6 * inch, PAGE_H - 0.15 * inch, 0.5 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(0.95 * inch, PAGE_H - 1.0 * inch, "Table of Contents")
    c.restoreState()


PAGE_NUM = {"n": 0}


def draw_content(c: canvas_mod.Canvas, doc):
    c.saveState()
    # left accent bar
    c.setFillColor(TEAL)
    c.rect(0, 0, 0.14 * inch, PAGE_H, fill=1, stroke=0)
    # footer
    c.setStrokeColor(GRAY_LINE)
    c.setLineWidth(0.6)
    c.line(0.85 * inch, 0.65 * inch, PAGE_W - 0.85 * inch, 0.65 * inch)
    c.setFont("Helvetica", 8.3)
    c.setFillColor(GRAY_MED)
    c.drawString(0.85 * inch, 0.48 * inch, "Customer Churn Prediction \u2014 MLOps Project Proposal")
    c.drawRightString(PAGE_W - 0.85 * inch, 0.48 * inch, f"MAI201NAA.06381.2264   \u00b7   Page {c.getPageNumber() - 2}")
    c.restoreState()


doc = BaseDocTemplate(
    "docs/Project_Proposal.pdf",
    pagesize=letter,
    topMargin=0.95 * inch, bottomMargin=0.95 * inch,
    leftMargin=0.95 * inch, rightMargin=0.95 * inch,
)

cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover")
toc_frame = Frame(0.95 * inch, 0.9 * inch, PAGE_W - 1.9 * inch, PAGE_H - 2.7 * inch, id="toc")
content_frame = Frame(0.95 * inch, 0.9 * inch, PAGE_W - 1.9 * inch, PAGE_H - 2.1 * inch, id="content")

doc.addPageTemplates([
    PageTemplate(id="Cover", frames=[cover_frame], onPage=draw_cover),
    PageTemplate(id="TOCPage", frames=[toc_frame], onPage=draw_toc_bg),
    PageTemplate(id="Content", frames=[content_frame], onPage=draw_content),
])


class ProposalDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style_name = flowable.style.name
            text = flowable.getPlainText()
            if style_name == "H1Num":
                self.notify("TOCEntry", (0, text, self.page))
                key = f"h1-{text}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=0, closed=False)
            elif style_name == "H2Num":
                self.notify("TOCEntry", (1, text, self.page))


doc.__class__ = ProposalDoc

story = []

# =============================== COVER ===============================
story.append(NextPageTemplate("Cover"))
story.append(Spacer(1, 1.7 * inch))
story.append(Paragraph("MLOPS COURSE PROJECT &nbsp;\u00b7&nbsp; MAI201NAA.06381.2264", styles["CoverKicker"]))
story.append(Spacer(1, 14))
story.append(Paragraph("Project Proposal", styles["CoverTitle"]))
story.append(Paragraph("Customer Churn Prediction", styles["CoverTitle"]))
story.append(Spacer(1, 16))
story.append(Paragraph(
    "A comprehensive end-to-end MLOps proposal covering data versioning, experiment tracking,<br/>"
    "containerized model serving, continuous integration/deployment, and automated drift monitoring.",
    styles["CoverSub"],
))
story.append(Spacer(1, 2.6 * inch))
cover_meta = Table(
    [["Prepared for", "Instructor approval \u2014 Project Phase 0"],
     ["Submission type", "Individual (solo) submission"],
     ["Date", "August 2026"]],
    colWidths=[1.7 * inch, 4.3 * inch],
)
cover_meta.setStyle(TableStyle([
    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#8FCDB8")),
    ("TEXTCOLOR", (1, 0), (1, -1), colors.white),
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 10.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
]))
story.append(cover_meta)
story.append(NextPageTemplate("TOCPage"))
story.append(PageBreak())

# ============================ TABLE OF CONTENTS ============================
toc = TableOfContents()
toc.levelStyles = [styles["TOC1"], styles["TOC2"]]
story.append(Spacer(1, 0.3 * inch))
story.append(toc)
story.append(NextPageTemplate("Content"))
story.append(PageBreak())

# ============================ CONTENT ============================

# --- Executive summary ---
story.append(Paragraph("Executive Summary", styles["H1Num"]))
story.append(Paragraph(
    "This proposal outlines a solo-submission MLOps project that builds a complete, production-style "
    "machine learning lifecycle around a customer-churn prediction model. Rather than treating churn "
    "prediction as a one-off notebook exercise, the project deliberately spans the full MLOps discipline: "
    "reproducible data preparation, versioned pipelines (DVC), tracked experimentation (MLflow), containerized "
    "serving (FastAPI + Docker), continuous integration and deployment (GitHub Actions), and automated "
    "production monitoring with drift-triggered retraining (EvidentlyAI). The project is organized into the "
    "three phases defined by the course \u2014 team/topic proposal, pipeline construction, and deployment with "
    "monitoring \u2014 and this document is the Phase 0 deliverable that establishes topic, dataset, architecture, "
    "and plan for the phases that follow.", styles["BodyText2"],
))
story.append(Paragraph(
    "Because all four required roles (Project Lead, ML Lead, Engineering Lead, Documentation Lead) are held "
    "by a single team member for this submission, the proposal also sets explicit scope boundaries so the "
    "workload stays realistic within the course timeline, while still exercising every stage of the MLOps "
    "toolchain the assignment specifications ask for.", styles["BodyText2"],
))

# --- 1. Introduction & problem statement ---
story.append(Paragraph("1. Introduction &amp; Problem Statement", styles["H1Num"]))
story.append(Paragraph(
    "Customer churn \u2014 a subscriber ending their relationship with a service provider \u2014 is one of the "
    "most consequential and well-studied problems in telecommunications, subscription software, and utility "
    "businesses. Acquiring a new customer typically costs several times more than retaining an existing one, "
    "so even a modest improvement in identifying at-risk customers before they leave translates directly into "
    "protected revenue. Retention teams, however, cannot act on every customer manually; they need a ranked, "
    "continuously refreshed list of who is likely to churn and why.", styles["BodyText2"],
))
story.append(Paragraph(
    "From an MLOps perspective, churn prediction is also a well-suited teaching vehicle: the feature set is "
    "moderate in size and interpretable, the classification task is binary and well understood, and \u2014 "
    "critically for this course \u2014 the *operational* problem (keeping a churn model accurate as customer "
    "behavior shifts over time) is at least as important as the initial modeling problem. A churn model "
    "trained once and never revisited will silently degrade as pricing, competitors, and customer mix change; "
    "this is precisely the failure mode that the monitoring and retraining components of this project are "
    "designed to catch automatically.", styles["BodyText2"],
))

# --- 2. Objectives & scope ---
story.append(Paragraph("2. Objectives &amp; Scope", styles["H1Num"]))
story.append(Paragraph("2.1 Primary objectives", styles["H2Num"]))
story.append(para_list([
    "Build a reproducible data-to-model pipeline that any team member (or grader) can re-run end to end with a single command (<font face='Courier'>dvc repro</font>).",
    "Track and compare multiple modeling approaches with full experiment lineage (parameters, metrics, artifacts) rather than ad-hoc notebook runs.",
    "Package the selected model as a versioned, independently deployable service rather than a script tied to one machine.",
    "Automate the path from a code change to a running, tested, deployed service using continuous integration and continuous deployment.",
    "Detect when the production model's assumptions about incoming data no longer hold, and respond automatically rather than waiting for a human to notice degraded performance.",
]))
story.append(Paragraph("2.2 Scope boundaries", styles["H2Num"]))
story.append(Paragraph(
    "To keep the project realistic for a solo submission within the course timeline, the following are "
    "explicitly out of scope: multi-model ensembling beyond the three algorithms compared in Phase 1; a "
    "customer-facing UI (the deliverable is an API, consumed via Swagger/cURL for demonstration); real-time "
    "streaming ingestion (the monitoring stage operates on periodic batches, which is standard practice for "
    "churn-style use cases); and multi-region or high-availability deployment infrastructure (a single Render "
    "free-tier instance is sufficient to demonstrate the CI/CD and monitoring mechanics).", styles["BodyText2"],
))

# --- 3. Team & roles ---
story.append(Paragraph("3. Team &amp; Roles", styles["H1Num"]))
story.append(Paragraph(
    "This project is completed individually. All four roles defined by the assignment are held by the sole "
    "team member, who is accountable for every deliverable across all three phases.", styles["BodyText2"],
))
team_tbl = styled_table(
    [["Role", "Responsibilities", "Owner"],
     ["Project Lead", "Scope, timeline, phase deliverables, instructor communication", "[Student Name]"],
     ["ML Lead", "Dataset design, feature engineering, model selection, MLflow tracking", "[Student Name]"],
     ["Engineering Lead", "FastAPI service, Dockerization, CI/CD pipeline, cloud deployment", "[Student Name]"],
     ["Documentation Lead", "Proposal, model/dataset cards, README, final presentation", "[Student Name]"]],
    col_widths=[1.5 * inch, 3.55 * inch, 1.35 * inch],
)
story.append(team_tbl)
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Holding every role individually is noted here explicitly so grading can account for the workload "
    "distribution difference relative to a 3\u20134 person team, rather than assuming role coverage implies "
    "additional contributors.", styles["BodyItalic"],
))

# --- 4. Dataset & data governance ---
story.append(Paragraph("4. Dataset &amp; Data Governance", styles["H1Num"]))
story.append(Paragraph(
    "The project uses a synthetic dataset generated by <font face='Courier'>src/generate_dataset.py</font>, "
    "engineered to match the schema, size, and statistical structure of the widely used public IBM/Kaggle "
    "\u201cTelco Customer Churn\u201d dataset. This choice was made for a specific, disclosed reason: the "
    "development environment used to build this project has no direct network access to Kaggle, so a "
    "synthetic dataset was generated instead of silently substituting unrelated data.", styles["BodyText2"],
))
story.append(Paragraph(
    "Rather than random noise, the churn label is generated from a logistic function over realistic churn "
    "drivers \u2014 contract type, tenure, internet service type, technical support, payment method, and "
    "monthly charges \u2014 so the resulting data has genuine, learnable signal for the pipeline to model, and "
    "the relationships a churn analyst would expect to see (e.g. month-to-month contracts churn more than "
    "two-year contracts) are preserved by construction.", styles["BodyText2"],
))
ds_tbl = styled_table(
    [["Property", "Value"],
     ["Rows \u00d7 columns", "7,043 \u00d7 21 (customerID + 19 features + Churn label)"],
     ["Target", "Churn (Yes/No) \u2014 baseline rate \u2248 38.7%"],
     ["Missing values", "None generated (real dataset has 11 in TotalCharges; pipeline handles both)"],
     ["Split", "80% train / 20% test, stratified on Churn"],
     ["Encoding", "Label encoding for categorical features (limitation documented in Section 7.1)"]],
    col_widths=[1.9 * inch, 4.5 * inch],
)
story.append(ds_tbl)
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Full lineage, schema documentation, and known limitations are maintained separately in "
    "<font face='Courier'>docs/dataset_card.md</font>, which is treated as a living document updated whenever "
    "the data-generation logic changes.", styles["BodyItalic"],
))

# --- 5. System architecture ---
story.append(Paragraph("5. Proposed System Architecture", styles["H1Num"]))
story.append(Paragraph(
    "The system is organized into five cooperating layers, shown in Figure 1: data &amp; versioning, the ML "
    "pipeline, experiment tracking, serving, and a monitoring loop that feeds back into retraining. Each "
    "layer maps directly onto one phase of the course deliverables.", styles["BodyText2"],
))
story.append(KeepTogether([
    Image("docs/architecture.png", width=3.35 * inch, height=3.35 * inch * (1256 / 657)),
]))
story.append(Paragraph("Figure 1. End-to-end system architecture, from raw data to a self-monitoring, self-redeploying production service.", styles["Caption"]))
story.append(Paragraph("5.1 Layer summary", styles["H2Num"]))
arch_tbl = styled_table(
    [["Layer", "Components", "Course phase"],
     ["Data & versioning", "DVC-tracked raw CSV, DVC pipeline definition", "Phase 1"],
     ["ML pipeline", "prepare.py \u2192 train.py \u2192 evaluate.py (3 DVC stages)", "Phase 1"],
     ["Experiment tracking", "MLflow: baseline + 2 experiments, metrics + model artifacts", "Phase 1"],
     ["Serving", "FastAPI app, Pydantic validation, Docker image", "Phase 2"],
     ["CI/CD", "GitHub Actions: lint, test, build, push, deploy", "Phase 2"],
     ["Monitoring & retraining", "EvidentlyAI drift detection, automated retrain + redeploy", "Phase 2"]],
    col_widths=[1.7 * inch, 3.75 * inch, 0.95 * inch],
)
story.append(arch_tbl)

# --- 6. Technology stack ---
story.append(Paragraph("6. Technology Stack", styles["H1Num"]))
tech_tbl = styled_table(
    [["Category", "Tool / Library", "Purpose"],
     ["Language & core libs", "Python 3.11, pandas, numpy, scikit-learn", "Data processing and modeling"],
     ["Data & pipeline versioning", "DVC", "Reproducible, versioned pipeline stages"],
     ["Experiment tracking", "MLflow", "Parameters, metrics, and model artifact logging"],
     ["Model serving", "FastAPI, Pydantic, Uvicorn", "Validated REST API for predictions"],
     ["Containerization", "Docker", "Portable, reproducible runtime environment"],
     ["CI/CD", "GitHub Actions", "Automated lint, test, build, and deploy"],
     ["Cloud hosting", "Render (free tier)", "Public HTTPS endpoint for the API"],
     ["Monitoring", "EvidentlyAI", "Statistical data-drift detection"],
     ["Testing & quality", "pytest, flake8", "Automated tests and style enforcement"]],
    col_widths=[1.65 * inch, 2.15 * inch, 2.6 * inch],
)
story.append(tech_tbl)

# --- 7. Methodology ---
story.append(Paragraph("7. Methodology", styles["H1Num"]))
story.append(Paragraph("7.1 Data preparation & modeling approach", styles["H2Num"]))
story.append(Paragraph(
    "The <font face='Courier'>prepare</font> stage drops the non-predictive customer identifier, imputes the "
    "one column known to carry missing values in the real-world dataset (TotalCharges, via median "
    "imputation), and label-encodes categorical fields. Label encoding is used uniformly so a single "
    "preprocessing path serves all three candidate models; this is computationally convenient for tree-based "
    "models (Random Forest, Gradient Boosting), which split on thresholds and are insensitive to encoding "
    "order, but it is a known simplification for the Logistic Regression baseline, which implicitly treats "
    "the encoded integers as ordered. This trade-off is deliberate and documented rather than hidden, and is "
    "revisited as a possible follow-up improvement in Section 11.", styles["BodyText2"],
))
story.append(Paragraph("7.2 Experimentation strategy", styles["H2Num"]))
story.append(Paragraph(
    "Three models are trained and logged to MLflow under a shared experiment: a Logistic Regression baseline, "
    "and two experiments (Random Forest and Gradient Boosting) with hand-tuned hyperparameters. Model "
    "selection uses ROC-AUC as the primary criterion, because the intended production use case is *ranking* "
    "customers by churn risk for a capacity-limited retention team rather than acting on a single fixed "
    "probability cutoff; ROC-AUC measures ranking quality independent of any particular threshold. Accuracy, "
    "precision, recall, and F1 are additionally reported at the standard 0.5 decision threshold for "
    "interpretability, and recall is monitored specifically because missing an actual churner is judged more "
    "costly than one unnecessary retention outreach to a customer who would not have churned.", styles["BodyText2"],
))
story.append(Paragraph("7.3 Serving & deployment approach", styles["H2Num"]))
story.append(Paragraph(
    "The selected model is wrapped in a FastAPI application with a Pydantic request schema that validates all "
    "19 input features (types, allowed categorical values, numeric ranges) before any prediction is made, so "
    "malformed requests fail fast with a clear 422 response rather than reaching the model. The application "
    "is containerized with a slim Python base image and a container health check, then deployed to Render, "
    "with GitHub Actions responsible for linting, testing, building, and triggering deployment on every push "
    "to the main branch.", styles["BodyText2"],
))
story.append(Paragraph("7.4 Monitoring & retraining approach", styles["H2Num"]))
story.append(Paragraph(
    "A scheduled GitHub Actions job compares a batch of recent (simulated, for demonstration) production data "
    "against the training-time reference distribution using EvidentlyAI's data-drift detection. If the share "
    "of drifted features exceeds a configured threshold, an automated retraining step re-runs the DVC "
    "pipeline, commits the refreshed model, and \u2014 critically \u2014 a downstream job rebuilds the Docker "
    "image and re-triggers the Render deploy hook, so a drift-triggered retrain reaches production without "
    "manual intervention.", styles["BodyText2"],
))

# --- 8. Timeline ---
story.append(Paragraph("8. Timeline &amp; Milestones", styles["H1Num"]))
timeline_tbl = styled_table(
    [["Phase", "Key deliverables", "Weight", "Due date"],
     ["Phase 0", "Team/topic proposal (this document)", "2.5%", "5/21/26"],
     ["Phase 1", "Dataset documentation, architecture diagram, DVC pipeline (3+ stages), MLflow tracking (baseline + 2 experiments)", "12.5%", "7/10/26"],
     ["Phase 2", "FastAPI + Docker deployment, CI/CD pipeline, drift monitoring & retraining, Model Card, final presentation with live demo", "25%", "8/13/26"]],
    col_widths=[0.85 * inch, 3.85 * inch, 0.65 * inch, 0.95 * inch],
)
story.append(timeline_tbl)
story.append(Spacer(1, 8))
story.append(Paragraph("8.1 Within-phase breakdown (Phase 2)", styles["H2Num"]))
gantt_tbl = styled_table(
    [["Task", "Status"],
     ["FastAPI service + Pydantic schema", "Complete"],
     ["Dockerfile + local container test", "Complete"],
     ["GitHub Actions: lint + test job", "Complete"],
     ["GitHub Actions: build + push + deploy jobs", "Complete (pending live Render credentials)"],
     ["EvidentlyAI drift detection + retrain trigger", "Complete"],
     ["Model Card & final documentation", "Complete"],
     ["Live deployment to Render", "Pending \u2014 requires the student's own Render/Docker Hub accounts"],
     ["Final presentation & live demo", "Complete (this deck); demo URL to be added after deployment"]],
    col_widths=[3.8 * inch, 3.35 * inch],
)
story.append(gantt_tbl)

# --- 9. Risk assessment ---
story.append(Paragraph("9. Risk Assessment", styles["H1Num"]))
risk_tbl = styled_table(
    [["Risk", "Likelihood", "Impact", "Mitigation"],
     ["Synthetic data does not fully reflect real churn patterns", "High", "Medium",
      "Documented transparently; pipeline accepts the real Kaggle CSV as a drop-in replacement with no code changes"],
     ["Render free-tier cold starts slow down the live demo", "Medium", "Low",
      "Warm up the service a few minutes before presenting; mention the limitation openly"],
     ["GitHub Actions secrets misconfigured, breaking CI/CD", "Medium", "Medium",
      "Step-by-step deployment guide provided (docs/deployment_guide.md); pipeline fails loudly with clear logs"],
     ["Retrain \u2192 redeploy loop triggers unnecessarily on noisy drift signals", "Low", "Medium",
      "Threshold (15% of features) tuned against a realistic simulated drift scenario before finalizing"],
     ["Single-person team limits available review/testing bandwidth", "High", "Low",
      "Automated tests (pytest) and linting (flake8) substitute for peer code review"]],
    col_widths=[2.1 * inch, 0.85 * inch, 0.7 * inch, 2.65 * inch],
    font_size=8.6,
)
story.append(risk_tbl)

# --- 10. Success criteria ---
story.append(Paragraph("10. Success Criteria &amp; KPIs", styles["H1Num"]))
story.append(para_list([
    "<b>Reproducibility:</b> a fresh clone of the repository can run <font face='Courier'>dvc repro</font> and reproduce the reported metrics exactly.",
    "<b>Model quality:</b> the selected model achieves ROC-AUC &ge; 0.80 on the held-out test set (achieved: 0.838).",
    "<b>Automation:</b> a push to main results in a tested, deployed service with no manual deployment steps.",
    "<b>Observability:</b> a simulated drift scenario is correctly detected and triggers retraining without manual intervention.",
    "<b>Documentation:</b> every non-obvious design decision (synthetic data, label encoding, threshold choices) is written down rather than left implicit.",
]))

# --- 11. Ethical considerations & limitations ---
story.append(Paragraph("11. Ethical Considerations &amp; Limitations", styles["H1Num"]))
story.append(para_list([
    "The model is trained on synthetic data and has never observed real customer behavior; it must not be used for real retention decisions without retraining on real, consented data.",
    "No fairness or bias audit across demographic slices (gender, senior-citizen status) has been performed; this should precede any production use on real customers.",
    "Label encoding introduces an ordinal assumption for the Logistic Regression baseline (Section 7.1); a future iteration could switch to one-hot encoding for linear models specifically.",
    "Class imbalance (38.7% churn) means recall on the minority class is lower than precision alone would suggest; this is reported explicitly rather than masked by accuracy.",
    "The model should never be the sole basis for denying service, adjusting pricing, or otherwise acting directly on a customer without human review.",
]))

# --- 12. References ---
story.append(Paragraph("12. References &amp; Further Reading", styles["H1Num"]))
story.append(para_list([
    "IBM/Kaggle \u201cTelco Customer Churn\u201d dataset \u2014 schema and structure referenced for the synthetic dataset design.",
    "DVC documentation \u2014 https://dvc.org/doc",
    "MLflow documentation \u2014 https://mlflow.org/docs/latest/index.html",
    "FastAPI documentation \u2014 https://fastapi.tiangolo.com",
    "EvidentlyAI documentation \u2014 https://docs.evidentlyai.com",
    "GitHub Actions documentation \u2014 https://docs.github.com/actions",
], style="BodyText2"))
story.append(Spacer(1, 10))
story.append(Paragraph(
    "Prepared for instructor approval \u2014 Project Phase 0, MAI201NAA.06381.2264.", styles["BodyItalic"]))

doc.multiBuild(story)
print("PDF created")
