import pytest

from app import create_app
from src.api.equipment import equipment_api
from src.api.vessel import vessel_api


@pytest.yield_fixture(scope='function')
def app():
    app = create_app()
    app.register_blueprint(vessel_api.get_blueprint(), url_prefix='/api/vessels')
    app.register_blueprint(equipment_api.get_blueprint(), url_prefix='/api/vessels/<vessel_code>/equipments')
    return app


@pytest.fixture(scope='function')
def mock_vessel():
    vessel = {
        "code": "AM123",
        "created_at": "2020-11-22 17:44:20.852511",
        "id": 9
    }
    return vessel


@pytest.fixture(scope='function')
def mock_vessel_equipments():
    vessel_equipments = [
        {
            "code": "MV102",
            "created_at": "2020-11-22 15:54:57.360100",
            "id": 12,
            "location": "JAPAN",
            "name": "turbine",
            "status": "ACTIVE",
            "vessel_id": 9
        },
        {
            "code": "MV103",
            "created_at": "2020-11-23 18:54:57.360100",
            "id": 18,
            "location": "BRAZIL",
            "name": "turbine",
            "status": "ACTIVE",
            "vessel_id": 9
        }
    ]
    return vessel_equipments


@pytest.fixture(scope='function')
def mock_vessel_equipment():
    vessel_equipment = {
        "code": "MV102",
        "created_at": "2020-11-22 15:54:57.360100",
        "id": 12,
        "location": "JAPAN",
        "name": "turbine",
        "status": "ACTIVE",
        "vessel_id": 9
    }
    return vessel_equipment


@pytest.fixture(scope='function')
def mock_inactivated_vessel_equipments():
    inactivated_vessel_equipments = [
        {
            "code": "MV102",
            "created_at": "2020-11-22 15:54:57.360100",
            "id": 12,
            "location": "JAPAN",
            "name": "turbine",
            "status": "INACTIVE",
            "vessel_id": 9
        },
        {
            "code": "MV103",
            "created_at": "2020-11-23 18:54:57.360100",
            "id": 18,
            "location": "BRAZIL",
            "name": "turbine",
            "status": "INACTIVE",
            "vessel_id": 9
        }
    ]
    return inactivated_vessel_equipments
