#!/usr/bin/env python
from typing import List

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
system_template = "Translate the following into {language}."
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])
model = ChatOpenAI() # 2. Create model
parser = StrOutputParser() # 3. Create parser
chain = prompt_template | model | parser # 4. Create chain
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces", 
) # 4. App definition
add_routes(
    app,
    chain,
    path="/chain",
) # 5. Adding chain route
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)