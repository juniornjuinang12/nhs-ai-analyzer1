# src/extractor.py

import os
import fitz  # PyMuPDF
from datetime import datetime

def log_error(message: str):
    os.makedirs("logs", exist_ok=True)
    with open("logs/errors.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")

def extract_text_from_pdf(filepath: str) -> str:
    """Extrait le texte d’un fichier PDF avec gestion d’erreurs."""
    try:
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        log_error(f"Erreur extraction {filepath} : {e}")
        print(f"[❌] Erreur lors de l’extraction de {filepath}")
        return ""
