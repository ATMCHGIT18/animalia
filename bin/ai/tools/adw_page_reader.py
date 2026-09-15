import warnings
warnings.filterwarnings('ignore')

import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import requests


def get_adw_page(scientific_name:str):
    '''Retrieve the whole page of the ADW of the animal'''
    name = "_".join(scientific_name.split(sep=" "))
    base_url = f"https://animaldiversity.org/accounts/{name}/"

    response = requests.get(url=base_url)

    if(not response.ok):
        raise KeyError("Something went wrong")

    page = response.text
    return page


if __name__ == "__main__":
    name = input("Please enter your animal \n")
    page = get_adw_page(name)
    with open("page.html",'w') as f:
        f.write(page)