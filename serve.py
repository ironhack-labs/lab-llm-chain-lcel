#!/usr/bin/env python
"""Run with python serve.py; use LAB_MODE=openai for real translations."""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from langserve import add_routes
from translation import build_chain

class TranslationInput(BaseModel):
    language: str = Field(min_length=1, max_length=100)
    text: str = Field(min_length=1, max_length=10000)

def create_app(mode=None):
    app = FastAPI(title='LCEL Translation Lab', version='1.0', description='Prompt → model → string. Default mode uses a documented offline test double.')
    chain = build_chain(mode).with_types(input_type=TranslationInput, output_type=str)
    add_routes(app, chain, path='/chain')
    return app

app = create_app()
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
