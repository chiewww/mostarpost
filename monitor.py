import re
import urllib.request
from pathlib import Path

PDF_URL = "https://www.post.ba/media/files/POPIS%20DR%C5%BDAVA%20MEDJ%20PROMET%2013_12_2023.pdf"

PDF_FILE = Path("mostar_post.pdf")
OUTPUT_FILE = Path("output.txt")


# ============================================================
# POSTCROSSING NUMBERS
# ============================================================

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
    "BELGIJA": (22, "Belgium"),
    "BELIZE": (23, "Belize"),
    "BENIN": (24, "Benin"),
    "BERMUDA": (25, "Bermuda"),
    "BJELORUSIJA": (21, "Belarus"),
    "BJELOKOSNA OBALA": (54, "Côte d'Ivoire"),
    "BOCVANA": (30, "Botswana"),
    "BOLIVIJA": (27, "Bolivia"),
    "BOŽIĆNI OTOK": (46, "Christmas Island"),
    "BRAZIL": (31, "Brazil"),
    "BRITANSKI DJEVIČANSKI OTOCI": (242, "Virgin Islands (UK)"),
    "BRUNEJ DARUSSALAM": (33, "Brunei"),
    "BUGARSKA": (34, "Bulgaria"),
    "BURKINA FASO": (35, "Burkina Faso"),
    "BURUNDI": (36, "Burundi"),
    "BUTAN": (26, "Bhutan"),
    "CIPAR": (58, "Cyprus"),
    "CRNA GORA": (147, "Montenegro"),
    "ČAD": (43, "Chad"),
    "ČEŠKA REPUBLIKA": (59, "Czechia"),
    "ČILE": (44, "Chile"),
    "DANSKA": (60, "Denmark"),
    "DEMOKRATSKA NARODNA REPUBLIKA KOREJA": (116, "Korea(North)"),
    "DEMOKRATSKA REPUBLIKA KONGO": (51, "Dem. Rep. Of Congo"),
    "DOMINIKA": (62, "Dominica"),
    "DOMINIKANSKA REPUBLIKA": (63, "Dominican Republic"),
    "DRŽAVA VATIKANSKOGA GRADA": (239, "Vatican"),
    "DŽIBUTI": (61, "Djibouti"),
    "EGIPAT": (65, "Egypt"),
    "EKVADOR": (64, "Ecuador"),
    "EKVATORSKA GVINEJA": (67, "Equatorial Guinea"),
    "ERITREJA": (68, "Eritrea"),
    "ESTONIJA": (69, "Estonia"),
    "ESVATINI": (70, "Eswatini /Swaziland"),
    "ETIOPIJA": (71, "Ethiopia"),
    "FAKLANDI": (72, "Falkland Islands /Malvinas"),
    "FIDŽI": (74, "Fiji"),
    "FILIPINI": (174, "Philippines"),
    "FINSKA": (75, "Finland"),
    "FRANCUSKA": (76, "France"),
    "FRANCUSKA GVAJANA": (77, "French Guiana"),
    "FRANCUSKA POLINEZIJA": (78, "French Polynesia"),
    "GABON": (80, "Gabon"),
    "GAMBIJA": (81, "Gambia"),
    "GANA": (84, "Ghana"),
    "GERNZI": (92, "Guernsey"),
    "GIBRALTAR": (85, "Gibraltar"),
    "GRČKA": (86, "Greece"),
    "GRENADA": (88, "Grenada"),
    "GRENLAND": (87, "Greenland"),
    "GRUZIJA": (82, "Georgia"),
    "GUAM": (90, "Guam"),
    "GVADALUPA": (89, "Guadeloupe"),
    "GVAJANA": (95, "Guyana"),
    "GVATEMALA": (91, "Guatemala"),
    "GVINEJA": (93, "Guinea"),
    "GVINEJA – BISAU": (94, "Guinea-Bissau"),
    "GVINEJA - BISAU": (94, "Guinea-Bissau"),
    "HAITI": (96, "Haiti"),
    "HONDURAS": (97, "Honduras"),
    "HONG KONG": (98, "Hong Kong"),
    "HRVATSKA": (55, "Croatia"),
    "INDIJA": (101, "India"),
    "INDONEZIJA": (102, "Indonesia"),
    "IRAK": (104, "Iraq"),
    "IRAN": (103, "Iran"),
    "IRSKA": (105, "Ireland"),
    "ISLAND": (100, "Iceland"),
    "ITALIJA": (108, "Italy"),
    "JAMAJKA": (109, "Jamaica"),
    "JAPAN": (110, "Japan"),
    "JORDAN": (112, "Jordan"),
    "JUŽNA AFRIKA": (205, "South Africa"),
    "JUŽNA DŽORDŽIJA": (206, "South Georgia and S. Sandwich Islands"),
    "JUŽNI SENDVIČ OTOCI": (206, "South Georgia and S. Sandwich Islands"),
    "KABO VERDE": (37, "Cabo Verde"),
    "KAJMANSKI OTOCI": (41, "Cayman Islands"),
    "KAMBODŽA": (38, "Cambodia"),
    "KAMERUN": (39, "Cameroon"),
    "KANADA": (40, "Canada"),
    "KATAR": (179, "Qatar"),
    "KAZAHSTAN": (113, "Kazakhstan"),
    "KENIJA": (114, "Kenya"),
    "KINA": (45, "China"),
    "KIRGISTAN": (120, "Kyrgyzstan"),
    "KIRIBATI": (115, "Kiribati"),
    "KOKOSOVI OTOCI": (47, "Cocos Islands"),
    "KOLUMBIJA": (48, "Colombia"),
    "KOMORI": (49, "Comoros"),
    "KONGO": (50, "Congo"),
    "KOSOVO": (118, "Kosovo"),
    "KOSTARIKA": (53, "Costa Rica"),
    "KUBA": (56, "Cuba"),
    "KUKOVI OTOCI": (52, "Cook Islands"),
    "KUVAJT": (119, "Kuwait"),
    "LAOSKA NARODNA DEMOKRATSKA REPUBLIKA": (121, "Laos"),
    "LATVIJA": (122, "Latvia"),
    "LESOTO": (124, "Lesotho"),
    "LIBANON": (123, "Lebanon"),
    "LIBERIJA": (125, "Liberia"),
    "LIHTENŠTAJN": (127, "Liechtenstein"),
    "LITVA": (128, "Lithuania"),
    "LUKSEMBURG": (129, "Luxembourg"),
    "MADAGASKAR": (131, "Madagascar"),
    "MAĐARSKA": (99, "Hungary"),
    "MAJOT": (141, "Mayotte"),
    "MAKAO": (130, "Macao"),
    "MAKEDONIJA": (164, "North Macedonia"),
    "MALAVI": (132, "Malawi"),
    "MALDIVI": (134, "Maldives"),
    "MALEZIJA": (133, "Malaysia"),
    "MALI": (135, "Mali"),
    "MALTA": (136, "Malta"),
    "MARIJANSKI OTOCI": (163, "Northern Mariana Islands"),
    "MAROKO": (149, "Morocco"),
    "MARŠALOVI OTOCI": (137, "Marshall Islands"),
    "MARTINIK": (138, "Martinique"),
    "MAURICIJUS": (140, "Mauritius"),
    "MEKSIKO": (142, "Mexico"),
    "MIKRONEZIJA": (143, "Micronesia"),
    "MJANMAR": (151, "Myanmar"),
    "MOLDAVIJA": (144, "Moldova"),
    "MONAKO": (145, "Monaco"),
    "MONGOLIJA": (146, "Mongolia"),
    "MONTSERAT": (148, "Montserrat"),
    "MOZAMBIK": (150, "Mozambique"),
    "NAMIBIJA": (152, "Namibia"),
    "NAURU": (153, "Nauru / Naoero"),
    "NEPAL": (154, "Nepal"),
    "NIGER": (159, "Niger"),
    "NIGERIJA": (160, "Nigeria"),
    "NIKARAGVA": (158, "Nicaragua"),
    "NIUE": (161, "Niue"),
    "NIZOZEMSKA": (155, "Netherlands"),
    "NIZOZEMSKI ANTILI": (None, "Netherlands Antilles"),
    "NJEMAČKA": (83, "Germany"),
    "NORVEŠKA": (165, "Norway"),
    "NOVA KALEDONIJA": (156, "New Caledonia"),
    "NOVI ZELAND": (157, "New Zealand"),
    "OMAN": (166, "Oman"),
    "OTOK MAN": (106, "Isle of Man"),
    "OTOK NORFOLK": (162, "Norfolk Island"),
    "OVČJI OTOCI": (73, "Faroe Islands"),
    "PAKISTAN": (167, "Pakistan"),
    "PALAU": (168, "Palau"),
    "PANAMA": (170, "Panama"),
    "PAPUA NOVA GVINEJA": (171, "Papua New Guinea"),
    "PARAGVAJ": (172, "Paraguay"),
    "PERU": (173, "Peru"),
    "PITKERN": (175, "Pitcairn"),
    "POLJSKA": (176, "Poland"),
    "PORTORIKO": (178, "Puerto Rico"),
    "PORTUGAL": (177, "Portugal"),
    "REPUBLIKA KINA NA TAJVANU": (216, "Taiwan"),
    "REPUBLIKA KOREJA": (117, "Korea(South)"),
    "REUNION": (180, "Réunion"),
    "RUANDA": (183, "Rwanda"),
    "RUMUNJSKA": (181, "Romania"),
    "RUSIJA": (182, "Russia"),
    "SAD": (235, "U.S.A."),
    "SALOMONOVI OTOCI": (203, "Solomon Islands"),
    "SALVADOR": (66, "El Salvador"),
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
    "UJEDINJENI ARAPSLI EMIRATI": (232, "United Arab Emirates"),
    "UJEDINJENA KRALJEVINA VELIKE BRITANIJE I SJEVERNE IRSKE": (
        233,
        "United Kingdom",
    ),
    "UKRAJINA": (231, "Ukraine"),
    "URUGVAJ": (234, "Uruguay"),
    "UZBEKISTAN": (237, "Uzbekistan"),
    "VALIS I FUTUNA": (244, "Wallis & Futuna"),
    "VANUATU": (238, "Vanuatu"),
    "VENEZUELA": (240, "Venezuela"),
    "VIJETNAM": (241, "Vietnam"),
    "ZAMBIJA": (247, "Zambia"),
    "ZIMBABVE": (248, "Zimbabwe"),
}


# ============================================================
# COUNTRY NAMES AS THEY APPEAR IN THE PDF
#
# Parenthetical service information is intentionally NOT part
# of these names.
#
# Duplicates are intentional.
# ============================================================

PDF_COUNTRIES = [
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
    "ARUBA",
    "ASENŠN",
    "AUSTRALIJA",
    "AUSTRALIJA",
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
    "BOCVANA",
    "BOLIVIJA",
    "BOŽIĆNI OTOK",
    "BOŽIĆNI OTOK",
    "BRAZIL",
    "BRITANSKI DJEVIČANSKI OTOCI",
    "BRUNEJ DARUSSALAM",
    "BUGARSKA",
    "BURKINA FASO",
    "BURUNDI",
    "BUTAN",
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
    "FAKLANDI",
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
    "KAJMANSKI OTOCI",
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
    "LAOSKA NARODNA DEMOKRATSKA REPUBLIKA",
    "LATVIJA",
    "LESOTO",
    "LIBANON",
    "LIBERIJA",
    "LIHTENŠTAJN",
    "LITVA",
    "LUKSEMBURG",
    "MADAGASKAR",
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
    "MONGOLIJA",
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
    "NIZOZEMSKI ANTILI",
    "NJEMAČKA",
    "NORVEŠKA",
    "NOVA KALEDONIJA",
    "NOVI ZELAND",
    "NOVI ZELAND",
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
    "VANUATU",
    "VENEZUELA",
    "VIJETNAM",
    "ZAMBIJA",
    "ZIMBABVE",
]


# ============================================================
# HELPERS
# ============================================================

def normalize_text(text):
    text = text.replace("\r", " ")
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    # Normalize dash variants.
    text = text.replace("—", "-")
    text = text.replace("–", "-")
    text = text.replace("-", "-")

    # Collapse whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def remove_parentheses(text):
    """
    Remove ALL parenthetical text.
    """

    while "(" in text and ")" in text:
        new_text = re.sub(r"\([^()]*\)", " ", text)

        if new_text == text:
            break

        text = new_text

    return normalize_text(text)


def download_pdf():
    print("Downloading Mostar Post PDF...")

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
            "The downloaded file is not a valid PDF."
        )

    PDF_FILE.write_bytes(data)

    print(f"Downloaded {len(data)} bytes.")


def extract_pdf_text():
    print("Extracting PDF text...")

    # Use the modern PyMuPDF import.
    import pymupdf

    document = pymupdf.open(PDF_FILE)

    parts = []

    for page in document:
        parts.append(page.get_text("text"))

    document.close()

    text = normalize_text(" ".join(parts))

    if not text:
        raise RuntimeError(
            "No text could be extracted from the PDF."
        )

    return text


# ============================================================
# PARSER
# ============================================================

def build_search_text(text):
    """
    Prepare the PDF text for matching.

    Parenthetical information is removed completely BEFORE
    country matching.

    This means differences such as:

        VANUATU (pismovne pošiljke i paketi)

    and

        VANUATU

    both become simply:

        VANUATU
    """

    # Remove title.
    text = re.sub(
        r"POPIS\s+DRŽAVA\s+U\s+KOJE\s+JE\s+MOGUĆE\s+SLATI\s+POŠILJKE\s*:?",
        " ",
        text,
        flags=re.IGNORECASE,
    )

    # Remove footer/date.
    text = re.split(
        r"Posljednje\s+izmjene",
        text,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    # Remove all parenthetical text.
    text = remove_parentheses(text)

    return normalize_text(text)


def normalize_country_for_matching(name):
    name = normalize_text(name)

    # Normalize dash spacing.
    name = re.sub(r"\s*-\s*", "-", name)

    return name.upper()


def find_country_entries(text):
    """
    Locate every PDF country in its original order.

    IMPORTANT:
    We process PDF_COUNTRIES sequentially.

    Therefore:

        AUSTRALIJA
        AUSTRALIJA

    remains:

        AUSTRALIJA
        AUSTRALIJA

    There is NO deduplication.
    """

    search_text = build_search_text(text)

    # The PDF occasionally has extraction artefacts where spaces
    # disappear around a dash.
    search_text = search_text.replace(
        "GVINEJA-BISAU",
        "GVINEJA – BISAU",
    )

    # Normalize whitespace/dashes for matching.
    search_text = normalize_country_for_matching(search_text)

    entries = []
    position = 0

    for expected in PDF_COUNTRIES:
        expected_normalized = normalize_country_for_matching(
            expected
        )

        # Special case for the dash in Guinea-Bissau.
        alternatives = [expected_normalized]

        if expected_normalized == "GVINEJA – BISAU":
            alternatives.extend(
                [
                    "GVINEJA - BISAU",
                    "GVINEJA-BISAU",
                ]
            )

        found = None

        for alternative in alternatives:
            pattern = re.escape(alternative)

            match = re.search(
                pattern,
                search_text[position:],
            )

            if match:
                found = match
                break

        if found is None:
            raise RuntimeError(
                "\nCould not find expected country entry:\n\n"
                f"    {expected}\n\n"
                "The PDF text extracted by PyMuPDF does not "
                "contain this entry in the expected order.\n\n"
                f"Parser position: {position}\n"
            )

        start = position + found.start()
        end = position + found.end()

        entries.append(expected)

        position = end

    return entries


# ============================================================
# TRANSLATION
# ============================================================

def translate_country(country):
    country = normalize_text(country)

    # Normalize the dash.
    country = country.replace("–", "-")
    country = re.sub(r"\s*-\s*", "-", country)

    special = {
        "GVINEJA-BISAU": (
            94,
            "Guinea-Bissau",
        ),

        "BOŽIĆNI OTOK": (
            46,
            "Christmas Island",
        ),

        "FAKLANDI": (
            72,
            "Falkland Islands /Malvinas",
        ),

        "NIZOZEMSKI ANTILI": (
            None,
            "Netherlands Antilles",
        ),

        "OVČJI OTOCI": (
            73,
            "Faroe Islands",
        ),

        "REUNION": (
            180,
            "Réunion",
        ),
    }

    key = country.upper()

    if key in special:
        number, english = special[key]

    elif key in POSTCROSSING:
        number, english = POSTCROSSING[key]

    else:
        # Unknown country.
        # Keep the Croatian name rather than silently inventing
        # a translation.
        number = None
        english = country

    if number is not None:
        return f"{number}. {country} — {english}"

    return f"{country} — {english}"


# ============================================================
# OUTPUT
# ============================================================

def create_output(entries):
    """
    Create output.txt.

    Every occurrence gets its own line.
    Nothing is deduplicated.
    """

    lines = []

    for entry in entries:
        # Safety check: absolutely no parentheses in output.
        entry = remove_parentheses(entry)

        lines.append(
            translate_country(entry)
        )

    output = "\n".join(lines) + "\n"

    # Final safety check.
    if "(" in output or ")" in output:
        raise RuntimeError(
            "ERROR: Parentheses were found in output.txt."
        )

    return output


# ============================================================
# MAIN
# ============================================================

def main():
    download_pdf()

    pdf_text = extract_pdf_text()

    print("Parsing country entries...")

    entries = find_country_entries(pdf_text)

    print(
        f"Successfully found {len(entries)} country entries."
    )

    output = create_output(entries)

    OUTPUT_FILE.write_text(
        output,
        encoding="utf-8",
    )

    print(
        f"Created {OUTPUT_FILE} with "
        f"{len(entries)} lines."
    )

    print("Done.")


if __name__ == "__main__":
    main()
