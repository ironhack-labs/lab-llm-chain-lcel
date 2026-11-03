![logo_ironhack_blue 7](https://user-images.githubusercontent.com/23629340/40541063-a07a0a8a-601a-11e8-91b5-2f13e4e6b441.png)

# Lab | Simple LLM App with LCEL

## Getting Started

Use Python 3.12 and an isolated environment. In PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Select `.venv` as the notebook kernel in your editor. Copy `.env.example` to
`.env` and fill in your OpenAI key. For the trace exercise, add a LangSmith
key and set `LANGCHAIN_TRACING_V2=true`. The notebook and server both load
this file; `.env` is ignored by Git.

Run notebook cells in order. Before the RemoteRunnable cell, start the server
in another terminal:

```powershell
.\.venv\Scripts\python.exe serve.py
```

Visit http://localhost:8000/chain/playground/ to test the API. Finish the final
summary using actual LangSmith traces, including measured token counts and
latencies. The dependency set uses LangChain 0.3 and Pydantic 2 because the
original Pydantic 1 pins conflict with LangChain on Python 3.12.4 and later.

Verification commands (the last two use your API keys and make model calls):

```powershell
.\.venv\Scripts\python.exe -X utf8 check_lab.py
.\.venv\Scripts\python.exe -X utf8 run_lab.py
.\.venv\Scripts\python.exe -X utf8 run_lab.py --traces-only
```

`run_lab.py` starts and stops a local server, executes the notebook, and saves
its outputs. It enables tracing for the run when a LangSmith key is present.
`--traces-only` reads recent traces and updates the final summary with measurements.

Follow the instructions provided in the notebook.

Read the instructions for each cell and provide your answers. Make sure to test your answers in each cell and save. Jupyter Notebook should automatically save your work progress. But it's a good idea to periodically save your work manually just in case.

## Deliverables

- Downloaded notebook with your responses to each of the exercises.


## Submission

- Upon completion, add your deliverables to git. 
- Then commit git and push your branch to the remote.
- Make a pull request and paste the PR link in the submission field in the Student Portal.

<br>

**Good luck!**
