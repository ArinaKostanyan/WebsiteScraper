from typing import Dict
from fastapi import Depends
from requests import Session
from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, FloorPlan, Property, User, Interested


DATABASE_URL = "mysql+pymysql://root:IHopeIWill@localhost:3306/scrapper_project_db"
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db: Session = Depends(get_db)
db_changer: Session = SessionLocal()


def get_app_description():
	return (
    	"Welcome to the floorplan data scraper API!"
    	"""This API allows to retrieve floorplan data based on filters, also manages user interested lists,
        and handles user data."""
        
    	"Use the '/floorplans' endpoint with a GET request to see Floorplans."
        "Use the '/s/{property_name}' to GET Property's Floorplans by Name"
        "Use the '/floorplans/{property_name}/{floorplan_name}' GET Floorplan by Name & Property Name"
)

def get_filtered_floorplan(price_min: float | None, 
                              price_max:float | None, 
                              number_of_bedrooms:int | None, 
                              number_of_bathrooms:int | None, 
                              square_feet_min:int | None, 
                              square_feet_max:float | None,
                              db: Session = db_changer):
    
    filters = []
    if price_min:
        filters.append(FloorPlan.price >= price_min)
    if price_max:
        filters.append(FloorPlan.price <= price_max)
    if number_of_bedrooms:
        filters.append(FloorPlan.bedrooms == number_of_bedrooms)
    if number_of_bathrooms:
        filters.append(FloorPlan.bathrooms == number_of_bathrooms)
    if square_feet_min:   
        filters.append(FloorPlan.square_feet >= square_feet_min)
    if square_feet_max:
        filters.append(FloorPlan.square_feet <= square_feet_max)
    
    result = db.query(FloorPlan).where(*filters).all()
    return result

def store_user_in_db(user: Dict, db: Session=db_changer):
    user = User(name=user.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    print("User successfully inserted into MySQL!")

def store_floorplan_in_interested(floorplan: Dict, db: Session=db_changer): 
    print('\n', '-'*30, type(floorplan), '\n', floorplan)
    
    floorplan_from_db = get_floorplan_by_floorplan_and_property_name(floorplan.property_name, floorplan.floorplan_name)
    if floorplan_from_db is None:
        return "No floorplan found with given names"
    print('\n'*2, floorplan_from_db, '\n'*2)
    
    interested = Interested(
        property_id=floorplan_from_db.property_id,
        floorplan_id=floorplan_from_db.id,
        user_id=floorplan.user_id
    )
    db.add(interested)
    db.commit()
    db.refresh(interested)

    return interested

def store_in_database(result: Dict, db: Session=db_changer):
    db_property = Property(
            name = result.get("property_name", "NULL"),
            website = result.get("website", "NULL")
        )
    db.add(db_property)
    db.commit()
    db.refresh(db_property)

    for floorplan in result.get("floorplan_details", []):
        db_floorplan = FloorPlan(
            property_id=db_property.id,
            name=floorplan.get("floorplan_name", "NULL"),
            price=floorplan.get("price", "NULL"),
            bedrooms=floorplan.get("number_of_bedrooms", "NULL"),
            bathrooms=floorplan.get("number_of_bathrooms", "NULL"),
            square_feet=floorplan.get("square_feet", "NULL"),
        )
        db.add(db_floorplan)

    print("Data successfully inserted into MySQL!")
    db.commit()

def get_floorplan_by_name(property_name: str, db: Session=db_changer):
    property = db.query(Property).filter(Property.name == property_name).first()
    if property is None:
        return "No property found with given name"
    return db.query(FloorPlan).filter(FloorPlan.property_id == property.id).all()

def get_floorplan_by_floorplan_and_property_name(property_name: str, floorplan_name: str, db: Session = db_changer):
    property = db.query(Property).filter(Property.name == property_name).first()
    if property is None:
        return "No property found with given name"
    floorplan = db.query(FloorPlan).filter(FloorPlan.name == floorplan_name).first()
    if floorplan is  None:
        return "No floorplan found with given name"
    return db.query(FloorPlan).filter(FloorPlan.property_id == property.id, FloorPlan.name == floorplan_name).first()

def get_user_by_id(user_id: int, db: Session = db_changer):
    return db.query(User).filter(User.id == user_id).first()

def get_interested_floorplan(user_id: int, db: Session = db_changer):
    interested_fp = db.query(Interested).filter(Interested.user_id == user_id)
    if interested_fp:
        return interested_fp.all()
    return "No interested floorplan found with given user ID"
    
