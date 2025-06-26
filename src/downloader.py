# src/downloader.py

import os
import requests

def log_error(message: str):
    os.makedirs("logs", exist_ok=True)
    with open("logs/errors.log", "a", encoding="utf-8") as f:
        f.write(message + "\n")

def download_pdf(url: str, output_dir: str = "pdfs") -> str:
    """Télécharge un PDF depuis une URL et le sauvegarde dans 'pdfs/'."""
    os.makedirs(output_dir, exist_ok=True)

    filename = url.split("/")[-1].split("?")[0]
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        print(f"[⏭️] Déjà existant : {filename}")
        return filepath

    for attempt in range(2):  # Essaye deux fois max
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"[✅] Téléchargé : {filename}")
            return filepath
        except Exception as e:
            print(f"[⚠️] Tentative {attempt + 1} échouée pour : {url}")
            last_error = f"[❌] {url} → {e}"

    log_error(last_error)
    return ""
