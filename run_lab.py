"""Execute and save the notebook against a temporary local API server."""
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

import httpx
import nbformat
from nbclient import NotebookClient


def summarize_traces():
    from dotenv import load_dotenv
    from langsmith import Client

    load_dotenv(".env")
    client = Client()
    projects = {p.name for p in client.list_projects()}
    project = os.environ.get("LANGCHAIN_PROJECT", "default")
    if project not in projects:
        print("Configured trace project is not present yet. Available:", sorted(projects))
        raise RuntimeError("Rerun with tracing enabled to create the lab project")
    runs = list(client.list_runs(
        project_name=project,
        start_time=datetime.now(timezone.utc) - timedelta(hours=1),
        limit=100,
    ))
    models = sorted(
        [r for r in runs if r.run_type == "llm" and not r.error and r.end_time],
        key=lambda r: r.start_time,
    )
    chains = [r for r in runs if r.name == "RunnableSequence" and not r.error]
    if len(models) < 2 or not chains:
        raise RuntimeError("Not enough successful traces to complete the summary")
    first, second = models[0], models[-1]
    elapsed = lambda r: (r.end_time - r.start_time).total_seconds()
    local_steps = [r for r in runs if r.run_type in ("prompt", "parser") and r.end_time and not r.error]
    if not local_steps:
        raise RuntimeError("Prompt/parser traces are missing")
    summary = (
        f"The earliest successful model trace in this verification window used {first.total_tokens} total tokens "
        "and received system and human messages requesting an Italian translation. "
        "The model-and-parser chain returns a plain string, while the full chain first converts the language/text dictionary "
        "into system and human messages, then calls the model and extracts its text. "
        f"Two model calls took {elapsed(first):.2f} and {elapsed(second):.2f} seconds; "
        f"the slowest recorded prompt/parser step took {max(map(elapsed, local_steps)):.3f} seconds, "
        "so model generation dominated the measured latency."
    )
    path = Path("lab-llm-chain-lcel.ipynb")
    notebook = nbformat.read(path, as_version=4)
    notebook.cells[40].source = summary
    nbformat.write(notebook, path)
    print(f"PASS: read {len(runs)} LangSmith traces and saved measured summary")


def main():
    from dotenv import load_dotenv

    root = Path(__file__).resolve().parent
    os.chdir(root)
    load_dotenv(".env")
    # This runner verifies the trace exercise as well as translations.
    if os.environ.get("LANGCHAIN_API_KEY"):
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["JUPYTER_PATH"] = str(root / ".venv/share/jupyter")
    os.environ["PYTHONIOENCODING"] = "utf-8"
    path = root / "lab-llm-chain-lcel.ipynb"
    notebook = nbformat.read(path, as_version=4)
    install_source = notebook.cells[2].source
    notebook.cells[2].source = "# Dependencies already installed from requirements.txt."
    server = subprocess.Popen(
        [sys.executable, "-X", "utf8", "serve.py"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(60):
            if server.poll() is not None:
                raise RuntimeError("Lab server failed to start")
            try:
                if httpx.get("http://localhost:8000/chain/input_schema").status_code == 200:
                    break
            except httpx.HTTPError:
                pass
            time.sleep(0.5)
        else:
            raise RuntimeError("Lab server did not become ready")
        NotebookClient(notebook, timeout=180, kernel_name="lcel-lab").execute()
        notebook.cells[2].source = install_source
        nbformat.write(notebook, path)
        print("PASS: notebook executed, including live model and RemoteRunnable calls")
    finally:
        server.terminate()
        server.wait(timeout=15)


if __name__ == "__main__":
    if "--traces-only" in sys.argv:
        summarize_traces()
    else:
        main()
