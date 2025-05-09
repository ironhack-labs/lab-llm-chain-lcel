from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

# 1. Prompt Template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. Model + Parser
model = ChatOpenAI(model="gpt-3.5-turbo")
parser = StrOutputParser()

# 3. Chain
chain = prompt_template | model | parser

# 4. FastAPI App
app = FastAPI(
    title="LangChain Translation API",
    version="1.0",
    description="Translation API using LangChain and LangServe"
)

# 5. Add Route
add_routes(app, chain, path="/chain")

# 6. Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
