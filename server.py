from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langserve import add_routes  # Changed from add_routes to add_route

# Create a FastAPI app
app = FastAPI()

# Create a simple chain
prompt = ChatPromptTemplate.from_template("Translate this text to {language}: {text}")
model = ChatOllama(model="llama2")
chain = prompt | model | StrOutputParser()

# Add the chain to the server using add_route instead of add_routes
add_routes(app, chain, path="/chain")

# Add a simple health check route
@app.get("/")
async def health_check():
    return {"status": "ok"}