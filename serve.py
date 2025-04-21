# app.py


from fastapi import FastAPI
from langserve import add_routes
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI



import os
os.environ["OPENAI_API_KEY"] = "my key"

app = FastAPI()

# Define the chain
system_template = "Translate the following into {language}:"
prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}"),
])
model = ChatOpenAI(model="gpt-3.5-turbo")
parser = StrOutputParser()

chain = prompt | model | parser

# Add the chain to the app
add_routes(app, chain, path="/chain")
