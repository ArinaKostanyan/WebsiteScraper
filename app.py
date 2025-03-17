
from fastapi import FastAPI, Depends
from db import get_db
from models import FloorPlan
from scrapper.website_scraper import PropertyWebsiteScrape
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

app = FastAPI()

property_websites = [
    "https://www.atmospheretempe.com/floor-plans/", 
    # "https://clemsonlivingsc.com/the-orchard/", 
    # "https://rambleratlanta.com/floorplans/", 
    # "https://www.millenniumok.com/floor-plans/", 
    # "https://www.churchandhenley.com/floor-plans/", 
    # "https://pavilion-berry.com/rates-floorplans/", 
    # "https://mapleridgeblacksburg.com/all-floor-plans/", 
    # "https://current-latimer.com/rates-floorplans/"
]

def get_app_description():
	return (
    	"Welcome to the floorplan data scraper API!"
    	"""This API allows to retrieve floorplan data based on filters, also manages user interested lists,
        and handles user data."""
        
    	"Use the '/floorplans' endpoint with a GET request to see Floorplans."
        "Use the '/floorplans/{property_name}' to GET Property's Floorplans by Name"
        "Use the '/floorplans/{property_name}/{floorplan_name}' GET Floorplan by Name & Property Name"
)

@app.get("/")
async def root():
	return {"message": get_app_description()}

@app.post("/scrape/")
def scrape_data(db: Session = Depends(get_db)):
  instance = PropertyWebsiteScrape(property_websites)
  result = instance.get_result()
#   store_in_database(db, result)
  return {"message": "Scraping complete"}


@app.get("/floorplans/")
def get_floorplans_by_filters(price_min:int = 0, 
                              price_max:float = float('inf'), 
                              number_of_bedrooms:int = 0, 
                              number_of_bathrooms:int = 0, 
                              square_feet_min:int = 0, 
                              square_feet_max:float = float('inf'),
                              db: Session = Depends(get_db)):
    filter_condition = FloorPlan.price >= price_min and FloorPlan.price<=price_max and \
                        FloorPlan.square_feet >= square_feet_min and FloorPlan.square_feet <= square_feet_max 
    if number_of_bathrooms:
        filter_condition += FloorPlan.bathrooms == number_of_bathrooms
    if number_of_bedrooms:
        filter_condition += FloorPlan.bedrooms == number_of_bedrooms
        
    result = db.query(FloorPlan).filter(filter_condition) #.delete(synchronize_session=False)
    print("Rows deleted:", result)