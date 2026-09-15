import warnings
warnings.filterwarnings('ignore')

import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)
import requests


def gbif_taxonomy_data_grabber(name:str):
    '''Retrieving the taxonomy data of the animal from GBIF api'''
    headers = {'User-Agent': 'Agent Tools for grabbing data'}
    response  = requests.get("https://api.gbif.org/v1/species/match",params={"name":name},headers=headers)

    if (not response.ok):
        raise KeyError("Something wrong with requesting the data")
    
    data = response.json()
    
    species_response = requests.get(f"https://api.gbif.org/v1/species/{int(data['usageKey'])}",headers=headers)
    if(not species_response.ok):
        raise KeyError("Something wrong with the data gathering")

    data = species_response.json()
    
    return [data,data['key']]


def occurrences_to_geojson(results: list) -> dict:
    """
    Convert a list of raw GBIF occurrence records into a GeoJSON
    FeatureCollection of Point features.
    """
    features = []
 
    for record in results:
        lat = record.get("decimalLatitude")
        lon = record.get("decimalLongitude")
 
        if lat is None or lon is None:
            continue  # skip anything without coordinates
 
        # Grab the first image if one exists, for popups/tooltips.
        media = record.get("media", [])
        image_url = media[0]["identifier"] if media else None
 
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat],
            },
            "properties": {
                "gbifID": record.get("gbifID"),
                "scientificName": record.get("scientificName"),
                "species": record.get("species"),
                "country": record.get("country"),
                "stateProvince": record.get("stateProvince"),
                "eventDate": record.get("eventDate"),
                "recordedBy": record.get("recordedBy"),
                "basisOfRecord": record.get("basisOfRecord"),
                "coordinateUncertaintyInMeters": record.get("coordinateUncertaintyInMeters"),
                "image": image_url,
                "reference": record.get("references"),
            },
        }
 
        features.append(feature)
 
    return {"type": "FeatureCollection", "features": features}

def gbif_geo_data_grabber(usageKey:int):
    '''Get the occurence data from GBIF databases'''
    headers = {'User-Agent': 'Agent Tools for grabbing data'}
    base_url = "https://api.gbif.org"
    endpoint = f"/v1/occurrence/search?taxonKey={usageKey}&hasCoordinate=true"
    url = base_url + endpoint
    response = requests.get(headers=headers,url=url)

    if (not response.ok):
        raise KeyError("Something is wrong with the request response")

    data = response.json()
    geodata = occurrences_to_geojson(data['results'])
    return geodata



# if __name__ == "__main__":
#     name = input("please place an input\n")
#     page = get_adw_page(name)

#     with open('page.html','w') as f:
#         f.write(page)
    