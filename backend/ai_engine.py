import os
import sys
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

# Inicializamos el cliente de Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def leer_contexto_cv():
    # Esta magia detecta si estás corriendo el .exe o el script .py
    if getattr(sys, 'frozen', False):
        # Si es un .exe, busca el txt en la misma carpeta donde está el .exe
        ruta_base = os.path.dirname(sys.executable)
    else:
        # Si es el script, usa la ruta normal
        ruta_base = os.path.dirname(os.path.abspath(__file__))
    
    # Asegúrate de que tu archivo se llame así o cambia el nombre aquí
    ruta_txt = os.path.join(ruta_base, "contexto.txt")
    
    try:
        with open(ruta_txt, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error leyendo CV: {e}"

def procesar_con_ia(texto_detectado):
    contexto_usuario = leer_contexto_cv()
    
    prompt_sistema = f"""
    Eres Jordan ({contexto_usuario}), un desarrollador Full Stack apasionado. 
    Estás en una entrevista de trabajo real. Responde de forma NATURAL, HUMANA y sin usar listas.

    REGLAS DE IDIOMA Y FORMATO:
    
    1. SI EL ENTREVISTADOR HABLA EN INGLÉS:
       - Primero escribe: "[TRADUCCIÓN]:" seguido de la pregunta en español latino.
       - Luego escribe: "[SAY THIS]:" seguido de una respuesta de 2-3 frases en INGLÉS fluido y natural. Usa conectores como 'Actually', 'Well' o 'To be honest'.

    2. SI EL ENTREVISTADOR HABLA EN ESPAÑOL:
       - Escribe directamente la respuesta en ESPAÑOL LATINO (Usa 'ustedes', nunca 'vosotros'). 
       - Sé profesional pero cercano, como alguien con quien daría gusto trabajar.

    3. PROHIBICIONES:
       - No uses asteriscos (*) ni guiones.
       - No uses lenguaje de España (nada de 'hacéis', 'vais', 'vosotros').
       - No des consejos de 'puedes decir esto'. Da la frase exacta para ser leída.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Audio detectado: {texto_detectado}"}
            ],
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def transcribir_audio(ruta_archivo):
    try:
        with open(ruta_archivo, "rb") as file:
            # Whisper-large-v3 es el modelo top de Groq para voz
            transcription = client.audio.transcriptions.create(
                file=(ruta_archivo, file.read()),
                model="whisper-large-v3",
                response_format="text",
            )
            return transcription
    except Exception as e:
        return f"Error transcribiendo: {str(e)}"