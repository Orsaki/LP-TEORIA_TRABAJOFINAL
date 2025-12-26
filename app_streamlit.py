import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pydeck as pdk
import plotly.express as px

# -----------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------
st.set_page_config(
    page_title="Lima Segura: Monitor de Criminalidad", 
    page_icon="🚨", 
    layout="wide"
)

# -----------------------------
# ESTILOS CSS PERSONALIZADOS (Tema: Alerta/Noticias)
# -----------------------------
st.markdown("""
    <style>
    /* Estilo para las tarjetas de KPIs en Inicio */
    .kpi-card {
        background-color: #FFFFFF;
        border-left: 5px solid #D32F2F; /* Rojo alerta */
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .kpi-card h3 {
        color: #D32F2F;
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    .kpi-card p {
        color: #333;
        font-size: 0.95em;
    }
    
    /* Estilo para el título principal */
    .main-title {
        font-family: 'Arial Black', sans-serif;
        color: #1a1a1a;
        text-align: center;
        font-size: 3em;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 1.2em;
        margin-top: -10px;
        margin-bottom: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# MENÚ LATERAL
# -----------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1083/1083584.png", width=50) # Icono genérico de alerta
    st.markdown("## 🚨 Lima Segura")
    menu = option_menu(
        menu_title="Navegación",
        options=[
            "Inicio", 
            "Mapa del Crimen", 
            "Análisis por Periódico", 
            "Equipo"
        ],
        icons=["house", "geo-alt", "newspaper", "people"],
        menu_icon="list",
        default_index=0,
        styles={
            "nav-link-selected": {"background-color": "#D32F2F"}, # Rojo al seleccionar
        }
    )

# -----------------------------
# SECCIÓN 1: INICIO (Contexto Teórico)
# -----------------------------
if menu == "Inicio":
    # 1. Título Actualizado
    st.markdown('<h1 class="main-title">SISTEMA DE ALERTA DE DELITOS Y ZONAS PELIGROSAS</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Monitor de Criminalidad basado en Web Scraping y Geolocalización</p>', unsafe_allow_html=True)

    # 2. Imágenes Locales (desde la carpeta 'imagenes')
    # Usamos columnas para que se vean una al lado de la otra
    col_img1, col_img2 = st.columns(2)
    
    with col_img1:
        # Asegúrate de que el nombre coincida exactamente con tu carpeta
        st.image("imagenes/cambio_habitos.jpg", use_container_width=True, caption="Impacto en la ciudadanía")
        
    with col_img2:
        st.image("imagenes/tukituki.png", use_container_width=True, caption="Análisis de seguridad")

    st.markdown("---")
    
    # 3. Resto del contenido (Texto informativo)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📢 La Realidad Actual")
        st.write("""
        La inseguridad ciudadana en Lima Metropolitana se ha convertido en uno de los principales problemas que aquejan a la población. 
        Diariamente, los medios de comunicación reportan incidentes que van desde hurtos menores hasta crímenes organizados.
        
        Este proyecto busca utilizar la tecnología para **centralizar, geolocalizar y visualizar** estas noticias en tiempo real, 
        permitiendo identificar "puntos calientes" y patrones delictivos basados en la información periodística.
        """)
    
    with col2:
        st.markdown("### 🤖 ¿Cómo funciona este sistema?")
        st.info("""
        1. **Web Scraping:** Un algoritmo recorre periódicos digitales (El Comercio, La República, etc.).
        2. **Procesamiento NLP:** Se analiza el texto para detectar ubicaciones (Distritos, Calles).
        3. **Geocoding:** Convertimos las direcciones en coordenadas (Latitud/Longitud).
        4. **Visualización:** Mostramos los incidentes en un mapa interactivo.
        """)

    # 4. KPIs (Indicadores)
    st.markdown("### 📊 Indicadores Clave (Demo)")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.markdown("""
        <div class="kpi-card">
            <h3>🗞️ Fuentes</h3>
            <p>Monitoreo activo de <b>3 periódicos</b> principales del país.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi2:
        st.markdown("""
        <div class="kpi-card">
            <h3>📍 Geolocalización</h3>
            <p>Detección automática de distritos mediante <b>NLP</b>.</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown("""
        <div class="kpi-card">
            <h3>🔥 Mapa de Calor</h3>
            <p>Identificación visual de zonas con alta densidad de noticias.</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown("""
        <div class="kpi-card">
            <h3>⏱️ Tiempo Real</h3>
            <p>Actualización de noticias al instante (Simulación).</p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# SECCIÓN 2: MAPA (Placeholder Pydeck)
# -----------------------------
elif menu == "Mapa del Crimen":
    st.title("📍 Mapa de Incidencias en Lima")
    st.write("Visualización geoespacial de las noticias extraídas. Los puntos brillantes indican noticias recientes.")

    col_control, col_map = st.columns([1, 4])

    with col_control:
        st.subheader("Filtros")
        st.selectbox("Seleccionar Distrito", ["Todos", "San Juan de Lurigancho", "Miraflores", "Los Olivos", "Cercado"])
        st.selectbox("Tipo de Delito", ["Todos", "Robo", "Asalto", "Homicidio", "Extorsión"])
        st.slider("Rango de tiempo (días)", 1, 30, 7)
        if st.button("Actualizar Mapa"):
            st.toast("Actualizando datos desde la web...", icon="🔄")

    with col_map:
        # --- CONFIGURACIÓN DEL MAPA VACÍO (POR AHORA) ---
        # Coordenadas centrales de Lima
        INITIAL_VIEW_STATE = pdk.ViewState(
            latitude=-12.0464,
            longitude=-77.0428,
            zoom=11,
            pitch=50,
        )

        # Aquí más adelante insertaremos tu DataFrame con lat/lon
        # Por ahora creamos un mapa base estilo "Dark" (mejor para ver luces)
        r = pdk.Deck(
            map_style='mapbox://styles/mapbox/dark-v10', # Estilo oscuro
            initial_view_state=INITIAL_VIEW_STATE,
            tooltip={"text": "Lima"},
            layers=[] # Aquí irán tus capas de ScatterplotLayer más adelante
        )
        
        st.pydeck_chart(r)
        
    st.info("Nota: Este mapa se poblará dinámicamente cuando conectemos el módulo de Web Scraping.")

# -----------------------------
# SECCIÓN 3: ANÁLISIS POR PERIÓDICO
# -----------------------------
elif menu == "Análisis por Periódico":
    st.title("📰 Análisis de Fuentes Periodísticas")
    st.write("Comparativa de titulares y frecuencia de noticias por medio de comunicación.")

    # Simulación de pestañas para los periódicos
    tab1, tab2, tab3 = st.tabs(["El Comercio", "La República", "RPP Noticias"])

    with tab1:
        st.subheader("El Comercio - Sección Sucesos")
        st.warning("⚠️ Módulo de Scraping pendiente de conexión.")
        st.code("""
        # Aquí se mostrará el DataFrame resultante de:
        # soup.find_all('h2', class_='title')
        """, language="python")
        
    with tab2:
        st.subheader("La República - Sección Sociedad")
        st.warning("⚠️ Módulo de Scraping pendiente de conexión.")
        
    with tab3:
        st.subheader("RPP - Sección Policiales")
        st.warning("⚠️ Módulo de Scraping pendiente de conexión.")

# -----------------------------
# SECCIÓN 4: EQUIPO
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