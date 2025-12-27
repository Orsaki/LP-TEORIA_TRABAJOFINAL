import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pydeck as pdk
import plotly.express as px
import requests
from bs4 import BeautifulSoup


import streamlit as st

# -----------------------------
# CONFIGURACIÓN DE LA PÁGINA (SIEMPRE PRIMERO)
# -----------------------------
st.set_page_config(
    page_title="Lima Segura: Monitor de Criminalidad", 
    page_icon="🚨", 
    layout="wide"
)

# -----------------------------
# TÍTULO PRINCIPAL CENTRADO
# -----------------------------
st.markdown(
    "<h1 style='text-align: center;'>Sistema de Alerta de Delitos</h1>",
    unsafe_allow_html=True
)

# -----------------------------
# SLIDER DE PORTADAS
# -----------------------------
items = [
    {
        "title": "Inseguridad ciudadana en Lima",
        "text": "Impacto en la población",
        "img": "imagenes/portada1.png"
    },
    {
        "title": "Análisis de delitos",
        "text": "Zonas de mayor riesgo",
        "img": "imagenes/portada2.png"
    }
]

# estado del slide
if "slide" not in st.session_state:
    st.session_state.slide = 0

item = items[st.session_state.slide]

# imagen centrada y tamaño controlado
col_left, col_center, col_right = st.columns([1, 3, 1])

with col_center:
    st.image(item["img"], use_container_width=True)
    st.markdown(
        f"<h3 style='text-align:center;'>{item['title']}</h3>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='text-align:center;'>{item['text']}</p>",
        unsafe_allow_html=True
    )

# -----------------------------
# -----------------------------
# -----------------------------
st.markdown("<br>", unsafe_allow_html=True)

# columna única centrada
_, col_center, _ = st.columns([3, 1, 3])

with col_center:
    c1, c2 = st.columns(2)

    with c1:
        if st.button("⬅️Atrás"):
            st.session_state.slide = (st.session_state.slide - 1) % len(items)
            st.rerun()

    with c2:
        if st.button("Adelante➡️"):
            st.session_state.slide = (st.session_state.slide + 1) % len(items)
            st.rerun()


# detectar clicks
if "prev" in st.session_state:
    st.session_state.slide = (st.session_state.slide - 1) % len(items)
    del st.session_state["prev"]
    st.rerun()

if "next" in st.session_state:
    st.session_state.slide = (st.session_state.slide + 1) % len(items)
    del st.session_state["next"]
    st.rerun()





# -----------------------------
# ESTILOS CSS PERSONALIZADOS
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
.kpi-card h3 {
    color: #D32F2F;
    font-size: 1.2em;
}
.kpi-card p {
    color: #333;
    font-size: 0.95em;
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
# SECCIÓN 3: ANÁLISIS POR PERIÓDICO (LÓGICA CORREGIDA)
# -----------------------------
elif menu == "Análisis por Periódico":
    from datetime import datetime 
    import time
    import re 
    
    # --- 1. MEMORIA (SESSION STATE) ---
    if 'historial_noticias' not in st.session_state:
        st.session_state['historial_noticias'] = pd.DataFrame(columns=["Titular", "Distrito", "Enlace"])

    # --- 2. CONSTANTES Y FUNCIONES (Las definimos primero) ---
    URL_BASE = "https://rpp.pe/tema/inseguridad-ciudadana"
    HEADERS = {'User-Agent': 'Mozilla/5.0'}

    PALABRAS_CLAVE = [
        "robo", "asalto", "delincuencia", "policia", "policía", "crimen", "sicario", 
        "balacera", "muerte", "asesinato", "comisaria", "comisaría", "extorsion", "extorsión", "terna", 
        "captura", "banda", "droga", "operativo", "homicidio", "armas", 
        "victima", "víctima", "delincuente", "ladrones", "atraco", "disparos", "cadáver", "cuerpo", "matan", "balean"
    ]

    EXCLUSIONES_TITULO = [
        "congreso", "parlamento", "dina", "boluarte", "rusia", "ucrania", "gaza", 
        "israel", "biden", "trump", "putin", "futbol", "fútbol", "liga 1", 
        "seleccion", "selección", "fossati", "alianza", "universitario", "jne", "onpe"
    ]

    EXCLUSIONES_URL = [
        "/mundo/", "/famosos/", "/entretenimiento/", "/cultura/", "/tecnologia/", 
        "/ciencia/", "/economia/", "/vital/", "/automovilismo/"
    ]

    DISTRITOS_INTEGRADOS = [
        "ancon", "ancón", "carabayllo", "comas", "independencia", "los olivos", "puente piedra", "san martin de porres", "smp", "santa rosa",
        "ate", "breña", "cercado de lima", "jesus maria", "jesús maría", "la victoria", "lince", "magdalena", "miraflores", "pueblo libre", "rimac", "rímac", "san borja", "san isidro", "san luis", "san miguel", "santa anita", "surquillo",
        "barranco", "chorrillos", "lurin", "lurín", "pachacamac", "pachacámac", "pucusana", "punta hermosa", "punta negra", "san bartolo", "san juan de miraflores", "sjm", "santiago de surco", "surco", "villa el salvador", "ves", "villa maria del triunfo", "vmt",
        "chaclacayo", "cieneguilla", "el agustino", "la molina", "lurigancho", "chosica", "san juan de lurigancho", "sjl",
        "callao", "bellavista", "carmen de la legua", "reynoso", "la perla", "la punta", "ventanilla", "mi peru", "mi perú"
    ]

    def buscar_palabra_exacta(texto, lista_palabras):
        texto = texto.lower()
        for palabra in lista_palabras:
            patron = r'\b' + re.escape(palabra) + r'\b'
            if re.search(patron, texto):
                return palabra.upper()
        return None

    @st.cache_data(ttl=300, show_spinner="Analizando RPP...")
    def escanear_inteligente():
        noticias_encontradas = []
        for pagina in range(1, 4): 
            try:
                url_paginada = f"{URL_BASE}?page={pagina}"
                response = requests.get(url_paginada, headers=HEADERS, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    titulares = soup.find_all(['h2', 'h3'])
                    for header in titulares:
                        enlace = header.find('a')
                        if enlace:
                            titulo_texto = enlace.text.strip()
                            url_noticia = enlace.get('href')
                            if url_noticia and not url_noticia.startswith("http"):
                                url_noticia = "https://rpp.pe" + url_noticia
                            
                            if any(seccion in url_noticia for seccion in EXCLUSIONES_URL): continue 
                            if buscar_palabra_exacta(titulo_texto, EXCLUSIONES_TITULO): continue
                            
                            distrito = buscar_palabra_exacta(titulo_texto, DISTRITOS_INTEGRADOS)
                            delito = buscar_palabra_exacta(titulo_texto, PALABRAS_CLAVE)
                            
                            ubicacion_final = district if (district := distrito) else "⚠️ No Especificado"
                            
                            # Filtro: Distrito O Delito
                            if distrito or delito:
                                noticias_encontradas.append({
                                    "Titular": titulo_texto,
                                    "Distrito": ubicacion_final,
                                    "Enlace": url_noticia
                                })
                time.sleep(0.5)
            except Exception:
                continue
        return pd.DataFrame(noticias_encontradas)

    # --- 3. EJECUCIÓN DEL SCRAPING (¡ESTO VA ANTES DE DIBUJAR!) ---
    df_nuevas = escanear_inteligente()
    
    if not df_nuevas.empty:
        df_total = pd.concat([st.session_state['historial_noticias'], df_nuevas])
        df_total = df_total.drop_duplicates(subset=["Titular"], keep='last')
        st.session_state['historial_noticias'] = df_total

    # --- 4. INTERFAZ GRÁFICA (Ahora sí dibujamos con los datos listos) ---
    
    st.title("🛡️ Monitor de Criminalidad (Lima + Callao)")
    st.markdown("Visualización en tiempo real de incidentes de seguridad ciudadana reportados por medios digitales.")
    st.write("---") 

    # ==============================================================================
    # BLOQUE 1: NOTICIAS RPP
    # ==============================================================================
    with st.container(border=True):
        col_rpp_title, col_rpp_metrics = st.columns([2, 3])
        
        with col_rpp_title:
            st.subheader("📰 Noticias RPP")
        
        with col_rpp_metrics:
            fecha_hoy = datetime.now().strftime("%d/%m/%Y")
            # AHORA ESTE NÚMERO SERÁ EL CORRECTO PORQUE YA ACTUALIZAMOS ARRIBA
            n_noticias = len(st.session_state['historial_noticias'])
            st.markdown(f"<div style='text-align: right;'>📅 <b>{fecha_hoy}</b> | 🚨 Capturadas: <b>{n_noticias}</b></div>", unsafe_allow_html=True)

        with st.expander("ℹ️ Detalles del Funcionamiento (RPP)", expanded=False):
            st.markdown("""
            * ⏱️ **Frecuencia:** Escaneo automático cada **5 minutos**.
            * 🔍 **Filtro:** Detecta palabras clave (Robo, Sicariato, etc.) y bloquea farándula/deportes.
            * 📍 **Geo:** Busca coincidencias exactas de los 50 distritos de Lima y Callao.
            """)

        df_final = st.session_state['historial_noticias']

        if not df_final.empty:
            df_view = df_final[["Titular", "Distrito", "Enlace"]]
            st.dataframe(
                df_view,
                column_config={
                    "Enlace": st.column_config.LinkColumn("Fuente", display_text="Leer Nota"),
                    "Distrito": st.column_config.TextColumn("Ubicación", width="medium"),
                    "Titular": st.column_config.TextColumn("Noticia", width="large"),
                },
                use_container_width=True,
                hide_index=True 
            )
        else:
            st.info("Sin alertas recientes en esta fuente.")

        if st.button("🔄 Escanear RPP", key="scan_rpp"):
            escanear_inteligente.clear()
            st.rerun()
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
