import streamlit as st
import os
import json
from dotenv import load_dotenv

# === Importer ton code existant ===
from src.scraper import extract_pdf_links
from src.downloader import download_pdf
from src.extractor import extract_text_from_pdf
from src.analyzer import analyze_text

load_dotenv()

st.set_page_config(page_title="NHS AI Analyzer", layout="centered")
st.title("🤖 NHS AI Analyzer")
st.markdown("Analyse automatique des rapports PDF des hôpitaux avec IA.")

# === Interface utilisateur ===
with st.form("url_form"):
    url = st.text_input("🔗 URL d’un hôpital (ex: https://www.nhshospital.org/...)")
    submitted = st.form_submit_button("Lancer l'analyse")

if submitted and url:
    with st.spinner("🔍 Scraping des PDFs..."):
        pdfs = extract_pdf_links(url)

    if pdfs:
        st.success(f"{len(pdfs)} PDF(s) trouvés.")
        report = []

        for i, pdf_url in enumerate(pdfs[:3]):
            with st.spinner(f"Téléchargement du PDF {i+1}..."):
                download_pdf(pdf_url)

        with st.spinner("🔎 Extraction et analyse IA en cours..."):
            for filename in os.listdir("pdfs")[:3]:
                if filename.endswith(".pdf"):
                    filepath = os.path.join("pdfs", filename)
                    text = extract_text_from_pdf(filepath)
                    summary = analyze_text(text)
                    report.append({
                        "filename": filename,
                        "summary": summary
                    })

        st.success("✅ Analyse terminée")
        st.json(report)

        # Option de téléchargement
        st.download_button("📥 Télécharger le rapport JSON", json.dumps(report, indent=2, ensure_ascii=False), "report.json")
    else:
        st.warning("Aucun PDF trouvé sur cette page.")
