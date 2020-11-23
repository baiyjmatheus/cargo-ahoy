from sqlalchemy.exc import IntegrityError

from src.core.exceptions.resource_exists_exception import ResourceExists
from src.core.exceptions.resource_not_found_exception import ResourceNotFound
from src.core.models import Equipment
from src.core.models.enums.equipment_status import EquipmentStatus


class EquipmentRepository:

    def find_by_code(self, code):
        """ Query an equipment by code """
        equipment = Equipment.query.filter_by(code=code).first()
        if equipment is None:
            raise ResourceNotFound('Equipment was not found')

        result = self._to_dict(equipment)

        return result

    def _find_vessel_equipment_by_code(self, vessel_id, code):
        equipment = Equipment.query.filter_by(vessel_id=vessel_id,
                                              code=code).first()
        if equipment is None:
            raise ResourceNotFound(f'Equipment {code} not found in this vessel')

        return equipment

    def find_vessel_active_equipments_by_code(self, vessel_id):
        equipments = Equipment.query.filter_by(vessel_id=vessel_id,
                                               status=EquipmentStatus.ACTIVE)

        results = list(map(self._to_dict, equipments))
        return results

    def create_equipment(self,
                         code,
                         name,
                         vessel_id,
                         location=None,
                         status=None):
        if self._equipment_exists(code=code):
            raise ResourceExists('Equipment already exists')

        equipment = Equipment(code=code,
                              name=name,
                              vessel_id=vessel_id,
                              location=location,
                              status=status)
        equipment.save()
        result = self._to_dict(equipment)

        return result

    def inactivate_vessel_equipments_by_code(self, vessel_id, equipments_code):
        equipments = []
        for code in equipments_code:
            equipment = self._find_vessel_equipment_by_code(vessel_id=vessel_id, code=code)
            equipment.status = EquipmentStatus.INACTIVE
            equipment.save()
            equipments.append(equipment)

        results = list(map(self._to_dict, equipments))

        return results

    def _equipment_exists(self, code):
        return Equipment.query.filter_by(code=code).scalar() is not None


    def _to_model(self, equipment):
        return Equipment(code=equipment.get('code'),
                         name=equipment.get('name'),
                         vessel_id=equipment.get('vessel_id'),
                         location=equipment.get('location'),
                         status=equipment.get('status'))

    def _to_dict(self, equipment: Equipment):
        result = {
            'id': equipment.id,
            'code': equipment.code,
            'name': equipment.name,
            'status': str(equipment.status.value),
            'location': str(equipment.location.value),
            'created_at': str(equipment.created_at),
            'vessel_id': equipment.vessel_id
        }

        return result
