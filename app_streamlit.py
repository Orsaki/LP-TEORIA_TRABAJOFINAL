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
# --- COORDENADAS DE DISTRITOS 

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
    "SAN JUAN DE MIRAFLORES": [-12.1497, -76.9669], "SAN LUIS": [-12.0750, -76.9958],
    "SAN MARTIN DE PORRES": [-12.0053, -77.0583],"SAN MIGUEL": [-12.0775, -77.0917],
    "SANTA ANITA": [-12.0439, -76.9686], "SURCO": [-12.1456, -76.9789], "SANTIAGO DE SURCO": [-12.1456, -76.9789],
    "SURQUILLO": [-12.1133, -77.0225], "VILLA EL SALVADOR": [-12.2133, -76.9367],
    "VILLA MARIA DEL TRIUNFO": [-12.1603, -76.9294], "CERCADO DE LIMA": [-12.0464, -77.0428],
    "CALLAO": [-12.0566, -77.1181], "VENTANILLA": [-11.8753, -77.1256], "LA PERLA": [-12.0675, -77.1025]
}

st.set_page_config(
    page_title="Lima Segura: Monitor de Criminalidad", 
    page_icon="🚨", 
    layout="wide"
)
# --- 2. HERRAMIENTAS DE BÚSQUEDA (Mover aquí arriba) ---
# --- NUEVAS FUENTES DE NOTICIAS ---
FUENTES = {
    "RPP": "https://rpp.pe/tema/inseguridad-ciudadana",
    "El Comercio": "https://elcomercio.pe/lima/policiales/",
    "La República": "https://larepublica.pe/sociedad/"
}

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

PALABRAS_CLAVE = ["robo", "asalto", "delincuencia", "policia", "policía", "crimen", "sicario", 
                  "balacera", "muerte", "asesinato", "extorsion", "extorsión", "homicidio", "atraco"]

DISTRITOS_INTEGRADOS = [d.lower() for d in COORDENADAS_LIMA.keys()]

def buscar_palabra_exacta(texto, lista_palabras):
    texto = texto.lower()
    for palabra in lista_palabras:
        patron = r'\b' + re.escape(palabra) + r'\b'
        if re.search(patron, texto):
            return palabra.upper()
    return None

@st.cache_data(ttl=300)
def escanear_inteligente():
    noticias_encontradas = []
    
    # Recorremos cada periódico definido en el diccionario FUENTES
    for nombre_fuente, url_base in FUENTES.items():
        try:
            response = requests.get(url_base, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscamos titulares en etiquetas comunes (h2 y h3)
                titulares = soup.find_all(['h2', 'h3'])
                
                for header in titulares:
                    enlace = header.find('a')
                    if enlace:
                        titulo_texto = enlace.text.strip()
                        path = enlace.get('href')
                        
                        # Construir URL completa según la fuente
                        if path.startswith("http"):
                            url_noticia = path
                        elif nombre_fuente == "RPP":
                            url_noticia = "https://rpp.pe" + path
                        elif nombre_fuente == "El Comercio":
                            url_noticia = "https://elcomercio.pe" + path
                        else:
                            url_noticia = "https://larepublica.pe" + path
                        
                        # Aplicar tu lógica de detección de distritos
                        distrito = buscar_palabra_exacta(titulo_texto, DISTRITOS_INTEGRADOS)
                        
                        if distrito:
                            noticias_encontradas.append({
                                "Titular": f"[{nombre_fuente}] {titulo_texto}",
                                "Distrito": distrito,
                                "Enlace": url_noticia,
                                "Fuente": nombre_fuente
                            })
        except Exception as e:
            print(f"Error escaneando {nombre_fuente}: {e}")
            continue
            
    return pd.DataFrame(noticias_encontradas)

# --- 3. MEMORIA COMPARTIDA (Session State) ---
if 'historial_noticias' not in st.session_state:
    # La primera vez que carga, busca noticias automáticamente
    st.session_state['historial_noticias'] = escanear_inteligente()

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
            <p>Monitoreo activo de <b>3 periódicos</b> (RPP, El Comercio, La República).</p>
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
# SECCIÓN 2: MAPA (CONEXIÓN DINÁMICA)
# -----------------------------
elif menu == "Mapa del Crimen":
    st.title("📍 Alerta de Delitos en Tiempo Real")
    
    df_noticias = st.session_state.get('historial_noticias', pd.DataFrame())

    col_control, col_map = st.columns([1, 4])

    with col_control:
        st.subheader("Filtros")
        # 1. Guardamos el distrito seleccionado en una variable
        distrito_sel = st.selectbox("Seleccionar Distrito", ["Todos"] + list(COORDENADAS_LIMA.keys()))
        
        if st.button("Actualizar Vista"):
            st.toast("Cambiando enfoque...", icon="🔍")

    with col_map:
        # 2. LÓGICA DE ENFOQUE (Zoom dinámico)
        # Si selecciona un distrito, usamos sus coordenadas; si es "Todos", usamos el centro de Lima.
        if distrito_sel != "Todos":
            coords_foco = COORDENADAS_LIMA[distrito_sel]
            zoom_actual = 14  # Más cerca para ver el distrito
        else:
            coords_foco = [-12.0464, -77.0428] # Centro de Lima
            zoom_actual = 10.5 # Vista general

        if not df_noticias.empty:
            df_mapa = df_noticias.copy()
            def get_lat_lon(dist):
                name = dist.replace("⚠️ ", "").strip().upper()
                return COORDENADAS_LIMA.get(name, [None, None])

            df_mapa['coords'] = df_mapa['Distrito'].apply(get_lat_lon)
            df_mapa['lat'] = df_mapa['coords'].apply(lambda x: x[0])
            df_mapa['lon'] = df_mapa['coords'].apply(lambda x: x[1])
            df_final = df_mapa.dropna(subset=['lat'])

            # 3. DIBUJAR MAPA CON VISTA DINÁMICA
            st.pydeck_chart(pdk.Deck(
                map_style='road', # O 'mapbox://styles/mapbox/dark-v10' si tienes Token
                initial_view_state=pdk.ViewState(
                    latitude=coords_foco[0], # <--- Usa la latitud del distrito
                    longitude=coords_foco[1], # <--- Usa la longitud del distrito
                    zoom=zoom_actual,         # <--- Cambia el zoom
                    pitch=45
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        df_final,
                        get_position='[lon, lat]',
                        get_color='[255, 0, 0, 180]',
                        get_radius=150, # Radio pequeño para precisión
                        pickable=True,
                        radius_min_pixels=4,
                        radius_max_pixels=10
                    ),
                ],
                tooltip={"text": "{Titular}\nUbicación: {Distrito}"}
            ))
            st.success(f"Enfocado en: {distrito_sel}. Mostrando {len(df_final)} alertas.")
        else:
            st.warning("⚠️ Sin datos. Ve a 'Análisis por Periódico' y pulsa 'Escanear RPP'.") 

# -----------------------------
# SECCIÓN 3: ANÁLISIS POR PERIÓDICO (UNIFICADO)
# -----------------------------
elif menu == "Análisis por Periódico":
    st.title("🛡️ Monitor de Criminalidad (Lima + Callao)")
    st.markdown("Visualización de incidentes reportados por RPP, El Comercio y La República.")
    st.write("---") 

    # --- BLOQUE DE NOTICIAS Y MÉTRICAS ---
    with st.container(border=True):
        col_title, col_metrics = st.columns([2, 1])
        
        with col_title:
            st.subheader("📰 Noticias Actuales de RPP, Comercio y la República")
        
        with col_metrics:
            fecha_hoy = datetime.now().strftime("%d/%m/%Y")
            # Obtenemos la cantidad de noticias capturadas en la sesión
            n_noticias = len(st.session_state['historial_noticias'])
            st.markdown(f"<div style='text-align: right;'>📅 <b>{fecha_hoy}</b> | 🚨 Capturadas: <b>{n_noticias}</b></div>", unsafe_allow_html=True)

        with st.expander("ℹ️ Detalles de la búsqueda multifuente", expanded=False):
            st.markdown("""
            * 🔍 **Fuentes:** Escaneo activo de RPP, El Comercio y La República.
            * 📍 **Geolocalización:** Filtro automático por distritos de Lima Metropolitana.
            * ⏱️ **Actualización:** El sistema busca noticias nuevas cada vez que presionas el botón.
            """)

        # Mostrar la tabla con los datos actuales
        df_final = st.session_state['historial_noticias']
        # --- NUEVO: Gráfico de Barras ---
        if not df_final.empty:
            st.write("---")
            st.subheader("📊 Estadísticas por Distrito")
            
            # Contamos cuántas noticias hay por distrito (ignorando los No Especificados)
            df_stats = df_final[df_final['Distrito'] != "⚠️ No Especificado"]
            conteo_distritos = df_stats['Distrito'].value_counts().reset_index()
            conteo_distritos.columns = ['Distrito', 'Alertas']

            # Creamos el gráfico con Plotly
            fig = px.bar(
                conteo_distritos, 
                x='Distrito', 
                y='Alertas',
                title="Cantidad de Incidentes Reportados por Distrito",
                color='Alertas',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)

        if not df_final.empty:
            st.dataframe(
                df_final,
                column_config={
                    "Enlace": st.column_config.LinkColumn("Fuente", display_text="Leer Nota"),
                    "Distrito": st.column_config.TextColumn("Ubicación", width="medium"),
                    "Titular": st.column_config.TextColumn("Noticia", width="large"),
                    "Fuente": st.column_config.TextColumn("Periódico")
                },
                use_container_width=True,
                hide_index=True 
            )
        else:
            st.info("Sin alertas recientes capturadas. Presiona el botón para escanear.")

        # Botón de escaneo único
        if st.button("🔄 Escanear Noticias Ahora", key="scan_full"):
            st.cache_data.clear()
            # Esta función ya debe incluir la lógica para los 3 periódicos que vimos antes
            st.session_state['historial_noticias'] = escanear_inteligente()
            st.rerun()
        # Botón de Descarga ---
        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Reporte en CSV",
            data=csv,
            file_name=f'reporte_inseguridad_{fecha_hoy}.csv',
            mime='text/csv',
        )

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