import pytest

from src.core.exceptions.resource_exists_exception import ResourceExists
from src.core.exceptions.resource_not_found_exception import ResourceNotFound
from src.core.models import Vessel
from src.core.services.vessel_service import VesselService
from src.tests.core.base_service_test import BaseServiceTest


class TestVesselService(BaseServiceTest):

    vessel_code = 'AM123'

    vessel_service = VesselService()

    def test_find_by_code_with_results(self):
        # given
        self._add_to_db(Vessel(code=self.vessel_code))

        # when
        fetched_vessel = self.vessel_service.find_by_code(self.vessel_code)

        # then
        assert fetched_vessel
        assert fetched_vessel.get('code') == self.vessel_code

    def test_find_by_code_without_results(self):
        with pytest.raises(ResourceNotFound):
            self.vessel_service.find_by_code(self.vessel_code)

    def test_create_vessel(self):
        # given
        data = dict(code=self.vessel_code)

        # when
        created_vessel = self.vessel_service.create_vessel_if_not_existing(data)

        # then
        assert created_vessel
        assert created_vessel.get('code') == self.vessel_code

    def test_create_vessel_already_exists(self):
        # given
        data = dict(code=self.vessel_code)
        self._add_to_db(Vessel(code=self.vessel_code))

        # then
        with pytest.raises(ResourceExists):
            self.vessel_service.create_vessel_if_not_existing(data)

