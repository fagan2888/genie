from flask import Flask, send_from_directory, request
from flask import render_template
from flask import jsonify
from flask import Blueprint
import pdb
import math
from connection import connection
journals = Blueprint("journals", __name__)
orders = [None, "ASC", "DESC"]
columns = ["Gene Disease", "Year", "Count"]
cols = [None, "year", "count"]

@journals.route("/journals/view")
def view():
    return render_template("journals.html", columns = columns)

@journals.route("/journals")
def index():
    search = request.args.get("search")
    search_sql = None
    if search:
        search_sql = "WHERE id LIKE %(search)s"
    order = "id, year"
    page = int(request.args.get("page"))

    if request.args.get("sortcol"):
        order = "{} {}, ".format(cols[int(request.args.get('sortcol'))], orders[int(request.args.get('sortstate'))]) + order

    with connection as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, year, count
                FROM journals
                {}
                ORDER BY {}
                LIMIT {}
                OFFSET {};
            """.format(search_sql, order, 50, page * 50), {"search": "%{}%".format(search)})
            journals = cur.fetchall()

            cur.execute("""
                SELECT count(1)
                FROM journals
                {};
            """.format(search_sql), {"search": "%{}%".format(search)})
            count = cur.fetchone()[0]

            results = []
            for journal in journals:
                results.append(journal)
            return jsonify({"items": results, "total_pages": math.ceil(count / 50)})
