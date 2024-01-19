import urllib.request



# Define the search term
search_term = '"sperm whale"'

# URL encode the search term
encoded_search_term = urllib.parse.quote(search_term)

# Define the date range for the year 2000
#date_range = "[200001010000+TO+200012312359]"

# Construct the query URL with the date range
url = f'http://export.arxiv.org/api/query?search_query=all:{encoded_search_term}&start=0&max_results=1000'

# Fetch the data from arXiv API
data = urllib.request.urlopen(url)
response = data.read().decode('utf-8')

#save the response to file
with open('arxiv_search_response.xml', 'w') as f:
    f.write(response)

# Print the response
print(response)


#TODO THIS NEEDS TO BE TURNED INTO A SEARCH FUNCTION AND A DOWNLOAD FUNCTION

