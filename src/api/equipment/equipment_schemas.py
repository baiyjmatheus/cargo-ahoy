from src.core.models.enums.equipment_location import EquipmentLocation
from src.core.models.enums.equipment_status import EquipmentStatus

equipment_location_list = [e.value for e in EquipmentLocation]
equipment_status_list = [e.value for e in EquipmentStatus]

create_equipment_schema = {
    'required': ['code', 'name'],
    'properties': {
        'code': {
            'type': 'string'
        },
        'name': {
            'type': 'string'
        },
        'status': {
            'enum': equipment_status_list
        },
        'location': {
            'enum': equipment_location_list
        }
    }
}

inactivate_equipments_schema = {
    'required': ['codes'],
    'properties': {
        'codes': {
            'type': 'array',
            'items': {'type': 'string'}
        }
    }
}
