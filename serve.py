# !/usr/bin/env python
from typing import List
import os
import uvicorn

# os.system("pip install fastapi")
# os.system("pip install uvicorn")
# os.system("pip install langchain") 
# os.system("pip show fastapi")

# import fastapi
# print(fastapi.__version__)

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
from dotenv import load_dotenv


# Load .env file if used
load_dotenv()

# Get the API key
OPEN_API_KEY = os.getenv("open_api_key")



# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. Create model

model = ChatOpenAI(model= "gpt-4o-mini", verbose=True)

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser


# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route

add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)