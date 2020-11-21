import datetime

from app import db
from .abc import BaseModel
from .enums.equipment_location import EquipmentLocation
from .enums.equipment_status import EquipmentStatus


class Equipment(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    code = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(64))
    status = db.Column(db.Enum(EquipmentStatus), default=EquipmentStatus.ACTIVE)
    location = db.Column(db.Enum(EquipmentLocation), default=EquipmentLocation.BRAZIL)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    vessel_id = db.Column(db.Integer, db.ForeignKey('vessel.id'))

    def __init__(self,
                 code: str,
                 name: str,
                 status: str,
                 location: str,
                 vessel_id: int):
        self.code = code
        self.name = name
        self.status = status
        self.location = location
        self.vessel_id = vessel_id
