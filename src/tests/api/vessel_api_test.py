from http import HTTPStatus

from src.core.exceptions.resource_exists_exception import ResourceExists
from src.core.exceptions.resource_not_found_exception import ResourceNotFound
from src.core.services.vessel_service import VesselService


class TestVesselApi:

    def test_create_vessel_successful(self, app, mocker, mock_vessel):
        # given
        mocker.patch.object(VesselService, 'create_vessel_if_not_existing', return_value=mock_vessel)

        # when
        client = app.test_client()
        response = client.post('/api/vessels/', json=dict(code='AM123'))

        # then
        assert response
        assert response.status_code == HTTPStatus.OK

    def test_create_vessel_already_exists(self, app, mocker):
        # given
        mock_create_vessel = mocker.patch.object(VesselService, 'create_vessel_if_not_existing', autospec=True)
        mock_create_vessel.side_effect = ResourceExists('Vessel already exists')

        # when
        client = app.test_client()
        response = client.post('/api/vessels/', json=dict(code='AM123'))

        # then
        assert response.status_code == HTTPStatus.CONFLICT

    def test_create_vessel_bad_request(self, app):
        # when
        client = app.test_client()
        response = client.post('/api/vessels/', json=dict(code=123))

        # then
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_succesfully_find_vessel_by_code(self, app, mocker, mock_vessel):
        # given
        mocker.patch.object(VesselService, 'find_by_code', return_value=mock_vessel)

        # when
        client = app.test_client()
        response = client.get('/api/vessels/AM123')

        # then
        assert response.status_code == HTTPStatus.OK
        assert response.data

    def test_find_vessel_by_code_not_found(self, app, mocker, mock_vessel):
        # given
        mock_find_by_code = mocker.patch.object(VesselService, 'find_by_code', autospec=True)
        mock_find_by_code.side_effect = ResourceNotFound('Vessel was not found')

        # when
        client = app.test_client()
        response = client.get('/api/vessels/AM123')

        # then
        assert response.status_code == HTTPStatus.NOT_FOUND

