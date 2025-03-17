from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey

class Base(DeclarativeBase):
    pass

class FloorPlan(Base):
    __tablename__ = "floorplans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=True)
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    square_feet = Column(Integer, nullable=True)


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    website = Column(String(255), nullable=False, unique=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)



class Interested(Base):
    __tablename__ = "interested"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    floorplan_id = Column(Integer, ForeignKey("floorplans.id"), nullable=False)

    user = relationship("User", back_populates="property")
    property = relationship("Property", back_populates="property")
    floorplan = relationship("FloorPlan", back_populates="property")
