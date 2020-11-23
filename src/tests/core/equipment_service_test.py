import pytest

from src.core.exceptions.resource_exists_exception import ResourceExists
from src.core.exceptions.resource_not_found_exception import ResourceNotFound
from src.core.models import Vessel, Equipment
from src.core.models.enums.equipment_location import EquipmentLocation
from src.core.models.enums.equipment_status import EquipmentStatus
from src.core.services.equipment_service import EquipmentService
from src.tests.core.base_service_test import BaseServiceTest


class EquipmentServiceTest(BaseServiceTest):

    equipment_service = EquipmentService()

    vessel_code = 'AM123'
    equipment_code1 = 'MV102'
    equipment_code2 = 'MV103'
    equipment_name = 'turbine'

    def test_create_equipment(self):
        # given
        data = dict(
            code=self.equipment_code1,
            name=self.equipment_name,
            location=EquipmentLocation.BRAZIL.value,
            status=EquipmentStatus.ACTIVE.value
        )
        self._add_to_db(Vessel(code=self.vessel_code))

        # when
        created_equipment = self.equipment_service.create_equipment(vessel_code=self.vessel_code,
                                                                    data=data)

        # then
        assert created_equipment
        assert created_equipment.get('code') == self.equipment_code1

    def test_create_equipment_non_existing_vessel(self):
        # given
        data = dict(
            code=self.equipment_code1,
            name=self.equipment_name,
            location=EquipmentLocation.BRAZIL.value,
            status=EquipmentStatus.ACTIVE.value
        )

        # then
        with pytest.raises(ResourceNotFound):
            self.equipment_service.create_equipment(vessel_code=self.vessel_code, data=data)

    def test_create_equipment_existing_equipment(self):
        # given
        data = dict(
            code=self.equipment_code1,
            name=self.equipment_name,
            location=EquipmentLocation.BRAZIL.value,
            status=EquipmentStatus.ACTIVE.value
        )
        vessel = self._add_to_db(Vessel(code=self.vessel_code))
        self._add_to_db(Equipment(code=self.equipment_code1,
                                  name=self.equipment_name,
                                  location=EquipmentLocation.BRAZIL.value,
                                  status=EquipmentStatus.ACTIVE.value,
                                  vessel_id=vessel.id))

        # then
        with pytest.raises(ResourceExists):
            self.equipment_service.create_equipment(vessel_code=self.vessel_code, data=data)

    def test_get_all_active_equipments_by_vessel(self):
        # given
        vessel = self._add_to_db(Vessel(code=self.vessel_code))
        self._add_to_db(Equipment(code=self.equipment_code1,
                                  name=self.equipment_name,
                                  location=EquipmentLocation.BRAZIL.value,
                                  status=EquipmentStatus.ACTIVE.value,
                                  vessel_id=vessel.id))
        self._add_to_db(Equipment(code=self.equipment_code2,
                                  name=self.equipment_name,
                                  location=EquipmentLocation.BRAZIL.value,
                                  status=EquipmentStatus.INACTIVE.value,
                                  vessel_id=vessel.id))

        # when
        equipments = self.equipment_service.get_all_active_equipments_by_vessel(vessel_code=self.vessel_code)

        # then
        assert equipments
        assert len(equipments) == 1
        assert equipments[0].get('status') == EquipmentStatus.ACTIVE.value

    def test_get_all_active_equipments_by_vessel_non_existing_vessel(self):
        with pytest.raises(ResourceNotFound):
            self.equipment_service.get_all_active_equipments_by_vessel(vessel_code=self.vessel_code)

    def test_get_all_active_equipments_by_vessel_empty_result(self):
        # given
        self._add_to_db(Vessel(code=self.vessel_code))

        # when
        equipments = self.equipment_service.get_all_active_equipments_by_vessel(vessel_code=self.vessel_code)

        # then
        assert len(equipments) == 0

    def test_inactivate_equipments(self):
        # given
        data = dict(codes=[self.equipment_code1, self.equipment_code2])
        vessel = self._add_to_db(Vessel(code=self.vessel_code))
        self._add_to_db(Equipment(code=self.equipment_code1,
                                  name=self.equipment_name,
                                  location=EquipmentLocation.BRAZIL.value,
                                  status=EquipmentStatus.ACTIVE.value,
                                  vessel_id=vessel.id))
        self._add_to_db(Equipment(code=self.equipment_code2,
                                  name=self.equipment_name,
                                  location=EquipmentLocation.BRAZIL.value,
                                  status=EquipmentStatus.ACTIVE.value,
                                  vessel_id=vessel.id))

        # when
        inactivated_equipments = self.equipment_service.inactivate_equipments(vessel_code=self.vessel_code, data=data)

        # then
        for inactivated_equipment in inactivated_equipments:
            assert inactivated_equipment
            assert inactivated_equipment.get('status') == EquipmentStatus.INACTIVE.value

    def test_inactivate_equipments_equipment_does_not_belong_to_vessel(self):
        # given
        data = dict(codes=[self.equipment_code1, self.equipment_code2])
        vessel1 = self._add_to_db(Vessel(code=self.vessel_code))
        vessel2 = self._add_to_db(Vessel(code='AN456'))
        self._add_to_db(Equipment(code=self.equipment_code1,
                                  name=self.equipment_name,
                                  location=EquipmentLocation.BRAZIL.value,
                                  status=EquipmentStatus.ACTIVE.value,
                                  vessel_id=vessel1.id))
        self._add_to_db(Equipment(code=self.equipment_code2,
                                  name=self.equipment_name,
                                  location=EquipmentLocation.BRAZIL.value,
                                  status=EquipmentStatus.ACTIVE.value,
                                  vessel_id=vessel2.id))

        # when
        with pytest.raises(ResourceNotFound):
            self.equipment_service.inactivate_equipments(vessel_code=self.vessel_code, data=data)

    def test_inactivate_equipments_equipment_vessel_does_not_exist(self):
        # given
        data = dict(codes=[self.equipment_code1, self.equipment_code2])

        # then
        with pytest.raises(ResourceNotFound):
            self.equipment_service.inactivate_equipments(vessel_code=self.vessel_code, data=data)
