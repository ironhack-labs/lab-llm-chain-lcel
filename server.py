from dotenv import load_dotenv
load_dotenv(override=True)

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

# Prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}")
])

# Model
model = ChatOpenAI(model="gpt-4o-mini")

# Parser
parser = StrOutputParser()

# Chain
chain = prompt_template | model | parser

# FastAPI app
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Simple API server using LangChain Runnable interfaces",
)

# Add route
add_routes(
    app,
    chain,
    path="/chain",
)

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)