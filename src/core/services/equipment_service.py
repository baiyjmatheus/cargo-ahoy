from src.core.exceptions.resource_exists_exception import ResourceExists
from src.core.repositories.equipment_repository import EquipmentRepository
from src.core.services.vessel_service import VesselService


class EquipmentService:
    def __init__(self):
        self.vessel_service = VesselService()
        self.equipment_repository = EquipmentRepository()

    def create_equipment(self, vessel_code: str, data: dict):
        vessel = self.vessel_service.find_by_code(vessel_code)
        vessel_id = vessel.get('id')
        equipment_code = data.get('code')
        name = data.get('name')
        location = data.get('location')
        status = data.get('status')

        return self.equipment_repository.create_equipment(code=equipment_code,
                                                          name=name,
                                                          vessel_id=vessel_id,
                                                          location=location,
                                                          status=status)
