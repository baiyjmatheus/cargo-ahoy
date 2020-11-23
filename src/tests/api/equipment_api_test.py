from http import HTTPStatus

from src.core.exceptions.resource_exists_exception import ResourceExists
from src.core.exceptions.resource_not_found_exception import ResourceNotFound
from src.core.services.equipment_service import EquipmentService


class TestEquipmentApi:

    def test_sucessfully_get_vessel_equipments(self, app, mocker, mock_vessel_equipments):
        # given
        mocker.patch.object(EquipmentService,
                            'get_all_active_equipments_by_vessel',
                            return_value=mock_vessel_equipments)

        # when
        client = app.test_client()
        response = client.get('/api/vessels/AM123/equipments/')

        # then
        assert response.status_code == 200
        assert response.data

    def test_get_vessel_equipments_vessel_not_found(self, app, mocker):
        # given
        mock_get_vessel_equipments = mocker.patch.object(EquipmentService,
                                                         'get_all_active_equipments_by_vessel',
                                                         autospec=True)
        mock_get_vessel_equipments.side_effect = ResourceNotFound('Vessel was not found')

        # when
        client = app.test_client()
        response = client.get('/api/vessels/AM123/equipments/')

        # then
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_successfully_create_vessel_equipment(self, app, mocker, mock_vessel_equipment):
        # given
        mocker.patch.object(EquipmentService, 'create_equipment', return_value=mock_vessel_equipment)

        # when
        client = app.test_client()
        response = client.post('/api/vessels/AM123/equipments/', json=dict(
            code='MV102',
            name='turbine',
            location='JAPAN'
        ))

        # then
        assert response.status_code == HTTPStatus.OK
        assert response.data

    def test_create_vessel_equipment_violate_schema(self, app, mock_vessel_equipment):
        # when
        client = app.test_client()
        response = client.post('/api/vessels/AM123/equipments/', json=dict(
            code='MV102',
            name='turbine',
            location='ENGLAND(not mapped)'
        ))

        # then
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_create_vessel_equipment_vessel_not_found(self, app, mocker, mock_vessel_equipment):
        # given
        mock_create_equipment = mocker.patch.object(EquipmentService, 'create_equipment', autospec=True)
        mock_create_equipment.side_effect = ResourceNotFound('Vessel was not found')

        # when
        client = app.test_client()
        response = client.post('/api/vessels/AM123/equipments/', json=dict(
            code='MV102',
            name='turbine',
            location='JAPAN'
        ))

        # then
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_create_vessel_equipment_vessel_equipment_already_exists(self, app, mocker, mock_vessel_equipment):
        # given
        mock_create_equipment = mocker.patch.object(EquipmentService, 'create_equipment', autospec=True)
        mock_create_equipment.side_effect = ResourceExists('Equipment already exists')

        # when
        client = app.test_client()
        response = client.post('/api/vessels/AM123/equipments/', json=dict(
            code='MV102',
            name='turbine',
            location='JAPAN'
        ))

        # then
        assert response.status_code == HTTPStatus.CONFLICT

    def test_sucessfully_inactivate_equipments(self, app, mocker, mock_inactivated_vessel_equipments):
        # given
        mocker.patch.object(EquipmentService, 'inactivate_equipments', return_value=mock_inactivated_vessel_equipments)

        # when
        client = app.test_client()
        response = client.patch('/api/vessels/AM123/equipments/inactivate', json=dict(
            codes=['MV102, MV103']
        ))

        # then
        assert response.status_code == HTTPStatus.OK
        assert response.data

    def test_inactivate_equipments_violate_schema(self, app, mocker, mock_inactivated_vessel_equipments):
        # when
        client = app.test_client()
        response = client.patch('/api/vessels/AM123/equipments/inactivate', json=dict(
            codes=[123]
        ))

        # then
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_inactivate_equipments_equipment_not_from_vessel(self, app, mocker, mock_inactivated_vessel_equipments):
        # given
        mock_inactivate_equipments = mocker.patch.object(EquipmentService, 'inactivate_equipments', autospec=True)
        mock_inactivate_equipments.side_effect = ResourceNotFound('Equipment MV102 was not found in this vessel')

        # when
        client = app.test_client()
        response = client.patch('/api/vessels/AM123/equipments/inactivate', json=dict(
            codes=['MV102, MV103']
        ))

        # then
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_inactivate_equipments_equipment_not_from_vessel(self, app, mocker, mock_inactivated_vessel_equipments):
        # given
        mock_inactivate_equipments = mocker.patch.object(EquipmentService, 'inactivate_equipments', autospec=True)
        mock_inactivate_equipments.side_effect = ResourceNotFound('Equipment MV102 was not found in this vessel')

        # when
        client = app.test_client()
        response = client.patch('/api/vessels/AM123/equipments/inactivate', json=dict(
            codes=['MV102, MV103']
        ))

        # then
        assert response.status_code == HTTPStatus.NOT_FOUND
