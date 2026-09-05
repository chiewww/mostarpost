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


# ----------------------------------------------------------------------
# POSTCROSSING COUNTRY NUMBERS
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
# CROATIAN/BOSNIAN PDF NAME -> ENGLISH NAME
# ----------------------------------------------------------------------

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
    "BERMUDI": "Bermuda",
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
    "DEMOKRATSKA NARODNA REPUBLIKA KOREJA": "Korea(North)",
    "DEMOKRATSKA REPUBLIKA KONGO": "Dem. Rep. Of Congo",
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
    "FAKLANDI": "Falkland Islands /Malvinas",
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
    "GVINEJA-BISAU": "Guinea-Bissau",
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
    "LAOSKA NARODNA DEMOKRATSKA REPUBLIKA": "Laos",
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
    "NIZOZEMSKI ANTILI": "Curaçao",
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
    "UJEDINJENI ARAPSLI EMIRATI": "United Arab Emirates",
    "UJEDINJENA KRALJEVINA VELIKE BRITANIJE I SJEVERNE IRSKE": "United Kingdom",
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


# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------

def normalize_text(text):
    text = text.replace("\u00a0", " ")
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("−", "-")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def remove_parenthetical_text(text):
    """
    Remove parenthetical service information.

    Example:
        AUSTRALIJA (pismovne pošiljke)
    becomes:
        AUSTRALIJA

    IMPORTANT:
    This does NOT remove duplicate entries.
    If AUSTRALIJA occurs twice, both occurrences remain.
    """
    return re.sub(r"\([^)]*\)", "", text)


# ----------------------------------------------------------------------
# PDF EXTRACTION
# ----------------------------------------------------------------------

def extract_pdf_entries():
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

    for page_number, page in enumerate(document, start=1):
        page_text = page.get_text("text")

        for line in page_text.splitlines():
            line = normalize_text(line)

            if line:
                raw_lines.append(line)

    document.close()

    # --------------------------------------------------------------
    # Remove only the title and final date.
    #
    # DO NOT remove duplicate country names.
    # DO NOT use a set().
    # DO NOT use a "seen" dictionary.
    # --------------------------------------------------------------

    entries = []

    for line in raw_lines:
        upper = line.upper()

        if "POPIS DRŽAVA U KOJE JE MOGUĆE SLATI POŠILJKE" in upper:
            continue

        if upper.startswith("POSLJEDNJE IZMJENE"):
            continue

        # Remove parenthetical service information.
        line = remove_parenthetical_text(line)
        line = normalize_text(line)

        if not line:
            continue

        entries.append(line)

    # --------------------------------------------------------------
    # Repair PDF page-break extraction problems.
    # --------------------------------------------------------------

    repaired = []

    i = 0

    while i < len(entries):
        current = entries[i]
        upper = current.upper()

        # GVINEJA – BISAU
        # HAITI
        #
        # Sometimes PDF extraction joins these around a page break.
        if (
            "GVINEJA" in upper
            and "BISAU" in upper
            and "HAITI" in upper
        ):
            repaired.append("GVINEJA")
            repaired.append("GVINEJA-BISAU")
            repaired.append("HAITI")
            i += 1
            continue

        # OVČJI OTOCI
        # PAKISTAN
        #
        # Sometimes extracted as OVČJI OTOCIPAKISTAN.
        if (
            "OVČJI OTOCI" in upper
            and "PAKISTAN" in upper
            and upper != "OVČJI OTOCI"
        ):
            repaired.append("OVČJI OTOCI")
            repaired.append("PAKISTAN")
            i += 1
            continue

        repaired.append(current)
        i += 1

    entries = repaired

    # --------------------------------------------------------------
    # Join known multi-line country names.
    # --------------------------------------------------------------

    joined = []

    i = 0

    while i < len(entries):
        current = entries[i]
        upper = current.upper()

        # DEMOKRATSKA NARODNA
        # REPUBLIKA KOREJA
        if (
            upper == "DEMOKRATSKA NARODNA"
            and i + 1 < len(entries)
            and entries[i + 1].upper() == "REPUBLIKA KOREJA"
        ):
            joined.append("DEMOKRATSKA NARODNA REPUBLIKA KOREJA")
            i += 2
            continue

        # LAOSKA NARODNA DEMOKRATSKA
        # REPUBLIKA
        if (
            upper == "LAOSKA NARODNA DEMOKRATSKA"
            and i + 1 < len(entries)
            and entries[i + 1].upper() == "REPUBLIKA"
        ):
            joined.append(
                "LAOSKA NARODNA DEMOKRATSKA REPUBLIKA"
            )
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
                "UJEDINJENA KRALJEVINA VELIKE "
                "BRITANIJE I SJEVERNE IRSKE"
            )
            i += 2
            continue

        joined.append(current)
        i += 1

    entries = joined

    return entries


# ----------------------------------------------------------------------
# TRANSLATION
# ----------------------------------------------------------------------

def get_translation(croatian_name):
    name = normalize_text(croatian_name).upper()

    if name in TRANSLATIONS:
        return TRANSLATIONS[name]

    print(f"WARNING: No translation found for: {croatian_name}")

    # Do not silently discard an unknown PDF entry.
    return croatian_name.title()


# ----------------------------------------------------------------------
# POSTCROSSING NUMBER
# ----------------------------------------------------------------------

def get_postcrossing_number(english_name):
    aliases = {
        "Côte d’Ivoire": "Côte d'Ivoire",
        "British Virgin Islands": "Virgin Islands (UK)",
        "U.S. Virgin Islands": "Virgin Islands of the USA",
        "North Korea": "Korea(North)",
        "South Korea": "Korea(South)",
        "North Macedonia": "North Macedonia",
        "United States": "U.S.A.",
    }

    lookup_name = aliases.get(
        english_name,
        english_name,
    )

    return POSTCROSSING_NUMBERS.get(lookup_name)


# ----------------------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------------------

def create_output(entries):
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


# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------

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

        # This should ALWAYS be true.
        # There is intentionally NO deduplication.
        if len(output_lines) != len(entries):
            raise RuntimeError(
                "ERROR: Output entry count does not match "
                "PDF entry count."
            )

        print(
            f"SUCCESS: {len(output_lines)} PDF entries produced "
            f"{len(output_lines)} output lines."
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
