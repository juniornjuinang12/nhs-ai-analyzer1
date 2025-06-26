import json
import re

def format_bold_stars(text: str) -> str:
    # Remplace **texte** par <strong>texte</strong>
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

def generate_html_report(json_path="report.json"):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ Lecture réussie : {json_path}")
    except FileNotFoundError:
        print("❌ Fichier report.json introuvable.")
        return

    html_content = """
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Rapport AI PDF</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background-color: #f5f7fa;
                color: #333;
                padding: 30px;
                display: flex;
                justify-content: center;
            }
            .wrapper {
                max-width: 1200px;
                width: 100%;
            }
            .container {
                display: flex;
                flex-wrap: wrap;
                gap: 30px;
                justify-content: center;
            }
            .card {
                background: white;
                border: 1px solid #ddd;
                border-radius: 16px;
                padding: 24px;
                box-shadow: 0 10px 24px rgba(0,0,0,0.1);
                width: 90%;
                max-width: 1000px;
                transition: transform 0.3s;
            }
            .card:hover {
                transform: translateY(-6px);
            }
            .filename {
                font-size: 1.2rem;
                font-weight: bold;
                color: #4a4a4a;
                margin-bottom: 12px;
            }
            .summary {
                background-color: #eaf4fe;
                padding: 18px;
                border-left: 4px solid #0077cc;
                border-radius: 10px;
                white-space: pre-line;
                font-size: 1rem;
                line-height: 1.7;
            }
        </style>
    </head>
    <body>
        <div class="wrapper">
        <h1>📑 Rapport d’analyse des fichiers PDF</h1>
        <div class="container">
    """

    for item in data:
        formatted_summary = format_bold_stars(item["summary"])
        html_content += f"""
        <div class="card">
            <div class="filename">📂 {item['filename']}</div>
            <div class="summary">🧠 <strong>Résumé :</strong><br>{formatted_summary}</div>
        </div>
        """

    html_content += """
        </div>
        </div>
    </body>
    </html>
    """

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ Fichier HTML stylisé généré : report.html")

if __name__ == "__main__":
    generate_html_report()
