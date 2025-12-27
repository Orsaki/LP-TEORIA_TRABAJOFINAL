import pandas as pd
import os
import time

# --- IMPORTACIÓN DE TUS SCRAPERS ---
# Asegúrate de que los nombres de los archivos (.py) y las funciones sean correctos
try:
    from web_scraping_el_comercio import extraer_noticias_comercio
    from webscraping_larepublica import extraer_noticias_larepublica
    from webscraping_canalN import extraer_noticias_canaln
    from webscraping_diariocorreo import extraer_noticias_correo
    # Si ya creaste el archivo de Perú21, descomenta la siguiente línea:
    from webscraping_peru21 import extraer_noticias_peru21
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Verifica que los nombres de tus archivos .py sean exactos.")


def ejecutar_scrapers():
    """Ejecuta secuencialmente todos los scripts de scraping."""
    print("\n🚀 INICIANDO PROCESO DE EXTRACCIÓN DE NOTICIAS...")

    # 1. El Comercio
    try:
        extraer_noticias_comercio()
    except Exception as e:
        print(f"⚠️ Error en El Comercio: {e}")

    # 2. La República
    try:
        extraer_noticias_larepublica()
    except Exception as e:
        print(f"⚠️ Error en La República: {e}")

    # 3. Canal N
    try:
        extraer_noticias_canaln()
    except Exception as e:
        print(f"⚠️ Error en Canal N: {e}")

    # 4. Diario Correo
    try:
        extraer_noticias_correo()
    except Exception as e:
        print(f"⚠️ Error en Diario Correo: {e}")

    # 5. Perú 21 (Opcional, si tienes el archivo)
    try:
        # Si no tienes el archivo aún, comenta esta línea
        if 'extraer_noticias_peru21' in globals():
            extraer_noticias_peru21()
    except Exception as e:
        print(f"⚠️ Error en Perú21: {e}")


def unificar_csvs():
    """Busca los CSV generados y los une en uno solo."""
    print("\n🔄 UNIFICANDO ARCHIVOS CSV...")

    # Lista de nombres exactos de los archivos que generan tus scripts
    archivos_generados = [
        "noticias_elcomercio_filtradas.csv",
        "noticias_larepublica_filtradas.csv",
        "noticias_canaln_filtradas.csv",
        "noticias_diariocorreo_filtradas.csv",
        "noticias_peru21_filtradas.csv"
    ]

    lista_dataframes = []

    for archivo in archivos_generados:
        if os.path.exists(archivo):
            try:
                # Leemos el CSV
                df = pd.read_csv(archivo)

                # Estandarizamos columnas (nos aseguramos de tener solo las necesarias)
                # Si tus CSV tienen columnas diferentes, esto evita errores al unir
                columnas_necesarias = ["Titulo", "Link", "Fuente"]

                # Verificamos que existan las columnas mínimas
                if all(col in df.columns for col in columnas_necesarias):
                    df_filtrado = df[columnas_necesarias]
                    lista_dataframes.append(df_filtrado)
                    print(f"✅ Integrado: {archivo} ({len(df)} registros)")
                else:
                    print(
                        f"⚠️ Formato incorrecto en {archivo}. Columnas encontradas: {df.columns}")

            except Exception as e:
                print(f"❌ Error leyendo {archivo}: {e}")
        else:
            print(f"⚪ No encontrado (se omitirá): {archivo}")

    # Unir todo
    if lista_dataframes:
        df_total = pd.concat(lista_dataframes, ignore_index=True)

        # Eliminamos duplicados por LINK (mismo link = misma noticia)
        cant_inicial = len(df_total)
        df_total.drop_duplicates(subset=['Link'], keep='first', inplace=True)
        duplicados = cant_inicial - len(df_total)

        # Guardamos el resultado final
        nombre_final = "dataset_unificado.csv"
        df_total.to_csv(nombre_final, index=False, encoding='utf-8')

        print(f"\n🎉 PROCESO COMPLETADO.")
        print(f"📊 Total noticias recolectadas: {len(df_total)}")
        print(f"🗑️  Duplicados eliminados: {duplicados}")
        print(f"💾 Archivo guardado como: {nombre_final}")
    else:
        print("\n❌ No se encontraron datos para unificar.")


if __name__ == "__main__":
    # Paso 1: Ejecutar los robots
    ejecutar_scrapers()

    # Paso 2: Unificar la data
    unificar_csvs()
