import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pydeck as pdk
import plotly.express as px
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re

# -----------------------------
# 1. COORDENADAS DE DISTRITOS
# -----------------------------
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

# --- 2. FUENTES ---
FUENTES = {
    "RPP": "https://rpp.pe/tema/inseguridad-ciudadana",
    "El Comercio": "https://elcomercio.pe/lima/policiales/",
    "La República": "https://larepublica.pe/sociedad/",
    "Canal N": "https://canaln.pe/noticias/policiales",
    "Diario Correo": "https://diariocorreo.pe/peru/",
    "Perú 21": "https://peru21.pe/lima/",
    "Infobae": "https://www.infobae.com/peru/"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

PALABRAS_CLAVE = ["robo", "asalto", "delincuencia", "policia", "policía", "crimen", "sicario",
                  "balacera", "muerte", "asesinato", "extorsion", "extorsión", "homicidio", "atraco", "arma", "droga"]

DISTRITOS_INTEGRADOS = [d.lower() for d in COORDENADAS_LIMA.keys()]


def buscar_palabra_exacta(texto, lista_palabras):
    texto = texto.lower()
    for palabra in lista_palabras:
        patron = r'\b' + re.escape(palabra) + r'\b'
        if re.search(patron, texto):
            return palabra.upper()
    return None


@st.cache_data(ttl=300, show_spinner="Escaneando las 7 fuentes de noticias... (Esto puede tardar unos segundos)")
def escanear_inteligente():
    noticias_encontradas = []

    for nombre_fuente, url_base in FUENTES.items():
        try:
            response = requests.get(url_base, headers=HEADERS, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                elementos = soup.find_all(['h2', 'h3', 'article'])

                for item in elementos:
                    enlace = item.find('a')
                    if not enlace:
                        enlace = item if item.name == 'a' else None

                    if enlace:
                        titulo_texto = enlace.text.strip()
                        path = enlace.get('href')

                        if not path or len(titulo_texto) < 10:
                            continue

                        if path.startswith("http"):
                            url_noticia = path
                        elif nombre_fuente == "RPP":
                            url_noticia = "https://rpp.pe" + path
                        elif nombre_fuente == "El Comercio":
                            url_noticia = "https://elcomercio.pe" + path
                        elif nombre_fuente == "La República":
                            url_noticia = "https://larepublica.pe" + path
                        elif nombre_fuente == "Canal N":
                            url_noticia = "https://canaln.pe" + path
                        elif nombre_fuente == "Diario Correo":
                            url_noticia = "https://diariocorreo.pe" + path
                        elif nombre_fuente == "Perú 21":
                            url_noticia = "https://peru21.pe" + path
                        elif nombre_fuente == "Infobae":
                            url_noticia = "https://www.infobae.com" + path
                        else:
                            url_noticia = path

                        distrito = buscar_palabra_exacta(
                            titulo_texto, DISTRITOS_INTEGRADOS)
                        delito = buscar_palabra_exacta(
                            titulo_texto, PALABRAS_CLAVE)

                        if distrito or delito:
                            ubicacion = distrito if distrito else "⚠️ No Especificado"
                            # AQUI GUARDAMOS EL TIPO DE DELITO DETECTADO
                            categoria = delito if delito else "General/Otro"

                            if not any(n['Enlace'] == url_noticia for n in noticias_encontradas):
                                noticias_encontradas.append({
                                    "Titular": f"[{nombre_fuente}] {titulo_texto}",
                                    "Distrito": ubicacion,
                                    "Enlace": url_noticia,
                                    "Fuente": nombre_fuente,
                                    "Categoría": categoria  # Nueva columna para gráficos
                                })
        except Exception:
            continue

    return pd.DataFrame(noticias_encontradas)


st.set_page_config(page_title="Lima Segura: Monitor",
                   page_icon="🚨", layout="wide")

if 'historial_noticias' not in st.session_state:
    st.session_state['historial_noticias'] = pd.DataFrame()

# -----------------------------
# ESTILOS CSS
# -----------------------------
st.markdown("""
    <style>
    .kpi-card {
        background-color: #FFFFFF;
        border-left: 5px solid #D32F2F;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .kpi-card h3 { color: #D32F2F; font-size: 1.2em; margin-bottom: 10px; }
    .main-title { font-family: 'Arial Black', sans-serif; color: #1a1a1a; text-align: center; font-size: 3em; margin-bottom: 0; }
    .subtitle { text-align: center; color: #555; font-size: 1.2em; margin-top: -10px; margin-bottom: 40px; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# MENÚ
# -----------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1083/1083584.png", width=50)
    st.markdown("## 🚨 Lima Segura")
    menu = option_menu(
        menu_title="Navegación",
        options=["Inicio", "Mapa del Crimen",
                 "Análisis por Periódico", "Emergencias", "Equipo"],
        icons=["house", "geo-alt", "newspaper", "phone", "people"],
        menu_icon="list",
        default_index=0,
        styles={"nav-link-selected": {"background-color": "#D32F2F"}}
    )

# -----------------------------
# SECCIÓN: INICIO
# -----------------------------
if menu == "Inicio":
    st.markdown('<h1 class="main-title">SISTEMA DE ALERTA DE DELITOS</h1>',
                unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Monitor de Criminalidad basado en Web Scraping</p>',
                unsafe_allow_html=True)

    col_img1, col_img2 = st.columns(2)
    try:
        with col_img1:
            st.image("imagenes/cambio_habitos.jpg", use_container_width=True)
    except:
        pass
    try:
        with col_img2:
            st.image("imagenes/tukituki.png", use_container_width=True)
    except:
        pass

    st.markdown("---")

    col_scan_center = st.columns([1, 2, 1])
    with col_scan_center[1]:
        if st.button("🔄 INICIAR ESCANEO DE NOTICIAS (7 FUENTES)", type="primary", use_container_width=True):
            st.cache_data.clear()
            st.session_state['historial_noticias'] = escanear_inteligente()
            st.rerun()

    df_kpi = st.session_state['historial_noticias']
    noticias_count = len(df_kpi)

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(
            f"""<div class="kpi-card"><h3>🗞️ {noticias_count}</h3><p>Noticias Recolectadas</p></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(
            f"""<div class="kpi-card"><h3>📡 7 Fuentes</h3><p>RPP, Comercio, República, etc.</p></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(
            f"""<div class="kpi-card"><h3>📍 Lima</h3><p>Geolocalización Activa</p></div>""", unsafe_allow_html=True)

# -----------------------------
# SECCIÓN: MAPA
# -----------------------------
elif menu == "Mapa del Crimen":
    st.title("📍 Mapa de Calor en Tiempo Real")

    df_base = st.session_state['historial_noticias']

    if df_base.empty:
        st.warning("⚠️ No hay datos. Ve a 'Inicio' y escanea noticias.")
    else:
        col_control, col_map = st.columns([1, 4])

        with col_control:
            st.subheader("Filtros")
            distrito_sel = st.selectbox(
                "Distrito:", ["Todos"] + list(COORDENADAS_LIMA.keys()))
            # Filtro por Categoría de Delito (NUEVO)
            delitos_disponibles = ["Todos"] + \
                list(df_base['Categoría'].unique())
            delito_sel = st.selectbox("Tipo de Delito:", delitos_disponibles)

        with col_map:
            df_filtrado = df_base.copy()
            if distrito_sel != "Todos":
                df_filtrado = df_filtrado[df_filtrado['Distrito']
                                          == distrito_sel]
            if delito_sel != "Todos":
                df_filtrado = df_filtrado[df_filtrado['Categoría']
                                          == delito_sel]

            df_filtrado['coords'] = df_filtrado['Distrito'].apply(
                lambda x: COORDENADAS_LIMA.get(x.upper(), [None, None]))
            df_final = df_filtrado.dropna(subset=['coords'])

            if not df_final.empty:
                df_final['lat'] = df_final['coords'].apply(lambda x: x[0])
                df_final['lon'] = df_final['coords'].apply(lambda x: x[1])

                lat_c, lon_c = (-12.0464, -
                                77.0428) if distrito_sel == "Todos" else COORDENADAS_LIMA[distrito_sel]
                zoom_c = 10 if distrito_sel == "Todos" else 13

                st.pydeck_chart(pdk.Deck(
                    map_style='https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
                    initial_view_state=pdk.ViewState(
                        latitude=lat_c, longitude=lon_c, zoom=zoom_c, pitch=45),
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            df_final,
                            get_position='[lon, lat]',
                            get_color='[200, 30, 0, 160]',
                            get_radius=200,
                            pickable=True,
                        ),
                    ],
                    tooltip={"text": "{Titular}\n({Categoría})"}
                ))
            else:
                st.info("No se encontraron noticias con esa ubicación o categoría.")

# -----------------------------
# SECCIÓN: ANÁLISIS
# -----------------------------
elif menu == "Análisis por Periódico":
    st.title("📊 Análisis Detallado de Criminalidad")

    df_analisis = st.session_state['historial_noticias']

    if df_analisis.empty:
        st.warning("⚠️ Primero debes escanear las noticias. Ve a Inicio.")
    else:
        # FILTROS DE ANÁLISIS
        st.write("### 🔍 Filtros")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            fuentes_sel = st.multiselect("Filtrar por Medio:", df_analisis['Fuente'].unique(
            ), default=df_analisis['Fuente'].unique())
        with col_f2:
            tipos_sel = st.multiselect("Filtrar por Tipo de Delito:", df_analisis['Categoría'].unique(
            ), default=df_analisis['Categoría'].unique())

        # Aplicar filtros
        df_viz = df_analisis[df_analisis['Fuente'].isin(
            fuentes_sel) & df_analisis['Categoría'].isin(tipos_sel)]

        st.write("---")

        # FILA DE GRÁFICOS
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("📰 Noticias por Medio")
            conteo = df_viz['Fuente'].value_counts().reset_index()
            conteo.columns = ['Fuente', 'Cantidad']
            fig1 = px.bar(conteo, x='Fuente', y='Cantidad',
                          color='Fuente', text='Cantidad')
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            st.subheader("🔫 Distribución por Tipo de Delito")
            # Gráfico de Pastel (Pie Chart)
            conteo_tipo = df_viz['Categoría'].value_counts().reset_index()
            conteo_tipo.columns = ['Categoría', 'Cantidad']
            fig2 = px.pie(conteo_tipo, names='Categoría',
                          values='Cantidad', hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)

        st.write("---")
        st.subheader("📋 Detalle de Noticias Filtradas")
        st.dataframe(
            df_viz[['Titular', 'Fuente', 'Categoría', 'Distrito']],
            hide_index=True,
            use_container_width=True
        )
# -----------------------------
# EQUIPO
# -----------------------------
elif menu == "Equipo":
    st.markdown("""
    <style>
        .team-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 40px;
            margin-top: 50px;
        }
        .member-card {
            background-color: #f8f9fa;
            border-top: 5px solid #D32F2F; /* Rojo Alerta */
            border-radius: 15px;
            padding: 30px;
            width: 250px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .member-card:hover {
            transform: translateY(-10px);
        }
        .member-name {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-top: 15px;
        }
        .member-role {
            color: #666;
            font-size: 0.85em;
            margin-bottom: 15px;
        }
        .avatar {
            font-size: 50px;
        }
        .github-btn {
            text-decoration: none; 
            color: #D32F2F; 
            font-weight: bold;
            border: 1px solid #D32F2F;
            padding: 5px 15px;
            border-radius: 20px;
            transition: all 0.3s ease;
        }
        .github-btn:hover {
            background-color: #D32F2F;
            color: white;
        }
    </style>
    <h2 style="text-align:center;">👥 El Equipo</h2>
    <p style="text-align:center;">Estudiantes de Ingeniería Estadística e Informática - UNALM</p>
    <div class="team-container">
    <div class="member-card">
    <div class="avatar">👨‍💻</div>
    <div class="member-name">Daniel Ormeño Sakihama</div>
    <div class="member-role">Ingeniería Estadística Informática</div>
    <a href="https://github.com/Orsaki" target="_blank" class="github-btn">GitHub Profile</a>
    </div>
    <div class="member-card">
    <div class="avatar">👨‍💻</div>
    <div class="member-name">Luis Huamayalli</div>
    <div class="member-role">Ingeniería Estadística Informática</div>
    <a href="https://github.com/Albert-ca" target="_blank" class="github-btn">GitHub Profile</a>
    </div>
    <div class="member-card">
    <div class="avatar">👩‍💻</div>
    <div class="member-name">Pamela Lázaro</div>
    <div class="member-role">Ingeniería Estadística Informática</div>
    <a href="https://github.com/lazaropamela" target="_blank" class="github-btn">GitHub Profile</a>
    </div>
    <div class="member-card">
    <div class="avatar">👩‍💻</div>
    <div class="member-name">Fátima Montes</div>
    <div class="member-role">Ingeniería Estadística Informática</div>
    <a href="https://github.com/FatimaMY" target="_blank" class="github-btn">GitHub Profile</a>
    </div>
    </div>
    """, unsafe_allow_html=True)
    # --- AGREGA ESTE BLOQUE AL FINAL (Commit 14) ---

# --- BUSCA ESTA LÍNEA Y ASEGÚRATE QUE TENGA LA "S" AL FINAL ---
elif menu == "Emergencias":
    st.title("📞 Centrales de Emergencia y Ayuda")
    st.markdown(
        "Contactos directos para asistencia inmediata en Lima Metropolitana y Callao.")
    st.write("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("### 👮 PNP")
        st.subheader("105")
        st.write("Policía Nacional del Perú.")
    with col2:
        st.warning("### 🚒 Bomberos")
        st.subheader("116")
        st.write("Incendios y rescates.")
    with col3:
        st.info("### 🚑 SAMU")
        st.subheader("106")
        st.write("Urgencias médicas.")

    st.write("---")
    with st.expander("📌 Otros números importantes"):
        st.write("* **Serenazgo de Lima:** (01) 318-5050")
