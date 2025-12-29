import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pydeck as pdk
import plotly.express as px
import requests
import time
import re

# ==============================================================================
# 1. IMPORTAR CONFIGURACIÓN CENTRALIZADA (TU ARCHIVO CONFIG.PY)
# ==============================================================================
try:
    from config import PALABRAS_CLAVE  # <--- AQUÍ USAMOS TU LISTA CENTRAL
except ImportError:
    st.error("⚠️ Error Crítico: No se encontró el archivo 'config.py'. Asegúrate de que esté en la misma carpeta que 'app_streamlit.py'.")
    PALABRAS_CLAVE = []  # Lista vacía de respaldo para que no explote

# ==============================================================================
# 2. IMPORTACIÓN DE MÓDULOS DE SCRAPING
# ==============================================================================
try:
    from webscraping import (
        webscraping_rpp,
        web_scraping_el_comercio,
        webscraping_canalN,
        webscraping_diariocorreo,
        webscraping_infobaePE,
        webscraping_larepublica,
        webscraping_peru21
    )
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    print(f"Error importando módulos: {e}")

# ==============================================================================
# 3. CONFIGURACIÓN Y GEOCODIFICACIÓN (API NOMINATIM)
# ==============================================================================
st.set_page_config(page_title="Lima Segura: Monitor",
                   page_icon="🚨", layout="wide")

if 'historial_noticias' not in st.session_state:
    st.session_state['historial_noticias'] = pd.DataFrame()


@st.cache_data(show_spinner=False)
def obtener_coordenadas(ubicacion):
    """Consulta la API de Nominatim (OpenStreetMap)"""
    if not ubicacion or ubicacion == "⚠️ No Especificado":
        return None, None

    url = f"https://nominatim.openstreetmap.org/search?q={ubicacion},+Lima,+Peru&format=json&limit=1"
    headers = {'User-Agent': 'SistemaAlertaDelitos_LP2_Final'}

    try:
        time.sleep(0.5)  # Pausa cortés a la API
        response = requests.get(url, headers=headers).json()
        if response:
            return float(response[0]['lat']), float(response[0]['lon'])
    except Exception as e:
        print(f"Error en {ubicacion}: {e}")

    return None, None

# ==============================================================================
# 4. ESCANEO CON FILTRO ESTRICTO (USANDO CONFIG.PY)
# ==============================================================================


@st.cache_data(ttl=300, show_spinner="Escaneando fuentes...")
def escanear_con_archivos_propios():
    # Verificamos si los módulos se cargaron bien
    if not MODULES_AVAILABLE:
        st.error("⚠️ Error: No se detectan los archivos en la carpeta 'webscraping'.")
        return pd.DataFrame()

    todas_las_noticias = []

    # Lista de tus scrapers
    mis_scrapers = [
        ("RPP", webscraping_rpp),
        ("El Comercio", web_scraping_el_comercio),
        ("Canal N", webscraping_canalN),
        ("Diario Correo", webscraping_diariocorreo),
        ("Infobae", webscraping_infobaePE),
        ("La República", webscraping_larepublica),
        ("Perú 21", webscraping_peru21)
    ]

    progress_bar = st.progress(0, text="Iniciando monitor de crimen...")
    total = len(mis_scrapers)

    for i, (nombre_web, modulo) in enumerate(mis_scrapers):
        try:
            progress_bar.progress(int(((i)/total)*100),
                                  text=f"Analizando: {nombre_web}...")

            # 1. EJECUTAR EL SCRAPER
            # (El scraper ya se encargó de filtrar, confiamos en él)
            if hasattr(modulo, 'obtener_noticias'):
                datos = modulo.obtener_noticias()
            elif hasattr(modulo, 'scrape'):
                datos = modulo.scrape()
            else:
                continue

            # 2. PROCESAR RESULTADOS (SIN VOLVER A FILTRAR)
            if datos:
                # Si devuelve un DataFrame, lo convertimos a lista
                if isinstance(datos, pd.DataFrame):
                    datos = datos.to_dict('records')

                for noticia in datos:
                    # Nos aseguramos de que tenga 'Fuente'
                    if 'Fuente' not in noticia:
                        noticia['Fuente'] = nombre_web

                    # Si no tiene categoría, le ponemos una por defecto
                    if 'Categoría' not in noticia or not noticia['Categoría']:
                        noticia['Categoría'] = "Delito Detectado"

                    # ¡IMPORTANTE! Agregamos la noticia directamente
                    # (Aquí borramos el bloque 'if re.search' que te estaba borrando la noticia)
                    todas_las_noticias.append(noticia)

        except Exception as e:
            # Si falla un periódico, seguimos con los otros sin detener todo
            print(f"Error leyendo {nombre_web}: {e}")
            continue

    progress_bar.empty()

    # Retornamos todo lo que encontramos
    return pd.DataFrame(todas_las_noticias) if todas_las_noticias else pd.DataFrame()


# ==============================================================================
# 5. INTERFAZ GRÁFICA
# ==============================================================================
st.markdown("""
    <style>
    .kpi-card { background-color: #FFFFFF; border-left: 5px solid #D32F2F; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .kpi-card h3 { color: #D32F2F; font-size: 1.2em; margin-bottom: 10px; }
    .main-title { font-family: 'Arial Black', sans-serif; color: #1a1a1a; text-align: center; font-size: 3em; margin-bottom: 0; }
    .subtitle { text-align: center; color: #555; font-size: 1.2em; margin-top: -10px; margin-bottom: 40px; }
    </style>
""", unsafe_allow_html=True)

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

# ==============================================================================
# 6. SECCIONES
# ==============================================================================

if menu == "Inicio":
    st.markdown('<h1 class="main-title">MONITOR DE CRIMINALIDAD</h1>',
                unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Sistema de Alerta Exclusivo de Delitos (Filtro Config.py)</p>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    try:
        with col1:
            st.image("imagenes/cambio_habitos.jpg", use_container_width=True)
        with col2:
            st.image("imagenes/tukituki.png", use_container_width=True)
    except:
        pass

    st.markdown("---")

    col_scan_center = st.columns([1, 2, 1])
    with col_scan_center[1]:
        if st.button("🔄 ESCANEAR DELITOS (FILTRO ACTIVADO)", type="primary", use_container_width=True):
            st.cache_data.clear()
            st.session_state['historial_noticias'] = escanear_con_archivos_propios()
            st.rerun()

    df_kpi = st.session_state['historial_noticias']
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(
            f"""<div class="kpi-card"><h3>🗞️ {len(df_kpi)}</h3><p>Delitos Confirmados</p></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(
            f"""<div class="kpi-card"><h3>🛡️ Filtro</h3><p>Centralizado (Config.py)</p></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(
            f"""<div class="kpi-card"><h3>📍 API</h3><p>Nominatim Activo</p></div>""", unsafe_allow_html=True)

elif menu == "Mapa del Crimen":
    st.title("📍 Mapa de Calor (Solo Delitos)")
    df_base = st.session_state['historial_noticias']

    if df_base.empty:
        st.warning("⚠️ No se han detectado delitos. Ve a 'Inicio' y escanea.")
    else:
        distritos_disponibles = sorted(
            df_base[df_base['Distrito'] != "⚠️ No Especificado"]['Distrito'].unique().tolist())

        col_control, col_map = st.columns([1, 4])
        with col_control:
            st.subheader("Filtros")
            distrito_sel = st.selectbox(
                "Distrito:", ["Todos"] + distritos_disponibles)

            cats_dispo = ["Todos"]
            if 'Categoría' in df_base.columns:
                cats_dispo += list(df_base['Categoría'].unique())
            delito_sel = st.selectbox("Tipo de Delito:", cats_dispo)

        with col_map:
            df_filtrado = df_base.copy()
            if distrito_sel != "Todos":
                df_filtrado = df_filtrado[df_filtrado['Distrito']
                                          == distrito_sel]
            if delito_sel != "Todos" and 'Categoría' in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado['Categoría']
                                          == delito_sel]

            with st.spinner("Geolocalizando delitos con API..."):
                coordenadas = df_filtrado['Distrito'].apply(
                    obtener_coordenadas)

            df_filtrado['lat'] = coordenadas.apply(
                lambda x: x[0] if x else None)
            df_filtrado['lon'] = coordenadas.apply(
                lambda x: x[1] if x else None)
            df_final = df_filtrado.dropna(subset=['lat', 'lon'])

            if not df_final.empty:
                lat_c = df_final['lat'].iloc[0]
                lon_c = df_final['lon'].iloc[0]
                zoom_c = 13 if distrito_sel != "Todos" else 10
                if distrito_sel == "Todos":
                    lat_c, lon_c = -12.0464, -77.0428

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
                st.success(f"📍 Mostrando {len(df_final)} delitos en mapa.")
            else:
                st.info("No hay delitos ubicables con estos filtros.")

elif menu == "Análisis por Periódico":
    st.title("📊 Estadísticas de Criminalidad")
    df_analisis = st.session_state['historial_noticias']

    if df_analisis.empty:
        st.warning("⚠️ Sin datos. Ejecuta el escaneo en Inicio.")
    else:
        st.write("### 🔍 Filtros")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            fuentes_sel = st.multiselect(
                "Medio:", df_analisis['Fuente'].unique(), default=df_analisis['Fuente'].unique())

        if 'Categoría' in df_analisis.columns:
            with col_f2:
                tipos_sel = st.multiselect("Tipo de Delito:", df_analisis['Categoría'].unique(
                ), default=df_analisis['Categoría'].unique())
            df_viz = df_analisis[df_analisis['Fuente'].isin(
                fuentes_sel) & df_analisis['Categoría'].isin(tipos_sel)]
        else:
            df_viz = df_analisis[df_analisis['Fuente'].isin(fuentes_sel)]

        st.write("---")

        # 1. GRÁFICOS DE RESUMEN (Los clásicos)
        c1, c2 = st.columns(2)
        with c1:
            conteo = df_viz['Fuente'].value_counts().reset_index()
            conteo.columns = ['Fuente', 'Cantidad']
            fig1 = px.bar(conteo, x='Fuente', y='Cantidad',
                          color='Fuente', title="Noticias por Medio")
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            if 'Categoría' in df_viz.columns:
                conteo_tipo = df_viz['Categoría'].value_counts().reset_index()
                conteo_tipo.columns = ['Categoría', 'Cantidad']
                fig2 = px.pie(conteo_tipo, names='Categoría',
                              values='Cantidad', hole=0.4, title="Distribución de Delitos")
                st.plotly_chart(fig2, use_container_width=True)

        # ====================================================================
        # NUEVO: MOSAICO DE CALOR (TREEMAP) - ¡MUCHO MÁS VISUAL!
        # ====================================================================
        st.write("---")
        st.subheader("🚨 Mapa de Calor por Distritos (Hotspots)")

        # Filtramos 'No Especificado'
        df_ranking = df_viz[df_viz['Distrito'] != "⚠️ No Especificado"].copy()

        if not df_ranking.empty:
            # --- CORRECCIÓN VISUAL: LIMA -> CERCADO DE LIMA ---
            # Esto arregla lo que me dijiste. "Lima" a secas se ve mal, mejor "Cercado".
            df_ranking.loc[df_ranking['Distrito'] ==
                           'LIMA', 'Distrito'] = 'CERCADO DE LIMA'

            # Preparamos datos para el Treemap
            # Agrupamos por Distrito Y Categoría para ver el detalle
            df_treemap = df_ranking.groupby(
                ['Distrito', 'Categoría']).size().reset_index(name='Casos')

            # Gráfico TREEMAP (Mosaico)
            fig3 = px.treemap(df_treemap,
                              # Jerarquía: Primero Distrito, luego Delito
                              path=['Distrito', 'Categoría'],
                              values='Casos',
                              color='Casos',
                              color_continuous_scale='Reds',  # Rojo = Peligro
                              title="Concentración de Crimen (Tamaño = Más Delitos)",
                              hover_data=['Casos'])

            # Personalizamos para que se vea moderno
            fig3.update_traces(root_color="lightgrey")
            fig3.update_layout(margin=dict(t=50, l=25, r=25, b=25))

            st.plotly_chart(fig3, use_container_width=True)
            st.info(
                "💡 Tip: Haz clic en un distrito (cuadro grande) para ver qué delitos específicos ocurren ahí.")
        else:
            st.info(
                "No hay suficientes datos de ubicación para generar el mapa de calor.")
        # ====================================================================

        st.dataframe(
            df_viz[['Titular', 'Categoría', 'Distrito', 'Fuente']],
            hide_index=True,
            use_container_width=True)
# =======================================================================
#  EQUIPO Y EMERGENCIAS
# =======================================================================

elif menu == "Equipo":
    st.markdown("""
    <style>
        .team-container { display: flex; justify-content: center; flex-wrap: wrap; gap: 40px; margin-top: 50px; }
        .member-card { background-color: #f8f9fa; border-top: 5px solid #D32F2F; border-radius: 15px; padding: 30px; width: 250px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s; }
        .member-card:hover { transform: translateY(-10px); }
        .member-name { font-size: 18px; font-weight: bold; color: #333; margin-top: 15px; }
        .member-role { color: #666; font-size: 0.85em; margin-bottom: 15px; }
        .avatar { font-size: 50px; }
        .github-btn { text-decoration: none; color: #D32F2F; font-weight: bold; border: 1px solid #D32F2F; padding: 5px 15px; border-radius: 20px; transition: all 0.3s ease; }
        .github-btn:hover { background-color: #D32F2F; color: white; }
    </style>
    <h2 style="text-align:center;">👥 El Equipo</h2>
    <p style="text-align:center;">Estudiantes de Ingeniería Estadística e Informática - UNALM</p>
    <div class="team-container">
    <div class="member-card"><div class="avatar">👨‍💻</div><div class="member-name">Daniel Ormeño Sakihama</div><div class="member-role">Ingeniería Estadística Informática</div><a href="https://github.com/Orsaki" target="_blank" class="github-btn">GitHub Profile</a></div>
    <div class="member-card"><div class="avatar">👨‍💻</div><div class="member-name">Luis Huamayalli</div><div class="member-role">Ingeniería Estadística Informática</div><a href="https://github.com/Albert-ca" target="_blank" class="github-btn">GitHub Profile</a></div>
    <div class="member-card"><div class="avatar">👩‍💻</div><div class="member-name">Pamela Lázaro</div><div class="member-role">Ingeniería Estadística Informática</div><a href="https://github.com/lazaropamela" target="_blank" class="github-btn">GitHub Profile</a></div>
    <div class="member-card"><div class="avatar">👩‍💻</div><div class="member-name">Fátima Montes</div><div class="member-role">Ingeniería Estadística Informática</div><a href="https://github.com/FatimaMY" target="_blank" class="github-btn">GitHub Profile</a></div>
    </div>
    """, unsafe_allow_html=True)

elif menu == "Emergencias":
    st.title("📞 Centrales de Emergencia")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("### 👮 PNP 105")
        st.write("Policía Nacional.")
    with col2:
        st.warning("### 🚒 Bomberos 116")
        st.write("Incendios y rescates.")
    with col3:
        st.info("### 🚑 SAMU 106")
        st.write("Urgencias médicas.")
