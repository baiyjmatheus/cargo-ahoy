from src.core.exceptions.resource_exists_exception import ResourceExists
from src.core.repositories import VesselRepository


class VesselService:
    def __init__(self):
        self.vessel_repository = VesselRepository()

    def find_by_code(self, code):
        return self.vessel_repository.find_by_code(code)

    def create_vessel_if_not_existing(self, data):
        code = data.get('code')
        return self.vessel_repository.create_vessel(code)
