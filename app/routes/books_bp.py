from flask import Blueprint, jsonify, request
from ..crud.book import create_book, get_book, update_book, delete_book, get_all_books
from ..database import get_db

blueprint = Blueprint('books', __name__)


@blueprint.route('/books', methods=['POST'])
def create_book_route():
    data = request.json
    db = next(get_db())
    book = create_book(db, **data)
    return jsonify(book.to_dict()), 201


@blueprint.route('/books/<int:book_id>', methods=['GET'])
def get_book_route(book_id):
    db = next(get_db())
    book = get_book(db, book_id)
    if book:
        return jsonify(book.to_dict())
    return jsonify({"error": "Book not found"}), 404


@blueprint.route('/books/<int:book_id>', methods=['PUT'])
def update_book_route(book_id):
    data = request.json
    db = next(get_db())
    book = update_book(db, **data)
    if book:
        return jsonify(book.to_dict())
    return jsonify({"error": "Book not found"}), 404


@blueprint.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book_route(book_id):
    db = next(get_db())
    book = delete_book(db, book_id)
    if book:
        return jsonify({"message": "Book deleted"})
    return jsonify({"error": "Book not found"}), 404


@blueprint.route('/books', methods=['GET'])
def get_all_books_route():
    db = next(get_db())
    books = get_all_books(db)
    return jsonify([book.to_dict() for book in books])
