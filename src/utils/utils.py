import requests

# Función para obtener el JSON desde un endpoint
def get_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()