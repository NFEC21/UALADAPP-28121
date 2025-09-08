from rapidfuzz import process, fuzz
import pyodbc

def connect_to_azure_sql(server, database, username, password):
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={"cdm"};"
        f"UID={"root"};"
        f"PWD={""};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(connection_string)


def fuzzy_match(queryRecord, choices, score_cutoff=0):
    scorers = [fuzz.WRatio, fuzz.QRatio, fuzz.token_set_ratio, fuzz.ratio]
    processor = lambda x: str(x).lower()
    processed_query = processor(queryRecord)
    choices_data = []

    for choice in choices:
        dict_choices = choice  # ya es un dict
        queryMatch = " ".join([str(v) for k, v in dict_choices.items() if k != "DestRecordId" and v is not None])
        choices_data.append({
            'query_match': queryMatch,
            'dest_record_id': dict_choices.get('DestRecordId'),
            'match_record_values': {k: v for k, v in dict_choices.items() if k != "DestRecordId"}
        })

    best_match = {
        'match_query': queryRecord,
        'match_result': None,
        'score': 0,
        'match_result_values': {}
    }

    for scorer in scorers:
        result = process.extractOne(
            query=processed_query,
            choices=[item['query_match'] for item in choices_data],
            scorer=scorer,
            score_cutoff=score_cutoff,
            processor=processor
        )

        if result:
            match_value, score, index = result
            if score >= best_match['score']:
                matched_item = choices_data[index]
                best_match = {
                    'match_query': queryRecord,
                    'match_result': match_value,
                    'score': score,
                    'match_result_values': matched_item['match_record_values']
                }

    return best_match


def execute_dynamic_matching(params_dict, score_cutoff=0):
    conn = connect_to_azure_sql(
        server=params_dict.get("server", ""),
        database=params_dict.get("database", ""),
        username=params_dict.get("username", ""),
        password=params_dict.get("password", "")
    )
    cursor = conn.cursor()

    if 'src_dest_mappings' not in params_dict or not params_dict['src_dest_mappings']:
        raise ValueError("Debe proporcionar src_dest_mappings con columnas origen y destino")

    src_cols = ", ".join(params_dict['src_dest_mappings'].keys())
    dest_cols = ", ".join(params_dict['src_dest_mappings'].values())

    sql_source = f"SELECT {src_cols} FROM {params_dict['sourceSchema']}.{params_dict['sourceTable']}"
    sql_dest   = f"SELECT {dest_cols} FROM {params_dict['destSchema']}.{params_dict['destTable']}"

    # Extraer datos de origen
    cursor.execute(sql_source)
    src_rows = cursor.fetchall()
    src_columns = [col[0] for col in cursor.description]
    source_data = [dict(zip(src_columns, row)) for row in src_rows]

    # Extraer datos de destino
    cursor.execute(sql_dest)
    dest_rows = cursor.fetchall()
    dest_columns = [col[0] for col in cursor.description]
    dest_data = [dict(zip(dest_columns, row)) for row in dest_rows]

    conn.close()

    matching_records = []

    for record in source_data:
        dict_query_records = {}
        query = " ".join([str(record.get(src_col)) for src_col in params_dict['src_dest_mappings'].keys() if record.get(src_col) is not None])
        dict_query_records.update(record)

        fm = fuzzy_match(query, dest_data, score_cutoff)
        dict_query_records.update(fm)
        dict_query_records.update({
            'destTable': params_dict['destTable'],
            'sourceTable': params_dict['sourceTable']
        })
        matching_records.append(dict_query_records)

    return matching_records


# Ejemplo de uso
params_dict = {
    "server": "tu_server",
    "database": "tu_database",
    "username": "tu_usuario",
    "password": "tu_contraseña",
    "sourceSchema": "dbo",
    "sourceTable": "tabla_origen",
    "destSchema": "dbo",
    "destTable": "tabla_destino",
    "src_dest_mappings": {
        "nombre": "first_name",
        "Ciudad": "City"
    }
}

if __name__ == "__main__":
    resultados = execute_dynamic_matching(params_dict, score_cutoff=80)
    for r in resultados:
        print(r)
