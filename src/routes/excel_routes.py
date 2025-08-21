from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.excelhandler import ExcelHandler

excel_bp = Blueprint("excel", __name__)

@excel_bp.post("/uploadExcel")
@jwt_required()
def trigger_excel():
    if 'file' not in request.files:
        return jsonify({
            "status": "error",
            "message": "No files uploaded"
        })
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            "status": "error",
            "message": "No selected file"
        })
        
    excel_handler = ExcelHandler()
    data, status_code = excel_handler.process_uploaded_file(file.stream)
    if status_code != 200:
        return jsonify({
            "status": "error",
            "message": data.get("error", "An error occurred")
        }), status_code
    
    return jsonify({
        "status": "success",
        "data": data
    })