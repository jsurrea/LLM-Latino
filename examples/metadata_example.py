import pandas as pd

from src.utils.utils import get_json
from src.metadata.metadata import extract_metadata

# UUID para extraer los metadatos
uuid = '4b005e8d-5527-46a9-bbf0-61ce879432b0'

# Página de la API
page = 1

# Base URL para la API
base_url = "https://repositorio.uniandes.edu.co/server/api/discover/search/objects?scope={uuid}&configuration=default&page={page}&size=10"

# Proceso de extracción de datos
url = base_url.format(uuid=uuid, page=page)
print(f"Fetching data from: {url}")
json_data = get_json(url)

search_result = json_data['_embedded']['searchResult']
objects = search_result['_embedded']['objects']

# Extraer los metadatos
data = extract_metadata(objects)

# Crear un DataFrame y exportarlo a CSV
df = pd.DataFrame(data)
df.to_csv('repositorio_uniandes_data.csv', index=False)
print("Datos exportados a repositorio_uniandes_data.csv")