# LCEL — utilisation

1. Installer les dépendances : `python -m pip install -r requirements.txt`.
2. Exécuter le notebook : le mode `offline` teste les vrais composants LCEL avec quatre traductions prédéfinies, clairement identifiées comme doublures de test.
3. Pour traduire librement : copier `.env.example` vers `.env`, renseigner `OPENAI_API_KEY` et choisir `LAB_MODE=openai`. Redémarrer le noyau et choisir également `MODE = "openai"` dans le notebook.
4. Serveur : `python serve.py`, puis ouvrir http://127.0.0.1:8000/chain/playground/.
5. Dans le notebook, activer `RUN_REMOTE=True` une fois le serveur lancé.
6. Tests : `python -m unittest -v test_translation.py`.

LangSmith est facultatif. Pour enregistrer de vraies traces, renseigner `LANGCHAIN_API_KEY` et passer `LANGCHAIN_TRACING_V2=true` dans `.env`. Les latences et consommations de tokens ne sont pas inventées dans le résumé du notebook.

Documentation : https://github.com/langchain-ai/langserve et https://docs.langchain.com/oss/python/langchain/models.
