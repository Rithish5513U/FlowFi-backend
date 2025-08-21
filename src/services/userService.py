from models.userModel import User
from extensions import db, pwd_context
from flask_jwt_extended import create_access_token
from datetime import timedelta

users = db['users']
transactions = db['transactions']

def create_user(user: User):
    """
    Inputs:
        user: User object
    Outputs:
        response: dict
        {
            "success" : bool,
            "message" : str
        }
    """
    try:
        found = users.find_one({"email": user.email})
        if found:
            return {
                "success" : False,
                "message" : "User already exists"
            }
        hashed_password = pwd_context.hash(user.password)
        users.insert_one({
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "assets": None,
            "virtualBalance": 10000
        })
        return {
            "success" : True,
            "message" : "User created"
        }
    except Exception as e:
        return {
            "success" : False,
            "message" : f"Error detected : {str(e)}"
        }
        
def verify_user(email, password):
    """
    Inputs:
        email: str
        password: str
    Outputs:
        response: dict
        {
            "success" : bool,
            "message" : str
        }
    """
    try:
        match = users.find_one({"email": email})
        if not match:
            return {
                "success" : False,
                "message" : "User not found"
            }
        if not pwd_context.verify(password, match["password"]):
            return {
                "success" : False,
                "message" : "Password incorrect"
            }
        token = create_access_token(identity=email, expires_delta=timedelta(hours=1))
        
        return {
            "success" : True,
            "message" : "User verified",
            "token" : token
        }
            
    except Exception as e:
        return {
            "success" : False,
            "message" : f"Error detected : {str(e)}"
        }
        
def fetchUser(email):
    """
    Inputs:
        email: str
    Outputs:
        User
    """
    try:
        match = users.find_one({"email": email})
        if not match:
            return {
                "success" : False,
                "message" : "User not found"
            }
        return User(**match)
    
    except Exception as e:
        return {
            "success" : False,
            "message" : f"Error detected : {str(e)}"
        }