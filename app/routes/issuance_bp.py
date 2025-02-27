from flask import Blueprint, jsonify, request
from ..crud.issuance import create_issuance, get_issuance, update_issuance, delete_issuance, get_all_issuances
from ..database import get_db
from datetime import datetime

blueprint = Blueprint('issuances', __name__)


@blueprint.route('/issuances', methods=['POST'])
def create_issuance_route():
    data = request.json
    db = next(get_db())
    try:
        issue_date = datetime.strptime(data.get("issue_date"), "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    issuance = create_issuance(
        db,
        reader_id=data.get("reader_id"),
        book_id=data.get("book_id"),
        issue_date=issue_date
    )
    return jsonify(issuance.to_dict()), 201


@blueprint.route('/issuances/<int:issuance_id>', methods=['GET'])
def get_issuance_route(issuance_id):
    db = next(get_db())
    issuance = get_issuance(db, issuance_id)
    if issuance:
        return jsonify(issuance.to_dict())
    return jsonify({"error": "Issuance not found"}), 404


@blueprint.route('/issuances/<int:issuance_id>', methods=['PUT'])
def update_issuance_route(issuance_id):
    data = request.json
    db = next(get_db())
    try:
        issue_date = datetime.strptime(data.get("issue_date"), "%Y-%m-%d").date() if data.get("issue_date") else None
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    issuance = update_issuance(
        db,
        issuance_id=issuance_id,
        reader_id=data.get("reader_id"),
        book_id=data.get("book_id"),
        issue_date=issue_date
    )
    if issuance:
        return jsonify(issuance.to_dict())
    return jsonify({"error": "Issuance not found"}), 404


@blueprint.route('/issuances/<int:issuance_id>', methods=['DELETE'])
def delete_issuance_route(issuance_id):
    db = next(get_db())
    issuance = delete_issuance(db, issuance_id)
    if issuance:
        return jsonify({"message": "Issuance deleted"})
    return jsonify({"error": "Issuance not found"}), 404


@blueprint.route('/issuances', methods=['GET'])
def get_all_issuances_route():
    db = next(get_db())
    issuances = get_all_issuances(db)
    return jsonify([issuance.to_dict() for issuance in issuances])
