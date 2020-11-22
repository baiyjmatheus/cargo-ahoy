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
