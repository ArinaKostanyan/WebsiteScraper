
from fastapi import FastAPI
from pydantic import BaseModel
# from alembic.config import Config
# from alembic import command

from db import get_app_description, get_filtered_floorplan, get_floorplan_by_name, \
              get_floorplan_by_floorplan_and_property_name, store_in_database, \
              store_user_in_db, get_user_by_id, \
              store_floorplan_in_interested, get_interested_floorplan
from scrapper.website_scraper import PropertyWebsiteScrape

# alembic_cfg = Config("alembic.ini")
# alembic_cfg.set_main_option("script_location", "alembic")
# alembic_cfg.set_main_option("sqlalchemy.url",  "mysql+pymysql://root:IHopeIWill@localhost:3306/scrapper_project_db")
# command.upgrade(alembic_cfg, "head")

app = FastAPI()

class User(BaseModel):
  name: str

class InterestedFloorplan(BaseModel):
  user_id: int
  floorplan_name: str
  property_name: str


property_websites = [
    # "https://www.atmospheretempe.com/floor-plans/", 
    "https://clemsonlivingsc.com/the-orchard/", 
    # "https://rambleratlanta.com/floorplans/", 
    # "https://www.millenniumok.com/floor-plans/", 
    # "https://www.churchandhenley.com/floor-plans/", 
    # "https://pavilion-berry.com/rates-floorplans/", 
    # "https://mapleridgeblacksburg.com/all-floor-plans/", 
    # "https://current-latimer.com/rates-floorplans/"
]

@app.get("/")
async def root():
	return {"message": get_app_description()}

@app.post("/scrape")
def scrape_data():
  instance = PropertyWebsiteScrape(property_websites)
  # result = instance.get_result()
  result = {'property_name': 'Tempe Apartment Community', 'website': 'https://www.example.com/tempe-apartment-community', 
    'floorplan_details': [{'floorplan_name': 'Studio', 'price': None, 'number_of_bedrooms': 1, 'number_of_bathrooms': 1, 'square_feet': None}, 
                          {'floorplan_name': '1-Bed', 'price': None, 'number_of_bedrooms': 1, 'number_of_bathrooms': 1, 'square_feet': None},
                          {'floorplan_name': '2-Bed', 'price': None, 'number_of_bedrooms': 2, 'number_of_bathrooms': 2, 'square_feet': None}, 
                          {'floorplan_name': '3-Bed', 'price': None, 'number_of_bedrooms': 3, 'number_of_bathrooms': 2, 'square_feet': None}, 
                          {'floorplan_name': '4-Bed', 'price': None, 'number_of_bedrooms': 4, 'number_of_bathrooms': 2, 'square_feet': None}], 
            'sources': ['https://www.atmospheretempe.com/floor-plans/']}
  store_in_database(result)
  return "Scraped data successfully inserted into MYSQL!", result


@app.get("/floorplans")
def get_floorplans_by_filters(price_min:int| None = None, 
                              price_max:float | None = None, 
                              number_of_bedrooms:int | None = None, 
                              number_of_bathrooms:int | None = None, 
                              square_feet_min:int | None = None, 
                              square_feet_max:float | None = None
                              ):
    filtered_floorplans = get_filtered_floorplan(price_min, 
                                                 price_max,
                                                 number_of_bedrooms, 
                                                 number_of_bathrooms, 
                                                 square_feet_min, 
                                                 square_feet_max)
    return {"Filtered rows: ": filtered_floorplans}

@app.get("/floorplans/{property_name}")
def get_property(property_name: str):
  floorplan_by_name = get_floorplan_by_name(property_name) 
  return {"Floorplan found with the given property name": floorplan_by_name}

@app.get("/floorplans/{property_name}/{floorplan_name}")
def get_property(property_name: str, floorplan_name: str):
  floorplan_by_name_and_property = get_floorplan_by_floorplan_and_property_name(property_name, floorplan_name) 
  return f"{floorplan_by_name_and_property} found with the given names"

@app.post("/users")
def add_user(user: User):
  store_user_in_db(user)
  return f"{user} user inserted into MySQL!"

@app.get("/users/{user_id}")
def get_user(user_id: int):
  user = get_user_by_id(user_id)
  return {"user found with the given ID": user}

@app.post("/interested")
def add_floorplan_interested(interested_floorplan: InterestedFloorplan):
  res = store_floorplan_in_interested(interested_floorplan)
  return f"{interested_floorplan} interested floorplan successfully inserted into MySQL!"

@app.get("/interested/{user_id}")
def get_interested_by_user_id(user_id: int):
  interested_floorplan = get_interested_floorplan(user_id)
  return {"Interested floorplans found with the given user ID": interested_floorplan}

@app.delete("/interested")
def delete_interested_by_user_id():
  pass