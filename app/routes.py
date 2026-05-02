from flask import Blueprint, render_template, request
from .database import get_db

main = Blueprint("main", __name__)

VALID_SEVERITIES = {"critical", "high", "medium", "low"}


@main.route("/")
def index():
    sort = request.args.get("sort", "desc")
    severity = request.args.get("severity", "all")

    # whitelist both user-supplied values before they touch anything
    order = "DESC" if sort == "desc" else "ASC"
    severity_clean = (
        severity.lower() if severity.lower() in VALID_SEVERITIES else None
    )

    conn = get_db()

    if severity_clean:
        cves = conn.execute(
            "SELECT * FROM cves WHERE severity = ? ORDER BY cvss_score "
            + order,
            (severity_clean.upper(),),
        ).fetchall()
    else:
        cves = conn.execute(
            "SELECT * FROM cves ORDER BY cvss_score " + order
        ).fetchall()

    critical_count = conn.execute(
        "SELECT COUNT(*) FROM cves WHERE severity = 'CRITICAL'"
    ).fetchone()[0]

    high_count = conn.execute(
        "SELECT COUNT(*) FROM cves WHERE severity = 'HIGH'"
    ).fetchone()[0]

    medium_count = conn.execute(
        "SELECT COUNT(*) FROM cves WHERE severity = 'MEDIUM'"
    ).fetchone()[0]

    low_count = conn.execute(
        "SELECT COUNT(*) FROM cves WHERE severity = 'LOW'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        cves=cves,
        sort=sort,
        severity=severity,
        critical_count=critical_count,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
    )