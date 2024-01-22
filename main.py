from fastapi import FastAPI
from app.routers import router as message_router
from app.services import get_current_user, generate_response, save_message, send_twilio_message

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(message_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8003)
