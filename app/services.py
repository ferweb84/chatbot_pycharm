# services.py
from decouple import config
from twilio.rest import Client
from app.models import User
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta, timezone
from .db import save_user

# Cargar las credenciales de Twilio desde el archivo .env
TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER")

client = MongoClient("mongodb+srv://ferwebreyna:5ltHR6wLRindhku9@cluster0.yxbtd6i.mongodb.net/")
db = client["chatbot_db"]

# Clave secreta para firmar y verificar los tokens
SECRET_KEY = config("SECRET_KEY")

def create_user(name: str, age: int):
    new_user = User(name=name, age=age)
    save_user(new_user)

def save_message(username: str, input_text: str, response_text: str):
    db.messages.insert_one({"username": username, "input_text": input_text, "response_text": response_text})

def get_current_user(token: str) -> User:
    try:
        # Decodificar el token y obtener la información del usuario
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload["sub"]  # El nombre de usuario se guarda como "sub" en el token

        # Buscar el usuario en la base de datos (esto puede variar según tu implementación)
        user = db.users.find_one({"username": username})
        if user:
            return User(username=user["username"])  # Devuelve el objeto User si se encuentra el usuario
        else:
            raise Exception("Usuario no encontrado")
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")

def generate_jwt(username: str) -> str:
    # Crear un token JWT con el nombre de usuario como sub
    expiration_time = datetime.utcnow() + timedelta(days=1)  # Token válido por 1 día
    payload = {"sub": username, "exp": expiration_time}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token.decode("utf-8")  # Devuelve el token como una cadena UTF-8


def generate_response(input_text: str) -> str:
    # Aquí puedes implementar la lógica para enviar la entrada a OpenAI GPT-3 y obtener una respuesta
    # Por ejemplo, puedes usar la API de OpenAI GPT-3

    # response = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt=input_text,
    #     max_tokens=150
    # )

    # Temporalmente, devuelve una respuesta de marcador de posición
    return "This is a placeholder response."

def send_twilio_message(phone_number: str, message_text: str):
    # Aquí puedes implementar la lógica para enviar mensajes a través de Twilio
    # Utiliza la biblioteca Twilio
    # Asegúrate de tener tus credenciales de Twilio configuradas correctamente
    # Ejemplo básico (necesitarás instalar la biblioteca Twilio usando pip install twilio)
    from twilio.rest import Client

    # Tus credenciales de Twilio
    TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER")

    # Crear un cliente Twilio
    client = Client(account_sid, auth_token)

    # Enviar mensaje
    message = client.messages.create(
        body=message_text,
        from_=twilio_phone_number,
        to=phone_number
    )
    print(f"Message sent successfully. SID: {message.sid}")

def send_twilio_message(user: User, message: str):
    try:
        message = client.messages.create(
            to=user.phone_number,  # El número de teléfono del usuario
            from_=twilio_phone_number,
            body=message
        )
        return True, "Mensaje enviado correctamente."
    except Exception as e:
        return False, f"Error al enviar el mensaje: {str(e)}"
