import requests
from app.config import OPENCLAW_URL

def ask_llm(prompt):
    res = requests.post(
        OPENCLAW_URL,
        json={"prompt": prompt}
    )
    return res.json()["response"]
