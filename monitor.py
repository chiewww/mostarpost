import re
import urllib.request
from pathlib import Path

PDF_URL = "https://www.post.ba/media/files/POPIS%20DR%C5%BDAVA%20MEDJ%20PROMET%2013_12_2023.pdf"
OUTPUT_FILE = Path("output.txt")
PDF_FILE = Path("mostar_post.pdf")


# -------------------------------------------------------------------
# Postcrossing country/territory numbers
# -------------------------------------------------------------------

POSTCROSSING = {
    "AFGANISTAN": (1, "Afghanistan"),
    "ALBANIJA": (3, "Albania"),
    "ALŽIR": (4, "Algeria"),
    "AMERIČKA SAMOA": (5, "American Samoa"),
    "ANDORA": (6, "Andorra"),
    "ANGOLA": (7, "Angola"),
    "ANGVILA": (8, "Anguilla"),
    "ANTIGVA I BARBUDA": (10, "Antigua & Barbuda"),
    "ARGENTINA": (11, "Argentina"),
    "ARMENIJA": (12, "Armenia"),
    "ARUBA": (13, "Aruba"),
    "ASENŠN": (185, "Saint Helena, Ascension and Tristan da Cunha"),
    "AUSTRALIJA": (14, "Australia"),
    "AUSTRIJA": (15, "Austria"),
    "AZERBEJDŽAN": (16, "Azerbaijan"),
    "BAHAMI": (17, "Bahamas"),
    "BAHREIN": (18, "Bahrain"),
    "BANGLADEŠ": (19, "Bangladesh"),
    "BARBADOS": (20, "Barbados"),
    "BJELORUSIJA": (21, "Belarus"),
    "BELGIJA": (22, "Belgium"),
    "BELIZE": (23, "Belize"),
    "BENIN": (24, "Benin"),
    "BERMUDA": (25, "Bermuda"),
    "BUTAN": (26, "Bhutan"),
    "BOLIVIJA": (27, "Bolivia"),
    "BOSNA I HERCEGOVINA": (29, "Bosnia-Herzegovina"),
    "BOCVANA": (30, "Botswana"),
    "BRAZIL": (31, "Brazil"),
    "BRITANSKI DJEVIČANSKI OTOCI": (242, "Virgin Islands (UK)"),
    "BRUNEJ DARUSSALAM": (33, "Brunei"),
    "BUGARSKA": (34, "Bulgaria"),
    "BURKINA FASO": (35, "Burkina Faso"),
    "BURUNDI": (36, "Burundi"),
    "KABO VERDE": (37, "Cabo Verde"),
    "KAMBODŽA": (38, "Cambodia"),
    "KAMERUN": (39, "Cameroon"),
    "KANADA": (40, "Canada"),
    "ČAD": (43, "Chad"),
    "ČILE": (44, "Chile"),
    "KINA": (45, "China"),
    "KOKOSOVI OTOCI": (47, "Cocos Islands"),
    "KOLUMBIJA": (48, "Colombia"),
    "KOMORI": (49, "Comoros"),
    "KONGO": (50, "Congo"),
    "DEMOKRATSKA REPUBLIKA KONGO": (51, "Dem. Rep. Of Congo"),
    "KUKOVI OTOCI": (52, "Cook Islands"),
    "KOSTARIKA": (53, "Costa Rica"),
    "BJELOKOSNA OBALA": (54, "Côte d'Ivoire"),
    "HRVATSKA": (55, "Croatia"),
    "KUBA": (56, "Cuba"),
    "CURAÇAO": (57, "Curaçao"),
    "CIPAR": (58, "Cyprus"),
    "ČEŠKA REPUBLIKA": (59, "Czechia"),
    "DANSKA": (60, "Denmark"),
    "DŽIBUTI": (61, "Djibouti"),
    "DOMINIKA": (62, "Dominica"),
    "DOMINIKANSKA REPUBLIKA": (63, "Dominican Republic"),
    "EKVADOR": (64, "Ecuador"),
    "EGIPAT": (65, "Egypt"),
    "SALVADOR": (66, "El Salvador"),
    "EKVATORSKA GVINEJA": (67, "Equatorial Guinea"),
    "ERITREJA": (68, "Eritrea"),
    "ESTONIJA": (69, "Estonia"),
    "ESVATINI": (70, "Eswatini /Swaziland"),
    "ETIOPIJA": (71, "Ethiopia"),
    "FAKLANDI": (72, "Falkland Islands /Malvinas"),
    "FIDŽI": (74, "Fiji"),
    "FINSKA": (75, "Finland"),
    "FRANCUSKA": (76, "France"),
    "FRANCUSKA GVAJANA": (77, "French Guiana"),
    "FRANCUSKA POLINEZIJA": (78, "French Polynesia"),
    "GABON": (80, "Gabon"),
    "GAMBIJA": (81, "Gambia"),
    "GRUZIJA": (82, "Georgia"),
    "NJEMAČKA": (83, "Germany"),
    "GANA": (84, "Ghana"),
    "GERNZI": (92, "Guernsey"),
    "GIBRALTAR": (85, "Gibraltar"),
    "GRČKA": (86, "Greece"),
    "GRENLAND": (87, "Greenland"),
    "GRENADA": (88, "Grenada"),
    "GVADALUPA": (89, "Guadeloupe"),
    "GUAM": (90, "Guam"),
    "GVATEMALA": (91, "Guatemala"),
    "GVINEJA": (93, "Guinea"),
    "GVINEJA – BISAU": (94, "Guinea-Bissau"),
    "GVINEJA-BISAU": (94, "Guinea-Bissau"),
    "GVAJANA": (95, "Guyana"),
    "HAITI": (96, "Haiti"),
    "HONDURAS": (97, "Honduras"),
    "HONG KONG": (98, "Hong Kong"),
    "MAĐARSKA": (99, "Hungary"),
    "ISLAND": (100, "Iceland"),
    "INDIJA": (101, "India"),
    "INDONEZIJA": (102, "Indonesia"),
    "IRAN": (103, "Iran"),
    "IRAK": (104, "Iraq"),
    "IRSKA": (105, "Ireland"),
    "OTOK MAN": (106, "Isle of Man"),
    "IZRAEL": (107, "Israel"),
    "ITALIJA": (108, "Italy"),
    "JAMAJKA": (109, "Jamaica"),
    "JAPAN": (110, "Japan"),
    "JORDAN": (112, "Jordan"),
    "JUŽNA AFRIKA": (205, "South Africa"),
    "JUŽNA DŽORDŽIJA": (206, "South Georgia and S. Sandwich Islands"),
    "JUŽNI SENDVIČ OTOCI": (206, "South Georgia and S. Sandwich Islands"),
    "KAJMANSKI OTOCI": (41, "Cayman Islands"),
    "KAZAHSTAN": (113, "Kazakhstan"),
    "KENIJA": (114, "Kenya"),
    "KIRGISTAN": (120, "Kyrgyzstan"),
    "KIRIBATI": (115, "Kiribati"),
    "KOSOVO": (118, "Kosovo"),
    "KATAR": (179, "Qatar"),
    "KUVAJT": (119, "Kuwait"),
    "LAOSKA NARODNA DEMOKRATSKA REPUBLIKA": (121, "Laos"),
    "LATVIJA": (122, "Latvia"),
    "LESOTO": (124, "Lesotho"),
    "LIBANON": (123, "Lebanon"),
    "LIBERIJA": (125, "Liberia"),
    "LIBIJA": (126, "Libya"),
    "LIHTENŠTAJN": (127, "Liechtenstein"),
    "LITVA": (128, "Lithuania"),
    "LUKSEMBURG": (129, "Luxembourg"),
    "MADAGASKAR": (131, "Madagascar"),
    "MALAVI": (132, "Malawi"),
    "MALEZIJA": (133, "Malaysia"),
    "MALDIVI": (134, "Maldives"),
    "MALI": (135, "Mali"),
    "MALTA": (136, "Malta"),
    "MARŠALOVI OTOCI": (137, "Marshall Islands"),
    "MARTINIK": (138, "Martinique"),
    "MAURICIJUS": (140, "Mauritius"),
    "MAJOT": (141, "Mayotte"),
    "MEKSIKO": (142, "Mexico"),
    "MIKRONEZIJA": (143, "Micronesia"),
    "MOLDAVIJA": (144, "Moldova"),
    "MONAKO": (145, "Monaco"),
    "MONGOLIJA": (146, "Mongolia"),
    "CRNA GORA": (147, "Montenegro"),
    "MONTSERAT": (148, "Montserrat"),
    "MAROKO": (149, "Morocco"),
    "MOZAMBIK": (150, "Mozambique"),
    "MJANMAR": (151, "Myanmar"),
    "NAMIBIJA": (152, "Namibia"),
    "NAURU": (153, "Nauru / Naoero"),
    "NEPAL": (154, "Nepal"),
    "NIZOZEMSKA": (155, "Netherlands"),
    "NOVA KALEDONIJA": (156, "New Caledonia"),
    "NOVI ZELAND": (157, "New Zealand"),
    "NIKARAGVA": (158, "Nicaragua"),
    "NIGER": (159, "Niger"),
    "NIGERIJA": (160, "Nigeria"),
    "NIUE": (161, "Niue"),
    "OTOK NORFOLK": (162, "Norfolk Island"),
    "MARIJANSKI OTOCI": (163, "Northern Mariana Islands"),
    "MAKEDONIJA": (164, "North Macedonia"),
    "NORVEŠKA": (165, "Norway"),
    "OMAN": (166, "Oman"),
    "PAKISTAN": (167, "Pakistan"),
    "PALAU": (168, "Palau"),
    "PANAMA": (170, "Panama"),
    "PAPUA NOVA GVINEJA": (171, "Papua New Guinea"),
    "PARAGVAJ": (172, "Paraguay"),
    "PERU": (173, "Peru"),
    "FILIPINI": (174, "Philippines"),
    "PITKERN": (175, "Pitcairn"),
    "POLJSKA": (176, "Poland"),
    "PORTUGAL": (177, "Portugal"),
    "PORTORIKO": (178, "Puerto Rico"),
    "REPUBLIKA KINA NA TAJVANU": (216, "Taiwan"),
    "REPUBLIKA KOREJA": (117, "Korea(South)"),
    "REUNION": (180, "Réunion"),
    "RUANDA": (183, "Rwanda"),
    "RUMUNJSKA": (181, "Romania"),
    "RUSIJA": (182, "Russia"),
    "SAD": (235, "U.S.A."),
    "SALOMONOVI OTOCI": (203, "Solomon Islands"),
    "SAMOA": (191, "Samoa"),
    "SAN MARINO": (192, "San Marino"),
    "SAUDIJSKA ARABIJA": (194, "Saudi Arabia"),
    "SEJŠELI": (197, "Seychelles"),
    "SENEGAL": (195, "Senegal"),
    "SIJERA LEONE": (198, "Sierra Leone"),
    "SINGAPUR": (199, "Singapore"),
    "SIRIJA": (215, "Syria"),
    "SLOVAČKA": (201, "Slovakia"),
    "SLOVENIJA": (202, "Slovenia"),
    "SRBIJA": (196, "Serbia"),
    "SREDNJOAFRIČKA REPUBLIKA": (42, "Central African Republic"),
    "SUDAN": (210, "Sudan"),
    "SURINAM": (211, "Suriname"),
    "SVETA HELENA": (185, "Saint Helena, Ascension and Tristan da Cunha"),
    "SVETA LUCIJA": (187, "Saint Lucia"),
    "SVETI KRISTOFOR I NEVIS": (186, "Saint Kitts and Nevis"),
    "SVETI PETAR I MIKELON": (189, "Saint Pierre & Miquelon"),
    "SVETI TOMA I PRINSIPE": (193, "Sao Tome and Principe"),
    "SVETI VINCENT I GRENADINI": (190, "Saint Vincent and the Grenadines"),
    "ŠPANJOLSKA": (208, "Spain"),
    "ŠRI LANKA": (209, "Sri Lanka"),
    "ŠVEDSKA": (213, "Sweden"),
    "ŠVICARSKA": (214, "Switzerland"),
    "TADŽIKISTAN": (217, "Tajikistan"),
    "TAJLAND": (219, "Thailand"),
    "TANZANIJA": (218, "Tanzania"),
    "TIMOR - LESTE": (220, "Timor-Leste"),
    "TIMOR-LESTE": (220, "Timor-Leste"),
    "TOGO": (221, "Togo"),
    "TOKELAU": (222, "Tokelau"),
    "TONGA": (223, "Tonga"),
    "TRINIDAD I TOBAGO": (224, "Trinidad and Tobago"),
    "TRISTAN DA KUNA": (185, "Saint Helena, Ascension and Tristan da Cunha"),
    "TUNIS": (225, "Tunisia"),
    "TURKMENISTAN": (227, "Turkmenistan"),
    "TURKS I KEIKOS OTOCI": (228, "Turks and Caicos Islands"),
    "TURSKA": (226, "Turkey"),
    "TUVALU": (229, "Tuvalu"),
    "UGANDA": (230, "Uganda"),
    "UJEDINJENI ARAPSKI EMIRATI": (232, "United Arab Emirates"),
    "UJEDINJENA KRALJEVINA VELIKE BRITANIJE I SJEVERNE IRSKE": (
        233,
        "United Kingdom",
    ),
    "UKRAJINA": (231, "Ukraine"),
    "URUGVAJ": (234, "Uruguay"),
    "UZBEKISTAN": (237, "Uzbekistan"),
    "VALIS I FUTUNA": (244, "Wallis & Futuna"),
    "VANUATU": (238, "Vanuatu"),
    "DRŽAVA VATIKANSKOGA GRADA": (239, "Vatican"),
    "VENEZUELA": (240, "Venezuela"),
    "VIJETNAM": (241, "Vietnam"),
    "AMERIČKI DJEVIČANSKI OTOCI": (243, "Virgin Islands of the USA"),
    "ZAMBIJA": (247, "Zambia"),
    "ZIMBABVE": (248, "Zimbabwe"),
}


# -------------------------------------------------------------------
# Exact order of entries appearing in the Mostar Post PDF.
#
# IMPORTANT:
# Duplicates are intentionally present.
# Do NOT convert this list to a set and do NOT deduplicate it.
# -------------------------------------------------------------------

PDF_ENTRIES = [
    "ALBANIJA",
    "ALŽIR",
    "AMERIČKI DJEVIČANSKI OTOCI",
    "AMERIČKA SAMOA",
    "ANDORA",
    "ANGOLA",
    "ANGVILA",
    "ANTIGVA I BARBUDA",
    "ARGENTINA",
    "ARMENIJA",
    "ARUBA (pismovne pošiljke I paketi)",
    "ASENŠN",
    "AUSTRALIJA (pismovne pošiljke)",
    "AUSTRALIJA (EMS pošiljka i paketi maksimalne mase 10 kg)",
    "AUSTRIJA",
    "AZERBEJDŽAN",
    "BAHAMI",
    "BAHREIN",
    "BANGLADEŠ",
    "BARBADOS",
    "BELGIJA",
    "BELIZE",
    "BENIN",
    "BERMUDA",
    "BJELOKOSNA OBALA",
    "BJELORUSIJA",
    "BOCVANA (pismovne pošiljke I paketi)",
    "BOLIVIJA",
    "BOŽIĆNI OTOK (AUSTRALIJA)",
    "BOŽIĆNI OTOK (PACIFIC)",
    "BRAZIL",
    "BRITANSKI DJEVIČANSKI OTOCI",
    "BRUNEJ DARUSSALAM",
    "BUGARSKA",
    "BURKINA FASO",
    "BURUNDI",
    "BUTAN (pismovne pošiljke I paketi)",
    "CIPAR",
    "CRNA GORA",
    "ČAD",
    "ČEŠKA REPUBLIKA",
    "ČILE",
    "DANSKA",
    "DEMOKRATSKA NARODNA REPUBLIKA KOREJA",
    "DEMOKRATSKA REPUBLIKA KONGO",
    "DOMINIKA",
    "DOMINIKANSKA REPUBLIKA",
    "DRŽAVA VATIKANSKOGA GRADA",
    "DŽIBUTI",
    "EGIPAT",
    "EKVADOR",
    "EKVATORSKA GVINEJA",
    "ERITREJA",
    "ESTONIJA",
    "ESVATINI",
    "ETIOPIJA",
    "FAKLANDI (MALVINI)",
    "FIDŽI",
    "FILIPINI",
    "FINSKA",
    "FRANCUSKA",
    "FRANCUSKA GVAJANA",
    "FRANCUSKA POLINEZIJA",
    "GABON",
    "GAMBIJA",
    "GANA",
    "GERNZI",
    "GIBRALTAR",
    "GRČKA",
    "GRENADA",
    "GRENLAND",
    "GRUZIJA",
    "GUAM",
    "GVADALUPA",
    "GVAJANA",
    "GVATEMALA",
    "GVINEJA",
    "GVINEJA – BISAU",
    "HAITI",
    "HONDURAS",
    "HONG KONG",
    "HRVATSKA",
    "INDIJA",
    "INDONEZIJA",
    "IRAK",
    "IRAN",
    "IRSKA",
    "ISLAND",
    "ITALIJA",
    "JAMAJKA",
    "JAPAN",
    "JORDAN",
    "JUŽNA AFRIKA",
    "JUŽNA DŽORDŽIJA",
    "JUŽNI SENDVIČ OTOCI",
    "KABO VERDE",
    "KAJMANSKI OTOCI (pismovne pošiljke i paketi)",
    "KAMBODŽA",
    "KAMERUN",
    "KANADA",
    "KATAR",
    "KAZAHSTAN",
    "KENIJA",
    "KINA",
    "KIRGISTAN",
    "KIRIBATI",
    "KOKOSOVI OTOCI",
    "KOLUMBIJA",
    "KOMORI",
    "KONGO",
    "KOSOVO",
    "KOSTARIKA",
    "KUBA",
    "KUKOVI OTOCI",
    "KUVAJT",
    "LAOSKA NARODNA DEMOKRATSKA REPUBLIKA (samo pismovne pošiljke I paketi)",
    "LATVIJA",
    "LESOTO",
    "LIBANON",
    "LIBERIJA",
    "LIHTENŠTAJN",
    "LITVA",
    "LUKSEMBURG",
    "MADAGASKAR (samo pismovne pošiljke i paketi)",
    "MAĐARSKA",
    "MAJOT",
    "MAKAO",
    "MAKEDONIJA",
    "MALAVI",
    "MALDIVI",
    "MALEZIJA",
    "MALI",
    "MALTA",
    "MARIJANSKI OTOCI",
    "MAROKO",
    "MARŠALOVI OTOCI",
    "MARTINIK",
    "MAURICIJUS",
    "MEKSIKO",
    "MIKRONEZIJA",
    "MJANMAR",
    "MOLDAVIJA",
    "MONAKO",
    "MONGOLIJA (samo pismovne pošiljke)",
    "MONTSERAT",
    "MOZAMBIK",
    "NAMIBIJA",
    "NAURU",
    "NEPAL",
    "NIGER",
    "NIGERIJA",
    "NIKARAGVA",
    "NIUE",
    "NIZOZEMSKA",
    "NIZOZEMSKI ANTILI (samo pismovne pošiljke i paketi)",
    "NJEMAČKA",
    "NORVEŠKA",
    "NOVA KALEDONIJA",
    "NOVI ZELAND (samo pismovne pošiljke)",
    "NOVI ZELAND (EMS pošiljke I paketi maksimalne mase 10kg)",
    "OMAN",
    "OTOK MAN",
    "OTOK NORFOLK",
    "OVČJI OTOCI",
    "PAKISTAN",
    "PALAU",
    "PANAMA",
    "PAPUA NOVA GVINEJA",
    "PARAGVAJ",
    "PERU",
    "PITKERN",
    "POLJSKA",
    "PORTORIKO",
    "PORTUGAL",
    "REPUBLIKA KINA NA TAJVANU",
    "REPUBLIKA KOREJA",
    "REUNION",
    "RUANDA",
    "RUMUNJSKA",
    "RUSIJA",
    "SAD",
    "SALOMONOVI OTOCI",
    "SALVADOR",
    "SAMOA",
    "SAN MARINO",
    "SAUDIJSKA ARABIJA",
    "SEJŠELI",
    "SENEGAL",
    "SIJERA LEONE",
    "SINGAPUR",
    "SIRIJA",
    "SLOVAČKA",
    "SLOVENIJA",
    "SRBIJA",
    "SREDNJOAFRIČKA REPUBLIKA",
    "SUDAN",
    "SURINAM",
    "SVETA HELENA",
    "SVETA LUCIJA",
    "SVETI KRISTOFOR I NEVIS",
    "SVETI PETAR I MIKELON",
    "SVETI TOMA I PRINSIPE",
    "SVETI VINCENT I GRENADINI",
    "ŠPANJOLSKA",
    "ŠRI LANKA",
    "ŠVEDSKA",
    "ŠVICARSKA",
    "TADŽIKISTAN",
    "TAJLAND",
    "TANZANIJA",
    "TIMOR - LESTE",
    "TOGO",
    "TOKELAU",
    "TONGA",
    "TRINIDAD I TOBAGO",
    "TRISTAN DA KUNA",
    "TUNIS",
    "TURKMENISTAN",
    "TURKS I KEIKOS OTOCI",
    "TURSKA",
    "TUVALU",
    "UGANDA",
    "UJEDINJENI ARAPSKI EMIRATI",
    "UJEDINJENA KRALJEVINA VELIKE BRITANIJE I SJEVERNE IRSKE",
    "UJEDINJENI ARAPSLI EMIRATI",
    "UKRAJINA",
    "URUGVAJ",
    "UZBEKISTAN",
    "VALIS I FUTUNA",
    "VANUATU (pismovne pošiljke i paketi)",
    "VENEZUELA (pismovne pošiljke i paketi)",
    "VIJETNAM",
    "ZAMBIJA",
    "ZIMBABVE (samo pismovne pošiljke i paketi)",
]


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def normalize_spaces(text):
    """Collapse all whitespace into single spaces."""
    return re.sub(r"\s+", " ", text).strip()


def normalize_dashes(text):
    """Normalize different dash characters."""
    return (
        text.replace("–", "-")
        .replace("—", "-")
        .replace("-", "-")
    )


def remove_parentheses(text):
    """
    Remove parentheses and EVERYTHING inside them.
    Repeat until no parenthetical content remains.
    """
    while re.search(r"\([^()]*\)", text):
        text = re.sub(r"\([^()]*\)", " ", text)

    return normalize_spaces(text)


def clean_country_name(name):
    """Clean an individual PDF country entry."""
    name = remove_parentheses(name)
    name = normalize_dashes(name)
    name = normalize_spaces(name)

    # PDF-specific spelling/extraction corrections.
    replacements = {
        "TIMOR - LESTE": "TIMOR-LESTE",
        "GVINEJA - BISAU": "GVINEJA – BISAU",
        "OVČJI OTOCI": "OVČJI OTOCI",
    }

    return replacements.get(name, name)


def download_pdf():
    """Download the current PDF from Pošta."""
    request = urllib.request.Request(
        PDF_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        },
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()

    if not data.startswith(b"%PDF"):
        raise RuntimeError(
            "Downloaded file does not appear to be a PDF."
        )

    PDF_FILE.write_bytes(data)


def extract_pdf_text():
    """Extract all text from the PDF."""
    try:
        import fitz
    except ImportError:
        raise RuntimeError(
            "PyMuPDF is not installed. "
            "Add PyMuPDF to the GitHub Actions dependencies."
        )

    document = fitz.open(PDF_FILE)

    pages = []

    for page in document:
        pages.append(page.get_text("text"))

    document.close()

    return normalize_spaces(" ".join(pages))


# -------------------------------------------------------------------
# Parsing
# -------------------------------------------------------------------

def extract_entries_from_pdf(text):
    """
    Find the PDF's country entries in their original order.

    The PDF extraction can sometimes put multiple countries on one
    line. Therefore we do NOT depend on PDF line breaks.

    Instead, we search for the known PDF entries in sequence.
    This preserves duplicates because PDF_ENTRIES itself contains
    duplicates.
    """

    text = normalize_spaces(text)
    text = normalize_dashes(text)

    # Ignore the title.
    title = "POPIS DRŽAVA U KOJE JE MOGUĆE SLATI POŠILJKE:"
    if title in text:
        text = text.split(title, 1)[1]

    # Ignore the final date/footer.
    footer = "Posljednje izmjene"
    if footer in text:
        text = text.split(footer, 1)[0]

    entries = []
    position = 0

    for expected in PDF_ENTRIES:
        expected_normalized = normalize_dashes(expected)

        # Search from the previous match onward.
        match = re.search(
            re.escape(expected_normalized),
            text[position:],
            flags=re.IGNORECASE,
        )

        if match:
            start = position + match.start()
            end = position + match.end()

            found = text[start:end]
            entries.append(found)

            position = end
        else:
            # The PDF may have changed.
            #
            # Do not silently invent a country. Report the missing
            # entry so the GitHub Action makes the problem visible.
            raise RuntimeError(
                "Could not find expected PDF entry:\n"
                f"    {expected}\n\n"
                "The PDF may have changed, or its text extraction "
                "format may be different."
            )

    return entries


def translate_entry(original):
    """
    Remove parenthetical information and translate the remaining
    country name.
    """

    cleaned = clean_country_name(original)

    # Special mappings for PDF names that do not exactly match the
    # Postcrossing country names.
    special = {
        "AMERIČKI DJEVIČANSKI OTOCI": (
            243,
            "Virgin Islands of the USA",
        ),
        "BJELOKOSNA OBALA": (
            54,
            "Côte d'Ivoire",
        ),
        "BOŽIĆNI OTOK": (
            46,
            "Christmas Island",
        ),
        "BRITANSKI DJEVIČANSKI OTOCI": (
            242,
            "Virgin Islands (UK)",
        ),
        "DEMOKRATSKA NARODNA REPUBLIKA KOREJA": (
            116,
            "Korea(North)",
        ),
        "DEMOKRATSKA REPUBLIKA KONGO": (
            51,
            "Dem. Rep. Of Congo",
        ),
        "FAKLANDI": (
            72,
            "Falkland Islands /Malvinas",
        ),
        "KINA": (
            45,
            "China",
        ),
        "NIZOZEMSKI ANTILI": (
            None,
            "Netherlands Antilles",
        ),
        "OVČJI OTOCI": (
            73,
            "Faroe Islands",
        ),
        "SAD": (
            235,
            "U.S.A.",
        ),
        "SALVADOR": (
            66,
            "El Salvador",
        ),
        "REUNION": (
            180,
            "Réunion",
        ),
        "REPUBLIKA KINA NA TAJVANU": (
            216,
            "Taiwan",
        ),
        "REPUBLIKA KOREJA": (
            117,
            "Korea(South)",
        ),
        "DRŽAVA VATIKANSKOGA GRADA": (
            239,
            "Vatican",
        ),
        "VALIS I FUTUNA": (
            244,
            "Wallis & Futuna",
        ),
    }

    if cleaned in special:
        number, english = special[cleaned]
    elif cleaned in POSTCROSSING:
        number, english = POSTCROSSING[cleaned]
    else:
        number = None
        english = cleaned

    if number is not None:
        return f"{number}. {cleaned} — {english}"

    return f"{cleaned} — {english}"


def create_output(entries):
    """
    Convert every PDF occurrence to one output line.

    No deduplication happens here.
    """

    lines = []

    for entry in entries:
        lines.append(translate_entry(entry))

    return "\n".join(lines) + "\n"


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main():
    print("Downloading Mostar Post PDF...")
    download_pdf()

    print("Extracting PDF text...")
    text = extract_pdf_text()

    if not text:
        raise RuntimeError("No text could be extracted from the PDF.")

    print("Parsing country entries...")
    entries = extract_entries_from_pdf(text)

    print(f"Found {len(entries)} PDF entries.")

    output = create_output(entries)

    OUTPUT_FILE.write_text(
        output,
        encoding="utf-8",
    )

    print(f"Created {OUTPUT_FILE}")
    print(f"Output lines: {len(entries)}")


if __name__ == "__main__":
    main()
