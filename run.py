import os
from werkzeug.middleware.proxy_fix import ProxyFix
from app import create_app

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

if __name__ == "__main__":
    app.run(host=os.getenv("FLASK_RUN_HOST", "0.0.0.0"), port=5000 ) # nosec B104 - nginx proxy manager reaches this app across the DMZ subnet (10.3.0.20 -> 10.3.0.90), not localhost; bind address is overridable via FLASK_RUN_HOST in production

