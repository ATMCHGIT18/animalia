import requests
import json
from IPython.display import Image , HTML
from IPython.display import display

def wiki_page(search_query,number_of_results):
    '''This is a tool to search and retrive data from a search_query and the 
    number_of_results. It retrieves a json files which contains some valuable 
    data from the Wikipedia page of that. It works for all the search_quesry and 
    it is good enough to retrieve the data for all kinds of the pages.'''
    endpoint = 'search/page'
    base_url = 'https://en.wikipedia.org/w/rest.php/v1/'

    headers = {'User-Agent': 'Agent Tools for grabbing data'}

    url = base_url + endpoint

    response = requests.get(url,headers=headers,params={'q':search_query,'limit':number_of_results})

    data = response.json()

    return data['pages']



# How to use this tool ------------------------------------------------------------------------------

# pages = wiki_page('solar system',3)

# for page in pages:
#   display(HTML('<a href="https://en.wikipedia.org/wiki/' + page['key'] + '">' + page['title'] + '</a>'))
#   display(HTML(page['excerpt']))
#   try:
#     thumbnail_url = 'https:' + page['thumbnail']['url']
#     display(Image(data=thumbnail_url, width=page['thumbnail']['width'], height=page['thumbnail']['height']))
#   except:
#     default_thumbnail = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/200px-Wikipedia-logo-v2.svg.png'
#     display(Image(data=default_thumbnail, width=150, height=136))




# --------------------------------------- Problems ----------------------------------------
# 1. This tools will retrieve all of the results for all topics I need to limit them into the animals only
# 2. Images are okay but they are good enough for only the searchbar not the detailed ones.
# 3. 
# 