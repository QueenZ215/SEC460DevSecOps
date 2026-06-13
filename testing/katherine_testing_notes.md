## Files Reviewed

- `README.md` – Gives the basic project overview.
- `requirements.txt` – Lists the Python packages needed to run the app.
- `run.py` – Starts the Flask application on port 5000.
- `app/routes.py` – Shows the main app logic for login protection, filtering, sorting, and CVE display.
- `.env.example` – Shows the environment variables needed for the app.

----

## Testing Checklist

Unauthorized email registration is blocked [x]
Weak passwords are rejected [x]
Mismatched passwords are rejected [x]
Critical severity filter works [x]
High severity filter works [x]
Medium severity filter works [x]
Low severity filter works  [x]
Sorting works correctly [x]
CVE detail pages open correctly [x]


# ***UPDATE: The checked items above were verified during Patricia's testing and documentation.**

## Roadblock

While preparing to test the live Nightwatch site, the application returned a **Cloudflare 502 Bad Gateway Host Error**. The browser and Cloudflare were working, but the host showed an error, which means the issue was likely on the server/application side.

Because of this, full live testing could not be completed at that time.

----

## Contribution Summary

My contribution focused on testing preparation and documentation. I reviewed the project structure, identified the main files needed to understand how the app runs, and created a checklist for testing login, registration, filtering, sorting, password validation, and CVE detail pages.
-----------------------------------------

## Additional Testing Findings                       **RESOLVED**

Local Environment Setup:

The Nightwatch repository was cloned successfully and dependencies were installed using:

pip install -r requirements.txt

The Flask application launched successfully using:

python run.py

and was accessible locally at:

http://127.0.0.1:5000

Database Initialization Issue

While attempting to create a local user account using:

python scripts/add_user.py Katherine.Ayala@bellevuecollege.edu [password]

the following error occurred:

sqlite3.OperationalError: no such table: users

This indicates that the local database had not been initialized before running the user creation script. As a result, local authentication testing could not be completed until the database setup issue is resolved.

Live Login Testing

Testing of the live application login was attempted using the provided credentials. Login was unsuccessful, and another team member reported experiencing the same issue. This finding was documented for follow-up investigation.

--------------------------------------

## Additional Security and Access Control Testing

==================================================
TEST 1: LIVE APPLICATION ACCESS
==================================================

Successfully registered an authorized account through the Nightwatch registration process and logged into the live application.

## Result:

- Login was successful.
- Dashboard loaded correctly.
- CVE data was displayed as expected.

## Observation:

- Authentication system is functioning correctly for authorized users.

**************************************************

==================================================
TEST 2: LOGOUT TESTING
==================================================

Tested the sign out functionality.

## Result:

- User session ended successfully.
- Application returned to the login page.

## Observation:

- Logout functionality is working correctly.

**************************************************

==================================================
TEST 3: ACCESS CONTROL TESTING
==================================================

Attempted to access a protected Nightwatch dashboard URL while logged out:

https://cve.zoec.me/?sort=desc&severity=critical

## Result:

- Application redirected to the login page.

## Observation:

- Unauthorized users cannot directly access protected dashboard content.
- Authentication controls appear to be functioning correctly.

**************************************************

==================================================
TEST 4: INCOGNITO SESSION TESTING
==================================================

Opened the application in a new Incognito browser session with no active login.

## Result:

- Application required authentication before allowing access.

## Observation:

- Access control is enforced server-side and is not dependent on an existing browser session.

**************************************************

==================================================
TEST 5: INVALID SEVERITY VALUE
==================================================

## Tested:

https://cve.zoec.me/?severity=banana

## Result:

- Application continued operating normally.
- No error or crash occurred.

## Observation:

- Invalid severity values appear to be handled safely.

**************************************************

==================================================
TEST 6: INVALID SORT VALUE
==================================================

## Tested:

https://cve.zoec.me/?sort=banana

## Result:

- Application remained functional.
- Page displayed the text "sorted bananaending by score."

## Observation:

- Application does not crash when receiving unexpected sort values.
- A minor display/input-handling issue was identified.
- No security impact was observed.