from flask import Blueprint, jsonify, request
from ..crud.reader import create_reader, get_reader, update_reader, delete_reader, get_all_readers
from ..database import get_db

blueprint = Blueprint('readers', __name__)


@blueprint.route('/readers', methods=['POST'])
def create_reader_route():
    data = request.json
    db = next(get_db())
    reader = create_reader(
        db,
        full_name=data.get("full_name"),
        address=data.get("address"),
        phone=data.get("phone")
    )
    return jsonify(reader.to_dict()), 201


@blueprint.route('/readers/<int:reader_id>', methods=['GET'])
def get_reader_route(reader_id):
    db = next(get_db())
    reader = get_reader(db, reader_id)
    if reader:
        return jsonify(reader.to_dict())
    return jsonify({"error": "Reader not found"}), 404


@blueprint.route('/readers/<int:reader_id>', methods=['PUT'])
def update_reader_route(reader_id):
    data = request.json
    db = next(get_db())
    reader = update_reader(
        db,
        reader_id=reader_id,
        full_name=data.get("full_name"),
        address=data.get("address"),
        phone=data.get("phone")
    )
    if reader:
        return jsonify(reader.to_dict())
    return jsonify({"error": "Reader not found"}), 404


@blueprint.route('/readers/<int:reader_id>', methods=['DELETE'])
def delete_reader_route(reader_id):
    db = next(get_db())
    reader = delete_reader(db, reader_id)
    if reader:
        return jsonify({"message": "Reader deleted"})
    return jsonify({"error": "Reader not found"}), 404


@blueprint.route('/readers', methods=['GET'])
def get_all_readers_route():
    db = next(get_db())
    readers = get_all_readers(db)
    return jsonify([reader.to_dict() for reader in readers])
