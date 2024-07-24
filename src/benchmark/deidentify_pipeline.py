import mimetypes
from typing import List
from faker import Faker
from typing import Optional
from collections import defaultdict

import random
import google.cloud.dlp

import re


dlp = google.cloud.dlp_v2.DlpServiceClient() # Instantiate a client.

fake = Faker()

##############
# Pipeline arguments
# TODO (Developer): Set the following variables before running the sample.

# The Google Cloud project id to use as a parent resource.
project = "unischedule-5ee93" 

# A list of strings representing info types to look for.
# Documentation: https://cloud.google.com/sensitive-data-protection/docs/infotypes-reference
selected_info_types = ["CREDIT_CARD_NUMBER", "EMAIL_ADDRESS", "GENERIC_ID", "PHONE_NUMBER", "LAST_NAME", "COLOMBIA_CDC_NUMBER", "STREET_ADDRESS"]

# List of files to inspect
files = [
    "3a64a4e9-57de-493b-aa20-a8d6191570f0.pdf.txt",
    "2ec9c48c-367f-49ba-a8ff-d4709f89b91f.pdf.txt",
    "d1290624-c70b-42b3-89cf-36ed5f1b7050.pdf.txt",
    "d548c4f6-e4a6-4c57-8cdf-4fd7b5365ef3.pdf.txt",
    "be8fba27-b571-493b-baae-1047c438d0e9.pdf.txt",
    "24320d7a-ac51-44b1-845c-adedbc01e79f.pdf.txt",
    "4201bfda-7b3b-440f-89f5-2c1e1f7b636c.pdf.txt",
    "30af61d4-d355-40ac-b31c-067ae46d9efb.pdf.txt",
    "18d1b751-e07e-4289-a90a-fc611c9e547d.pdf.txt",
    "7dadb516-f4dc-4d6e-829d-47297acd8ba4.pdf.txt"
]


##############

def inspect_string(
    string: str,
    min_likelihood: str = None,
    max_findings: Optional[int] = None,
    include_quote: bool = True,
) -> None:
    """Uses the Data Loss Prevention API to analyze a string for protected data.
    API documentation: https://cloud.google.com/sensitive-data-protection/docs/reference/rest/v2/projects.content/inspect
    Args:
        string: The string to inspect.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        include_quote: Boolean for whether to display a quote of the detected
            information in the results.
    Returns:
        findings: A list of dictionaries containing the findings.
        findings_truncated: A boolean indicating whether the findings were truncated.
    """

    # Prepare info_types by converting the list of strings into a list of dictionaries
    info_types = [{"name": info_type} for info_type in selected_info_types]

    # Prepare the configuration dictionary
    inspect_config = {
        "info_types": info_types,
        "min_likelihood": min_likelihood,
        "include_quote": include_quote,
        "limits": {"max_findings_per_request": max_findings},
        "custom_info_types": [
            {
                "info_type": {
                    "name": "COLOMBIA_CDC_NUMBER",
                },
                "regex": {
                    "pattern": r"\b\d{1,3}(\.\d{3}){0,2}|\d{6,10}\b"
                },
            }
        ],
    }

    # Construct the item, containing the string to inspect
    item = {"value": string}

    # Convert the project id into a full resource id.
    parent = f"projects/{project}"

    # Call the API.
    response = dlp.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
    )

    if not response.result.findings:
        #raise ValueError("No findings.")
        return [], False

    return response.result.findings, response.result.findings_truncated

def print_findings(findings: List[google.cloud.dlp_v2.types.Finding]) -> None:
    """Prints the results from the API in human-readable format."""
    for finding in findings:
        try:
            print(f"Quote: {finding.quote}")
        except AttributeError:
            pass
        print(f"Info type: {finding.info_type.name}")
        print(f"Likelihood: {finding.likelihood}")
        print()

def remove_infotypes_from_string(original_string: str, findings: List[google.cloud.dlp_v2.types.Finding]) -> str:
    """Removes the detected info types from the original string.
    Args:
        original_string: The original string.
        findings: The findings from the API.
    Returns:
        The modified string with the info types removed.
    """
    # Iterate over the findings and remove them from the original string.
    # We could also use finding.location to remove based on byte offsets.
    modified_string = original_string
    for finding in findings:
        modified_string = modified_string.replace(finding.quote, f"<{finding.info_type.name}>")
    return modified_string


def add_synthetic_data_to_file(filename, min_data, max_data):
    # Generar una cantidad aleatoria de datos sintéticos dentro del rango dado para cada categoría
    synthetic_data = []
    categories = [
        lambda: fake.email(),
        lambda: fake.phone_number(),
        lambda: fake.name(),
        lambda: fake.credit_card_number(card_type=None),
        lambda: fake.address().replace("\n", " "),
        lambda: str(fake.random_int(min=1, max=9))+"."+str(fake.random_int(min=100, max=999))+"."+str(fake.random_int(min=100, max=999))+"."+str(fake.random_int(min=100, max=999)),
    ]

    categories_names = ["EMAIL_ADDRESS", "PHONE_NUMBER", "LAST_NAME", "CREDIT_CARD_NUMBER", "STREET_ADDRESS", "COLOMBIA_CDC_NUMBER"]

    dict_categories = {}
    for category in range(len(categories)):
        for _ in range(random.randint(min_data, max_data)):
            data = categories[category]()
            synthetic_data.append(data)
            dict_categories[data] = categories_names[category]

    # Mezclar todos los datos sintéticos para insertarlos aleatoriamente
    random.shuffle(synthetic_data)

    # Leer el contenido original del archivo
    with open(filename, "r", encoding='utf-8') as file:
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
    with open(filename, "w", encoding='utf-8') as file:
        file.writelines(content)

    # Guardar el registro de datos en un archivo externo
    with open("data_log.txt", "w", encoding='utf-8') as log_file:
        log_file.writelines(data_log)

    return dict_categories

# Pipeline
# TODO (Developer): Implement the pipeline logic here.

# def censor_cedulas(text):
#     regex = r'\b(\d{1,3}(\.\d{3}){0,2}|\d{6,10})\b'
#     censored_text = re.sub(regex, lambda x: re.sub(r'\d', '*', x.group()), text)
#     return censored_text

def split_into_chunks(text, chunk_size=1000):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]


total_by_type = defaultdict(int)
true_positives_by_type = defaultdict(int)
false_positives_by_type = defaultdict(int)
false_negatives_by_type = defaultdict(int)
number_of_chunks = 0

for file in files:
    # Read the file
    with open(file, "r", encoding='utf-8') as file:
        data = file.read()

    # Inspect the string
    findings, findings_truncated = inspect_string(data, max_findings=0)
    if len(findings) != 0:
    # Print the findings
    #print_findings(findings)

    # Remove the findings from the original string
        modified_string = remove_infotypes_from_string(data, findings)
    else:
        modified_string = data
    # Split the modified string into chunks
    chunks = split_into_chunks(modified_string)
    #print(f"Number of chunks: {len(chunks)}")
    number_of_chunks += len(chunks)

    for chunk in chunks:
        
        temp_filename = "temp_modified_file.txt"
        with open(temp_filename, "w", encoding='utf-8') as temp_file:
            temp_file.write(modified_string)

        dict_categories = add_synthetic_data_to_file(temp_filename, 1, 3)
        for category in dict_categories.values():
            total_by_type[category] += 1

        with open(temp_filename, "r", encoding='utf-8') as file:
            synthetic_data = file.read()

        with open("data_log.txt", "r", encoding='utf-8') as file:
            data_log = file.read()
        data_log = data_log.split("\n")

        synthetic_findings, synthetic_findings_truncated = inspect_string(synthetic_data)
        finding_strings = {finding.quote:finding.info_type.name for finding in synthetic_findings}
        real_strings = [i.split("Data: ")[1] for i in data_log if i != ""]
        set_of_real_strings = set(real_strings)
        for finding_string in finding_strings:
            found = False  # Variable para rastrear si se encontró el finding_string
            for real_string in real_strings:
                if finding_string in real_string:
                    #print(f"Found: {finding_string} in {real_string}")
                    found = True  # Se encontró el finding_string
                    try:
                        set_of_real_strings.remove(real_string)
                        true_positives_by_type[dict_categories[real_string]] += 1
                    except:
                        pass
                    break
            if not found:  # Si no se encontró el finding_string en ningún real_string
                #print(f"Did not find: {finding_string}")
                false_positives_by_type[finding_strings[finding_string]] += 1
        for real_string in set_of_real_strings:
            #print(f"Did not find: {real_string}")
            false_negatives_by_type[dict_categories[real_string]] += 1
        
    # print("-" * 50)
    # print(f"File: {file}")
    # print(f"Number of chunks: {number_of_chunks}")
    # print(f"Total by type: {total_by_type}")
    # print(f"True positives by type: {true_positives_by_type}")
    # print(f"False positives by type: {false_positives_by_type}")
    # print(f"False negatives by type: {false_negatives_by_type}")
    # # Print the modified string
    #print(modified_string)

print("-" * 50)
print("Summary:")
print(f"Number of chunks: {number_of_chunks}")
print(f"Total by type: {total_by_type}")
print(f"True positives by type: {true_positives_by_type}")
print(f"False positives by type: {false_positives_by_type}")
print(f"False negatives by type: {false_negatives_by_type}")