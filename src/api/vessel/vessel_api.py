from http import HTTPStatus

from flask import Blueprint, request, Response, jsonify, make_response
from flask_json_schema import JsonValidationError

from app import schema
from src.api.vessel.vessel_schemas import create_vessel_schema
from src.core.exceptions.resource_not_found_exception import ResourceNotFound
from src.core.services.vessel_service import VesselService
from src.core.exceptions.resource_exists_exception import ResourceExists


def get_blueprint() -> Blueprint:
    vessel_blueprint = Blueprint('vessels', __name__)
    vessel_service = VesselService()

    @vessel_blueprint.route('/', methods=['POST'])
    @schema.validate(create_vessel_schema)
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

    @vessel_blueprint.errorhandler(JsonValidationError)
    def validation_error(e):
        return make_response(
            jsonify({'error': e.message, 'errors': [validation_error.message for validation_error in e.errors]}),
            HTTPStatus.BAD_REQUEST)

    return vessel_blueprint
