#!/usr/bin/env python3

import re
import sys
import urllib.request
from pathlib import Path

import fitz  # PyMuPDF


# ============================================================
# CONFIGURATION
# ============================================================

PDF_URL = (
    "https://www.post.ba/media/files/"
    "POPIS%20DR%C5%BDAVA%20MEDJ%20PROMET%2013_12_2023.pdf"
)

OUTPUT_FILE = Path("countries.txt")
PDF_FILE = Path("source.pdf")


# ============================================================
# POSTCROSSING NUMBERS
#
# These are the numbers supplied by the user from the
# Postcrossing countries/territories list.
# ============================================================

POSTCROSSING_DATA = """
1|Afghanistan
2|Åland Islands
3|Albania
4|Algeria
5|American Samoa
6|Andorra
7|Angola
8|Anguilla
9|Antarctica
10|Antigua & Barbuda
11|Argentina
12|Armenia
13|Aruba
14|Australia
15|Austria
16|Azerbaijan
17|Bahamas
18|Bahrain
19|Bangladesh
20|Barbados
21|Belarus
22|Belgium
23|Belize
24|Benin
25|Bermuda
26|Bhutan
27|Bolivia
28|Bonaire, Sint Eustatius and Saba
29|Bosnia-Herzegovina
30|Botswana
31|Brazil
32|British Indian Ocean Territory
33|Brunei
34|Bulgaria
35|Burkina Faso
36|Burundi
37|Cabo Verde
38|Cambodia
39|Cameroon
40|Canada
41|Cayman Islands
42|Central African Republic
43|Chad
44|Chile
45|China
46|Christmas Island
47|Cocos Islands
48|Colombia
49|Comoros
50|Congo
51|Dem. Rep. Of Congo
52|Cook Islands
53|Costa Rica
54|Côte d'Ivoire
55|Croatia
56|Cuba
57|Curaçao
58|Cyprus
59|Czechia
60|Denmark
61|Djibouti
62|Dominica
63|Dominican Republic
64|Ecuador
65|Egypt
66|El Salvador
67|Equatorial Guinea
68|Eritrea
69|Estonia
70|Eswatini /Swaziland
71|Ethiopia
72|Falkland Islands /Malvinas
73|Faroe Islands
74|Fiji
75|Finland
76|France
77|French Guiana
78|French Polynesia
79|French Southern Territories
80|Gabon
81|Gambia
82|Georgia
83|Germany
84|Ghana
85|Gibraltar
86|Greece
87|Greenland
88|Grenada
89|Guadeloupe
90|Guam
91|Guatemala
92|Guernsey
93|Guinea
94|Guinea-Bissau
95|Guyana
96|Haiti
97|Honduras
98|Hong Kong
99|Hungary
100|Iceland
101|India
102|Indonesia
103|Iran
104|Iraq
105|Ireland
106|Isle of Man
107|Israel
108|Italy
109|Jamaica
110|Japan
111|Jersey
112|Jordan
113|Kazakhstan
114|Kenya
115|Kiribati
116|Korea(North)
117|Korea(South)
118|Kosovo
119|Kuwait
120|Kyrgyzstan
121|Laos
122|Latvia
123|Lebanon
124|Lesotho
125|Liberia
126|Libya
127|Liechtenstein
128|Lithuania
129|Luxembourg
130|Macao
131|Madagascar
132|Malawi
133|Malaysia
134|Maldives
135|Mali
136|Malta
137|Marshall Islands
138|Martinique
139|Mauritania
140|Mauritius
141|Mayotte
142|Mexico
143|Micronesia
144|Moldova
145|Monaco
146|Mongolia
147|Montenegro
148|Montserrat
149|Morocco
150|Mozambique
151|Myanmar
152|Namibia
153|Nauru / Naoero
154|Nepal
155|Netherlands
156|New Caledonia
157|New Zealand
158|Nicaragua
159|Niger
160|Nigeria
161|Niue
162|Norfolk Island
163|Northern Mariana Islands
164|North Macedonia
165|Norway
166|Oman
167|Pakistan
168|Palau
169|Palestine
170|Panama
171|Papua New Guinea
172|Paraguay
173|Peru
174|Philippines
175|Pitcairn
176|Poland
177|Portugal
178|Puerto Rico
179|Qatar
180|Réunion
181|Romania
182|Russia
183|Rwanda
184|Saint Barthélemy
185|Saint Helena, Ascension and Tristan da Cunha
186|Saint Kitts and Nevis
187|Saint Lucia
188|Saint Martin
189|Saint Pierre & Miquelon
190|Saint Vincent and the Grenadines
191|Samoa
192|San Marino
193|Sao Tome and Principe
194|Saudi Arabia
195|Senegal
196|Serbia
197|Seychelles
198|Sierra Leone
199|Singapore
200|Sint Maarten
201|Slovakia
202|Slovenia
203|Solomon Islands
204|Somalia
205|South Africa
206|South Georgia and S. Sandwich Islands
207|South Sudan
208|Spain
209|Sri Lanka
210|Sudan
211|Suriname
212|Svalbard and Jan Mayen
213|Sweden
214|Switzerland
215|Syria
216|Taiwan
217|Tajikistan
218|Tanzania
219|Thailand
220|Timor-Leste
221|Togo
222|Tokelau
223|Tonga
224|Trinidad and Tobago
225|Tunisia
226|Turkey
227|Turkmenistan
228|Turks and Caicos Islands
229|Tuvalu
230|Uganda
231|Ukraine
232|United Arab Emirates
233|United Kingdom
234|Uruguay
235|U.S.A.
236|U.S. Minor Outlying Islands
237|Uzbekistan
238|Vanuatu
239|Vatican
240|Venezuela
241|Vietnam
242|Virgin Islands (UK)
243|Virgin Islands of the USA
244|Wallis & Futuna
245|Western Sahara
246|Yemen
247|Zambia
248|Zimbabwe
"""


def build_postcrossing_numbers():
    numbers = {}

    for line in POSTCROSSING_DATA.strip().splitlines():
        number, name = line.split("|", 1)
        numbers[name.strip()] = int(number)

    return numbers


POSTCROSSING_NUMBERS = build_postcrossing_numbers()


# ============================================================
# CROATIAN/BOSNIAN PDF NAME -> ENGLISH NAME
#
# These are the names used in the Posta PDF, mapped to English.
# ============================================================

TRANSLATIONS = {
    "ALBANIJA": "Albania",
    "ALŽIR": "Algeria",
    "AMERIČKI DJEVIČANSKI OTOCI": "Virgin Islands of the USA",
    "AMERIČKA SAMOA": "American Samoa",
    "ANDORA": "Andorra",
    "ANGOLA": "Angola",
    "ANGVILA": "Anguilla",
    "ANTIGVA I BARBUDA": "Antigua & Barbuda",
    "ARGENTINA": "Argentina",
    "ARMENIJA": "Armenia",
    "ARUBA": "Aruba",
    "ASENŠN": "Saint Helena, Ascension and Tristan da Cunha",
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
    "BERMUDA": "Bermuda",
    "BJELOKOSNA OBALA": "Côte d'Ivoire",
    "BJELORUSIJA": "Belarus",
    "BOCVANA": "Botswana",
    "BOLIVIJA": "Bolivia",
    "BOŽIĆNI OTOK": "Christmas Island",
    "BRAZIL": "Brazil",
    "BRITANSKI DJEVIČANSKI OTOCI": "Virgin Islands (UK)",
    "BRUNEJ DARUSSALAM": "Brunei",
    "BUGARSKA": "Bulgaria",
    "BURKINA FASO": "Burkina Faso",
    "BURUNDI": "Burundi",
    "BUTAN": "Bhutan",
    "CIPAR": "Cyprus",
    "CRNA GORA": "Montenegro",
    "ČAD": "Chad",
    "ČEŠKA REPUBLIKA": "Czechia",
    "ČILE": "Chile",
    "DANSKA": "Denmark",
    "DEMOKRATSKA NARODNA REPUBLIKA KOREJA":
        "Korea(North)",
    "DEMOKRATSKA REPUBLIKA KONGO":
        "Dem. Rep. Of Congo",
    "DOMINIKA": "Dominica",
    "DOMINIKANSKA REPUBLIKA": "Dominican Republic",
    "DRŽAVA VATIKANSKOGA GRADA": "Vatican",
    "DŽIBUTI": "Djibouti",
    "EGIPAT": "Egypt",
    "EKVADOR": "Ecuador",
    "EKVATORSKA GVINEJA": "Equatorial Guinea",
    "ERITREJA": "Eritrea",
    "ESTONIJA": "Estonia",
    "ESVATINI": "Eswatini /Swaziland",
    "ETIOPIJA": "Ethiopia",
    "FAKLANDI (MALVINI)": "Falkland Islands /Malvinas",
    "FIDŽI": "Fiji",
    "FILIPINI": "Philippines",
    "FINSKA": "Finland",
    "FRANCUSKA": "France",
    "FRANCUSKA GVAJANA": "French Guiana",
    "FRANCUSKA POLINEZIJA": "French Polynesia",
    "GABON": "Gabon",
    "GAMBIJA": "Gambia",
    "GANA": "Ghana",
    "GERNZI": "Guernsey",
    "GIBRALTAR": "Gibraltar",
    "GRČKA": "Greece",
    "GRENADA": "Grenada",
    "GRENLAND": "Greenland",
    "GRUZIJA": "Georgia",
    "GUAM": "Guam",
    "GVADALUPA": "Guadeloupe",
    "GVAJANA": "Guyana",
    "GVATEMALA": "Guatemala",
    "GVINEJA": "Guinea",
    "GVINEJA - BISAU": "Guinea-Bissau",
    "GVINEJA – BISAU": "Guinea-Bissau",
    "HAITI": "Haiti",
    "HONDURAS": "Honduras",
    "HONG KONG": "Hong Kong",
    "HRVATSKA": "Croatia",
    "INDIJA": "India",
    "INDONEZIJA": "Indonesia",
    "IRAK": "Iraq",
    "IRAN": "Iran",
    "IRSKA": "Ireland",
    "ISLAND": "Iceland",
    "ITALIJA": "Italy",
    "JAMAJKA": "Jamaica",
    "JAPAN": "Japan",
    "JORDAN": "Jordan",
    "JUŽNA AFRIKA": "South Africa",
    "JUŽNA DŽORDŽIJA": "South Georgia and S. Sandwich Islands",
    "JUŽNI SENDVIČ OTOCI": "South Georgia and S. Sandwich Islands",
    "KABO VERDE": "Cabo Verde",
    "KAJMANSKI OTOCI": "Cayman Islands",
    "KAMBODŽA": "Cambodia",
    "KAMERUN": "Cameroon",
    "KANADA": "Canada",
    "KATAR": "Qatar",
    "KAZAHSTAN": "Kazakhstan",
    "KENIJA": "Kenya",
    "KINA": "China",
    "KIRGISTAN": "Kyrgyzstan",
    "KIRIBATI": "Kiribati",
    "KOKOSOVI OTOCI": "Cocos Islands",
    "KOLUMBIJA": "Colombia",
    "KOMORI": "Comoros",
    "KONGO": "Congo",
    "KOSOVO": "Kosovo",
    "KOSTARIKA": "Costa Rica",
    "KUBA": "Cuba",
    "KUKOVI OTOCI": "Cook Islands",
    "KUVAJT": "Kuwait",
    "LAOSKA NARODNA DEMOKRATSKA REPUBLIKA":
        "Laos",
    "LATVIJA": "Latvia",
    "LESOTO": "Lesotho",
    "LIBANON": "Lebanon",
    "LIBERIJA": "Liberia",
    "LIHTENŠTAJN": "Liechtenstein",
    "LITVA": "Lithuania",
    "LUKSEMBURG": "Luxembourg",
    "MADAGASKAR": "Madagascar",
    "MAĐARSKA": "Hungary",
    "MAJOT": "Mayotte",
    "MAKAO": "Macao",
    "MAKEDONIJA": "North Macedonia",
    "MALAVI": "Malawi",
    "MALDIVI": "Maldives",
    "MALEZIJA": "Malaysia",
    "MALI": "Mali",
    "MALTA": "Malta",
    "MARIJANSKI OTOCI": "Northern Mariana Islands",
    "MAROKO": "Morocco",
    "MARŠALOVI OTOCI": "Marshall Islands",
    "MARTINIK": "Martinique",
    "MAURICIJUS": "Mauritius",
    "MEKSIKO": "Mexico",
    "MIKRONEZIJA": "Micronesia",
    "MJANMAR": "Myanmar",
    "MOLDAVIJA": "Moldova",
    "MONAKO": "Monaco",
    "MONGOLIJA": "Mongolia",
    "MONTSERAT": "Montserrat",
    "MOZAMBIK": "Mozambique",
    "NAMIBIJA": "Namibia",
    "NAURU": "Nauru / Naoero",
    "NEPAL": "Nepal",
    "NIGER": "Niger",
    "NIGERIJA": "Nigeria",
    "NIKARAGVA": "Nicaragua",
    "NIUE": "Niue",
    "NIZOZEMSKA": "Netherlands",
    "NIZOZEMSKI ANTILI": "Netherlands",
    "NJEMAČKA": "Germany",
    "NORVEŠKA": "Norway",
    "NOVA KALEDONIJA": "New Caledonia",
    "NOVI ZELAND": "New Zealand",
    "OMAN": "Oman",
    "OTOK MAN": "Isle of Man",
    "OTOK NORFOLK": "Norfolk Island",
    "OVČJI OTOCI": "Faroe Islands",
    "PAKISTAN": "Pakistan",
    "PALAU": "Palau",
    "PANAMA": "Panama",
    "PAPUA NOVA GVINEJA": "Papua New Guinea",
    "PARAGVAJ": "Paraguay",
    "PERU": "Peru",
    "PITKERN": "Pitcairn",
    "POLJSKA": "Poland",
    "PORTORIKO": "Puerto Rico",
    "PORTUGAL": "Portugal",
    "REPUBLIKA KINA NA TAJVANU": "Taiwan",
    "REPUBLIKA KOREJA": "Korea(South)",
    "REUNION": "Réunion",
    "RUANDA": "Rwanda",
    "RUMUNJSKA": "Romania",
    "RUSIJA": "Russia",
    "SAD": "U.S.A.",
    "SALOMONOVI OTOCI": "Solomon Islands",
    "SALVADOR": "El Salvador",
    "SAMOA": "Samoa",
    "SAN MARINO": "San Marino",
    "SAUDIJSKA ARABIJA": "Saudi Arabia",
    "SEJŠELI": "Seychelles",
    "SENEGAL": "Senegal",
    "SIJERA LEONE": "Sierra Leone",
    "SINGAPUR": "Singapore",
    "SIRIJA": "Syria",
    "SLOVAČKA": "Slovakia",
    "SLOVENIJA": "Slovenia",
    "SRBIJA": "Serbia",
    "SREDNJOAFRIČKA REPUBLIKA": "Central African Republic",
    "SUDAN": "Sudan",
    "SURINAM": "Suriname",
    "SVETA HELENA": "Saint Helena, Ascension and Tristan da Cunha",
    "SVETA LUCIJA": "Saint Lucia",
    "SVETI KRISTOFOR I NEVIS": "Saint Kitts and Nevis",
    "SVETI PETAR I MIKELON": "Saint Pierre & Miquelon",
    "SVETI TOMA I PRINSIPE": "Sao Tome and Principe",
    "SVETI VINCENT I GRENADINI": "Saint Vincent and the Grenadines",
    "ŠPANJOLSKA": "Spain",
    "ŠRI LANKA": "Sri Lanka",
    "ŠVEDSKA": "Sweden",
    "ŠVICARSKA": "Switzerland",
    "TADŽIKISTAN": "Tajikistan",
    "TAJLAND": "Thailand",
    "TANZANIJA": "Tanzania",
    "TIMOR - LESTE": "Timor-Leste",
    "TOGO": "Togo",
    "TOKELAU": "Tokelau",
    "TONGA": "Tonga",
    "TRINIDAD I TO TOBAGO": "Trinidad and Tobago",
    "TRINIDAD I TOBAGO": "Trinidad and Tobago",
    "TRISTAN DA KUNA": "Saint Helena, Ascension and Tristan da Cunha",
    "TUNIS": "Tunisia",
    "TURKMENISTAN": "Turkmenistan",
    "TURKS I KEIKOS OTOCI": "Turks and Caicos Islands",
    "TURSKA": "Turkey",
    "TUVALU": "Tuvalu",
    "UGANDA": "Uganda",
    "UJEDINJENI ARAPSKI EMIRATI": "United Arab Emirates",
    "UJEDINJENA KRALJEVINA VELIKE BRITANIJE I SJEVERNE IRSKE":
        "United Kingdom",
    "UJEDINJENI ARAPSLI EMIRATI": "United Arab Emirates",
    "UKRAJINA": "Ukraine",
    "URUGVAJ": "Uruguay",
    "UZBEKISTAN": "Uzbekistan",
    "VALIS I FUTUNA": "Wallis & Futuna",
    "VANUATU": "Vanuatu",
    "VENEZUELA": "Venezuela",
    "VIJETNAM": "Vietnam",
    "ZAMBIJA": "Zambia",
    "ZIMBABVE": "Zimbabwe",
}


# ============================================================
# DOWNLOAD PDF
# ============================================================

def download_pdf():
    print("Downloading PDF...")

    request = urllib.request.Request(
        PDF_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "(compatible; mostarpost-monitor/1.0)"
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

    print(f"Downloaded {len(data):,} bytes.")


# ============================================================
# EXTRACT PDF TEXT
# ============================================================

def extract_pdf_text():
    print("Reading PDF...")

    document = fitz.open(PDF_FILE)

    try:
        pages = []

        for page in document:
            pages.append(page.get_text("text"))

        return "\n".join(pages)

    finally:
        document.close()


# ============================================================
# CLEAN PDF TEXT
# ============================================================

def clean_pdf_text(text):
    # Normalize different dash characters.
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Normalize non-breaking spaces.
    text = text.replace("\u00a0", " ")

    # --------------------------------------------------------
    # IMPORTANT:
    # Remove everything in parentheses.
    #
    # Examples:
    #
    # ARUBA (pismovne pošiljke I paketi)
    # becomes:
    #
    # ARUBA
    # --------------------------------------------------------

    text = re.sub(r"\([^)]*\)", "", text)

    # --------------------------------------------------------
    # Repair PDF extraction artifacts.
    #
    # These are present in the supplied PDF.
    # --------------------------------------------------------

    text = re.sub(
        r"GVINEJA\s*-\s*BISAUHAITI",
        "GVINEJA - BISAU\nHAITI",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"OVČJI\s+OTOCI\s*PAKISTAN",
        "OVČJI OTOCI\nPAKISTAN",
        text,
        flags=re.IGNORECASE,
    )

    return text


# ============================================================
# EXTRACT DESTINATION NAMES
# ============================================================

def extract_candidates(text):
    text = clean_pdf_text(text)

    lines = []

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        # Ignore heading.
        if line.startswith("POPIS DRŽAVA"):
            continue

        # Ignore footer.
        if line.startswith("Posljednje izmjene"):
            continue

        # Normalize spaces.
        line = re.sub(r"\s+", " ", line).strip()

        lines.append(line)

    # --------------------------------------------------------
    # Join PDF line breaks that are actually part of one name.
    # --------------------------------------------------------

    joined = []
    i = 0

    while i < len(lines):
        current = lines[i]

        # DEMOKRATSKA NARODNA
        # REPUBLIKA KOREJA
        if (
            current == "DEMOKRATSKA NARODNA"
            and i + 1 < len(lines)
            and lines[i + 1] == "REPUBLIKA KOREJA"
        ):
            joined.append(
                "DEMOKRATSKA NARODNA REPUBLIKA KOREJA"
            )
            i += 2
            continue

        # LAOSKA NARODNA DEMOKRATSKA
        # REPUBLIKA
        if (
            current == "LAOSKA NARODNA DEMOKRATSKA"
            and i + 1 < len(lines)
            and lines[i + 1] == "REPUBLIKA"
        ):
            joined.append(
                "LAOSKA NARODNA DEMOKRATSKA REPUBLIKA"
            )
            i += 2
            continue

        # UJEDINJENA KRALJEVINA VELIKE
        # BRITANIJE I SJEVERNE IRSKE
        if (
            current == "UJEDINJENA KRALJEVINA VELIKE"
            and i + 1 < len(lines)
            and lines[i + 1]
            == "BRITANIJE I SJEVERNE IRSKE"
        ):
            joined.append(
                "UJEDINJENA KRALJEVINA VELIKE "
                "BRITANIJE I SJEVERNE IRSKE"
            )
            i += 2
            continue

        joined.append(current)
        i += 1

    return joined


# ============================================================
# NORMALIZE DESTINATION NAME
# ============================================================

def normalize_name(name):
    name = name.strip()

    name = name.replace("–", "-")
    name = name.replace("—", "-")

    name = re.sub(r"\s+", " ", name)

    name = name.strip(" -")

    # Known PDF typo.
    if name == "UJEDINJENI ARAPSLI EMIRATI":
        return "UJEDINJENI ARAPSKI EMIRATI"

    return name


# ============================================================
# TRANSLATE
# ============================================================

def translate(name):
    return TRANSLATIONS.get(name)


# ============================================================
# FIND POSTCROSSING NUMBER
# ============================================================

def get_postcrossing_number(english_name):
    if not english_name:
        return None

    # Direct match.
    if english_name in POSTCROSSING_NUMBERS:
        return POSTCROSSING_NUMBERS[english_name]

    # --------------------------------------------------------
    # A few intentional alternate spellings.
    # --------------------------------------------------------

    aliases = {
        "United States": "U.S.A.",
        "Côte d’Ivoire": "Côte d'Ivoire",
        "Guinea-Bissau": "Guinea-Bissau",
        "North Macedonia": "North Macedonia",
        "South Korea": "Korea(South)",
        "North Korea": "Korea(North)",
        "United Kingdom": "United Kingdom",
        "British Virgin Islands": "Virgin Islands (UK)",
        "U.S. Virgin Islands": "Virgin Islands of the USA",
    }

    alias = aliases.get(english_name)

    if alias:
        return POSTCROSSING_NUMBERS.get(alias)

    return None


# ============================================================
# BUILD OUTPUT
# ============================================================

def build_output():
    raw_text = extract_pdf_text()

    candidates = extract_candidates(raw_text)

    results = []
    seen = set()

    print("Processing destinations...")

    for candidate in candidates:
        name = normalize_name(candidate)

        if not name:
            continue

        english = translate(name)

        # ----------------------------------------------------
        # If a new destination is added to the PDF and we have
        # not yet added its translation, keep it rather than
        # silently losing it.
        # ----------------------------------------------------

        if english is None:
            print(
                f"WARNING: No translation found for: {name}",
                file=sys.stderr,
            )

            english = name.title()

        number = get_postcrossing_number(english)

        # ----------------------------------------------------
        # Deduplicate.
        #
        # This is important because the PDF can list the same
        # destination more than once for different services.
        # ----------------------------------------------------

        unique_key = english.casefold()

        if unique_key in seen:
            continue

        seen.add(unique_key)

        results.append(
            {
                "original": name,
                "english": english,
                "number": number,
            }
        )

    # --------------------------------------------------------
    # Create final text.
    #
    # Numbered:
    #
    # 3. ALBANIJA — Albania
    #
    # Unnumbered:
    #
    # Some Destination — English Name
    # --------------------------------------------------------

    output_lines = []

    for item in results:
        if item["number"] is not None:
            line = (
                f"{item['number']}. "
                f"{item['original']} — "
                f"{item['english']}"
            )
        else:
            line = (
                f"{item['original']} — "
                f"{item['english']}"
            )

        output_lines.append(line)

    return output_lines


# ============================================================
# WRITE OUTPUT FILE
# ============================================================

def write_output(lines):
    output = "\n".join(lines) + "\n"

    OUTPUT_FILE.write_text(
        output,
        encoding="utf-8",
    )

    print(
        f"Wrote {len(lines)} destinations "
        f"to {OUTPUT_FILE}."
    )


# ============================================================
# MAIN
# ============================================================

def main():
    try:
        download_pdf()

        lines = build_output()

        write_output(lines)

        # Do not leave the downloaded PDF in the repository.
        try:
            PDF_FILE.unlink()
        except FileNotFoundError:
            pass

        print("Done.")

    except Exception as exc:
        print(
            f"ERROR: {exc}",
            file=sys.stderr,
        )

        try:
            PDF_FILE.unlink()
        except FileNotFoundError:
            pass

        sys.exit(1)


if __name__ == "__main__":
    main()
