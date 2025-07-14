import sys
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

if len(sys.argv) != 2:
    print("Usage: python extract_links.py <url>")
    sys.exit(1)

url = sys.argv[1]

try:

    domain = urlparse(url).netloc.replace("www.", "")
    output_file = f"{domain} Schema have been generated successfully "

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    root = ET.Element("urlset")

    for a_tag in soup.find_all("a", href=True):
        url_element = ET.SubElement(root, "url")
        ET.SubElement(url_element, "loc").text = a_tag["href"]

    ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)

    print(f"Extracted {len(root)} links to {output_file}")

except requests.exceptions.RequestException as e:
    print(f"Failed to fetch URL: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
