import warnings
warnings.filterwarnings('ignore')

import random

import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from bin.ai.tools.animal_datastructure import *
from bin.ai.tools.GBIF_tools import gbif_taxonomy_data_grabber , gbif_geo_data_grabber
from bin.ai.tools.adw_page_reader import get_adw_page
from bin.ai.tools.wiki_tools import get_wikipedia_page
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

def generate_random_hex():
    # Generate a random integer up to 16777215 (0xFFFFFF) and convert to hex
    return f"#{random.randint(0, 0xFFFFFF):06x}"

def random_number():
    return (random.randint(30,75) / 100)

@tool("animal_data_creator",response_format='content')
def animal_data_grabber(animal_page:WikipediaPage) -> AnimalInfoResult:
    '''Searching articles in the wikipedia and the other sources that gives you the information
    on the animal that is searched'''

    animal_taxo_data , key = gbif_taxonomy_data_grabber(animal_page.scientific_name)

    geodata = gbif_geo_data_grabber(int(key))

    distr_data = []

    for i in geodata['features']:
        props = AnimalDistributionProperties(
            species=i['properties']['species'],
            fill_color=generate_random_hex(),
            fill_opacity=random_number(),
            border_color=generate_random_hex(),
            gbifID=i['properties']['gbifID'],
            scientificName=i['properties']['scientificName'],
            country=i['properties']['country'],
            stateProvince=i['properties']['stateProvince'],
            eventDate=i['properties']['eventDate'],
            recordedBy=i['properties']['recordedBy'],
            basisOfRecord=i['properties']['basisOfRecord'],
            coordinateUncertaintyInMeters=i['properties']['coordinateUncertaintyInMeters'],
            image=i['properties']['image'],
            reference=i['properties']['reference']
        )

        geometry = AnimalDistributionGeometry(
            type=i['geometry']['type'],
            coordinate=i['geometry']["coordinates"]
        )

        data = AnimalDistributionFeature(
            type="Feature",
            properties=props,
            geometry=geometry
        )

        distr_data.append(data)


    distribution = AnimalDistributionFeatureCollection(
        type="FeatureCollection",
        data=distr_data

    )


    physical = AnimalPhysical()

    conservation = AnimalConservation(
        status="EN",
        population_trend=""
    )

    ref = TaxonomyAnimalReference()

    taxonomy = AnimalTaxonomy(
        kingdom=animal_taxo_data['kingdom'],
        phylum=animal_taxo_data['phylum'],
        class_=animal_taxo_data['class'],
        order=animal_taxo_data['order'],
        family=animal_taxo_data['family'],
        genus=animal_taxo_data['genus'],
        species=animal_taxo_data['species'],
        taxonomicStatus=animal_taxo_data['taxonomicStatus'],
        reference=ref,
        subspecies=None
    )

    result = AnimalInfoResult(
        id=animal_taxo_data['scientificName'],
        scientific_name=animal_taxo_data['canonicalName'],
        common_name=animal_page.title,
        imageurl=animal_page.thumbnail.url,
        taxonomy=taxonomy,
        status=None,
        clades=None,
        synonyms=None,authority=animal_taxo_data['authorship'],
        conservation=conservation,
        physical=physical,
        habitat=[""],
        diet=[""],
        distribution=distribution,
        description=None,
        source=[AnimalSource()]
    )

    return result


@tool("adw_page_reader",response_format='content')
def adw_page_reader(scientific_name:str) -> str:
    '''This tool will retrieve the full page of the selected animal from ADW.'''
    page = get_adw_page(scientific_name=scientific_name)
    return page

@tool("wikipedia_page_reader",response_format='content')
def wikipedia_page_reader(name:str) -> str:
    '''This tool will retrieve the full page of the selected animal from Wikipedia'''
    page = get_wikipedia_page(name)
    return page

