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
        "code": "123",
        "created_at": "2020-11-22 17:44:20.852511",
        "id": 9
    }
    return vessel
