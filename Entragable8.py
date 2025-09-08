import pandas as pd

def exportar_csv(resultado, nombre_archivo="resultado.csv"):
    
    df = pd.DataFrame(resultado)  
    df.to_csv(nombre_archivo, index=False, encoding="utf-8-sig")
    print(f" Resultados exportados a {nombre_archivo}")
