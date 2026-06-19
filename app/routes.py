import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .database import get_db

main = Blueprint("main", __name__)

VALID_SEVERITIES = {"critical", "high", "medium", "low"}
VALID_ORDER = {"asc": "ASC", "desc": "DESC"}

@main.route("/")
@login_required
def index():
    sort = request.args.get("sort", "desc")
    severity = request.args.get("severity", "all")
    relevant = request.args.get("relevant") == "1"

    # whitelist both user-supplied values before they touch anything
    order = VALID_ORDER.get(sort, "DESC")
    severity_clean = severity.lower() if severity.lower() in VALID_SEVERITIES else None

    conn = get_db()

    keywords = []
    if relevant:
        keywords = [row["keyword"] for row in conn.execute(
            "SELECT keyword FROM user_keywords WHERE user_id = ?", (current_user.id,)
        ).fetchall()]
        if not keywords:
            flash("Add keywords first to use the relevant-to-me filter.")
            relevant = False

    where, params = [], []
    if severity_clean:
        where.append("severity = ?")
        params.append(severity_clean.upper())
    if relevant and keywords:
        where.append("(" + " OR ".join(["description LIKE ?"] * len(keywords)) + ")")
        params.extend(f"%{kw}%" for kw in keywords)

    query = "SELECT * FROM cves"
    if where:
        query += " WHERE " + " AND ".join(where)
    query += " ORDER BY cvss_score " + order  # nosec B608 - order whitelisted above

    cves = conn.execute(query, params).fetchall()
    conn.close()
    return render_template("index.html", cves=cves, sort=sort, severity=severity, relevant=relevant)


@main.route("/keywords")
@login_required

def keywords():
    conn = get_db()
    rows = conn.execute(
        "SELECT id, keyword FROM user_keywords WHERE user_id = ? ORDER BY keyword",
        (current_user.id,)
    ).fetchall()
    conn.close()
    return render_template("keywords.html", keywords=rows)


@main.route("/keywords/add", methods=["POST"])
@login_required
def add_keyword():
    keyword = request.form.get("keyword", "").strip().lower()
    if keyword:
        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO user_keywords (user_id, keyword) VALUES (?, ?)",
                (current_user.id, keyword)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            flash(f'"{keyword}" is already on your list.')
        conn.close()
    return redirect(url_for("main.keywords"))


@main.route("/keywords/delete/<int:keyword_id>", methods=["POST"])
@login_required
def delete_keyword(keyword_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM user_keywords WHERE id = ? AND user_id = ?",
        (keyword_id, current_user.id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("main.keywords"))