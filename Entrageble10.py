import pandas as pd
import os

def exportar_excel(resultado, nombre_archivo="resultado.xlsx", limite_filas=None):
    
    if not resultado or all(len(v) == 0 for v in resultado.values()):
        print(" No se puede exportar: el resultado está vacío.")
        return
    
    if limite_filas is not None:
        df = df.head(limite_filas)

    carpeta = os.path.dirname(nombre_archivo)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)

    df.to_excel(nombre_archivo, index=False, engine="openpyxl")
    print(f"Resultados exportados a {nombre_archivo} ({len(df)} filas)")


def exportar_csv(resultado, nombre_archivo="resultado.csv", limite_filas=None):

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
    print(f"Resultados exportados a {nombre_archivo} ({len(df)} filas)")
