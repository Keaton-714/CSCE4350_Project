import re
from pathlib import Path
from flask import Flask
from backend.routes.auth_routes import auth_bp # For auth_routes.py (authentication endpoint)
from backend.routes.main_routes import main_bp # For main_routes.py (authentication endpoint)

# This section of code is to find the frontend files (for now login and main)  
FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
app = Flask(
    __name__,
    template_folder=str(FRONTEND / "templates"),
    static_folder=str(FRONTEND / "static"),
)
app.secret_key = "change-me" # temporary for know 

app.register_blueprint(auth_bp) # Needed to allow for the endpoint to exist in another module (outside of app.py)
app.register_blueprint(main_bp) # Needed to allow for the endpoint to exist in another module (outside of app.py)

if __name__ == "__main__":
    app.run(debug=True)