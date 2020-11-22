class TestEquipmentApi:

    def test_create_vessel_successful(self, app, mocker, mock_vessel):
        # given
        mocker.patch.object(VesselService, 'create_vessel_if_not_existing', return_value=mock_vessel)

        # when
        client = app.test_client()
        response = client.post('/api/vessels/', json=dict(code='123'))

        # then
        assert response.status_code == 200