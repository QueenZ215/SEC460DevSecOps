## Files Reviewed

- `README.md` – Gives the basic project overview.
- `requirements.txt` – Lists the Python packages needed to run the app.
- `run.py` – Starts the Flask application on port 5000.
- `app/routes.py` – Shows the main app logic for login protection, filtering, sorting, and CVE display.
- `.env.example` – Shows the environment variables needed for the app.

----

## Testing Checklist

- [ ] Valid login works
- [ ] Invalid login is rejected
- [ ] Authorized user registration works
- [ ] Unauthorized email registration is blocked
- [ ] Weak passwords are rejected
- [ ] Mismatched passwords are rejected
- [ ] Critical severity filter works
- [ ] High severity filter works
- [ ] Medium severity filter works
- [ ] Low severity filter works
- [ ] Sorting works correctly
- [ ] CVE detail pages open correctly

----

## Roadblock

While preparing to test the live Nightwatch site, the application returned a **Cloudflare 502 Bad Gateway Host Error**. The browser and Cloudflare were working, but the host showed an error, which means the issue was likely on the server/application side.

Because of this, full live testing could not be completed at that time.

----

## Contribution Summary

My contribution focused on testing preparation and documentation. I reviewed the project structure, identified the main files needed to understand how the app runs, and created a checklist for testing login, registration, filtering, sorting, password validation, and CVE detail pages.

## Additional Testing Findings

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