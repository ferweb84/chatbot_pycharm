# app/gpt3_integration.py
import openai

def gpt3_generate_response(input_text: str) -> str:
    # Utiliza tu clave de API de OpenAI
    openai.api_key = config("OPENAI_API_KEY")

    # Lógica para enviar la entrada a OpenAI GPT-3 y obtener una respuesta
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=input_text,
        max_tokens=150
    )

    return response.choices[0].text.strip()
