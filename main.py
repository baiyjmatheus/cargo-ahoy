from flask_migrate import Migrate

from src.api.equipment import equipment_api
from src.api.vessel import vessel_api
from src.core.models import Vessel as VesselModel
from src.core.models import Equipment as EquipmentModel
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)


# Blueprints
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'ok'


app.register_blueprint(vessel_api.get_blueprint(), url_prefix='/api/vessels')
app.register_blueprint(equipment_api.get_blueprint(), url_prefix='/api/vessels/<vessel_code>/equipments')

if __name__ == '__main__':
    app.run()


# CLI for migrations
@app.shell_context_processor
def make_shell_context():
    return dict(app=app,
                db=db,
                Vessel=VesselModel,
                Equipment=EquipmentModel)
