import mimetypes
from typing import List
from typing import Optional

import google.cloud.dlp


dlp = google.cloud.dlp_v2.DlpServiceClient() # Instantiate a client.


##############
# Pipeline arguments
# TODO (Developer): Set the following variables before running the sample.

# The Google Cloud project id to use as a parent resource.
project = "unischedule-5ee93" 

# A list of strings representing info types to look for.
# Documentation: https://cloud.google.com/sensitive-data-protection/docs/infotypes-reference
selected_info_types = ["CREDIT_CARD_NUMBER", "EMAIL_ADDRESS", "GENERIC_ID", "PASSPORT", "PHONE_NUMBER", "LAST_NAME", "COLOMBIA_CDC_NUMBER"]

# List of files to inspect
files = ["3a64a4e9-57de-493b-aa20-a8d6191570f0.pdf.txt"]

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
        raise ValueError("No findings.")

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

# Pipeline
# TODO (Developer): Implement the pipeline logic here.

for file in files:
    # Read the file
    with open(file, "r") as file:
        data = file.read()

    # Inspect the string
    findings, findings_truncated = inspect_string(data)

    # Print the findings
    print_findings(findings)

    # Remove the findings from the original string
    modified_string = remove_infotypes_from_string(data, findings)

    # Print the modified string
    print(modified_string)
