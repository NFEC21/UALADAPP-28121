import pandas as pd
params_dict = {
    "server": "tu_server",
    "database": "tu_database",
    "username": "tu_usuario",
    "password": "tu_contraseña",
    "sourceSchema": "dbo",
    "sourceTable": "tabla_origen",
    "destSchema": "dbo",
    "destTable": "tabla_destino",
    "src_dest_mappings": 
        "nombre": "first_name",
        "Ciudad": "City"}
df_resultado = pd.DataFrame(params_dict)
print(df_resultado)
