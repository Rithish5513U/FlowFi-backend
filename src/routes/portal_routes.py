from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.portalService import fetchStocks, save_user
from services.userService import fetchUser
from models.portalSchema import Asset

portal_bp = Blueprint("portal", __name__)

@portal_bp.get("/stockDetails")
@jwt_required()
def stockDetails():
    try:
        stocks = fetchStocks()
        
        if stocks == []:
            return jsonify({
                "status": "error",
                "message": "Error occurred while fetching stocks"
            })
            
        stocks = [stock.model_dump() for stock in stocks]
        
        # Assuming you want to return the stocks data as JSON
        return jsonify({
            "status": "Success",
            "stocks": stocks
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        })
        
@portal_bp.get("/getAssets")
@jwt_required()
def getAssets():
    try:
        email = get_jwt_identity()
        user = fetchUser(email)
        
        if not user:
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404
            
        assets = [asset.model_dump() for asset in user.assets]
        
        symbols = [asset.symbol for asset in user.assets]
        stocks = fetchStocks(symbols)
        
        return jsonify({
            "status": "success",
            "assets": assets,
            "virtualBalance": user.virtualBalance,
            "currentAssetValue": stocks.lastPrice
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
        
@portal_bp.put("/addAssets")
@jwt_required()
def addAsset():
    try:
        user_email = get_jwt_identity()
        
        data = request.get_json()
        symbol = data.get("symbol")
        price = data.get("price")
        quantity = data.get("quantity")

        if not all([symbol, price, quantity]):
            return jsonify({
                "status": "error",
                "message": "symbol, price, and quantity are required"
            }), 400

        user = fetchUser(user_email)
        if not user:
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404
            
        if user.virtualBalance < price * quantity:
            return jsonify({
                "status": "error",
                "message": "Insufficient balance"
            }), 400

        new_asset = Asset(symbol=symbol, price=price, quantity=quantity)
        user.assets.append(new_asset)
        
        # Deduct the cost from the user's virtual balance
        user.virtualBalance -= price * quantity

        save_user(user)

        return jsonify({
            "status": "Success",
            "message": "Asset added successfully",
            "assets": [asset.model_dump() for asset in user.assets]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
        
@portal_bp.put("/removeAssets")
@jwt_required()
def removeAsset():
    try:
        user_email = get_jwt_identity()
        
        data = request.get_json()
        symbol = data.get("symbol")
        price = data.get("price")
        quantity = data.get("quantity")

        if not all([symbol, price, quantity]):
            return jsonify({
                "status": "error",
                "message": "symbol, price, and quantity are required"
            }), 400

        user = fetchUser(user_email)
        if not user:
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404
            
        asset_to_remove = next((asset for asset in user.assets if asset.symbol == symbol), None)
        
        if not asset_to_remove:
            return jsonify({
                "status": "error",
                "message": f"Asset {symbol} not found"
            }), 404
        
        # Check if the quantity to remove is valid
        if asset_to_remove.quantity < quantity:
            return jsonify({
                "status": "error",
                "message": f"Not enough quantity of {symbol} to remove"
            }), 400
        
        # Update the asset quantity
        asset_to_remove.quantity -= quantity
        
        # If the quantity becomes zero, remove the asset from the list
        if asset_to_remove.quantity == 0:
            user.assets.remove(asset_to_remove)
        
        # Add the proceeds back to the user's virtual balance
        user.virtualBalance += price * quantity

        save_user(user)

        return jsonify({
            "status": "Success",
            "message": f"Asset {symbol} removed successfully",
            "assets": [asset.model_dump() for asset in user.assets]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500