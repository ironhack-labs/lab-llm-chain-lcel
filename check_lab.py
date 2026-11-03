"""Check the real prompt, parser, and API without paid model calls."""
import os
from unittest.mock import patch

from fastapi.testclient import TestClient
from langchain_core.language_models.fake_chat_models import FakeListChatModel


def main():
    os.environ["LANGCHAIN_TRACING_V2"] = "false"
    fake = FakeListChatModel(responses=["Buonasera, come stai?"])
    with patch("langchain_openai.ChatOpenAI", return_value=fake):
        import serve

    payload = {"language": "italian", "text": "Good evening, how are you?"}
    messages = serve.prompt_template.invoke(payload).to_messages()
    assert messages[0].content == "Translate the following into italian:"
    assert messages[1].content == payload["text"]
    assert serve.chain.invoke(payload) == "Buonasera, come stai?"
    with TestClient(serve.app) as client:
        for path in ["/docs", "/openapi.json", "/chain/input_schema", "/chain/playground/"]:
            response = client.get(path)
            assert response.status_code == 200, (path, response.status_code)
        response = client.post("/chain/invoke", json={"input": payload})
        assert response.status_code == 200, response.text
        assert response.json()["output"] == "Buonasera, come stai?"
        response = client.post("/chain/batch", json={"inputs": [payload, payload]})
        assert response.status_code == 200, response.text
        assert response.json()["output"] == ["Buonasera, come stai?"] * 2
    print("PASS: prompt formatting, chain, API invoke/batch, schemas, docs, playground")
    print("Uses a fake model; live OpenAI and LangSmith still require verification.")


if __name__ == "__main__":
    main()
