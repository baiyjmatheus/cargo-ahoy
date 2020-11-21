from sqlalchemy.exc import IntegrityError

from src.core.exceptions.resource_exists_exception import ResourceExists
from src.core.exceptions.resource_not_found_exception import ResourceNotFound
from src.core.models import Equipment


class EquipmentRepository:

    def find_by_code(self, code):
        """ Query an equipment by code """
        equipment = Equipment.query.filter_by(code=code).first()
        if equipment is None:
            raise ResourceNotFound('Equipment was not found')

        result = {
            'id': equipment.id,
            'code': equipment.code,
            'name': equipment.name,
            'status': equipment.status,
            'location': equipment.location,
            'created_at': str(equipment.created_at),
            'vessel_id': equipment.vessel_id
        }

        return result

    def create_equipment(self,
                         code,
                         name,
                         vessel_id,
                         location=None,
                         status=None):
        try:
            equipment = Equipment(code=code,
                                  name=name,
                                  vessel_id=vessel_id,
                                  location=location,
                                  status=status)
            equipment.save()
        except IntegrityError:
            Equipment.rollback()
            raise ResourceExists('Equipment already exists')

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
