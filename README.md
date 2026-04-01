✈️ LingoPilot AI: Tu Copiloto de Entrevistas en Tiempo Real

LingoPilot AI es un asistente de escritorio nativo diseñado para romper la barrera del idioma en videollamadas y entrevistas técnicas. Intercepta el audio del sistema, lo transcribe, lo traduce y genera sugerencias de respuesta basadas en tu perfil profesional, todo en tiempo real y con una latencia mínima.
✨ Características Principales

    🎙️ Captura de Audio Interno: Intercepta el audio de Zoom, Google Meet o Microsoft Teams sin necesidad de micrófonos externos.

    🧠 Inferencia Ultra Rápida: Utiliza la infraestructura de Groq (Llama 3.1 & Whisper V3) para procesar respuestas en milisegundos.

    👻 Overlay Transparente: Una interfaz flotante minimalista que se mantiene siempre al frente de tus aplicaciones.

    🙈 Modo Pánico (Hotkeys): Atajos de teclado globales para ocultar/mostrar la interfaz instantáneamente (Ctrl+Alt+H).

    🧹 Limpieza Automática: Atajo para limpiar el historial de conversación (Ctrl+Alt+L).

🛠️ Stack Tecnológico

    Lenguaje: Python 3.11

    Interfaz Gráfica: PyQt5 (Nativa y ligera)

    Procesamiento de Voz: Whisper-large-v3 (via Groq API)

    Lógica de IA: Llama-3.1-8b-instant

    Manejo de Audio: Soundcard (Windows Media Foundation)

    Detección de Silencio (VAD): Algoritmo personalizado basado en Numpy para optimizar costos de API.


    🚀 Instalación y Uso
1. Clonar el repositorio
git clone https://github.com/UNPROGRAMADORMAS-6b/LingoPilot-AI.git
cd LingoPilot-AI
2. Configurar entorno virtual
python -m venv venv
source venv/Scripts/activate  # En Windows
pip install -r requirements.txt
3. Variables de Entorno
GROQ_API_KEY=tu_api_key_aqui
4. Personaliza tu Perfil
Edita el archivo my_cv.txt con tu experiencia, stack tecnológico y logros. LingoPilot usará esta información para responder por ti.


⌨️ Atajos de Teclado
Acción  Atajo
Ocultar / Mostrar Ventana   Ctrl + Alt + H
Limpiar Texto en Pantalla   Ctrl + Alt + L

🤝 Contribuciones

¡Las contribuciones son lo que hacen a la comunidad de código abierto un lugar increíble! Cualquier mejora en la latencia o en la UI es bienvenida.

    Haz un Fork del proyecto.

    Crea tu Feature Branch (git checkout -b feature/AmazingFeature).

    Haz un Commit de tus cambios (git commit -m 'Add some AmazingFeature').

    Haz un Push a la rama (git push origin feature/AmazingFeature).

    Abre un Pull Request.

    📄 Licencia

    Distribuido bajo la licencia MIT. Vea LICENSE para más información.
    
