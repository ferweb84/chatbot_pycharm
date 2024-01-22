
# app/routers.py
from fastapi import APIRouter, Depends
from app.models import Message, User
from app.services import generate_response, save_message, get_current_user, send_twilio_message

router = APIRouter()

@router.post("/process-message")
async def process_message(message: Message, current_user: User = Depends(get_current_user)):
    input_text = message.text

    # Aquí utilizamos la lógica de GPT-3
    response_text = generate_response(input_text)

    save_message(current_user.username, input_text, response_text)

    return {"user": current_user.username, "input_text": input_text, "response_text": response_text}
