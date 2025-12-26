# 🚨 Lima Segura: Sistema de Alerta de Delitos y Zonas Peligrosas

¡Bienvenido al repositorio de **Lima Segura**! Este proyecto es una solución tecnológica enfocada en el monitoreo, análisis y geolocalización de la criminalidad en Lima Metropolitana, utilizando **Web Scraping** y **Ciencia de Datos**.

---

## 📖 Descripción del Proyecto

La inseguridad ciudadana es uno de los mayores desafíos en Lima. Este proyecto automatiza la recolección de noticias policiales de los principales medios digitales del país (RPP, El Comercio, La República) para:

1.  **Centralizar la información** en tiempo real.
2.  **Geolocalizar incidentes** mediante procesamiento de texto (NLP).
3.  **Visualizar zonas de riesgo** en un mapa interactivo para la ciudadanía.

---

## 🚀 Aplicación en Vivo

Nuestra solución está desplegada como un dashboard interactivo usando Streamlit. Puedes explorar los mapas de calor y las últimas noticias aquí:

**➡️ [Accede al dashboard de Lima Segura aquí](https://tu-link-de-streamlit-aqui.app/)**

*(Nota: Si aún no has desplegado la app, este enlace estará pendiente)*

<br>

---

## 🎥 Video Demo

Mira nuestra presentación donde explicamos cómo el algoritmo detecta noticias y genera las alertas en el mapa.

*Haz clic en la imagen para ver el video en YouTube:*

[![Video Demo de Lima Segura](https://img.youtube.com/vi/TU_VIDEO_ID/0.jpg)](https://youtube.com/watch?v=TU_VIDEO_ID)

*(Reemplaza el ID del video cuando lo subas a YouTube)*

---

## 🛠️ Tecnologías Utilizadas

Este proyecto fue construido integrando diversas herramientas de Data Science y Desarrollo Web:

* **Python 🐍:** Lenguaje principal para todo el backend y lógica.
* **Streamlit 🎈:** Framework para la creación del dashboard web interactivo.
* **BeautifulSoup & Requests 🕷️:** Para el Web Scraping automatizado de noticias.
* **Pandas 🐼:** Limpieza, estructuración y análisis de los datos extraídos.
* **Pydeck & Mapbox 🗺️:** Para la visualización geoespacial avanzada (mapas oscuros y capas de calor).
* **GitHub:** Control de versiones y colaboración.

---

## 👥 El Equipo

Proyecto desarrollado por estudiantes de **Ingeniería Estadística e Informática - UNALM**:

* **Daniel Ormeño Sakihama** - [GitHub](https://github.com/Orsaki)
* **Luis Huamayalli** - [GitHub](https://github.com/Albert-ca)
* **Pamela Lázaro** - [GitHub](https://github.com/lazaropamela)
* **Fátima Montes** - [GitHub](https://github.com/FatimaMY)

---

### 💻 Cómo ejecutar este proyecto localmente

1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/Orsaki/lima-segura.git](https://github.com/Orsaki/lima-segura.git)
    ```
2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Ejecuta la aplicación:
    ```bash
    streamlit run app_streamlit.py
    ```
