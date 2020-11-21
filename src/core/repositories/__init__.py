from flask_sqlalchemy import SQLAlchemy
from .vessel_repository import VesselRepository


db = SQLAlchemy()
__all__ = ['VesselRepository']
