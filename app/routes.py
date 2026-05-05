from flask import Blueprint, render_template, request
from flask_login import login_required
from .database import get_db

main = Blueprint("main", __name__)

VALID_SEVERITIES = {"critical", "high", "medium", "low"}
VALID_ORDER = {"asc": "ASC", "desc": "DESC"}

@main.route("/")
@login_required
def index():
    sort = request.args.get("sort", "desc")
    severity = request.args.get("severity", "all")

    # whitelist both user-supplied values before they touch anything
    order = VALID_ORDER.get(sort, "DESC")
    severity_clean = severity.lower() if severity.lower() in VALID_SEVERITIES else None

    conn = get_db()
    if severity_clean:
        cves = conn.execute( 
            "SELECT * FROM cves WHERE severity = ? ORDER BY cvss_score " + order, # nosec B608
            (severity_clean.upper(),)
        ).fetchall()
    else:
        cves = conn.execute( 
            "SELECT * FROM cves ORDER BY cvss_score " + order # nosec B608
        ).fetchall()
    conn.close()
    return render_template("index.html", cves=cves, sort=sort, severity=severity)