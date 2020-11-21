from sqlalchemy.exc import IntegrityError

from src.core.exceptions.resource_not_found_exception import ResourceNotFound
from src.core.models import Vessel
from src.core.exceptions.resource_exists_exception import ResourceExists


class VesselRepository:

    def create_vessel(self, code: str) -> dict:
        """ Create Vessel """
        try:
            vessel = Vessel(code=code)
            vessel.save()
        except IntegrityError:
            Vessel.rollback()
            raise ResourceExists('Vessel already exists')

        result = {
            'id': vessel.id,
            'code': vessel.code,
            'created_at': str(vessel.created_at),
        }
        return result

    def find_by_code(self, code: str) -> dict:
        """ Query a vessel by code """
        vessel = Vessel.query.filter_by(code=code).first()
        if vessel is None:
            raise ResourceNotFound('Vessel was not found')

        result = {
            'id': vessel.id,
            'code': vessel.code,
            'created_at': str(vessel.created_at),
        }

        return result
