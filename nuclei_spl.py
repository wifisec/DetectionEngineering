"""
Author: Adair John Collins
Date: 2024-12-01
Description: This script downloads Nuclei templates, parses HTTP request information, and converts it into Splunk SPL queries.
"""

import os
import json
import requests
import re
import logging
import argparse
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_nuclei_templates(url: str, output_dir: str) -> str:
    """
    Downloads Nuclei templates from a given URL and saves them to the specified directory.

    Args:
    url (str): URL of the Nuclei templates.
    output_dir (str): Directory where the templates will be saved.

    Returns:
    str: Path to the saved templates file.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to download Nuclei templates: {e}")
        raise

    output_file = os.path.join(output_dir, 'nuclei-templates.zip')
    with open(output_file, 'wb') as file:
        file.write(response.content)

    logging.info(f"Nuclei templates downloaded to {output_file}")
    return output_file

def extract_http_info(template: Dict) -> Dict:
    """
    Extracts HTTP request information from a Nuclei template.

    Args:
    template (Dict): Nuclei template data.

    Returns:
    Dict: Extracted HTTP request information.
    """
    http_info = {}
    http_template = template.get('requests', [{}])[0].get('raw', '')

    if http_template:
        matches = re.findall(r'(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)\s+(\S+)', http_template[0])
        if matches:
            http_info['method'], http_info['url'] = matches[0]

        headers = template.get('requests', [{}])[0].get('headers', {})
        http_info['headers'] = headers

    return http_info

def convert_to_splunk_spl(http_info: Dict) -> str:
    """
    Converts HTTP request information into a Splunk SPL query.

    Args:
    http_info (Dict): Extracted HTTP request information.

    Returns:
    str: Generated Splunk SPL query.
    """
    method = http_info.get('method', '')
    url = http_info.get('url', '')
    headers = http_info.get('headers', {})

    spl_query = f"search index=web sourcetype=access_combined method={method} uri={url}"
    if headers:
        spl_query += " | fields " + ', '.join(headers.keys())

    return spl_query

def main():
    """
    Main function to download, parse, and convert Nuclei templates to Splunk SPL queries.
    """
    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description='Download, parse, and convert Nuclei templates to Splunk SPL queries.')
    parser.add_argument('--url', type=str, default="https://github.com/projectdiscovery/nuclei-templates/archive/master.zip",
                        help='URL of the Nuclei templates. Default: "https://github.com/projectdiscovery/nuclei-templates/archive/master.zip"')
    parser.add_argument('--output_dir', type=str, required=True,
                        help='Directory where the templates will be saved')
    parser.add_argument('--template_file', type=str, required=True,
                        help='Path to the Nuclei template file to be parsed and converted')

    args = parser.parse_args()

    try:
        templates_file = download_nuclei_templates(args.url, args.output_dir)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return

    # Assume templates are extracted here and loaded
    with open(args.template_file, 'r') as file:
        template_data = json.load(file)

    http_info = extract_http_info(template_data)
    if http_info:
        spl_query = convert_to_splunk_spl(http_info)
        logging.info(f"Generated Splunk SPL query: {spl_query}")
    else:
        logging.warning("No HTTP information found in the template.")

if __name__ == "__main__":
    main()
