import warnings
warnings.filterwarnings('ignore')

import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from typing import List,Literal,Optional
from pydantic import BaseModel,Field


class TaxonomyAnimalReference(BaseModel):
    itis_id: str | None = Field(default=None,description="The ID from the Integrated Taxonomic Information System.")
    ncbi_taxon_id: str | None = Field(default=None,description="The ID used by the National Center for Biotechnology Information.")
    iucn_status: str | None = Field(default=None,description="The conservation status, which Wikipedia always includes in animal sidebars (e.g., \"Vulnerable\").")

# Follows the ICZN coding of the taxonomy
class AnimalTaxonomy(BaseModel):
    kingdom: str = Field(description="which kingdom they this animal is in mostly is 'animalia' for animals")
    phylum: str = Field(description="The primary broad division of the animal kingdom (e.g., 'Chordata').")
    class_: str = Field(description="The structural group the animal belongs to (e.g., 'Mammalia').")
    order: str = Field(description="The broad grouping of related families (e.g., \"Carnivora\").")
    family: str = Field(description="A collection of closely related genera (e.g., \"Felidae\").")
    genus: str = Field(description="The first part of the scientific name, grouping closely related species (e.g., \"Panthera\").")
    species: str = Field(description="he specific epithet identifying the individual organism (e.g., \"leo\").")
    subspecies: str | None = Field(default=None,description="(Optional) A sub-category for geographic or physical variants (e.g., 'leo' for the Northern lion).")
    taxonomicStatus: str | None = Field(default=None,description="Whether this taxonomy is accepted or not or something else.")
    reference: TaxonomyAnimalReference = Field(description="include the links to the major global databases for standard verifications")

# Bsed on the IUNC Red list Codes
class AnimalConservation(BaseModel):
    status: Literal['EX','EW','CR','EN','VU','NT','LC','DD','NE'] = Field(description="Status of the animal conservation in the wild the codes are translated by IUNC Red List codes which is " \
    "EX : Extinct: No remaining individuals. EW: Extinct in the Wild: Survives only in captivity or cultivation. CR: Critically Endangered: Facing an extremely high risk of extinction. EN: Endangered: Facing a very high risk of extinction. VU: Vulnerable: Facing a high risk of extinction. NT: Near Threatened: Close to qualifying for a threatened category. LC: Least Concern: Lowest risk; widespread and abundant. DD: Data Deficient: Not enough information to assess risk. NE: Not Evaluated: Has not yet been studied against the criteria.")
    population_trend: str = Field(description="The trend of the population if it is increasing, decreasing or stable")

class Measurement(BaseModel):
    value: Optional[float] = Field(
        default=None,
        description="Measured or reported value"
    )
    min_value: Optional[float] = Field(
        default=None,
        description="Minimum value when the source reports a range"
    )
    max_value: Optional[float] = Field(
        default=None,
        description="Maximum value when the source reports a range"
    )
    unit: str = Field(
        description="Unit of measurement, e.g. kg, cm, m"
    )
    sex: Optional[str] = Field(
        default=None,
        description="Sex associated with the measurement: male, female, or both"
    )
    measurement_type: str = Field(
        description="Type of measurement, e.g. weight, height, body_length"
    )
    is_average: bool = Field(
        default=False,
        description="Whether the value represents an average"
    )
    is_maximum: bool = Field(
        default=False,
        description="Whether the value represents a reported maximum"
    )
    approximate: bool = Field(
        default=False,
        description="Whether the measurement is approximate"
    )
    source: Optional[str] = Field(
        default=None,
        description="Source of the measurement"
    )
    source_reference: Optional[str] = Field(
        default=None,
        description="URL, DOI, citation, or other source reference"
    )
    original_text: Optional[str] = Field(
        default=None,
        description="Original wording from the source"
    )


class AnimalPhysical(BaseModel):
    male_weight: Optional[Measurement] = None
    female_weight: Optional[Measurement] = None
    max_weight: Optional[Measurement] = None

    male_height: Optional[Measurement] = None
    female_height: Optional[Measurement] = None
    max_height: Optional[Measurement] = None

    male_length: Optional[Measurement] = None
    female_length: Optional[Measurement] = None
    max_length: Optional[Measurement] = None

    additional_measurements: List[Measurement] = Field(
        default_factory=list,
        description="Other physical measurements such as limb length, wingspan, tail length, etc."
    )

    
class AnimalDistributionGeometry(BaseModel):
    type_:str = Field(alias="type",description="the type of the geometry , is it point , polygon,multipolygon, or circle")
    coordinate: List[float] = Field(description="List of the coordinates of the borders of the shape of the habitat of the animal which inlcudes of List of latitude and longitude of the vertices of the shape that shape the habitat on the earth")


class AnimalDistributionProperties(BaseModel):
    species: str = Field(description="Scientific name of the animal")
    fill_color: str = Field(description="The fill color in the format of '#D97706")
    fill_opacity: float = Field(description="the fill opacity of the fill color on the earth it should be around 0.5 ")
    border_color: str = Field(description="The border color of the shape in the format '#D97706")
    gbifID: str = Field(description="the ID of the animal in the GBIF database ( the id that used to retrieve the data from GBIF)")
    scientificName: str = Field(description="Scientifc name of the animal")
    country: str = Field(description="Country of the observation")
    stateProvince: str = Field(description="Province or state of the observaiton within the country of the observation")
    eventDate: str = Field(description="The date of the observation")
    recordedBy: str = Field(description="Recorded by who")
    basisOfRecord: str = Field(description="The basis of the record if it is recorded by human or not")
    coordinateUncertaintyInMeters: float = Field( description="The uncertainty of the coordinates of the observation")
    image: str = Field(description="URL of the image that retrieved from GBIF database ( it is already in the data that is retrieved)")
    reference: str = Field(description="Reference URL")
    

class AnimalDistributionFeature(BaseModel):
    type_: str = Field(alias="type",description="Always Feature", default="Feature")
    properties:AnimalDistributionProperties = Field(description="The properties of the animal distribution feature for feed into the maplibre-gl geojson")
    geometry: AnimalDistributionGeometry = Field(description="The geometry data of the animal range")

class AnimalDistributionFeatureCollection(BaseModel):
    type_: str = Field(alias="type",default="FeatureCollection")
    data: List[AnimalDistributionFeature] = Field(description="some animals have a wide range which cannot be described by one geometry so this is the list of those")

class AnimalInfoResult(BaseModel):
    id: str = Field(description="id of the animal which is the lowercase of the name without any space between")
    common_name: str = Field(description="The common name of the animal that every one is using in english")
    scientific_name: str = Field(description="Scientific name of the animal")
    imageurl: str = Field(description="The image url of the animal")
    taxonomy: AnimalTaxonomy = Field(description="The taxonomy of the animal ")
    status: str | None = Field(default=None,description="Status of the animal.")
    clades: str | None = Field(default=None,description="An array of unranked evolutionary branches that sit between the major ranks (e.g., [\"Tetrapoda\", \"Amniota\"]).")
    synonyms: str | None = Field(default=None,description="An array of invalid or historic scientific names previously used for the animal (e.g., [\"Felis leo\"]).")
    authority: str | None = Field(default=None,description="The name of the scientist who first described the species and the year it was published (e.g., \"Linnaeus, 1758\").")
    conservation: AnimalConservation = Field(description="The conservation status of the animal in the wild life")
    physical: AnimalPhysical = Field(description="The physical traits and data of the animal")
    habitat: List[str] = Field(description="List of habitats of the animal , remember this is not a reference to a country but the place or characteristics of the habitat like forest, savana, etc")
    diet: List[str] = Field(description="List of the diets of the animal")
    distribution: AnimalDistributionFeatureCollection = Field(description="distribution data of the animal in the globe and where we can find it")
    description: str | None = Field(default=None,description="The description of the animal")

class WikipediaThumbnailPage(BaseModel):
    mimetype:str = Field(description="Thumbnail media type")
    size:int | None = Field(description="File size in bytes or null if not available",default=None)
    width:int | None = Field(description=" Maximum recommended image width in pixels or null if not available",default=None)
    height:int | None = Field(description="Maximum recommended image height in pixels or null if not available",default=None)
    duration:int | None = Field(description="Length of the video, audio, or multimedia file or null for other media types",default=None)
    url:str = Field(description="URL to download the file")

class WikipediaPage(BaseModel):
    id:int = Field(description="Page identifier which is integer number")
    key:str =Field(description="Page title in URL-friendly format")
    title:str = Field(description="The exact title of the wikipedia page")
    excerpt:str | None = Field(default=None,description="A few lines giving a sample of page content with search terms highlighted with <span class=\"searchmatch\"> tags. Excerpts may end mid-sentence")
    matched_title:str | None = Field(default=None,description="Title of the page redirected from, if the search term originally matched a redirect page or null if search term did not match a redirect page")
    anchor:str | None = Field(description="Just put the anchor there if it is inside this key unless it is null",default=None)
    description:str | None = Field(description="Short summary of the page topic based on the corresponding entry on Wikidata or null if no entry exists.",default=None)
    thumbnail:WikipediaThumbnailPage | None = Field(description="Reduced-size version of the page's lead image or null if no lead imagine exists",default=None)
    scientific_name: str | None = Field(description="The scientific name of the animal",default=None)

class WikiSearchResult(BaseModel):
    query:str = Field(description="The original search result")
    results: List[WikipediaPage] = Field(description="A list of  matching Wikipedia pages")
