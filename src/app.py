from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import jwt
from routes.auth_routes import auth_bp
from routes.news_routes import news_bp
from routes.faq_routes import faq_bp
from routes.excel_routes import excel_bp
from routes.portal_routes import portal_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
jwt.init_app(app)
CORS(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(news_bp, url_prefix="/news")
app.register_blueprint(faq_bp, url_prefix="/faq")
app.register_blueprint(excel_bp, url_prefix="/excel")
app.register_blueprint(portal_bp, url_prefix="/portal")

# Home Route
@app.route("/")
def home():
    return "Welcome to FlowFi!"

if __name__ == "__main__":
    app.run(debug=True, port=8080)