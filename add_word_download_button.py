#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pridėti Word atsisiuntimo mygtuką į HTML failus
"""

from bs4 import BeautifulSoup
import re

# Straipsnių sąrašas
STRAIPSNIAI = [1, 2, 3, 4, 5, 6]

def add_download_button(html_file, straipsnis_id):
    """Pridėti atsisiuntimo mygtuką į HTML failą"""
    print(f"Atnaujiname {html_file}...")

    try:
        # Skaityti HTML failą
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        # Rasti warning div
        warning_div = soup.find('div', class_='warning')

        if warning_div:
            # Sukurti naują download mygtuką
            download_section = soup.new_tag('div', **{'class': 'download-section', 'style': 'background: #e8f5e9; border-left: 4px solid #4caf50; padding: 15px; margin: 20px 0;'})

            # Pridėti tekstą
            strong_tag = soup.new_tag('strong')
            strong_tag.string = '📥 ATSISIŲSTI WORD FORMATĄ:'
            download_section.append(strong_tag)

            download_section.append(' Galite atsisiųsti šį straipsnį Word dokumentu (.docx) redagavimui ir spausdinimui. ')

            # Pridėti mygtuką
            download_btn = soup.new_tag('a', href=f'straipsnis-{straipsnis_id}-pilnas.docx', download='', **{'class': 'download-btn', 'style': 'display: inline-block; background: #4caf50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px 0; font-weight: bold;'})
            download_btn.string = f'⬇ Atsisiųsti Word (.docx)'

            download_section.append(download_btn)

            # Įterpti po warning div
            warning_div.insert_after(download_section)

            # Išsaugoti atnaujintą HTML
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))

            print(f"✓ Sėkmingai atnaujintas {html_file}")
            return True
        else:
            print(f"⚠ Nerasta warning div {html_file}")
            return False

    except Exception as e:
        print(f"✗ Klaida: {e}")
        return False

def main():
    """Pagrindinė funkcija"""
    print("\n" + "="*70)
    print(" PRIDEDAMAS WORD ATSISIUNTIMO MYGTUKAS Į HTML FAILUS ")
    print("="*70 + "\n")

    success_count = 0

    for straipsnis_id in STRAIPSNIAI:
        html_file = f"straipsnis-{straipsnis_id}-pilnas.html"
        if add_download_button(html_file, straipsnis_id):
            success_count += 1

    print("\n" + "="*70)
    print(f" ✓ Atnaujinta {success_count}/{len(STRAIPSNIAI)} failų ")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
