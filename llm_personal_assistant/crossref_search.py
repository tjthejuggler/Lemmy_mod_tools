import requests

def search_crossref(query, rows=20):
    base_url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": rows
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None



def get_crossref_details(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
query = "sperm whale"
part_details = []
full_details = []
results = search_crossref(query)
if results:
    for item in results['message']['items']:
        part_details.append(item['DOI'])
        print(f"Title: {item['title'][0]}")
        print(f"DOI: {item['DOI']}\n")
        details = get_crossref_details(item['DOI'])

        if details:
            # Print all available data to find the download link or relevant information
            full_details.append(details)
            print(details)

with open('crossref_search_response.json', 'w') as f:
    f.write(str(full_details))

with open('crossref_search_response_part.json', 'w') as f:
    f.write(str(part_details))