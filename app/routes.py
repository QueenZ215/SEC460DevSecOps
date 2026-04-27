from flask import Blueprint, render_template, request
from .database import get_db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    sort = request.args.get("sort", "desc")
    severity = request.args.get("severity", "all")
    order = "DESC" if sort == "desc" else "ASC"
    conn = get_db()
    if severity != "all":
        cves = conn.execute(
            "SELECT * FROM cves WHERE severity = ? ORDER BY cvss_score " + order,
            (severity.upper(),)
        ).fetchall()
    else:
        cves = conn.execute(
            "SELECT * FROM cves ORDER BY cvss_score " + order
        ).fetchall()
    conn.close()
    return render_template("index.html", cves=cves, sort=sort, severity=severity)