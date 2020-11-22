from src.core.exceptions.resource_not_found_exception import ResourceNotFound
from src.core.models import Vessel
from src.core.exceptions.resource_exists_exception import ResourceExists


class VesselRepository:

    def create_vessel(self, code: str) -> dict:
        """ Create Vessel """
        if self._find_by_code(code) is not None:
            raise ResourceExists('Vessel already exists')
        vessel = Vessel(code=code)
        vessel.save()
        result = self._to_dict(vessel)
        return result

    def find_by_code(self, code: str) -> dict:
        """ Query a vessel by code """
        vessel = self._find_by_code(code)
        if vessel is None:
            raise ResourceNotFound('Vessel was not found')

        result = self._to_dict(vessel)
        return result

    def _find_by_code(self, code):
        vessel = Vessel.query.filter_by(code=code).first()
        return vessel

    def _to_dict(self, vessel: Vessel):
        result = {
            'id': vessel.id,
            'code': vessel.code,
            'created_at': str(vessel.created_at),
        }
        return result
