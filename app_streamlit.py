import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pydeck as pdk
import plotly.express as px
import os
import numpy as np

# -----------------------------
# 1. BASE DE DATOS DE COORDENADAS
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

# -----------------------------
# 2. CONFIGURACIÓN E IMPORTACIÓN DE DATOS
# -----------------------------
st.set_page_config(
    page_title="Lima Segura: Monitor de Criminalidad",
    page_icon="🚨",
    layout="wide"
)

# Función para cargar y procesar datos desde TU CSV


@st.cache_data
def cargar_datos():
    archivo = "dataset_unificado.csv"
    if not os.path.exists(archivo):
        return None

    try:
        df = pd.read_csv(archivo)

        # --- PROCESAMIENTO DE COORDENADAS ---
        # Función interna para buscar distrito en el título
        def detectar_distrito_y_coords(titulo):
            titulo_upper = titulo.upper()
            for distrito, coords in COORDENADAS_LIMA.items():
                # Buscamos el nombre del distrito como palabra completa
                if f" {distrito} " in f" {titulo_upper} " or titulo_upper.startswith(distrito + " ") or titulo_upper.endswith(" " + distrito):
                    # Añadimos un pequeño "ruido" aleatorio para que los puntos no caigan uno encima de otro exacto
                    lat_noise = coords[0] + np.random.uniform(-0.002, 0.002)
                    lon_noise = coords[1] + np.random.uniform(-0.002, 0.002)
                    return distrito, lat_noise, lon_noise
            return "No Identificado", None, None

        # Aplicamos la detección
        df[['Distrito_Detectado', 'lat', 'lon']] = df['Titulo'].apply(
            lambda x: pd.Series(detectar_distrito_y_coords(x))
        )

        return df
    except Exception as e:
        st.error(f"Error procesando datos: {e}")
        return None


# Cargamos el dataframe global
df_global = cargar_datos()

# -----------------------------
# 3. ESTILOS CSS (DE TU COMPAÑERO)
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
    .kpi-card p { color: #333; font-size: 0.95em; }
    .main-title { font-family: 'Arial Black', sans-serif; color: #1a1a1a; text-align: center; font-size: 3em; margin-bottom: 0; }
    .subtitle { text-align: center; color: #555; font-size: 1.2em; margin-top: -10px; margin-bottom: 40px; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# 4. MENÚ LATERAL
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
    st.markdown('<p class="subtitle">Monitor de Criminalidad basado en Web Scraping y Geolocalización</p>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📢 La Realidad Actual")
        st.write("La inseguridad ciudadana en Lima Metropolitana es un problema crítico. Este proyecto centraliza noticias de múltiples fuentes para identificar puntos calientes.")
    with col2:
        st.markdown("### 🤖 Tecnología")
        st.info("Utilizamos Python para extraer noticias, NLP para detectar lugares y Streamlit para visualizar mapas de calor.")

    # KPIs Dinámicos
    st.markdown("---")
    k1, k2, k3 = st.columns(3)

    cantidad_noticias = len(df_global) if df_global is not None else 0
    fuente_top = df_global['Fuente'].mode(
    )[0] if df_global is not None and not df_global.empty else "N/A"

    with k1:
        st.markdown(
            f"""<div class="kpi-card"><h3>🗞️ {cantidad_noticias}</h3><p>Noticias Procesadas</p></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(
            f"""<div class="kpi-card"><h3>🏆 {fuente_top}</h3><p>Fuente Principal</p></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(
            """<div class="kpi-card"><h3>📍 Lima</h3><p>Cobertura Geográfica</p></div>""", unsafe_allow_html=True)

# -----------------------------
# SECCIÓN: MAPA DEL CRIMEN
# -----------------------------
elif menu == "Mapa del Crimen":
    st.title("📍 Mapa de Calor de Incidentes")

    if df_global is None:
        st.error("⚠️ Ejecuta main.py primero para generar los datos.")
    else:
        # Filtramos solo las que tienen coordenadas válidas
        df_mapa = df_global.dropna(subset=['lat', 'lon'])

        col_filtro, col_mapa = st.columns([1, 3])

        with col_filtro:
            st.subheader("Filtros")
            fuentes = st.multiselect(
                "Fuente:", df_mapa['Fuente'].unique(), default=df_mapa['Fuente'].unique())
            df_view = df_mapa[df_mapa['Fuente'].isin(fuentes)]

            st.metric("Incidentes localizados", len(df_view))

            # Mostrar lista de distritos afectados
            st.write("Distritos con más casos:")
            st.dataframe(df_view['Distrito_Detectado'].value_counts().head(5))

        with col_mapa:
            view_state = pdk.ViewState(
                latitude=-12.0464, longitude=-77.0428, zoom=10, pitch=45)

            layer_hex = pdk.Layer(
                "HexagonLayer",
                data=df_view,
                get_position='[lon, lat]',
                radius=300,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            )

            layer_scatter = pdk.Layer(
                "ScatterplotLayer",
                data=df_view,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=150,
                pickable=True,
            )

            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=view_state,
                layers=[layer_hex, layer_scatter],
                tooltip={"text": "{Titulo}\n({Fuente})"}
            ))

# -----------------------------
# SECCIÓN: ANÁLISIS POR PERIÓDICO
# -----------------------------
elif menu == "Análisis por Periódico":
    st.title("📊 Análisis Comparativo")

    if df_global is not None:
        c1, c2 = st.columns([2, 1])

        with c1:
            # Gráfico de barras por Fuente
            conteo = df_global['Fuente'].value_counts().reset_index()
            conteo.columns = ['Fuente', 'Cantidad']
            fig = px.bar(conteo, x='Fuente', y='Cantidad',
                         color='Fuente', title="Noticias por Medio")
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Buscar Noticia")
            txt = st.text_input("Palabra clave (ej: robo)")
            if txt:
                res = df_global[df_global['Titulo'].str.contains(
                    txt, case=False, na=False)]
                st.dataframe(res[['Titulo', 'Fuente']], hide_index=True)

# -----------------------------
# SECCIÓN: EMERGENCIAS
# -----------------------------
elif menu == "Emergencias":
    st.title("📞 Centrales de Emergencia")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("### 👮 PNP: 105")
    with col2:
        st.warning("### 🚒 Bomberos: 116")
    with col3:
        st.info("### 🚑 SAMU: 106")

# -----------------------------
# SECCIÓN: EQUIPO
# -----------------------------
elif menu == "Equipo":
    # Mismo código de tu compañero para el equipo
    st.markdown("""
    <h2 style="text-align:center;">👥 El Equipo</h2>
    <div style="display:flex; justify-content:center; gap:20px; flex-wrap:wrap;">
        <div style="background:#f9f9f9; padding:20px; border-radius:10px; border-top: 4px solid #D32F2F; width:200px; text-align:center;">
            <h3>👨‍💻</h3>
            <p><b>Daniel Ormeño</b></p>
        </div>
        <div style="background:#f9f9f9; padding:20px; border-radius:10px; border-top: 4px solid #D32F2F; width:200px; text-align:center;">
            <h3>👨‍💻</h3>
            <p><b>Luis Huamayalli</b></p>
        </div>
        <div style="background:#f9f9f9; padding:20px; border-radius:10px; border-top: 4px solid #D32F2F; width:200px; text-align:center;">
            <h3>👩‍💻</h3>
            <p><b>Pamela Lázaro</b></p>
        </div>
    </div>
    """, unsafe_allow_html=True)
