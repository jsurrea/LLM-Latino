import os
import pandas as pd
import shutil

# Cargar el archivo CSV
csv_path = "./metadata.csv"
df = pd.read_csv(csv_path)
print(df)
# Ruta de la carpeta de origen y destino
source_folder = "./downloads_copy"
destination_folder = "./downloads_copy"

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)
else:
    print("Existe")

no_faculty_folder = os.path.join(destination_folder, 'Unknown')
if not os.path.exists(no_faculty_folder):
    os.makedirs(no_faculty_folder)
    print("Lo creé")
for _, row in df.iterrows():
    file_id = row['id'] + '.pdf.txt'
    faculties = row['dc.publisher.faculty']
    departments = row['dc.publisher.department']

    if pd.notna(faculties):
        faculties = eval(faculties) if isinstance(faculties, str) else []
    else:
        faculties = []

    if pd.notna(departments):
        departments = eval(departments) if isinstance(departments, str) else []
    else:
        departments = []

    if not faculties:
        source_file = os.path.join(source_folder, file_id)
        destination_file = os.path.join(no_faculty_folder, file_id)

        if os.path.exists(source_file):
            shutil.move(source_file, destination_file)
    else:
        for faculty in faculties:
            faculty_folder = os.path.join(destination_folder, faculty)
            if not os.path.exists(faculty_folder):
                os.makedirs(faculty_folder)

            if not departments:
                no_department_folder = os.path.join(faculty_folder, 'Unknown')
                if not os.path.exists(no_department_folder):
                    os.makedirs(no_department_folder)

                source_file = os.path.join(source_folder, file_id)
                destination_file = os.path.join(no_department_folder, file_id)

                if os.path.exists(source_file):
                    shutil.move(source_file, destination_file)
            else:
                for department in departments:
                    department_folder = os.path.join(faculty_folder, department)
                    if not os.path.exists(department_folder):
                        os.makedirs(department_folder)

                    source_file = os.path.join(source_folder, file_id)
                    destination_file = os.path.join(department_folder, file_id)

                    if os.path.exists(source_file):
                        shutil.move(source_file, destination_file)

print("Archivos organizados correctamente.")
