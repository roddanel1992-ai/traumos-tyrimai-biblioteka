#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Translation Script - Išversti akademinį straipsnį iš anglų į lietuvių kalbą
Naudoja Google Translate API per googletrans biblioteką
"""

import PyPDF2
import time
from googletrans import Translator
import sys
import re

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
                print(f"Puslapio {page_num + 1}/{total_pages} tekstas išgautas")
    except Exception as e:
        print(f"Klaida skaitant PDF: {e}")
        sys.exit(1)

    return text_by_page

def clean_text(text):
    """Išvalyti tekstą prieš vertimą"""
    # Pašalinti perteklinius tarpus
    text = re.sub(r'\s+', ' ', text)
    # Pašalinti puslapio numerius
    text = re.sub(r'\n\d+\s+C\.R\. Brewin.*?\n', '\n', text)
    return text.strip()

def split_into_chunks(text, max_length=4500):
    """
    Padalinti tekstą į gabalus (Google Translate limitas ~5000 simbolių)
    Stengiamės padalinti pagal sakinius
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_length:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def translate_text(text, translator, src='en', dest='lt', retry=3):
    """Išversti tekstą su retry logika"""
    for attempt in range(retry):
        try:
            # Google Translate turi limitą, todėl dedame delay
            time.sleep(1)

            if not text.strip():
                return ""

            result = translator.translate(text, src=src, dest=dest)
            return result.text
        except Exception as e:
            print(f"Vertimo klaida (bandymas {attempt + 1}/{retry}): {e}")
            if attempt < retry - 1:
                time.sleep(3)  # Laukti prieš retry
            else:
                return f"[VERTIMO KLAIDA: {text[:100]}...]"

    return text  # Grąžinti originalą jei nepavyko

def translate_pdf_content(text_by_page, output_file):
    """Išversti visą PDF turinį"""
    translator = Translator()
    translated_pages = []

    print("\n" + "="*60)
    print("PRADEDAMAS VERTIMAS")
    print("="*60 + "\n")

    total_pages = len(text_by_page)

    for page_data in text_by_page:
        page_num = page_data['page']
        text = page_data['text']

        print(f"\n--- Verčiamas puslapis {page_num}/{total_pages} ---")

        # Išvalyti tekstą
        cleaned_text = clean_text(text)

        if not cleaned_text:
            print(f"Puslapis {page_num} tuščias, praleidžiamas")
            continue

        # Padalinti į gabalus
        chunks = split_into_chunks(cleaned_text)
        print(f"Tekstas padalintas į {len(chunks)} gabalus")

        translated_chunks = []
        for i, chunk in enumerate(chunks):
            print(f"  Verčiamas gabalas {i+1}/{len(chunks)} ({len(chunk)} simbolių)...")
            translated_chunk = translate_text(chunk, translator)
            translated_chunks.append(translated_chunk)

        # Sujungti išverstus gabalus
        translated_page_text = " ".join(translated_chunks)

        translated_pages.append({
            'page': page_num,
            'original': text,
            'translated': translated_page_text
        })

        print(f"✓ Puslapis {page_num} išverstas ({len(translated_page_text)} simbolių)")

    # Išsaugoti rezultatus
    save_translation(translated_pages, output_file)

    return translated_pages

def save_translation(translated_pages, output_file):
    """Išsaugoti vertimą į failą"""
    print(f"\n--- Saugomas vertimas į {output_file} ---")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("AKADEMINIO STRAIPSNIO VERTIMAS IŠ ANGLŲ Į LIETUVIŲ KALBĄ\n")
            f.write("Straipsnis: Psychological theories of posttraumatic stress disorder\n")
            f.write("Autoriai: Chris R. Brewin, Emily A. Holmes\n")
            f.write("Šaltinis: Clinical Psychology Review 23 (2003) 339-376\n")
            f.write("="*80 + "\n\n")

            for page_data in translated_pages:
                f.write(f"\n{'='*80}\n")
                f.write(f"PUSLAPIS {page_data['page']}\n")
                f.write(f"{'='*80}\n\n")
                f.write(page_data['translated'])
                f.write("\n\n")

        print(f"✓ Vertimas sėkmingai išsaugotas!")

    except Exception as e:
        print(f"Klaida saugant failą: {e}")

def create_html_output(translated_pages, output_html):
    """Sukurti HTML failą su vertimu"""
    print(f"\n--- Kuriamas HTML failas {output_html} ---")

    html_content = """<!DOCTYPE html>
<html lang="lt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Psichologinės potrauminio streso sutrikimo teorijos - PILNAS VERTIMAS</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        .pilnas-straipsnis {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.8;
        }
        .page-section {
            margin-bottom: 40px;
            padding: 20px;
            background: #f9f9f9;
            border-left: 4px solid #3498db;
        }
        .page-number {
            font-weight: bold;
            color: #3498db;
            margin-bottom: 15px;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        .meta-info {
            background: #e8f4f8;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
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
        <a href="straipsnis.html?id=6" class="back-btn">← Grįžti į santrauką</a>
        <a href="index.html" class="back-btn">← Grįžti į pagrindinį</a>

        <article class="pilnas-straipsnis">
            <h1>Psichologinės potrauminio streso sutrikimo teorijos</h1>
            <h2>PILNAS AUTOMATINIS VERTIMAS</h2>

            <div class="meta-info">
                <p><strong>Autoriai:</strong> Chris R. Brewin ir Emily A. Holmes</p>
                <p><strong>Šaltinis:</strong> Clinical Psychology Review 23 (2003) 339-376</p>
                <p><strong>DOI:</strong> <a href="https://doi.org/10.1016/S0272-7358(03)00033-3" target="_blank">10.1016/S0272-7358(03)00033-3</a></p>
                <p><strong>Vertimo data:</strong> 2026 sausio 16 d.</p>
                <p><strong>Vertimo metodas:</strong> Google Translate API (automatinis vertimas)</p>
                <p style="color: #d35400;"><strong>Pastaba:</strong> Tai yra automatinis vertimas. Rekomenduojama palyginti su originalu svarbių dalių atveju.</p>
            </div>
"""

    for page_data in translated_pages:
        html_content += f"""
            <div class="page-section">
                <div class="page-number">Puslapis {page_data['page']}</div>
                <p>{page_data['translated']}</p>
            </div>
"""

    html_content += """
        </article>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 Traumos Tyrimai Baltijos Šalyse</p>
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
        print(f"Klaida kuriant HTML: {e}")

def main():
    """Pagrindinė funkcija"""
    # Nustatymai
    pdf_path = "/Users/Danel.Rod/Downloads/vertimui/6_PTSS teorijos_Brewin, Holmes.pdf"
    output_txt = "/Users/Danel.Rod/Downloads/vertimui/straipsnis-6-PILNAS-VERTIMAS.txt"
    output_html = "/Users/Danel.Rod/Downloads/vertimui/straipsnis-6-PILNAS-AUTO.html"

    print("\n" + "="*80)
    print("AKADEMINIO STRAIPSNIO VERTIMAS - 100% TURINYS")
    print("="*80)
    print(f"\nPDF failas: {pdf_path}")
    print(f"Išvesties TXT: {output_txt}")
    print(f"Išvesties HTML: {output_html}")
    print("\n" + "="*80 + "\n")

    # 1. Išgauti tekstą iš PDF
    text_by_page = extract_text_from_pdf(pdf_path)

    if not text_by_page:
        print("Nepavyko išgauti teksto iš PDF!")
        sys.exit(1)

    # 2. Išversti turinį
    translated_pages = translate_pdf_content(text_by_page, output_txt)

    # 3. Sukurti HTML failą
    create_html_output(translated_pages, output_html)

    print("\n" + "="*80)
    print("VERTIMAS BAIGTAS!")
    print("="*80)
    print(f"\n✓ Išversta puslapių: {len(translated_pages)}")
    print(f"✓ Tekstinis failas: {output_txt}")
    print(f"✓ HTML failas: {output_html}")
    print("\nGalite atidaryti HTML failą naršyklėje arba skaityti TXT failą.\n")

if __name__ == "__main__":
    main()
