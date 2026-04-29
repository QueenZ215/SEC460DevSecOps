import os
import sqlite3
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

DB_PATH = "nightwatch.db"
API_KEY = os.getenv("NVD_API_KEY")
BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def score_to_severity(score):
    if score is None:
        return "UNKNOWN"
    if score >= 9.0: return "CRITICAL"
    if score >= 7.0: return "HIGH"
    if score >= 4.0: return "MEDIUM"
    return "LOW"

def get_score(cve):
    metrics = cve.get("metrics", {})
    for key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
        if key in metrics:
            return metrics[key][0]["cvssData"]["baseScore"]
    return None

def fetch_cves():
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=1)
    headers = {"apiKey": API_KEY} if API_KEY else {}
    params = {
        "pubStartDate": start.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "pubEndDate":   end.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "resultsPerPage": 100,
    }
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retry))
    resp = session.get(BASE_URL, params=params, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json().get("vulnerabilities", [])

def save(vulns):
    conn = sqlite3.connect(DB_PATH)
    saved = 0
    for item in vulns:
        cve = item["cve"]
        cve_id = cve["id"]
        desc = next(
            (d["value"] for d in cve.get("descriptions", []) if d["lang"] == "en"),
            "No description available."
        )
        score = get_score(cve)
        try:
            conn.execute(
                """INSERT OR IGNORE INTO cves
                   (cve_id, description, cvss_score, severity, published, last_modified)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (cve_id, desc, score, score_to_severity(score),
                 cve.get("published", ""), cve.get("lastModified", ""))
            )
            saved += 1
        except sqlite3.Error as e:
            print(f"  error on {cve_id}: {e}")
    conn.commit()
    conn.close()
    print(f"Saved {saved} of {len(vulns)} CVEs")

if __name__ == "__main__":
    print("Fetching from NVD...")
    vulns = fetch_cves()
    print(f"Found {len(vulns)} CVEs")
    save(vulns)