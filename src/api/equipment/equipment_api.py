from http import HTTPStatus

from flask import Blueprint, request, Response, jsonify

from src.core.exceptions.resource_exists_exception import ResourceExists
from src.core.exceptions.resource_not_found_exception import ResourceNotFound
from src.core.services.equipment_service import EquipmentService


def get_blueprint() -> Blueprint:
    equipment_blueprint = Blueprint('equipments', __name__)
    equipment_service = EquipmentService()

    @equipment_blueprint.route('/', methods=['GET'])
    def get_equipments_by_vessel(vessel_code):
        try:
            return jsonify(equipment_service.get_all_active_equipments_by_vessel(vessel_code))
        except ResourceNotFound as e:
            return Response(e.message, HTTPStatus.NOT_FOUND)

    @equipment_blueprint.route('/', methods=['POST'])
    def create_equipment(vessel_code):
        try:
            data = request.get_json()
            return equipment_service.create_equipment(vessel_code, data)
        except ResourceExists as e:
            return Response(e.message, HTTPStatus.CONFLICT)
        except ResourceNotFound as e:
            return Response(e.message, HTTPStatus.NOT_FOUND)

    return equipment_blueprint
