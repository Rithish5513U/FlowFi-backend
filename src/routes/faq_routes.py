from flask import Blueprint, request, jsonify
from services.faq_chatbot import FAQChatBot
from flask_jwt_extended import jwt_required

faq_bp = Blueprint("faq", __name__)

@faq_bp.post("/faqHandler")
@jwt_required()
def faq_handler():
    data = request.json
    user_query = data.get("user_query")

    if not user_query:
        return jsonify({"error": "Please provide a user query"}), 400
    
    chatbot = FAQChatBot()
    response = chatbot.get_financial_insight(user_query)
    
    return jsonify(response)
