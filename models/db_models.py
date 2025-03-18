from sqlalchemy.orm import DeclarativeBase
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
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)

    # floorplan_property = relationship("Property", back_populates="property_floorplans")
    # interests_floorplan = relationship("Interested", back_populates="interests_floorplan")


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    website = Column(String(255), nullable=False, unique=True)

    # property_floorplans = relationship("FloorPlan", back_populates="floorplan_property")
    # property_interests = relationship("Interested", back_populates="interests_property")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    # user_interests = relationship("Interested", back_populates="interests_user")


class Interested(Base):
    __tablename__ = "interested"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    floorplan_id = Column(Integer, ForeignKey("floorplans.id"), nullable=False)

    # interests_user = relationship("User", back_populates="user_interests")
    # interests_property = relationship("Property", back_populates="property_interests")
    # interests_floorplan = relationship("FloorPlan", back_populates="floorplan_interests")
