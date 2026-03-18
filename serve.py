from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

# 1. Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Translate the following into {language}:"),
    ("user", "{text}")
])

# 2. Model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3. Chain
chain = prompt | model | StrOutputParser()

# 4. FastAPI app
app = FastAPI(
    title="LCEL Translation API",
    version="1.0",
    description="Simple LangChain LCEL app served with LangServe",
)

# 5. Route
add_routes(app, chain, path="/chain")

# 6. Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
    