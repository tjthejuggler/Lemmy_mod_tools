import urllib.request
import xml.etree.ElementTree as ET
import requests

def search_arxiv(search_term):
    # URL encode the search term
    encoded_search_term = urllib.parse.quote(search_term)

    # Construct the query URL
    url = f'http://export.arxiv.org/api/query?search_query=all:{encoded_search_term}&start=0&max_results=1000'

    # Fetch the data from arXiv API
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')

    # Parse the XML response
    root = ET.fromstring(data)
    pdf_urls = []
    
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
            if link.get('title') == 'pdf':
                pdf_urls.append(link.get('href'))

    return pdf_urls


def download_papers(pdf_urls):
    for i, url in enumerate(pdf_urls):
        response = requests.get(url)
        filename = f'paper_{i}.pdf'

        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded: {filename}')

search_term = '"sperm whale"'
pdf_urls = search_arxiv(search_term)
download_papers(pdf_urls)
