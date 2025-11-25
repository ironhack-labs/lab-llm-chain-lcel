#!/usr/bin/env python

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# 1. Prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. Model
model = ChatOpenAI(model="gpt-3.5-turbo")

# 3. Parser
parser = StrOutputParser()

# 4. Full chain
chain = prompt_template | model | parser

# 5. FastAPI server
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Local LCEL + LangServe app"
)

# 6. Add route
add_routes(app, chain, path="/chain")

# 7. Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
