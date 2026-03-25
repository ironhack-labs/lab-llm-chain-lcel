# Simple LLM App with LCEL

Builds a multilingual translation app using LangChain Expression Language, then serves it as a REST API with LangServe.

→ [lab-llm-chain-lcel.ipynb](lab-llm-chain-lcel.ipynb)

## What it demonstrates

LCEL (LangChain Expression Language) is the framework's answer to the question of how to compose LLM components without boilerplate glue code. The `|` pipe operator chains a `ChatPromptTemplate`, a model, and an output parser into a single Runnable — and because everything in the chain is a Runnable, the same interface works whether you're invoking locally, streaming, or calling the chain remotely via HTTP. This lab makes that abstraction concrete by going end-to-end: notebook → chain → LangServe REST API → `RemoteRunnable` client calling it back.

## Key things worth noting

**The pipe operator is the point, not the translation task.** The translation use case is intentionally trivial — the lab is really about understanding that `model.invoke(messages)` returns an `AIMessage` object with metadata, that `StrOutputParser` extracts just the string content downstream components need, and that `prompt_template | model | parser` composes these into one unit where each component's output type becomes the next one's input type.

**Replaced ChatOpenAI with ChatGroq throughout.** The original scaffold assumes an OpenAI key. Both the notebook chain and `serve.py` use `ChatGroq(model="llama-3.3-70b-versatile")` instead — same LCEL interface, no OpenAI dependency, open-source model with a 131K token context window.

**Added dynamic model discovery before hardcoding a model name.** The notebook queries the Groq API (`/openai/v1/models`) and pretty-prints all available models. This matters because not all listed models are suitable for chat — audio (Whisper), guard, and TTS models appear in the list and would fail silently or produce wrong output if used for translation.

**`load_dotenv()` must be called before LangChain components are instantiated.** In `serve.py`, `load_dotenv()` is called before the `add_routes` import. Env vars set after an object is instantiated are not picked up — this is a common source of "API key not found" errors that look like environment issues but are actually ordering issues.

**LangServe decouples the chain from its consumers.** `add_routes(app, chain, path="/chain")` exposes the chain as a FastAPI endpoint with a built-in Playground UI. The notebook client uses `RemoteRunnable("http://localhost:8000/chain/")` and calls `.invoke()` identically to a local chain — HTTP is completely abstracted. API keys and model logic stay on the server side.

## Stack

| Component | Choice |
|---|---|
| LLM | Groq `llama-3.3-70b-versatile` |
| Chain framework | LangChain LCEL (`langchain-core`) |
| API server | LangServe + FastAPI + Uvicorn |
| Client | `langserve.RemoteRunnable` |

## How to run

1. Install dependencies:
   ```bash
   pip install langchain langchain-core langchain-groq langserve fastapi uvicorn python-dotenv
   ```

2. Add your key to `.env`:
   ```
   GROQ_API_KEY=gsk_...
   ```

3. Run the notebook top to bottom (`lab-llm-chain-lcel.ipynb`) for the chain walkthrough.

4. To test the served API, start the server in a separate terminal:
   ```bash
   python serve.py
   ```
   Then run the `RemoteRunnable` cell in the notebook. The LangServe Playground is available at `http://localhost:8000/chain/playground`.
