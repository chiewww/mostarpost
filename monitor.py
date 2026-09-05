import re
import urllib.request
from pathlib import Path

import pymupdf


PDF_URL = (
    "https://www.post.ba/media/files/"
    "POPIS%20DR%C5%BDAVA%20MEDJ%20PROMET%2013_12_2023.pdf"
)

OUTPUT_FILE = Path("output.txt")


# ---------------------------------------------------------------------------
# POSTCROSSING MAPPING
# ---------------------------------------------------------------------------

POSTCROSSING = {
    "ALBANIJA": (3, "Albania"),
    "ALŽIR": (None, "Algeria"),
    "AMERIČKI DJEVIČANSKI OTOCI": (243, "Virgin Islands of the USA"),
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
    "BJELOKOSNA OBALA": (54, "Côte d'Ivoire"),
    "BJELORUSIJA": (21, "Belarus"),
    "BOCVANA": (30, "Botswana"),
    "BOLIVIJA": (27, "Bolivia"),
    "BOŽIĆNI OTOK": (46, "Christmas Island"),
    "BRAZIL": (31, "Brazil"),
    "BRITANSKI DJEVIČANSKI OTOCI": (242, "Virgin Islands UK"),
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
    "DEMOKRATSKA NARODNA REPUBLIKA KOREJA": (116, "Korea North"),
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
    "ESVATINI": (70, "Eswatini"),
    "ETIOPIJA": (71, "Ethiopia"),
    "FAKLANDI": (72, "Falkland Islands Malvinas"),
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
    "NAURU": (153, "Nauru"),
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
    "REPUBLIKA KOREJA": (117, "Korea South"),
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
    "UJEDINJENA KRALJEVINA VELIKE BRITANIJE I SJEVERNE IRSKE": (
        233,
        "United Kingdom",
    ),
    "UJEDINJENI ARAPSLI EMIRATI": (232, "United Arab Emirates"),
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


# ---------------------------------------------------------------------------
# EXACT PDF ORDER
#
# Duplicates are intentional.
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------------------------------

def download_pdf():
    print("Downloading Mostar Post PDF...")

    request = urllib.request.Request(
        PDF_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            )
        },
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()

    print(f"Downloaded {len(data)} bytes.")

    if not data.startswith(b"%PDF"):
        raise RuntimeError("Downloaded file does not appear to be a PDF.")

    return data


# ---------------------------------------------------------------------------
# PDF TEXT EXTRACTION
# ---------------------------------------------------------------------------

def extract_pdf_text(pdf_data):
    print("Extracting PDF text...")

    document = pymupdf.open(
        stream=pdf_data,
        filetype="pdf",
    )

    try:
        pages = []

        for page in document:
            pages.append(page.get_text("text"))

        return "\n".join(pages)

    finally:
        document.close()


# ---------------------------------------------------------------------------
# TEXT NORMALIZATION
# ---------------------------------------------------------------------------

def normalize_text(text):
    text = text.replace("\u00a0", " ")
    text = text.replace("\u2013", " – ")
    text = text.replace("\u2014", " – ")
    text = text.replace("\u2212", " - ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_extraction_glitches(text):
    """
    Fix known places where PDF text extraction joins adjacent words.
    """

    replacements = {
        "GVINEJA – BISAUHAITI": "GVINEJA – BISAU HAITI",
        "OVČJI OTOCIPAKISTAN": "OVČJI OTOCI PAKISTAN",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


# ---------------------------------------------------------------------------
# PARSING
# ---------------------------------------------------------------------------

def find_entries(text):
    """
    Find entries in their exact PDF order.

    IMPORTANT:
    We do NOT remove parentheses before parsing.

    This means:

        AUSTRALIJA (pismovne pošiljke)
        AUSTRALIJA (EMS pošiljka...)

    remain two separate occurrences.

    After locating an entry, the parenthetical information is discarded
    only from that individual occurrence.
    """

    print("Parsing country entries...")

    text = normalize_text(text)
    text = clean_extraction_glitches(text)

    # Remove title.
    text = re.sub(
        r"POPIS DRŽAVA U KOJE JE MOGUĆE SLATI POŠILJKE\s*:?",
        " ",
        text,
        flags=re.IGNORECASE,
    )

    # Remove footer.
    text = re.sub(
        r"Posljednje izmjene.*$",
        " ",
        text,
        flags=re.IGNORECASE,
    )

    text = normalize_text(text)

    entries = []
    position = 0

    for expected in PDF_ENTRIES:

        # Search for the exact country name from the current position.
        index = text.find(expected, position)

        if index == -1:

            # Try alternate dash form.
            alternatives = []

            if " – " in expected:
                alternatives.append(expected.replace(" – ", " - "))

            if " - " in expected:
                alternatives.append(expected.replace(" - ", " – "))

            found = False

            for alternative in alternatives:
                index = text.find(alternative, position)

                if index != -1:
                    expected_used = alternative
                    found = True
                    break

            if not found:
                context_start = max(0, position - 150)
                context_end = min(len(text), position + 500)

                raise RuntimeError(
                    "\nCould not find expected PDF entry:\n"
                    f"    {expected}\n\n"
                    "Text near current parsing position:\n"
                    f"    {text[context_start:context_end]}"
                )

        else:
            expected_used = expected

        entries.append(expected)

        # IMPORTANT:
        # Move forward only by the matched country name.
        #
        # We intentionally DO NOT delete or consume the parenthetical
        # text here. This guarantees that a second identical country
        # immediately after the first one can still be found.
        position = index + len(expected_used)

    print(f"Successfully found {len(entries)} country entries.")

    return entries


# ---------------------------------------------------------------------------
# OUTPUT CLEANUP
# ---------------------------------------------------------------------------

def remove_parentheses(text):
    """
    Remove all parenthetical sections from one individual entry.

    This happens AFTER the entry occurrence has already been identified,
    so duplicate PDF entries remain separate.
    """

    previous = None

    while previous != text:
        previous = text
        text = re.sub(r"\([^()]*\)", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def create_output(entries):
    lines = []

    for entry in entries:

        if entry not in POSTCROSSING:
            raise RuntimeError(
                f"No Postcrossing translation defined for: {entry}"
            )

        number, english = POSTCROSSING[entry]

        original = remove_parentheses(entry)
        english = remove_parentheses(english)

        if number is not None:
            line = f"{number}. {original} — {english}"
        else:
            line = f"{original} — {english}"

        line = re.sub(r"\s+", " ", line).strip()

        lines.append(line)

    output = "\n".join(lines) + "\n"

    return output


# ---------------------------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------------------------

def validate_output(entries, output):
    """
    Strong validation to make sure duplicates have not disappeared.
    """

    lines = output.splitlines()

    print("")
    print("Validation:")
    print(f"  PDF entries:    {len(entries)}")
    print(f"  Output lines:   {len(lines)}")

    if len(entries) != len(lines):
        raise RuntimeError(
            f"ERROR: PDF contains {len(entries)} entries, "
            f"but output contains {len(lines)} lines."
        )

    # Parentheses must never appear in the final file.
    if "(" in output or ")" in output:
        raise RuntimeError(
            "ERROR: Parentheses were found in output.txt."
        )

    # Explicit duplicate checks.
    australia_count = entries.count("AUSTRALIJA")
    new_zealand_count = entries.count("NOVI ZELAND")
    christmas_island_count = entries.count("BOŽIĆNI OTOK")

    print(f"  AUSTRALIJA:     {australia_count}")
    print(f"  NOVI ZELAND:    {new_zealand_count}")
    print(f"  BOŽIĆNI OTOK:   {christmas_island_count}")

    if australia_count != 2:
        raise RuntimeError(
            "ERROR: Expected exactly 2 AUSTRALIJA entries, "
            f"but found {australia_count}."
        )

    if new_zealand_count != 2:
        raise RuntimeError(
            "ERROR: Expected exactly 2 NOVI ZELAND entries, "
            f"but found {new_zealand_count}."
        )

    if christmas_island_count != 2:
        raise RuntimeError(
            "ERROR: Expected exactly 2 BOŽIĆNI OTOK entries, "
            f"but found {christmas_island_count}."
        )

    # Make sure the actual output contains the duplicate lines.
    australia_lines = [
        line for line in lines
        if "AUSTRALIJA — Australia" in line
    ]

    new_zealand_lines = [
        line for line in lines
        if "NOVI ZELAND — New Zealand" in line
    ]

    if len(australia_lines) != 2:
        raise RuntimeError(
            "ERROR: Australia duplicate lines are missing from output."
        )

    if len(new_zealand_lines) != 2:
        raise RuntimeError(
            "ERROR: New Zealand duplicate lines are missing from output."
        )

    print("  Parentheses:    OK")
    print("  Duplicates:     OK")
    print("  Line count:     OK")
    print("")
    print("Validation successful.")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():

    pdf_data = download_pdf()

    raw_text = extract_pdf_text(pdf_data)

    entries = find_entries(raw_text)

    output = create_output(entries)

    validate_output(entries, output)

    OUTPUT_FILE.write_text(
        output,
        encoding="utf-8",
    )

    print(f"Created {OUTPUT_FILE}")
    print(f"Output contains {len(output.splitlines())} lines.")


if __name__ == "__main__":
    main()
