import datetime

from app import db
from .abc import BaseModel


class Vessel(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    code = db.Column(db.String(32), unique=True,nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, code: str):
        self.code = code
