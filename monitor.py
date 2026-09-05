import re
import urllib.request
from pathlib import Path

import pymupdf


PDF_URL = (
    "https://www.post.ba/media/files/"
    "POPIS%20DR%C5%BDAVA%20MEDJ%20PROMET%2013_12_2023.pdf"
)

OUTPUT_FILE = Path("output.txt")
PDF_FILE = Path("mostar_post.pdf")


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


MAPPING = {
    "ALBANIJA": (3, "Albania"),
    "ALŽIR": (4, "Algeria"),
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
    "GANA": (83, "Ghana"),
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
    "NAURU": (153, "Nauru / Naoero"),
    "NEPAL": (154, "Nepal"),
    "NIGER": (159, "Niger"),
    "NIGERIJA": (160, "Nigeria"),
    "NIKARAGVA": (158, "Nicaragua"),
    "NIUE": (161, "Niue"),
    "NIZOZEMSKA": (155, "Netherlands"),
    "NIZOZEMSKI ANTILI": [
        (13, "Aruba"),
        (28, "Bonaire, Sint Eustatius and Saba"),
        (57, "Curaçao"),
        (200, "Sint Maarten"),
    ],
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
    "TRINIDAD I TO TOBAGO": (224, "Trinidad and Tobago"),
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


def normalize_text(text):
    text = text.replace("\u00a0", " ")
    text = text.replace("\r", " ")
    text = text.replace("\n", " ")
    text = text.replace("–", " – ")
    text = text.replace("—", " — ")

    text = text.replace(
        "GVINEJA – BISAUHAITI",
        "GVINEJA – BISAU HAITI",
    )

    text = text.replace(
        "OVČJI OTOCIPAKISTAN",
        "OVČJI OTOCI PAKISTAN",
    )

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def remove_parentheses(text):
    text = re.sub(r"\s*\([^)]*\)", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def base_entry(entry):
    return remove_parentheses(entry)


def download_pdf():
    print("Downloading PDF...")

    request = urllib.request.Request(
        PDF_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/131.0 Safari/537.36"
            )
        },
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()

    if not data.startswith(b"%PDF"):
        raise RuntimeError(
            "Downloaded file is not a valid PDF."
        )

    PDF_FILE.write_bytes(data)

    print(f"Downloaded {len(data):,} bytes.")


def extract_pdf_text():
    print("Extracting PDF text...")

    with pymupdf.open(PDF_FILE) as document:
        pages = [
            page.get_text("text")
            for page in document
        ]

    text = normalize_text("\n".join(pages))

    if not text:
        raise RuntimeError(
            "No text could be extracted from the PDF."
        )

    return text


def find_pdf_entries(text):
    print("Finding PDF entries...")

    normalized_text = normalize_text(text)
    search_text = normalized_text.casefold()

    found_entries = []
    position = 0

    for index, expected in enumerate(
        PDF_ENTRIES,
        start=1,
    ):
        expected_normalized = normalize_text(expected)
        expected_search = expected_normalized.casefold()

        found_at = search_text.find(
            expected_search,
            position,
        )

        if found_at != -1:
            position = (
                found_at
                + len(expected_normalized)
            )

            found_entries.append(expected)
            continue

        base = base_entry(expected)
        base_normalized = normalize_text(base)
        base_search = base_normalized.casefold()

        found_at = search_text.find(
            base_search,
            position,
        )

        if found_at == -1:
            context_start = max(
                0,
                position - 150,
            )

            context_end = min(
                len(normalized_text),
                position + 500,
            )

            context = normalized_text[
                context_start:context_end
            ]

            raise RuntimeError(
                f"Could not find PDF entry #{index}:\n\n"
                f"{expected}\n\n"
                f"Search context:\n\n{context}"
            )

        position = (
            found_at
            + len(base_normalized)
        )

        found_entries.append(expected)

        print(
            "  Note: entry "
            f"#{index} matched by base name: "
            f"{base}"
        )

    print(
        f"Found {len(found_entries)} PDF entries."
    )

    return found_entries


def create_output(entries):
    print("Creating output.txt...")

    output_lines = []

    for entry in entries:
        source = base_entry(entry)

        if source == "NIZOZEMSKI ANTILI":
            destinations = MAPPING[
                "NIZOZEMSKI ANTILI"
            ]

            for number, english in destinations:
                english = remove_parentheses(
                    english
                )

                output_lines.append(
                    f"{number}. "
                    f"{source} — "
                    f"{english}"
                )

            continue

        if source not in MAPPING:
            raise RuntimeError(
                "No Postcrossing mapping exists "
                f"for PDF entry: {source}"
            )

        mapping = MAPPING[source]

        if (
            not isinstance(mapping, tuple)
            or len(mapping) != 2
        ):
            raise RuntimeError(
                f"Invalid mapping for PDF entry: "
                f"{source}"
            )

        number, english = mapping

        source_clean = remove_parentheses(
            source
        )

        english_clean = remove_parentheses(
            english
        )

        if number is None:
            line = (
                f"{source_clean} — "
                f"{english_clean}"
            )
        else:
            line = (
                f"{number}. "
                f"{source_clean} — "
                f"{english_clean}"
            )

        output_lines.append(line)

    OUTPUT_FILE.write_text(
        "\n".join(output_lines) + "\n",
        encoding="utf-8",
    )

    print(f"Created {OUTPUT_FILE}")
    print(
        f"Output lines: {len(output_lines)}"
    )

    return output_lines


def validate_output(entries, output_lines):
    print("Validating output...")

    expected_output_lines = sum(
        4
        if base_entry(entry)
        == "NIZOZEMSKI ANTILI"
        else 1
        for entry in entries
    )

    if len(output_lines) != expected_output_lines:
        raise RuntimeError(
            "Output line count is incorrect: "
            f"expected {expected_output_lines}, "
            f"got {len(output_lines)}."
        )

    for line in output_lines:
        if "(" in line or ")" in line:
            raise RuntimeError(
                "Parentheses remain in output:\n"
                f"{line}"
            )

    australia_count = sum(
        1
        for line in output_lines
        if "AUSTRALIJA — Australia" in line
    )

    if australia_count != 2:
        raise RuntimeError(
            "Expected 2 Australia lines, "
            f"got {australia_count}."
        )

    new_zealand_count = sum(
        1
        for line in output_lines
        if "NOVI ZELAND — New Zealand" in line
    )

    if new_zealand_count != 2:
        raise RuntimeError(
            "Expected 2 New Zealand lines, "
            f"got {new_zealand_count}."
        )

    christmas_count = sum(
        1
        for line in output_lines
        if "BOŽIĆNI OTOK — Christmas Island"
        in line
    )

    if christmas_count != 2:
        raise RuntimeError(
            "Expected 2 Christmas Island lines, "
            f"got {christmas_count}."
        )

    cayman_lines = [
        line
        for line in output_lines
        if "KAJMANSKI OTOCI — Cayman Islands"
        in line
    ]

    if len(cayman_lines) != 1:
        raise RuntimeError(
            "Expected exactly one Cayman Islands "
            "line, "
            f"got {len(cayman_lines)}."
        )

    venezuela_lines = [
        line
        for line in output_lines
        if "VENEZUELA — Venezuela" in line
    ]

    if len(venezuela_lines) != 1:
        raise RuntimeError(
            "Expected exactly one "
            "VENEZUELA — Venezuela line, "
            f"got {len(venezuela_lines)}."
        )

    expected_venezuela = (
        "240. VENEZUELA — Venezuela"
    )

    if venezuela_lines != [
        expected_venezuela
    ]:
        raise RuntimeError(
            "Venezuela mapping is incorrect.\n\n"
            "Expected:\n"
            f"{expected_venezuela}\n\n"
            "Got:\n"
            + "\n".join(venezuela_lines)
        )

    antilles_lines = [
        line
        for line in output_lines
        if "NIZOZEMSKI ANTILI —" in line
    ]

    expected_antilles = [
        "13. NIZOZEMSKI ANTILI — Aruba",
        (
            "28. NIZOZEMSKI ANTILI — "
            "Bonaire, Sint Eustatius and Saba"
        ),
        "57. NIZOZEMSKI ANTILI — Curaçao",
        "200. NIZOZEMSKI ANTILI — Sint Maarten",
    ]

    if antilles_lines != expected_antilles:
        raise RuntimeError(
            "NIZOZEMSKI ANTILI mapping is "
            "incorrect.\n\n"
            "Expected:\n"
            + "\n".join(expected_antilles)
            + "\n\nGot:\n"
            + "\n".join(antilles_lines)
        )

    for line in antilles_lines:
        if "Netherlands" in line:
            raise RuntimeError(
                "ERROR: Netherlands was "
                "incorrectly included in "
                "NIZOZEMSKI ANTILI."
            )

    netherlands_lines = [
        line
        for line in output_lines
        if "NIZOZEMSKA — Netherlands" in line
    ]

    if len(netherlands_lines) != 1:
        raise RuntimeError(
            "Expected exactly one separate "
            "NIZOZEMSKA — Netherlands line."
        )

    print("Validation successful.")
    print(
        f"Expected output lines: "
        f"{expected_output_lines}"
    )
    print(
        f"Actual output lines:   "
        f"{len(output_lines)}"
    )
    print("Australia entries:     2")
    print("New Zealand entries:   2")
    print("Christmas Island:      2")
    print("Cayman Islands:        1")
    print("Venezuela:             1")
    print("Netherlands Antilles:  4")
    print("Netherlands in Antilles: NO")


def main():
    download_pdf()

    text = extract_pdf_text()

    entries = find_pdf_entries(text)

    output_lines = create_output(entries)

    validate_output(
        entries,
        output_lines,
    )

    print()
    print("Done.")
    print(
        f"Generated: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
