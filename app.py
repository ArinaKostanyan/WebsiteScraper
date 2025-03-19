import yaml
from typing import List
from fastapi import Body, FastAPI

# from alembic.config import Config
# from alembic import command

from db import (
    get_app_description,
    get_filtered_floorplan,
    get_floorplan_by_floorplan_and_property_name,
    get_property_by_name,
    store_in_database,
    store_user_in_db,
    get_user_by_id,
    store_floorplan_in_interested,
    get_interested_floorplan_by_user_id,
    delete_floorplan_data,
)
from models.models import InterestedFloorplan, User
from scrapper.website_scraper import PropertyWebsiteScrape

# alembic_cfg = Config("alembic.ini")
# alembic_cfg.set_main_option("script_location", "alembic")
# alembic_cfg.set_main_option("sqlalchemy.url",  "mysql+pymysql://root:IHopeIWill@localhost:3306/scrapper_project_db")
# command.upgrade(alembic_cfg, "head")

fastapi_app = FastAPI(
    title="Property Management API",
    version="1.0",
    description="API for managing properties and floorplans, including interested floorplans.",
)


property_websites = [
    "https://clemsonlivingsc.com/the-orchard/",
    # "https://www.atmospheretempe.com/floor-plans/",
    # "https://rambleratlanta.com/floorplans/",
    # "https://www.millenniumok.com/floor-plans/",
    # "https://www.churchandhenley.com/floor-plans/",
    # "https://pavilion-berry.com/rates-floorplans/",
    # "https://mapleridgeblacksburg.com/all-floor-plans/",
    # "https://current-latimer.com/rates-floorplans/"
]


@fastapi_app.get("/", tags=["Root"])
def root():
    return {"message": get_app_description()}


@fastapi_app.post("/scrape", tags=["Scrape websites"])
def scrape_data():
    instance = PropertyWebsiteScrape(property_websites)
    result = instance.get_result()

    # result = {
    #     "property_name": "Tempe Apartment Community",
    #     "website": "https://www.example.com/tempe-apartment-community",
    #     "floorplan_details": [
    #         {
    #             "floorplan_name": "Studio",
    #             "price": None,
    #             "number_of_bedrooms": 1,
    #             "number_of_bathrooms": 1,
    #             "square_feet": None,
    #         },
    #         {
    #             "floorplan_name": "1-Bed",
    #             "price": None,
    #             "number_of_bedrooms": 1,
    #             "number_of_bathrooms": 1,
    #             "square_feet": None,
    #         },
    #         {
    #             "floorplan_name": "2-Bed",
    #             "price": None,
    #             "number_of_bedrooms": 2,
    #             "number_of_bathrooms": 2,
    #             "square_feet": None,
    #         },
    #         {
    #             "floorplan_name": "3-Bed",
    #             "price": None,
    #             "number_of_bedrooms": 3,
    #             "number_of_bathrooms": 2,
    #             "square_feet": None,
    #         },
    #         {
    #             "floorplan_name": "4-Bed",
    #             "price": None,
    #             "number_of_bedrooms": 4,
    #             "number_of_bathrooms": 2,
    #             "square_feet": None,
    #         },
    #     ],
    #     "sources": ["https://www.atmospheretempe.com/floor-plans/"],
    # }

    store_in_database(result)
    return "Scraped data successfully inserted into MYSQL!", result


@fastapi_app.get("/floorplans", tags=["Floorplans"])
def get_floorplans_by_filters(
    price_min: int | None = None,
    price_max: float | None = None,
    number_of_bedrooms: int | None = None,
    number_of_bathrooms: int | None = None,
    square_feet_min: int | None = None,
    square_feet_max: float | None = None,
):
    filtered_floorplans = get_filtered_floorplan(
        price_min,
        price_max,
        number_of_bedrooms,
        number_of_bathrooms,
        square_feet_min,
        square_feet_max,
    )
    return {"Filtered rows: ": filtered_floorplans}


@fastapi_app.get("/floorplans/{property_name}", tags=["Floorplans"])
def get_property(property_name: str):
    floorplan_by_name = get_property_by_name(property_name)
    return floorplan_by_name


@fastapi_app.get(
    "/floorplans/{property_name}/{floorplan_name}",
    tags=["Floorplans", "Property"],
)
def get_floorplan(property_name: str, floorplan_name: str):
    floorplan_by_name_and_property = get_floorplan_by_floorplan_and_property_name(
        property_name, floorplan_name
    )
    return f"{floorplan_by_name_and_property} found with the given names"


@fastapi_app.post("/users", tags=["Users"], response_model=User)
def add_user(user: User):
    store_user_in_db(user)
    return f"{user} user inserted into MySQL!"


@fastapi_app.get("/users/{user_id}", tags=["Users"])
def get_user(user_id: int):
    user = get_user_by_id(user_id)
    return {"user found with the given ID": user}


@fastapi_app.post("/interested", tags=["Interested"])
def add_floorplan_interested(interested_floorplan: InterestedFloorplan):
    res = store_floorplan_in_interested(interested_floorplan)
    if type(res) != str:
        return f"Interested floorplan successfully inserted into MySQL!"
    return res


@fastapi_app.get("/interested/{user_id}", tags=["Interested"])
def get_interested_by_user_id(user_id: int):
    interested_floorplan = get_interested_floorplan_by_user_id(user_id)
    return {"Interested floorplans found with the given user ID": interested_floorplan}


@fastapi_app.delete("/interested", tags=["Interested"])
def delete_interested(property_data: InterestedFloorplan = Body(...)):
    res = delete_floorplan_data(property_data)
    if type(res) != str:
        return f"Interested floorplan successfully deleted from MySQL!"
    return res


def generate_openapi_yaml():
    openapi_schema = fastapi_app.openapi()
    with open("swagger.yaml", "w") as f:
        yaml.dump(openapi_schema, f, default_flow_style=False)


generate_openapi_yaml()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(fastapi_app, host="127.0.0.1", port=8080)
