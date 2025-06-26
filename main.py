# main.py

# main.py

import os
from dotenv import load_dotenv
load_dotenv()  # Charge les variables d’environnement avant les imports dépendants

import json
from src.scraper import extract_pdf_links
from src.downloader import download_pdf
from src.extractor import extract_text_from_pdf
from src.analyzer import analyze_text


def load_urls(filepath: str) -> list[str]:
    with open(filepath, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    urls = load_urls("config/hospitals.json")
    
    for url in urls:
        print(f"\n🔍 Scraping : {url}")
        pdfs = extract_pdf_links(url)
        
        if pdfs:
            print(f"📄 PDFs trouvés ({len(pdfs)}) :\n")
            for pdf in pdfs:
                download_pdf(pdf)
        else:
            print("⚠️ Aucun PDF trouvé.")

    # ✅ Ce bloc doit être ici, en dehors de la boucle et du else
    # 🔎 Extraction du texte des fichiers téléchargés + Analyse AI
print("\n🔎 Extraction et analyse des fichiers téléchargés :")

pdf_folder = "pdfs"
report = []

for filename in os.listdir(pdf_folder)[:3]:  # Analyser seulement 3 fichiers
    if filename.endswith(".pdf"):
        filepath = os.path.join(pdf_folder, filename)
        text = extract_text_from_pdf(filepath)
        
        print(f"\n--- {filename} ---")
        print(f"[📄] Texte brut : {text[:400]}...\n")

        summary = analyze_text(text)
        print(f"[🤖] Résumé AI :\n{summary}\n")

        report.append({
            "filename": filename,
            "summary": summary
        })

# 💾 Sauvegarde dans un fichier JSON
with open("report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print("\n📁 Rapport final enregistré dans : report.json ✅")
