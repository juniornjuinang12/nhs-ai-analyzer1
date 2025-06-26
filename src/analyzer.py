# src/analyzer.py

import os
import datetime
from dotenv import load_dotenv
from together import Together

load_dotenv()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

LOG_PATH = "logs/ai_errors.log"
os.makedirs("logs", exist_ok=True)

def log_ai_error(message: str):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def analyze_text(text: str, max_words: int = 1500) -> str:
    """Résume et extrait les points clés depuis un texte brut PDF."""

    prompt = f"""
Tu es un expert en lecture de documents hospitaliers. Résume et analyse ce texte (en français) :
{text[:max_words]}
Donne-moi les points clés et décisions importantes.
"""

    try:
        response = client.chat.completions.create(
            model="togethercomputer/llama-3-8b-chat",
            messages=[
                {"role": "system", "content": "Tu es un assistant d’analyse de documents PDF hospitaliers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        result = response.choices[0].message.content.strip()
        log_ai_error("✅ Succès pour un appel AI.")
        return result

    except Exception as e:
        log_ai_error(f"❌ Erreur AI : {e}")
        return f"[❌ Erreur Together API] {e}"
