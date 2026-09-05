import re
import urllib.request
from pathlib import Path

import fitz  # PyMuPDF


PDF_URL = (
    "https://www.post.ba/media/files/"
    "POPIS%20DR%C5%BDAVA%20MEDJ%20PROMET%2013_12_2023.pdf"
)

PDF_FILE = Path("source.pdf")
OUTPUT_FILE = Path("output.txt")


POSTCROSSING_DATA = """
1 Afghanistan
2 Åland Islands
3 Albania
4 Algeria
5 American Samoa
6 Andorra
7 Angola
8 Anguilla
9 Antarctica
10 Antigua & Barbuda
11 Argentina
12 Armenia
13 Aruba
14 Australia
15 Austria
16 Azerbaijan
17 Bahamas
18 Bahrain
19 Bangladesh
20 Barbados
21 Belarus
22 Belgium
23 Belize
24 Benin
25 Bermuda
26 Bhutan
27 Bolivia
28 Bonaire, Sint Eustatius and Saba
29 Bosnia-Herzegovina
30 Botswana
31 Brazil
32 British Indian Ocean Territory
33 Brunei
34 Bulgaria
35 Burkina Faso
36 Burundi
37 Cabo Verde
38 Cambodia
39 Cameroon
40 Canada
41 Cayman Islands
42 Central African Republic
43 Chad
44 Chile
45 China
46 Christmas Island
47 Cocos Islands
48 Colombia
49 Comoros
50 Congo
51 Dem. Rep. Of Congo
52 Cook Islands
53 Costa Rica
54 Côte d'Ivoire
55 Croatia
56 Cuba
57 Curaçao
58 Cyprus
59 Czechia
60 Denmark
61 Djibouti
62 Dominica
63 Dominican Republic
64 Ecuador
65 Egypt
66 El Salvador
67 Equatorial Guinea
68 Eritrea
69 Estonia
70 Eswatini /Swaziland
71 Ethiopia
72 Falkland Islands /Malvinas
73 Faroe Islands
74 Fiji
75 Finland
76 France
77 French Guiana
78 French Polynesia
79 French Southern Territories
80 Gabon
81 Gambia
82 Georgia
83 Germany
84 Ghana
85 Gibraltar
86 Greece
87 Greenland
88 Grenada
89 Guadeloupe
90 Guam
91 Guatemala
92 Guernsey
93 Guinea
94 Guinea-Bissau
95 Guyana
96 Haiti
97 Honduras
98 Hong Kong
99 Hungary
100 Iceland
101 India
102 Indonesia
103 Iran
104 Iraq
105 Ireland
106 Isle of Man
107 Israel
108 Italy
109 Jamaica
110 Japan
111 Jersey
112 Jordan
113 Kazakhstan
114 Kenya
115 Kiribati
116 Korea(North)
117 Korea(South)
118 Kosovo
119 Kuwait
120 Kyrgyzstan
121 Laos
122 Latvia
123 Lebanon
124 Lesotho
125 Liberia
126 Libya
127 Liechtenstein
128 Lithuania
129 Luxembourg
130 Macao
131 Madagascar
132 Malawi
133 Malaysia
134 Maldives
135 Mali
136 Malta
137 Marshall Islands
138 Martinique
139 Mauritania
140 Mauritius
141 Mayotte
142 Mexico
143 Micronesia
144 Moldova
145 Monaco
146 Mongolia
147 Montenegro
148 Montserrat
149 Morocco
150 Mozambique
151 Myanmar
152 Namibia
153 Nauru / Naoero
154 Nepal
155 Netherlands
156 New Caledonia
157 New Zealand
158 Nicaragua
159 Niger
160 Nigeria
161 Niue
162 Norfolk Island
163 Northern Mariana Islands
164 North Macedonia
165 Norway
166 Oman
167 Pakistan
168 Palau
169 Palestine
170 Panama
171 Papua New Guinea
172 Paraguay
173 Peru
174 Philippines
175 Pitcairn
176 Poland
177 Portugal
178 Puerto Rico
179 Qatar
180 Réunion
181 Romania
182 Russia
183 Rwanda
184 Saint Barthélemy
185 Saint Helena, Ascension and Tristan da Cunha
186 Saint Kitts and Nevis
187 Saint Lucia
188 Saint Martin
189 Saint Pierre & Miquelon
190 Saint Vincent and the Grenadines
191 Samoa
192 San Marino
193 Sao Tome and Principe
194 Saudi Arabia
195 Senegal
196 Serbia
197 Seychelles
198 Sierra Leone
199 Singapore
200 Sint Maarten
201 Slovakia
202 Slovenia
203 Solomon Islands
204 Somalia
205 South Africa
206 South Georgia and S. Sandwich Islands
207 South Sudan
208 Spain
209 Sri Lanka
210 Sudan
211 Suriname
212 Svalbard and Jan Mayen
213 Sweden
214 Switzerland
215 Syria
216 Taiwan
217 Tajikistan
218 Tanzania
219 Thailand
220 Timor-Leste
221 Togo
222 Tokelau
223 Tonga
224 Trinidad and Tobago
225 Tunisia
226 Turkey
227 Turkmenistan
228 Turks and Caicos Islands
229 Tuvalu
230 Uganda
231 Ukraine
232 United Arab Emirates
233 United Kingdom
234 Uruguay
235 U.S.A.
236 U.S. Minor Outlying Islands
237 Uzbekistan
238 Vanuatu
239 Vatican
240 Venezuela
241 Vietnam
242 Virgin Islands (UK)
243 Virgin Islands of the USA
244 Wallis & Futuna
245 Western Sahara
246 Yemen
247 Zambia
248 Zimbabwe
"""


def parse_postcrossing_numbers(data):
    numbers = {}

    for line in data.strip().splitlines():
        line = line.strip()

        if not line:
            continue

        match = re.match(r"^(\d+)\s+(.+)$", line)

        if match:
            number = int(match.group(1))
            name = match.group(2).strip()
            numbers[name] = number

    return numbers


POSTCROSSING_NUMBERS = parse_postcrossing_numbers(POSTCROSSING_DATA)


TRANSLATIONS = {
    "AFGANISTAN": "Afghanistan",
    "ALBANIJA": "Albania",
    "ALŽIR": "Algeria",
    "AMERIČKA SAMOA": "American Samoa",
    "ANDORA": "Andorra",
    "ANGOLA": "Angola",
    "ANGVILA": "Anguilla",
    "ANTARKTIK": "Antarctica",
    "ANTIGVA I BARBUDA": "Antigua & Barbuda",
    "ARGENTINA": "Argentina",
    "ARMENIJA": "Armenia",
    "ARUBA": "Aruba",
    "AUSTRALIJA": "Australia",
    "AUSTRIJA": "Austria",
    "AZERBEJDŽAN": "Azerbaijan",
    "BAHAMI": "Bahamas",
    "BAHREIN": "Bahrain",
    "BANGLADEŠ": "Bangladesh",
    "BARBADOS": "Barbados",
    "BELGIJA": "Belgium",
    "BELIZE": "Belize",
    "BENIN": "Benin",
    "BERMUDI": "Bermuda",
    "BJELORUSIJA": "Belarus",
    "BUTAN": "Bhutan",
    "BOLIVIJA": "Bolivia",
    "BOSNA I HERCEGOVINA": "Bosnia-Herzegovina",
    "BOTSVANA": "Botswana",
    "BRAZIL": "Brazil",
    "BRITANSKI INDIJSKI OCEANSKI TERITORIJ": "British Indian Ocean Territory",
    "BRUNEJ": "Brunei",
    "BUGARSKA": "Bulgaria",
    "BURKINA FASO": "Burkina Faso",
    "BURUNDI": "Burundi",
    "ZELENORTSKA OTOČJA": "Cabo Verde",
    "KAMBODŽA": "Cambodia",
    "KAMERUN": "Cameroon",
    "KANADA": "Canada",
    "KAJMANSKI OTOCI": "Cayman Islands",
    "SREDNJOAFRIČKA REPUBLIKA": "Central African Republic",
    "ČAD": "Chad",
    "ČILE": "Chile",
    "KINA": "China",
    "BOŽIĆNI OTOK": "Christmas Island",
    "KOKOSOVI OTOCI": "Cocos Islands",
    "KOLUMBIJA": "Colombia",
    "KOMORI": "Comoros",
    "KONGO": "Congo",
    "DEMOKRATSKA REPUBLIKA KONGO": "Dem. Rep. Of Congo",
    "KUKOVI OTOCI": "Cook Islands",
    "KOSTARIKA": "Costa Rica",
    "OBALA BJELOKOSTI": "Côte d'Ivoire",
    "HRVATSKA": "Croatia",
    "KUBA": "Cuba",
    "KURASAO": "Curaçao",
    "CIPAR": "Cyprus",
    "ČEŠKA": "Czechia",
    "DANSKA": "Denmark",
    "DŽIBUTI": "Djibouti",
    "DOMINIKA": "Dominica",
    "DOMINIKANSKA REPUBLIKA": "Dominican Republic",
    "EKVADOR": "Ecuador",
    "EGIPAT": "Egypt",
    "EL SALVADOR": "El Salvador",
    "EKVATORSKA GVINEJA": "Equatorial Guinea",
    "ERITREJA": "Eritrea",
    "ESTONIJA": "Estonia",
    "ESVATINI": "Eswatini /Swaziland",
    "ETIOPIJA": "Ethiopia",
    "FAKLANDI": "Falkland Islands /Malvinas",
    "OVČJI OTOCI": "Faroe Islands",
    "FIDŽI": "Fiji",
    "FINSKA": "Finland",
    "FRANCUSKA": "France",
    "FRANCUSKA GVAJANA": "French Guiana",
    "FRANCUSKA POLINEZIJA": "French Polynesia",
    "FRANCUSKI JUŽNI TERITORIJI": "French Southern Territories",
    "GABON": "Gabon",
    "GAMBIJA": "Gambia",
    "GRUZIJA": "Georgia",
    "NJEMAČKA": "Germany",
    "GANA": "Ghana",
    "GIBRALTAR": "Gibraltar",
    "GRČKA": "Greece",
    "GRENLAND": "Greenland",
    "GRENADA": "Grenada",
    "GVADALUPA": "Guadeloupe",
    "GUAM": "Guam",
    "GVATEMALA": "Guatemala",
    "GUERNSEY": "Guernsey",
    "GVINEJA": "Guinea",
    "GVINEJA-BISAU": "Guinea-Bissau",
    "GVAJANA": "Guyana",
    "HAITI": "Haiti",
    "HONDURAS": "Honduras",
    "HONG KONG": "Hong Kong",
    "MAĐARSKA": "Hungary",
    "ISLAND": "Iceland",
    "INDIJA": "India",
    "INDONEZIJA": "Indonesia",
    "IRAN": "Iran",
    "IRAK": "Iraq",
    "IRSKA": "Ireland",
    "OTOK MAN": "Isle of Man",
    "IZRAEL": "Israel",
    "ITALIJA": "Italy",
    "JAMAJKA": "Jamaica",
    "JAPAN": "Japan",
    "JERSEY": "Jersey",
    "JORDAN": "Jordan",
    "KAZAHSTAN": "Kazakhstan",
    "KENIJA": "Kenya",
    "KIRIBATI": "Kiribati",
    "SJEVERNA KOREJA": "Korea(North)",
    "JUŽNA KOREJA": "Korea(South)",
    "KOSOVO": "Kosovo",
    "KUVAJT": "Kuwait",
    "KIRGISTAN": "Kyrgyzstan",
    "LAOSKA NARODNA DEMOKRATSKA REPUBLIKA": "Laos",
    "LATVIJA": "Latvia",
    "LIBANON": "Lebanon",
    "LESOTO": "Lesotho",
    "LIBERIJA": "Liberia",
    "LIBIJA": "Libya",
    "LIHTENŠTAJN": "Liechtenstein",
    "LITVA": "Lithuania",
    "LUKSEMBURG": "Luxembourg",
    "MAKAO": "Macao",
    "MADAGASKAR": "Madagascar",
    "MALAVI": "Malawi",
    "MALEZIJA": "Malaysia",
    "MALDIVI": "Maldives",
    "MALI": "Mali",
    "MALTA": "Malta",
    "MARŠALOVI OTOCI": "Marshall Islands",
    "MARTINIK": "Martinique",
    "MAURITANIJA": "Mauritania",
    "MAURICIJUS": "Mauritius",
    "MAJOT": "Mayotte",
    "MEKSIKO": "Mexico",
    "MIKRONEZIJA": "Micronesia",
    "MOLDAVIJA": "Moldova",
    "MONAKO": "Monaco",
    "MONGOLIJA": "Mongolia",
    "CRNA GORA": "Montenegro",
    "MONTSERRAT": "Montserrat",
    "MAROKO": "Morocco",
    "MOZAMBIK": "Mozambique",
    "MIJANMAR": "Myanmar",
    "NAMIBIJA": "Namibia",
    "NAURU": "Nauru / Naoero",
    "NEPAL": "Nepal",
    "NIZOZEMSKA": "Netherlands",
    "NOVA KALEDONIJA": "New Caledonia",
    "NOVI ZELAND": "New Zealand",
    "NIKARAGVA": "Nicaragua",
    "NIGER": "Niger",
    "NIGERIJA": "Nigeria",
    "NIUE": "Niue",
    "NORFOLK": "Norfolk Island",
    "SJEVERNI MARIJANSKI OTOCI": "Northern Mariana Islands",
    "SJEVERNA MAKEDONIJA": "North Macedonia",
    "NORVEŠKA": "Norway",
    "OMAN": "Oman",
    "PAKISTAN": "Pakistan",
    "PALAU": "Palau",
    "PALESTINA": "Palestine",
    "PANAMA": "Panama",
    "PAPUA NOVA GVINEJA": "Papua New Guinea",
    "PARAGVAJ": "Paraguay",
    "PERU": "Peru",
    "FILIPINI": "Philippines",
    "PITCAIRN": "Pitcairn",
    "POLJSKA": "Poland",
    "PORTUGAL": "Portugal",
    "PORTORIKO": "Puerto Rico",
    "KATAR": "Qatar",
    "REUNION": "Réunion",
    "RUMUNJSKA": "Romania",
    "RUSIJA": "Russia",
    "RUANDA": "Rwanda",
    "SVETI BARTOLOMEJ": "Saint Barthélemy",
    "SVETA HELENA": "Saint Helena, Ascension and Tristan da Cunha",
    "SVETI KIT I NEVIS": "Saint Kitts and Nevis",
    "SVETA LUCIJA": "Saint Lucia",
    "SVETI MARTIN": "Saint Martin",
    "SVETI PETAR I MIKELO": "Saint Pierre & Miquelon",
    "SVETI VINCENT I GRENADINI": "Saint Vincent and the Grenadines",
    "SAMOA": "Samoa",
    "SAN MARINO": "San Marino",
    "SAO TOME I PRINCIPE": "Sao Tome and Principe",
    "SAUDIJSKA ARABIJA": "Saudi Arabia",
    "SENEGAL": "Senegal",
    "SRBIJA": "Serbia",
    "SEJŠELI": "Seychelles",
    "SIJERA LEONE": "Sierra Leone",
    "SINGAPUR": "Singapore",
    "SINT MAARTEN": "Sint Maarten",
    "SLOVAČKA": "Slovakia",
    "SLOVENIJA": "Slovenia",
    "SALOMONSKI OTOCI": "Solomon Islands",
    "SOMALIJA": "Somalia",
    "JUŽNA AFRIKA": "South Africa",
    "JUŽNA DŽORDŽIJA": "South Georgia and S. Sandwich Islands",
    "JUŽNI SENDVIČ OTOCI": "South Georgia and S. Sandwich Islands",
    "JUŽNI SUDAN": "South Sudan",
    "ŠPANJOLSKA": "Spain",
    "ŠRI LANKA": "Sri Lanka",
    "SUDAN": "Sudan",
    "SURINAM": "Suriname",
    "SVALBARD I JAN MAYEN": "Svalbard and Jan Mayen",
    "ŠVEDSKA": "Sweden",
    "ŠVICARSKA": "Switzerland",
    "SIRIJA": "Syria",
    "TAJVAN": "Taiwan",
    "TADŽIKISTAN": "Tajikistan",
    "TANZANIJA": "Tanzania",
    "TAJLAND": "Thailand",
    "TIMOR-LESTE": "Timor-Leste",
    "TOGO": "Togo",
    "TOKELAU": "Tokelau",
    "TONGA": "Tonga",
    "TRINIDAD I TOBAGO": "Trinidad and Tobago",
    "TUNIS": "Tunisia",
    "TURSKA": "Turkey",
    "TURKMENISTAN": "Turkmenistan",
    "TURKS I CAICOS OTOCI": "Turks and Caicos Islands",
    "TUVALU": "Tuvalu",
    "UGANDA": "Uganda",
    "UKRAJINA": "Ukraine",
    "UJEDINJENI ARAPSKI EMIRATI": "United Arab Emirates",
    "UJEDINJENI ARAPSLI EMIRATI": "United Arab Emirates",
    "UJEDINJENO KRALJEVSTVO VELIKE BRITANIJE I SJEVERNE IRSKE": "United Kingdom",
    "URUGVAJ": "Uruguay",
    "SAD": "U.S.A.",
    "AMERIČKI MANJI OTOCI": "U.S. Minor Outlying Islands",
    "UZBEKISTAN": "Uzbekistan",
    "VANUATU": "Vanuatu",
    "VATIKAN": "Vatican",
    "VENECUELA": "Venezuela",
    "VIJETNAM": "Vietnam",
    "DJEVIČANSKI OTOCI (UK)": "Virgin Islands (UK)",
    "DJEVIČANSKI OTOCI SAD": "Virgin Islands of the USA",
    "WALLIS I FUTUNA": "Wallis & Futuna",
    "ZAPADNA SAHARA": "Western Sahara",
    "JEMEN": "Yemen",
    "ZAMBIJA": "Zambia",
    "ZIMBABVE": "Zimbabwe",
    "TRISTAN DA KUNA": "Saint Helena, Ascension and Tristan da Cunha",
}


def normalize_text(text):
    """
    Normalize whitespace and dash characters.
    """
    text = text.replace("\u00a0", " ")
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("−", "-")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def remove_parenthetical_text(text):
    """
    Remove everything inside parentheses, including the parentheses.
    """
    return re.sub(r"\([^)]*\)", "", text)


def extract_pdf_entries():
    """
    Download the PDF and extract the destination entries.

    The PDF has a few formatting/page-break problems, so several
    known entries are repaired after extraction.
    """
    request = urllib.request.Request(
        PDF_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (compatible; MostarPostMonitor/1.0)"
            )
        },
    )

    print("Downloading PDF...")

    with urllib.request.urlopen(request, timeout=60) as response:
        pdf_data = response.read()

    if not pdf_data.startswith(b"%PDF"):
        raise RuntimeError("Downloaded file does not appear to be a PDF.")

    PDF_FILE.write_bytes(pdf_data)

    print(f"Downloaded {len(pdf_data):,} bytes.")

    document = fitz.open(PDF_FILE)

    raw_lines = []

    for page in document:
        page_text = page.get_text("text")

        for line in page_text.splitlines():
            line = normalize_text(line)

            if line:
                raw_lines.append(line)

    document.close()

    # Remove the title/header and other obvious non-country lines.
    entries = []

    for line in raw_lines:
        upper = line.upper().strip()

        if not upper:
            continue

        if "POPIS DRŽAVA U KOJE JE MOGUĆE SLATI POŠILJKE" in upper:
            continue

        if upper in {
            "DRŽAVE",
            "DRZAVE",
            "STRANICA",
        }:
            continue

        # Remove parenthetical service notes.
        line = remove_parenthetical_text(line)
        line = normalize_text(line)

        if not line:
            continue

        entries.append(line)

    # ------------------------------------------------------------
    # Repair PDF extraction problems.
    # ------------------------------------------------------------

    repaired = []

    i = 0

    while i < len(entries):
        current = entries[i]
        upper = current.upper()

        # Page-break problem:
        # GVINEJA – BISAUHAITI
        if "GVINEJA" in upper and "BISAU" in upper:
            repaired.append("GVINEJA")
            repaired.append("GVINEJA-BISAU")
            repaired.append("HAITI")
            i += 1
            continue

        # Page-break problem:
        # OVČJI OTOCIPAKISTAN
        if "OVČJI OTOCI" in upper and "PAKISTAN" in upper:
            repaired.append("OVČJI OTOCI")
            repaired.append("PAKISTAN")
            i += 1
            continue

        repaired.append(current)
        i += 1

    entries = repaired

    # ------------------------------------------------------------
    # Join known multi-line country names.
    # ------------------------------------------------------------

    joined = []

    i = 0

    while i < len(entries):
        current = entries[i].strip()
        upper = current.upper()

        # DEMOKRATSKA NARODNA
        # REPUBLIKA KOREJA
        if (
            upper == "DEMOKRATSKA NARODNA"
            and i + 1 < len(entries)
            and entries[i + 1].upper() == "REPUBLIKA KOREJA"
        ):
            joined.append("SJEVERNA KOREJA")
            i += 2
            continue

        # LAOSKA NARODNA DEMOKRATSKA
        # REPUBLIKA
        if (
            upper == "LAOSKA NARODNA DEMOKRATSKA"
            and i + 1 < len(entries)
            and entries[i + 1].upper() == "REPUBLIKA"
        ):
            joined.append("LAOSKA NARODNA DEMOKRATSKA REPUBLIKA")
            i += 2
            continue

        # UJEDINJENA KRALJEVINA VELIKE
        # BRITANIJE I SJEVERNE IRSKE
        if (
            upper == "UJEDINJENA KRALJEVINA VELIKE"
            and i + 1 < len(entries)
            and entries[i + 1].upper()
            == "BRITANIJE I SJEVERNE IRSKE"
        ):
            joined.append(
                "UJEDINJENO KRALJEVSTVO VELIKE BRITANIJE "
                "I SJEVERNE IRSKE"
            )
            i += 2
            continue

        joined.append(current)
        i += 1

    entries = joined

    # ------------------------------------------------------------
    # Clean up known OCR/PDF extraction typos.
    # ------------------------------------------------------------

    cleaned = []

    for entry in entries:
        entry = normalize_text(entry)

        if entry.upper() == "UJEDINJENI ARAPSLI EMIRATI":
            entry = "UJEDINJENI ARAPSLI EMIRATI"

        cleaned.append(entry)

    return cleaned


def get_translation(croatian_name):
    """
    Return the English/Postcrossing name for a PDF entry.
    """
    name = normalize_text(croatian_name).upper()

    if name in TRANSLATIONS:
        return TRANSLATIONS[name]

    # Try a few common normalization variations.
    name = name.replace("  ", " ")

    if name in TRANSLATIONS:
        return TRANSLATIONS[name]

    # Fallback: preserve the entry rather than silently dropping it.
    print(f"WARNING: No translation found for: {croatian_name}")

    return croatian_name.title()


def get_postcrossing_number(english_name):
    """
    Find the Postcrossing number.

    Several Postcrossing names differ slightly from the English
    translation used in the PDF.
    """
    aliases = {
        "United States": "U.S.A.",
        "Côte d’Ivoire": "Côte d'Ivoire",
        "North Macedonia": "North Macedonia",
        "South Korea": "Korea(South)",
        "North Korea": "Korea(North)",
        "British Virgin Islands": "Virgin Islands (UK)",
        "U.S. Virgin Islands": "Virgin Islands of the USA",
        "Saint Helena": "Saint Helena, Ascension and Tristan da Cunha",
    }

    lookup_name = aliases.get(english_name, english_name)

    return POSTCROSSING_NUMBERS.get(lookup_name)


def create_output(entries):
    """
    Create output.txt.

    IMPORTANT:
    There is deliberately NO deduplication here.

    Every entry extracted from the PDF produces one output line.
    """
    output_lines = []

    for croatian_name in entries:
        english_name = get_translation(croatian_name)
        number = get_postcrossing_number(english_name)

        if number is not None:
            output_lines.append(
                f"{number}. {croatian_name} — {english_name}"
            )
        else:
            output_lines.append(
                f"{croatian_name} — {english_name}"
            )

    OUTPUT_FILE.write_text(
        "\n".join(output_lines) + "\n",
        encoding="utf-8",
    )

    return output_lines


def main():
    try:
        entries = extract_pdf_entries()

        print(f"PDF entries detected: {len(entries)}")

        if not entries:
            raise RuntimeError(
                "No destination entries were extracted from the PDF."
            )

        output_lines = create_output(entries)

        print(f"Output entries written: {len(output_lines)}")
        print(f"Output file: {OUTPUT_FILE}")

        # This is intentionally informational only.
        # Repeated destinations are NOT removed.
        if len(output_lines) != len(entries):
            raise RuntimeError(
                "Internal error: output entry count does not match "
                "PDF entry count."
            )

    except Exception as exc:
        print(f"ERROR: {exc}")
        raise

    finally:
        if PDF_FILE.exists():
            PDF_FILE.unlink()
            print("Removed temporary source.pdf")


if __name__ == "__main__":
    main()
