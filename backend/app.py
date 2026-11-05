from pathlib import Path
from flask import Flask
from backend.routes.auth_routes import auth_bp 
from backend.routes.main_routes import main_bp 
from backend.routes.part_routes import part_bp
from backend.routes.store_routes import store_bp 

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
app.register_blueprint(part_bp)
app.register_blueprint(store_bp)

if __name__ == "__main__":
    app.run(debug=True)