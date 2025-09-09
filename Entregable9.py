import os
import pandas as pd

def exportar_excel(resultado, nombre_archivo="resultado.xlsx", limite_filas=None):
    """
    Exporta el resultado (dict) a un archivo Excel (.xlsx).
    - Crea carpeta automáticamente si no existe.
    - No exporta si el resultado está vacío.
    - Permite limitar número de filas exportadas.
    """
    if not resultado or all(len(v) == 0 for v in resultado.values()):
        print("⚠️ No se puede exportar: el resultado está vacío.")
        return

    df = pd.DataFrame(resultado)

    if limite_filas is not None:
        df = df.head(limite_filas)

    carpeta = os.path.dirname(nombre_archivo)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)

    df.to_excel(nombre_archivo, index=False, engine="openpyxl")
    print(f"✅ Resultados exportados a {nombre_archivo} ({len(df)} filas)")


def exportar_csv(resultado, nombre_archivo="resultado.csv", limite_filas=None):
    """
    Exporta el resultado (dict) a un archivo CSV.
    - Crea carpeta automáticamente si no existe.
    - No exporta si el resultado está vacío.
    - Permite limitar número de filas exportadas.
    """
    if not resultado or all(len(v) == 0 for v in resultado.values()):
        print("⚠️ No se puede exportar: el resultado está vacío.")
        return

    df = pd.DataFrame(resultado)

    if limite_filas is not None:
        df = df.head(limite_filas)


    carpeta = os.path.dirname(nombre_archivo)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)

    df.to_csv(nombre_archivo, index=False, encoding="utf-8-sig")
    print(f"✅ Resultados exportados a {nombre_archivo} ({len(df)} filas)")
