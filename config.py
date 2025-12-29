# config.py

# 1. IDENTIDAD DEL ROBOT (HEADERS)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 2. DICCIONARIO DE PALABRAS CLAVE (VOCABULARIO AMPLIADO)
PALABRAS_CLAVE = [
    # --- A. DELITOS CONTRA LA VIDA (Verbos y Sustantivos) ---
    "asesinato", "asesinan", "asesino", "homicidio", "muerte", "muere", "fallece",
    "matan", "matar", "crimen", "sicario", "sicariato", "feminicidio",
    "acribillado", "acribillan", "baleado", "balean", "disparos", "disparan", "balacera",
    "cadáver", "cuerpo", "hallan cuerpo", "degollado", "descuartizado", "quemado",
    "envenenado", "estrangulado", "ajuste de cuentas", "tiroteo",

    # --- B. ROBOS Y ASALTOS (Modalidades) ---
    "robo", "roban", "asaltan", "asalto", "delincuencia", "delincuente", "ladrón", "ladrones",
    "atraco", "arrebatador", "arrebatan", "raquetero", "raqueteros", "bujiazo",
    "marca", "marcas", "sacapintas", "cogotero", "tendero", "patrones", 
    "celular", "mochila", "cartera", "billetera", "autopartes", "desmantelan",

    # --- C. CRIMEN ORGANIZADO Y EXTORSIÓN ---
    "extorsion", "extorsión", "extorsionadores", "cupos", "cobro de cupos",
    "vacunas", "gota a gota", "gotagota", "prestamistas", 
    "banda criminal", "organización criminal", "clan", "cártel", "mafia",
    "tren de aragua", "los pulpos", "malditos", "hijos de dios",

    # --- D. VIOLENCIA Y AMENAZAS ---
    "secuestro", "secuestran", "tentativa", "amenaza", "amedrentan", "golpean", "golpiza",
    "agresión", "violencia", "abuso", "tocamientos", "violación", "ultrajan",
    "pepean", "pepeado", "pildoritas", "droga", "tráfico ilícito", "microcomercialización",

    # --- E. POLICIALES Y JUSTICIA (Acciones de la autoridad) ---
    "policia", "policía", "pnp", "comisaria", "comisaría", "serenazgo", "serenos",
    "captura", "capturan", "detenido", "detienen", "cae", "caen", "intervención", 
    "intervienen", "operativo", "allanamiento", "desarticulan",
    "incautan", "decomisan", "fiscalía", "fiscal", "prisión", "cárcel", "marrocas",
    "terna", "escuadrón verde", "suat", "dirincri", "diviac",

    # --- F. ARMAS Y PELIGRO ---
    "armas", "arma de fuego", "pistola", "revólver", "fusil", "cuchillo", "navaja", "arma blanca",
    "granada", "explosivo", "detonación", "dinamita", "artefacto explosivo",
    "incendio", "siniestro", "fuego", "bomberos", "rescate", "emergencia"
]

# 3. GEOLOCALIZACIÓN (COORDENADAS DE DISTRITOS)
COORDENADAS_LIMA = {
    "ANCON": [-11.7731, -77.1758], "ATE": [-12.0253, -76.9204], "BARRANCO": [-12.1481, -77.0211],
    "BREÑA": [-12.0601, -77.0450], "CARABAYLLO": [-11.8481, -77.0286], "CHACLACAYO": [-11.9723, -76.7694],
    "CHORRILLOS": [-12.1750, -77.0175], "CIENEGUILLA": [-12.0911, -76.7725], "COMAS": [-11.9333, -77.0433],
    "EL AGUSTINO": [-12.0461, -77.0031], "INDEPENDENCIA": [-11.9925, -77.0494], "JESUS MARIA": [-12.0753, -77.0450],
    "LA MOLINA": [-12.0725, -76.9419], "LA VICTORIA": [-12.0651, -77.0309], "LINCE": [-12.0847, -77.0347],
    "LOS OLIVOS": [-11.9922, -77.0709], "LURIGANCHO": [-11.9442, -76.8406], "CHOSICA": [-11.9442, -76.8406],
    "LURIN": [-12.2742, -76.8669], "MAGDALENA": [-12.0914, -77.0694], "MIRAFLORES": [-12.1211, -77.0297],
    "PUEBLO LIBRE": [-12.0736, -77.0625], "PUENTE PIEDRA": [-11.8661, -77.0764], "RIMAC": [-12.0294, -77.0286],
    "SAN BORJA": [-12.1064, -76.9933], "SAN ISIDRO": [-12.0950, -77.0347], "SAN JUAN DE LURIGANCHO": [-11.9764, -77.0002],
    "SJL": [-11.9764, -77.0002], "SAN JUAN DE MIRAFLORES": [-12.1497, -76.9669], "SJM": [-12.1497, -76.9669],
    "SAN LUIS": [-12.0750, -76.9958], "SAN MARTIN DE PORRES": [-12.0053, -77.0583], "SMP": [-12.0053, -77.0583],
    "SAN MIGUEL": [-12.0775, -77.0917], "SANTA ANITA": [-12.0439, -76.9686], "SURCO": [-12.1456, -76.9789],
    "SANTIAGO DE SURCO": [-12.1456, -76.9789], "SURQUILLO": [-12.1133, -77.0225], "VILLA EL SALVADOR": [-12.2133, -76.9367],
    "VES": [-12.2133, -76.9367], "VILLA MARIA DEL TRIUNFO": [-12.1603, -76.9294], "VMT": [-12.1603, -76.9294],
    "CERCADO DE LIMA": [-12.0464, -77.0428], "LIMA": [-12.0464, -77.0428], "CALLAO": [-12.0566, -77.1181],
    "VENTANILLA": [-11.8753, -77.1256], "LA PERLA": [-12.0675, -77.1025]
}

# 4. LISTA DE DISTRITOS PARA BÚSQUEDA
DISTRITOS_INTEGRADOS = [d.lower() for d in COORDENADAS_LIMA.keys()]