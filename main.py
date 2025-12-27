import pandas as pd
import os
import time

try:
    print("🔄 Importando scrapers...")
    from web_scraping_el_comercio import extraer_noticias_comercio
    from webscraping_larepublica import extraer_noticias_larepublica
    from webscraping_canalN import extraer_noticias_canaln
    from webscraping_diariocorreo import extraer_noticias_correo
    from webscraping_peru21 import extraer_noticias_peru21
    from webscraping_rpp import extraer_noticias_html as extraer_noticias_rpp
    from webscraping_infobaePE import extraer_noticias_infobae

    print("✅ Todos los módulos importados correctamente.\n")

except ImportError as e:
    print(f"❌ ERROR CRÍTICO: No se pudo importar algún archivo. Detalles: {e}")
    print("Verifica que todos los archivos .py estén en la misma carpeta.")
    exit()

# Función principal para ejecutar todos los scrapers


def ejecutar_scrapers():
    """Ejecuta secuencialmente todos los scripts de scraping."""

    # Lista de tuplas: (Función a ejecutar, Nombre para mostrar)
    scrapers = [
        (extraer_noticias_comercio, "El Comercio"),
        (extraer_noticias_larepublica, "La República"),
        (extraer_noticias_canaln, "Canal N"),
        (extraer_noticias_correo, "Diario Correo"),
        (extraer_noticias_peru21, "Perú 21"),
        (extraer_noticias_rpp, "RPP Noticias"),
        (extraer_noticias_infobae, "Infobae Perú")]

    print("="*50)
    print("🚀 INICIANDO EXTRACCIÓN DE NOTICIAS")
    print("="*50)

    for funcion, nombre in scrapers:
        print(f"\n▶️  Ejecutando: {nombre}...")
        try:
            start_time = time.time()
            funcion()  # Ejecuta el scraper
            elapsed = time.time() - start_time
            print(f"   ⏱️  Tiempo: {elapsed:.2f} segundos")
        except Exception as e:
            print(f"   ⚠️  Error en {nombre}: {e}")

# Unificar datos de todos los CSV generados


def unificar_datos():
    """Lee todos los CSV generados y los une en uno solo."""

    print("\n" + "="*50)
    print("🔄 UNIFICANDO ARCHIVOS CSV")
    print("="*50)

    # Lista de archivos que generan tus scripts (basado en el código de tus archivos)
    archivos_csv = [
        "noticias_elcomercio_filtradas.csv",
        "noticias_larepublica_filtradas.csv",
        "noticias_canaln_filtradas.csv",
        "noticias_diariocorreo_filtradas.csv",
        "noticias_peru21_filtradas.csv",
        "noticias_rpp_filtradas.csv",
        "noticias_infobae_filtradas.csv"]

    dataframes = []

    for archivo in archivos_csv:
        if os.path.exists(archivo):
            try:
                # Leemos el CSV
                df = pd.read_csv(archivo)

                # ESTANDARIZACIÓN DE COLUMNAS
                # RPP usa 'Categoria' en vez de 'Fuente', lo corregimos aquí:
                if 'Categoria' in df.columns:
                    df.rename(columns={'Categoria': 'Fuente'}, inplace=True)

                # Aseguramos tener solo las columnas necesarias
                cols_necesarias = ["Titulo", "Link", "Fuente"]

                # Verificamos si existen las columnas (o si el archivo está vacío/erróneo)
                if set(cols_necesarias).issubset(df.columns):
                    df_filtrado = df[cols_necesarias]
                    dataframes.append(df_filtrado)
                    print(f"✅ Integrado: {archivo} ({len(df)} registros)")
                else:
                    print(
                        f"⚠️  Formato incorrecto en {archivo} (columnas distintas).")
            except Exception as e:
                print(f"❌ Error leyendo {archivo}: {e}")
        else:
            print(f"⚪ No encontrado: {archivo}")

    # Concatenar y guardar
    if dataframes:
        df_total = pd.concat(dataframes, ignore_index=True)

        # Eliminar duplicados exactos de Links
        total_antes = len(df_total)
        df_total.drop_duplicates(subset=['Link'], keep='first', inplace=True)
        total_despues = len(df_total)

        output_file = "dataset_unificado.csv"
        df_total.to_csv(output_file, index=False, encoding='utf-8')

        print("\n" + "-"*50)
        print(f"🏆 PROCESO TERMINADO")
        print(f"📊 Total bruto: {total_antes}")
        print(f"🗑️  Duplicados eliminados: {total_antes - total_despues}")
        print(f"💾 DATASET FINAL: {output_file} ({total_despues} noticias)")
        print("-"*50)
    else:
        print("\n❌ No se generó ningún dato para unificar.")


# Ejecución
if __name__ == "__main__":
    ejecutar_scrapers()
    unificar_datos()
