from flask import Blueprint, jsonify, request
from ..crud.publisher import create_publisher, get_publisher, update_publisher, delete_publisher, \
    get_all_publishers
from ..database import get_db

blueprint = Blueprint('publishers', __name__)


@blueprint.route('/publishers', methods=['POST'])
def create_publisher_route():
    data = request.json
    db = next(get_db())
    publisher = create_publisher(
        db,
        name=data.get("name"),
        city=data.get("city")
    )
    return jsonify(publisher.to_dict()), 201


@blueprint.route('/publishers/<int:publisher_id>', methods=['GET'])
def get_publisher_route(publisher_id):
    db = next(get_db())
    publisher = get_publisher(db, publisher_id)
    if publisher:
        return jsonify(publisher.to_dict())
    return jsonify({"error": "Publisher not found"}), 404


@blueprint.route('/publishers/<int:publisher_id>', methods=['PUT'])
def update_publisher_route(publisher_id):
    data = request.json
    db = next(get_db())
    publisher = update_publisher(
        db,
        publisher_id=publisher_id,
        name=data.get("name"),
        city=data.get("city")
    )
    if publisher:
        return jsonify(publisher.to_dict())
    return jsonify({"error": "Publisher not found"}), 404


@blueprint.route('/publishers/<int:publisher_id>', methods=['DELETE'])
def delete_publisher_route(publisher_id):
    db = next(get_db())
    publisher = delete_publisher(db, publisher_id)
    if publisher:
        return jsonify({"message": "Publisher deleted"})
    return jsonify({"error": "Publisher not found"}), 404


@blueprint.route('/publishers', methods=['GET'])
def get_all_publishers_route():
    db = next(get_db())
    publishers = get_all_publishers(db)
    return jsonify([publisher.to_dict() for publisher in publishers])
