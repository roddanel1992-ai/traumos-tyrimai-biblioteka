# INSTRUKCIJA: Kaip išversti straipsnį 100%

## 1. Įdiegti reikalingas bibliotekas

Atidarykite terminalą ir įvykdykite šias komandas:

```bash
cd /Users/Danel.Rod/Downloads/vertimui

# Įdiegti Python bibliotekas
pip3 install -r requirements.txt
```

## 2. Paleisti vertimo skriptą

```bash
python3 translate_pdf.py
```

## 3. Kas bus sukurta?

Skriptas sukurs 2 failus:

1. **straipsnis-6-PILNAS-VERTIMAS.txt** - Tekstinis failas su visu išverstu turiniu
2. **straipsnis-6-PILNAS-AUTO.html** - HTML svetainės puslapis su visu išverstu turiniu

## 4. Kaip veikia?

1. Skriptas nuskaito visą PDF failą (38 puslapius)
2. Išgauna tekstą iš kiekvieno puslapio
3. Naudoja Google Translate API išversti tekstą į lietuvių kalbą
4. Išsaugo rezultatus į TXT ir HTML failus

## 5. Svarbu žinoti

- Vertimas yra **automatinis**, todėl gali būti smulkių netiksumų
- Akademiniai terminai bus išversti, bet kartais gali reikėti rankinės pataisos
- Procesas gali užtrukti 10-20 minučių (38 puslapiai)
- Google Translate API yra nemokamas, bet turi limitus

## 6. Jei kyla problemų

### Problema: "ModuleNotFoundError"
**Sprendimas:** Įvykdykite:
```bash
pip3 install PyPDF2 googletrans==4.0.0rc1
```

### Problema: "googletrans stopped working"
**Sprendimas:** Pabandykite alternatyvią biblioteką:
```bash
pip3 uninstall googletrans
pip3 install googletrans==3.1.0a0
```

### Problema: Lėtas vertimas
**Sprendimas:** Tai normalu - Google Translate turi rate limiting. Skriptas automatiškai laukia tarp užklausų.

## 7. Alternatyvūs vertimo variantai

Jei Google Translate neveikia, galite naudoti:

### Variantas A: DeepL (geresnis vertimas, bet reikia API rakto)
```bash
pip3 install deepl
```

### Variantas B: Microsoft Translator (nemokamas, bet reikia registracijos)
```bash
pip3 install azure-cognitiveservices-language-translation
```

## 8. Peržiūrėti rezultatus

### TXT failas:
```bash
open straipsnis-6-PILNAS-VERTIMAS.txt
```

### HTML failas:
```bash
open straipsnis-6-PILNAS-AUTO.html
```

Arba tiesiog dvigubai spustelėkite ant failo Finder programoje.

## 9. Integruoti į esamą svetainę

Jei norite naudoti automatinį vertimą vietoje esamo failą:

```bash
# Atsargin ės kopijos sukūrimas
cp straipsnis-6-pilnas.html straipsnis-6-pilnas-BACKUP.html

# Pakeisti failą nauju vertimu
cp straipsnis-6-PILNAS-AUTO.html straipsnis-6-pilnas.html
```

## Kontaktai

Jei kyla klausimų ar problemų, patikrinkite:
- Python versija: `python3 --version` (turėtų būti 3.7+)
- Pip versija: `pip3 --version`
- Įdiegtos bibliotekos: `pip3 list | grep -E "(PyPDF2|googletrans)"`
