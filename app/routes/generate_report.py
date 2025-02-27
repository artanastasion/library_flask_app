from flask import Blueprint, request, Response
from datetime import datetime, timedelta
import csv
from io import StringIO
from sqlalchemy.orm import Session
from ..models.reader import Reader
from ..models.issuance import Issuance
from ..models.book import Book
from ..database import get_db

blueprint = Blueprint("report", __name__, url_prefix="/api")


@blueprint.route("/report", methods=["GET"])
def generate_report():
    date_str = request.args.get("date")
    if not date_str:
        return "Parameter 'date' is required", 400
    try:
        report_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD", 400

    db: Session = next(get_db())

    overdue_issues = (
        db.query(Reader, Book, Issuance)
        .join(Issuance, Reader.id == Issuance.reader_id)
        .join(Book, Issuance.book_id == Book.id)
        .filter(Issuance.issue_date <= report_date - timedelta(days=20))  # Просроченные книги
        .all()
    )

    if not overdue_issues:
        return "No overdue issues found.", 404

    report_data = {}
    total_books_library = 0

    for reader, book, issue in overdue_issues:
        if reader.id not in report_data:
            report_data[reader.id] = {
                "reader": reader,
                "books": [],
                "total_books": 0,
                "total_price": 0,
            }
        report_data[reader.id]["books"].append((book, issue))
        report_data[reader.id]["total_books"] += 1
        report_data[reader.id]["total_price"] += book.price
        total_books_library += 1

    # Формирование CSV-отчета
    output = StringIO()
    writer = csv.writer(output)

    # Заголовок отчета
    writer.writerow([f"Сведения о читателях, у которых наступил срок возврата на {report_date.strftime('%d.%m.%y')}"])
    writer.writerow(["Домашний телефон", "Автор", "Название книги", "Цена книги, тыс. руб.", "Дата выдачи"])

    for reader_id, data in report_data.items():
        for book, issue in data["books"]:
            writer.writerow([data['reader'].phone, book.author, book.title, f"{book.price:.2f}",
                             issue.issue_date.strftime('%d.%m.%Y')])

        writer.writerow([f"Итого книг у читателя: {data['total_books']}"])
        writer.writerow([])  # Пустая строка для разделения читателей

    writer.writerow([f"Итого по библиотеке: {total_books_library}"])

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=report_{date_str}.csv"},
    )
