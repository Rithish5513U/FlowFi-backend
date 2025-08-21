from pymongo import MongoClient
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from config import Config

mongo = MongoClient(Config.MONGO_URI)
db = mongo.get_database('test')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
jwt = JWTManager()