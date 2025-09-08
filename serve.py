#!/usr/bin/env python
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}")
])

# 2. Create model
model = ChatOpenAI()

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain by chaining prompt_template, model, and parser
chain = prompt_template | model | parser

# 5. Create FastAPI app
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

# 6. Add routes to serve the chain at /chain endpoint
add_routes(
    app,
    chain,
    path="/chain",
)

# 7. Run server with uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)