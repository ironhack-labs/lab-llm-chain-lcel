from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser  # Use StrOutputParser instead
from langchain_openai import ChatOpenAI
from langserve import add_routes
from fastapi import FastAPI
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

OPENAI_API_KEY  = os.getenv('OPENAI_API_KEY')

# Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# Create model
model = ChatOpenAI(model='gpt-4o-mini')

# Create parser using StrOutputParser
parser = StrOutputParser()  # Use StrOutputParser instead of RetryOutputParser

# Create chain
chain = prompt_template | model | parser

# FastAPI app definition
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

# Adding chain route
add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)