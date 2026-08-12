import graphviz

g = graphviz.Digraph("architecture", format="png")
g.attr(rankdir="TB", bgcolor="white", fontname="Helvetica", fontsize="11")
g.attr("node", fontname="Helvetica", fontsize="11", shape="box", style="rounded,filled", margin="0.15,0.1")

# Colors
c_data = "#E6F1FB"; c_data_b = "#378ADD"
c_pipe = "#E1F5EE"; c_pipe_b = "#1D9E75"
c_serve = "#FAEEDA"; c_serve_b = "#BA7517"
c_ci = "#EEEDFE"; c_ci_b = "#7F77DD"
c_mon = "#FAECE7"; c_mon_b = "#D85A30"

with g.subgraph(name="cluster_data") as c:
    c.attr(label="Data & Versioning", style="dashed", color="#888780")
    c.node("raw", "Raw churn.csv\n(synthetic dataset)", fillcolor=c_data, color=c_data_b)
    c.node("dvc", "DVC\n(data + pipeline versioning)", fillcolor=c_data, color=c_data_b)

with g.subgraph(name="cluster_pipeline") as c:
    c.attr(label="ML Pipeline (DVC stages)", style="dashed", color="#888780")
    c.node("prepare", "prepare.py\nclean + encode + split", fillcolor=c_pipe, color=c_pipe_b)
    c.node("train", "train.py\ntrain + log to MLflow", fillcolor=c_pipe, color=c_pipe_b)
    c.node("evaluate", "evaluate.py\nmetrics + reference stats", fillcolor=c_pipe, color=c_pipe_b)

g.node("mlflow", "MLflow Tracking\n(experiments, metrics, models)", fillcolor=c_pipe, color=c_pipe_b)
g.node("registry", "models/model.pkl\n(best model artifact)", fillcolor=c_pipe, color=c_pipe_b)

with g.subgraph(name="cluster_serve") as c:
    c.attr(label="Serving", style="dashed", color="#888780")
    c.node("api", "FastAPI app\n/predict endpoint", fillcolor=c_serve, color=c_serve_b)
    c.node("docker", "Docker container", fillcolor=c_serve, color=c_serve_b)
    c.node("cloud", "Cloud deployment\n(Render)", fillcolor=c_serve, color=c_serve_b)

with g.subgraph(name="cluster_ci") as c:
    c.attr(label="CI/CD", style="dashed", color="#888780")
    c.node("github", "GitHub repo", fillcolor=c_ci, color=c_ci_b)
    c.node("actions", "GitHub Actions\ntest + lint + deploy", fillcolor=c_ci, color=c_ci_b)

with g.subgraph(name="cluster_monitor") as c:
    c.attr(label="Monitoring", style="dashed", color="#888780")
    c.node("evidently", "EvidentlyAI\ndrift detection", fillcolor=c_mon, color=c_mon_b)
    c.node("retrain", "Retraining trigger", fillcolor=c_mon, color=c_mon_b)

g.edge("raw", "dvc")
g.edge("dvc", "prepare")
g.edge("prepare", "train")
g.edge("train", "mlflow")
g.edge("train", "evaluate")
g.edge("evaluate", "registry")
g.edge("registry", "api")
g.edge("api", "docker")
g.edge("docker", "cloud")
g.edge("github", "actions")
g.edge("actions", "docker", label="build & push", fontsize="9")
g.edge("actions", "cloud", label="auto-deploy", fontsize="9")
g.edge("cloud", "evidently", label="live traffic", fontsize="9")
g.edge("evidently", "retrain", label="drift detected", fontsize="9")
g.edge("retrain", "prepare", style="dashed", label="new baseline", fontsize="9")

g.render("architecture", cleanup=True)
print("saved architecture.png")
