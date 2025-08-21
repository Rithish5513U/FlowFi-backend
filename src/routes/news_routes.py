from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.news import News

news_bp = Blueprint("news", __name__)

@news_bp.post("/financialInsights")
@jwt_required()
def extract_news():
    try:
        data = request.json
        preferences = data.get("preferences", [])

        if not preferences:
            return jsonify({"error": "Preferences required"}), 400

        news = News()
        news_data = news.get_everything(preferences)

        return jsonify({"message": "Success", "data": news_data}), 200

    except Exception as e:
        return jsonify({"error": f"Error extracting news: {str(e)}"}), 500