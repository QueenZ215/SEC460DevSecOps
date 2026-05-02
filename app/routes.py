from flask import Blueprint, render_template, request
from .database import get_db

main = Blueprint("main", __name__)

VALID_SEVERITIES = {"critical", "high", "medium", "low"}


@main.route("/")
def index():
    sort = request.args.get("sort", "desc")
    severity = request.args.get("severity", "all")

    VALID_SEVERITIES = {"critical", "high", "medium", "low"}

    order = "DESC" if sort == "desc" else "ASC"

    severity_clean = (
        severity.lower()
        if severity.lower() in VALID_SEVERITIES
        else None
    )

    conn = get_db()

    if order == "DESC":
        order_clause = " ORDER BY cvss_score DESC"
    else:
        order_clause = " ORDER BY cvss_score ASC"

    if severity_clean:
        query = "SELECT * FROM cves WHERE severity = ?" + order_clause
        cves = conn.execute(query, (severity_clean.upper(),)).fetchall()
    else:
        query = "SELECT * FROM cves" + order_clause
        cves = conn.execute(query).fetchall()

    conn.close()

    return render_template(
        "index.html",
        cves=cves,
        sort=sort,
        severity=severity
    )