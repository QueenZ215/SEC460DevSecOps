from flask import Blueprint, render_template, request
from .database import get_db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    sort = request.args.get("sort", "desc")
    severity = request.args.get("severity", "all")

    # whitelist -- never let user input touch the query string directly
    order = "DESC" if sort == "desc" else "ASC"
    severity = severity.upper() if severity in ("critical", "high", "medium", "low") else None

    conn = get_db()
    if severity:
        cves = conn.execute(
            "SELECT * FROM cves WHERE severity = ? ORDER BY cvss_score " + order,
            (severity,)
        ).fetchall()
    else:
        cves = conn.execute(
            "SELECT * FROM cves ORDER BY cvss_score " + order
        ).fetchall()
    conn.close()
    return render_template("index.html", cves=cves, sort=sort, severity=request.args.get("severity", "all"))