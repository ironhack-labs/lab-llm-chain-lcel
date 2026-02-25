from fastapi import FastAPI
from langserve import add_routes

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI()

model = ChatOllama(model="mistral:latest", base_url="http://127.0.0.1:11434")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Translate the following from English into {language}."),
    ("human", "{text}"),
])

chain = prompt | model | StrOutputParser()

add_routes(app, chain, path="/chain")