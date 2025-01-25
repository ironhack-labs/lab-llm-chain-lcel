#!/usr/bin/env python
import os
from dotenv import load_dotenv
from fastapi import FastAPI

# 1. Load environment variables from .env
# Load the .env file:
load_dotenv()

# Now your environment variables are available via os.getenv
langchain_tracing = os.getenv("LANGCHAIN_TRACING_V2")
langchain_key = os.getenv("LANGCHAIN_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

# 2. Create Prompt Template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}"),
])

# 3. Create Model (will read OPENAI_API_KEY from environment)
model = ChatOpenAI(model="gpt-4")

# 4. Create Parser
parser = StrOutputParser()

# 5. Create a Chain using the pipe operator
chain = prompt_template | model | parser

# 6. Initialize FastAPI
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces"
)

# 7. Add the chain as a route
add_routes(app, chain, path="/chain")

# 8. Run with uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
