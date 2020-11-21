from http import HTTPStatus

from flask import Blueprint, request, Response

from src.core.exceptions.resource_not_found_exception import ResourceNotFound
from src.core.services.vessel_service import VesselService
from src.core.exceptions.resource_exists_exception import ResourceExists


def get_blueprint() -> Blueprint:
    vessel_blueprint = Blueprint('vessels', __name__)
    vessel_service = VesselService()

    @vessel_blueprint.route('/', methods=['POST'])
    def create_vessel():
        try:
            data = request.get_json()
            return vessel_service.create_vessel_if_not_existing(data)
        except ResourceExists as e:
            return Response(e.message, HTTPStatus.CONFLICT)

    @vessel_blueprint.route('/<code>', methods=['GET'])
    def find_by_code(code):
        try:
            vessel = vessel_service.find_by_code(code)
            return vessel
        except ResourceNotFound as e:
            return Response(e.message, HTTPStatus.NOT_FOUND)

    return vessel_blueprint
