from faker import Faker
import random
from glob import glob

fake = Faker()

def add_synthetic_data_to_file(filename, min_data, max_data):
    # Generar una cantidad aleatoria de datos sintéticos dentro del rango dado para cada categoría
    synthetic_data = []
    categories = [
        lambda: fake.email(),
        lambda: fake.phone_number(),
        lambda: fake.name(),
        lambda: fake.credit_card_number(card_type=None),
        lambda: fake.address(),
        lambda: fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
        lambda: fake.company(),
        lambda: fake.ssn(),
        lambda: str(fake.unique.random_int(min=1000000000, max=9999999999)),
        lambda: str(fake.unique.random_int(min=100000, max=999999))
    ]

    for category in categories:
        for _ in range(random.randint(min_data, max_data)):
            synthetic_data.append(category())

    # Mezclar todos los datos sintéticos para insertarlos aleatoriamente
    random.shuffle(synthetic_data)

    # Leer el contenido original del archivo
    with open(filename, "r") as file:
        content = file.readlines()

    # Datos y posiciones para guardar en el registro
    data_log = []

    # Determinar posiciones aleatorias para insertar los datos
    positions = sorted([random.randint(0, len(content) + i) for i in range(len(synthetic_data))])

    # Agregar datos sintéticos en posiciones aleatorias dentro del contenido
    for item, pos in zip(synthetic_data, positions):
        content.insert(pos, f"{item}\n")
        data_log.append(f"Position: {pos}, Data: {item}\n")

    # Guardar el contenido modificado de nuevo en el archivo
    with open(filename, "w") as file:
        file.writelines(content)

    # Guardar el registro de datos en un archivo externo
    with open(f"data_log_{filename}.txt", "w") as log_file:
        log_file.writelines(data_log)
# Uso de la función

for file in glob("*.pdf.txt"):
    add_synthetic_data_to_file(file, 3, 10)  
