from src.core.exceptions.resource_exists_exception import ResourceExists
from src.core.services.vessel_service import VesselService


class TestVesselApi:

    def test_create_vessel_successful(self, app, mocker, mock_vessel):
        # given
        mocker.patch.object(VesselService, 'create_vessel_if_not_existing', return_value=mock_vessel)

        # when
        client = app.test_client()
        response = client.post('/api/vessels/', json=dict(code='123'))

        # then
        assert response.status_code == 200

    def test_create_vessel_already_exists(self, app, mocker):
        # given
        mock_create_vessel = mocker.patch.object(VesselService, 'create_vessel_if_not_existing', autospec=True)
        mock_create_vessel.side_effect = ResourceExists('a')

        # when
        client = app.test_client()
        response = client.post('/api/vessels/', json=dict(code='123'))

        # then
        assert response.status_code == 409

    def test_create_vessel_bad_request(self, app):
        # when
        client = app.test_client()
        response = client.post('/api/vessels/', json=dict(code=123))

        # then
        assert response.status_code == 400

