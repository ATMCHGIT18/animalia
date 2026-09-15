import requests
import json
from IPython.display import Image , HTML
from IPython.display import display
import warnings
warnings.filterwarnings('ignore')

import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

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
    try:
        data = response.json()
    except:
        data = {'pages': []}

    return data['pages']


def get_wikipedia_page(key:str):
    '''This tool will retrive the full page of the selected topic for you'''

    headers = {'User-Agent': 'Agent Tools for grabbing data'}

    page_url = 'https://en.wikipedia.org/wiki/' + key

    response = requests.get(page_url,headers=headers)
    if (not response.ok):
        raise KeyError("Something wrong with the response of the page that you requested")
    
    try:
        content = response.text
    except Exception as e:
        print(f"Error occured in reading HTML of the page : \n{e}")
        content = ""

    return content


# How to use this tool ------------------------------------------------------------------------------

# pages = wiki_page('lion',3)

# print(type(pages))
# for page in pages:
#     print(page)
#     print()

# for page in pages:
#   display(HTML('<a href="https://en.wikipedia.org/wiki/' + page['key'] + '">' + page['title'] + '</a>'))
#   display(HTML(page['excerpt']))
#   try:
#     thumbnail_url = 'https:' + page['thumbnail']['url']
#     display(Image(data=thumbnail_url, width=page['thumbnail']['width'], height=page['thumbnail']['height']))
#   except:
#     default_thumbnail = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/200px-Wikipedia-logo-v2.svg.png'
#     display(Image(data=default_thumbnail, width=150, height=136))
