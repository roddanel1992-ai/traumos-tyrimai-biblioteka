#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universalus PDF vertimo skriptas - Išversti visus straipsnius
"""

import PyPDF2
import time
from deep_translator import GoogleTranslator
import sys
import re
import json

# Straipsnių duomenys
STRAIPSNIAI = [
    {
        "id": 1,
        "pdf_file": "2_Istorija_Trauma research in the Baltic countries-1.pdf",
        "pavadinimas": "Traumos tyrimai Baltijos šalyse: nuo politinio engimo iki atsigavimo",
        "autoriai": "Evaldas Kazlauskas ir Paulina Zelvienė",
        "original_title": "Trauma research in the Baltic countries: From political oppression to recovery"
    },
    {
        "id": 2,
        "pdf_file": "7_Trauma tarp kartu_Dashorst et al..pdf",
        "pavadinimas": "Holokausto tarpkartinės pasekmės palikuonių psichinei sveikatai",
        "autoriai": "Patricia Dashorst, Trudy M. Mooren, Rolf J. Kleber, Peter J. de Jong & Rafaele J. C. Huntjens",
        "original_title": "Intergenerational consequences of the Holocaust on offspring mental health"
    },
    {
        "id": 3,
        "pdf_file": "8_Posttraumatic Growth Conceptual Foundations and Empirical Evidence, Tedeschi and Calhoun.pdf",
        "pavadinimas": "Potrauminis augimas: koncepciniai pagrindai ir empiriniai įrodymai",
        "autoriai": "Richard G. Tedeschi ir Lawrence G. Calhoun",
        "original_title": "Posttraumatic Growth: Conceptual Foundations and Empirical Evidence"
    },
    {
        "id": 4,
        "pdf_file": "9_Pagalbos budai PTSS_Schnyder et al..pdf",
        "pavadinimas": "Psichoterapijos metodai PTSS gydymui: kas jiems bendra?",
        "autoriai": "Ulrich Schnyder, Anke Ehlers, Thomas Elbert, et al.",
        "original_title": "Psychotherapies for PTSD: what do they have in common?"
    },
    {
        "id": 5,
        "pdf_file": "10_Pagalbos budai ir issukiai_Kazlauskas.pdf",
        "pavadinimas": "Sveikatos priežiūros teikimo traumuotoms populiacijoms iššūkiai",
        "autoriai": "Evaldas Kazlauskas",
        "original_title": "Challenges for providing health care to traumatized populations"
    }
]

def extract_text_from_pdf(pdf_path):
    """Išgauti tekstą iš PDF failo"""
    print(f"Skaitomas PDF failas: {pdf_path}")
    text_by_page = []

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            print(f"Rasta puslapių: {total_pages}")

            for page_num in range(total_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                text_by_page.append({
                    'page': page_num + 1,
                    'text': text
                })
                print(f"Puslapio {page_num + 1}/{total_pages} tekstas išgautas ({len(text)} simbolių)")
    except Exception as e:
        print(f"Klaida skaitant PDF: {e}")
        return None

    return text_by_page

def clean_text(text):
    """Išvalyti tekstą prieš vertimą"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_into_chunks(text, max_length=4500):
    """Padalinti tekstą į gabalus"""
    if len(text) <= max_length:
        return [text]

    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 < max_length:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def translate_text(text, retry=3):
    """Išversti tekstą su retry logika"""
    if not text or not text.strip():
        return ""

    for attempt in range(retry):
        try:
            if attempt > 0:
                time.sleep(2)

            translator = GoogleTranslator(source='en', target='lt')
            result = translator.translate(text)
            time.sleep(0.5)
            return result

        except Exception as e:
            print(f"  ⚠ Vertimo klaida (bandymas {attempt + 1}/{retry}): {str(e)[:100]}")
            if attempt < retry - 1:
                wait_time = (attempt + 1) * 2
                print(f"  Laukiama {wait_time}s prieš kitą bandymą...")
                time.sleep(wait_time)
            else:
                return f"[KLAIDA: {text[:50]}...]"

    return text

def translate_pdf_content(text_by_page):
    """Išversti visą PDF turinį"""
    translated_pages = []

    total_pages = len(text_by_page)
    start_time = time.time()

    for page_data in text_by_page:
        page_num = page_data['page']
        text = page_data['text']

        print(f"\n{'─'*70}")
        print(f" Puslapis {page_num}/{total_pages}")
        print(f"{'─'*70}")

        cleaned_text = clean_text(text)

        if not cleaned_text or len(cleaned_text) < 20:
            print(f"⊘ Puslapis {page_num} tuščias arba per trumpas, praleidžiamas")
            continue

        print(f"📄 Originalaus teksto ilgis: {len(cleaned_text)} simbolių")

        chunks = split_into_chunks(cleaned_text)
        print(f"✂  Tekstas padalintas į {len(chunks)} gabalų")

        translated_chunks = []
        for i, chunk in enumerate(chunks):
            chunk_len = len(chunk)
            print(f"  [{i+1}/{len(chunks)}] Verčiamas gabalas ({chunk_len} simb.)...", end=" ")

            translated_chunk = translate_text(chunk)
            translated_chunks.append(translated_chunk)

            print(f"✓ ({len(translated_chunk)} simb.)")

        translated_page_text = " ".join(translated_chunks)

        translated_pages.append({
            'page': page_num,
            'original': text,
            'translated': translated_page_text
        })

        elapsed = time.time() - start_time
        avg_time = elapsed / page_num if page_num > 0 else 0
        remaining = (total_pages - page_num) * avg_time

        print(f"✓ Puslapis {page_num} baigtas | Iš viso: {len(translated_page_text)} simbolių")
        print(f"⏱  Praėjo: {elapsed/60:.1f}min | Liko ~{remaining/60:.1f}min")

    return translated_pages

def create_html_output(translated_pages, straipsnis_info, output_html):
    """Sukurti HTML failą su vertimu"""
    print(f"\n{'─'*70}")
    print(f" Kuriamas HTML failas {output_html}")
    print(f"{'─'*70}")

    html_content = f"""<!DOCTYPE html>
<html lang="lt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{straipsnis_info['pavadinimas']} - PILNAS VERTIMAS 100%</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {{ font-family: 'Georgia', 'Times New Roman', serif; }}
        .pilnas-straipsnis {{
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.8;
        }}
        .page-section {{
            margin-bottom: 35px;
            padding: 25px;
            background: #fafafa;
            border-left: 5px solid #3498db;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .page-number {{
            font-weight: bold;
            color: #3498db;
            font-size: 0.9em;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }}
        h2 {{
            color: #e74c3c;
            margin-top: 10px;
        }}
        .meta-info {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            margin: 25px 0;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .meta-info strong {{ color: #fff; }}
        .meta-info a {{ color: #ffd700; text-decoration: none; }}
        .warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
        }}
        .page-text {{
            text-align: justify;
            line-height: 1.9;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Traumos Tyrimai Baltijos Šalyse</h1>
            <p class="tagline">Mokslinių straipsnių biblioteka</p>
        </div>
    </header>

    <main class="container">
        <a href="straipsnis.html?id={straipsnis_info['id']}" class="back-btn">← Grįžti į santrauką</a>
        <a href="index.html" class="back-btn">← Grįžti į pagrindinį</a>

        <article class="pilnas-straipsnis">
            <h1>{straipsnis_info['pavadinimas']}</h1>
            <h2>PILNAS AUTOMATINIS VERTIMAS (100%)</h2>

            <div class="meta-info">
                <p><strong>Originalus pavadinimas:</strong> {straipsnis_info['original_title']}</p>
                <p><strong>Autoriai:</strong> {straipsnis_info['autoriai']}</p>
                <p><strong>PDF:</strong> <a href="{straipsnis_info['pdf_file']}" target="_blank">Originalus PDF</a></p>
                <p><strong>Vertimo data:</strong> {time.strftime('%Y m. %B %d d.')}</p>
                <p><strong>Vertimo metodas:</strong> Google Translate API (deep-translator)</p>
            </div>

            <div class="warning">
                <strong>⚠ SVARBI PASTABA:</strong> Tai yra automatinis vertimas naudojant Google Translate.
                Akademiniai terminai ir sudėtingos frazės gali būti išversti ne visai tiksliai.
                Svarbiems teiginiams rekomenduojama pasitikrinti su originaliuoniu PDF failu.
            </div>
"""

    for page_data in translated_pages:
        translated_text = page_data['translated']
        if '[KLAIDA:' in translated_text:
            translated_text = translated_text.replace('[KLAIDA:', '<span style="color: red;">[VERTIMO KLAIDA:</span>')

        html_content += f"""
            <div class="page-section">
                <div class="page-number">📄 Originalus puslapis {page_data['page']}</div>
                <div class="page-text">{translated_text}</div>
            </div>
"""

    html_content += f"""
            <div class="meta-info" style="margin-top: 50px;">
                <h3>Apie šį vertimą</h3>
                <p>Šis vertimas buvo sukurtas automatiškai naudojant Google Translate API.</p>
                <p>Iš viso išversta <strong>{len(translated_pages)} puslapių</strong> akademinio teksto.</p>
                <p>Vertimas apima visą straipsnio turinį.</p>
            </div>

        </article>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 Traumos Tyrimai Baltijos Šalyse | Automatinis vertimas</p>
        </div>
    </footer>
</body>
</html>
"""

    try:
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ HTML failas sėkmingai sukurtas!")
    except Exception as e:
        print(f"✗ Klaida kuriant HTML: {e}")

def translate_article(straipsnis_info):
    """Išversti vieną straipsnį"""
    base_dir = "/Users/Danel.Rod/Downloads/vertimui"
    pdf_path = f"{base_dir}/{straipsnis_info['pdf_file']}"
    output_html = f"{base_dir}/straipsnis-{straipsnis_info['id']}-pilnas.html"

    print("\n" + "="*70)
    print(f" STRAIPSNIS {straipsnis_info['id']}: {straipsnis_info['pavadinimas']}")
    print("="*70)
    print(f"\n📁 PDF failas: {pdf_path}")
    print(f"🌐 Išvesties HTML: {output_html}")
    print("\n" + "="*70 + "\n")

    # 1. Išgauti tekstą iš PDF
    text_by_page = extract_text_from_pdf(pdf_path)

    if not text_by_page:
        print("✗ Nepavyko išgauti teksto iš PDF!")
        return False

    # 2. Išversti turinį
    print("\n" + "="*70)
    print(" PRADEDAMAS PILNAS 100% VERTIMAS ")
    print("="*70 + "\n")

    translated_pages = translate_pdf_content(text_by_page)

    # 3. Sukurti HTML failą
    create_html_output(translated_pages, straipsnis_info, output_html)

    print("\n" + "="*70)
    print(f" ✓✓✓ STRAIPSNIS {straipsnis_info['id']} SĖKMINGAI IŠVERSTAS! ✓✓✓ ")
    print("="*70)
    print(f"\n📊 Statistika:")
    print(f"   • Išversta puslapių: {len(translated_pages)}")
    total_chars = sum(len(p['translated']) for p in translated_pages)
    print(f"   • Iš viso simbolių: {total_chars:,}")
    print(f"\n📂 Sukurtas failas: {output_html}")
    print("\n")

    return True

def main():
    """Pagrindinė funkcija - išversti visus straipsnius"""
    print("\n" + "="*70)
    print(" VISŲ STRAIPSNIŲ VERTIMAS - 100% TURINYS ")
    print("="*70)
    print(f"\nIš viso straipsnių vertimui: {len(STRAIPSNIAI)}")
    print("="*70 + "\n")

    start_time = time.time()
    success_count = 0
    failed = []

    for straipsnis in STRAIPSNIAI:
        try:
            if translate_article(straipsnis):
                success_count += 1
            else:
                failed.append(straipsnis['id'])
        except Exception as e:
            print(f"✗ KLAIDA verčiant straipsnį {straipsnis['id']}: {e}")
            failed.append(straipsnis['id'])

    total_time = time.time() - start_time

    print("\n" + "="*70)
    print(" ✓✓✓ VISŲ STRAIPSNIŲ VERTIMAS BAIGTAS! ✓✓✓ ")
    print("="*70)
    print(f"\n📊 Galutinė statistika:")
    print(f"   • Sėkmingai išversta: {success_count}/{len(STRAIPSNIAI)}")
    if failed:
        print(f"   • Nepavyko: {', '.join(map(str, failed))}")
    print(f"   • Bendras laikas: {total_time/60:.1f} minutės")
    print("\n")

if __name__ == "__main__":
    main()
