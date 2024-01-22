from pymongo import MongoClient
from .models import User

client = MongoClient("mongodb+srv://ferwebreyna:5ltHR6wLRindhku9@cluster0.yxbtd6i.mongodb.net/")
db = client["chatbot_db"]
def get_mongo_db():
    # Establece la conexión a MongoDB
    client = MongoClient("mongodb+srv://ferwebreyna:5ltHR6wLRindhku9@cluster0.yxbtd6i.mongodb.net/")  # Cambia la URL según tu configuración
    # Selecciona la base de datos
    db = client["chatbot_db"]  # Cambia por el nombre de tu base de datos
    return db
def save_user(user: User):
    user_data = user.dict()
    db.users.insert_one(user_data)