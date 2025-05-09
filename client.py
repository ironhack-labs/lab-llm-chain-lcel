from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://localhost:8000/chain/")

response = remote_chain.invoke({
    "language": "italian",
    "text": "Hello! How are you doing today?"
})
print("Example Translation:", response)
print("-" * 50)
print("Welcome to the Language Translator (powered by LangChain + LangServe)")
print("Type 'exit' to quit\n")

while True:
    text = input("Enter a sentence in English: ")
    if text.lower() == "exit":
        break

    language = input("Translate to (e.g. Arabic, Italian, French): ")
    if language.lower() == "exit":
        break

    response = remote_chain.invoke({
        "language": language,
        "text": text
    })

    print(f"Translation ({language.title()}): {response}\n")
