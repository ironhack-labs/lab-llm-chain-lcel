#!/usr/bin/env python

import os
from dotenv import load_dotenv

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes


# ==========================================
# 1. Load environment variables
# ==========================================

load_dotenv(override=True)

print("OpenAI API Key Loaded:", bool(os.getenv("OPENAI_API_KEY")))


# ==========================================
# 2. Create Prompt Template
# ==========================================

system_template = "Translate the following into {language}:"

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}")
])


# ==========================================
# 3. Create Model
# ==========================================

model = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


# ==========================================
# 4. Create Output Parser
# ==========================================

parser = StrOutputParser()


# ==========================================
# 5. Create LCEL Chain
# ==========================================

chain = prompt_template | model | parser


# ==========================================
# 6. Create FastAPI App
# ==========================================

app = FastAPI(
    title="LangChain Translation Server",
    version="1.0",
    description="A simple translation API built with LangChain and LangServe",
)


# ==========================================
# 7. Add LangServe Routes
# ==========================================

add_routes(
    app,
    chain,
    path="/chain",
)


# ==========================================
# 8. Run Server
# ==========================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="localhost",
        port=8000
    )