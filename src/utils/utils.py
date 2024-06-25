import pandas as pd
import requests
import os

# Función para obtener el JSON desde un endpoint
def get_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def count_words(csv_file="src/downloads/repositorio_uniandes_data.csv", txt_directory="src/downloads"):
    # Leer el archivo CSV
    df = pd.read_csv(csv_file)

    # Inicializar una lista para almacenar los resultados
    results = []

    # Iterar sobre cada fila del dataframe
    for index, row in df.iterrows():
        file_name = row['file_name']
        id_value = row['id']
        if file_name!=file_name:continue
        # Construir la ruta completa al archivo txt
        txt_path = os.path.join(txt_directory, file_name)
        
        # Contar las palabras en el archivo txt
        with open(txt_path, 'r', encoding='utf-8') as file:
            content = file.read()
            words_count = len(content.split())
        
        # Agregar resultados a la lista
        results.append({'id': id_value, 'words': words_count})

    # Crear un nuevo dataframe con los resultados
    result_df = pd.DataFrame(results)

    # Exportar el dataframe a un archivo CSV
    result_df.to_csv('src/downloads/words_for_id.csv', index=False)