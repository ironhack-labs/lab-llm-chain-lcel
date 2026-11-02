#!/usr/bin/env python

import os
from dotenv import load_dotenv
from fastapi import FastAPI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes



# Load environment variables (e.g. OPENAI_API_KEY) from a local .env file, if present
load_dotenv()

# Optional: enable LangSmith tracing
# Disable LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGSMITH_TRACING"] = "false"


# 1. Create prompt template
system_template = "Translate the following into {language}:"

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", "{text}")
    ]
)


# 2. Create model
model = ChatOpenAI(
    model="gpt-4o-mini"
)


# 3. Create output parser
parser = StrOutputParser()


# 4. Create LCEL chain
chain = prompt_template | model | parser


# 5. Create FastAPI app
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain Runnable interfaces",
)


# 6. Add chain endpoint
add_routes(
    app,
    chain,
    path="/chain",
)


# 7. Run server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="localhost",
        port=8000
    )