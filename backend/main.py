import sys
import os
import time
import keyboard  # ¡NUEVO! Para el modo pánico
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

# Añadimos las rutas para que Python encuentre todo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos nuestros módulos
import audio_handler
from ai_engine import transcribir_audio, procesar_con_ia
from frontend.overlay import LingoPilotOverlay
from scipy.io.wavfile import write

# --- SISTEMA DE ATAJOS (HOTKEYS) ---
def configurar_atajos(ventana):
    ventana.esta_visible = True

    def toggle_visibilidad():
        if ventana.esta_visible:
            ventana.hide()
            ventana.esta_visible = False
            print("🙈 MODO PÁNICO: LingoPilot Oculto.")
        else:
            ventana.show()
            ventana.esta_visible = True
            # Forzamos que la ventana vuelva a estar al frente de todo
            ventana.raise_()
            ventana.activateWindow()
            print("👀 LingoPilot Visible.")

    def limpiar_texto():
        ventana.actualizar_texto("Esperando audio...", "")
        print("🧹 Texto limpiado.")

    # Registramos combinaciones seguras que no chocan con tu PC
    keyboard.add_hotkey('ctrl+alt+h', toggle_visibilidad) # H de Hide/Ocultar
    keyboard.add_hotkey('ctrl+alt+l', limpiar_texto)      # L de Limpiar

# --- EL TRABAJADOR DE FONDO (BACKEND) ---
class LingoWorker(QThread):
    # Esta señal enviará la (pregunta, respuesta) a la interfaz
    nueva_respuesta = pyqtSignal(str, str)

    def run(self):
        archivo_temp = "temp_audio.wav"
        print("🚀 LingoPilot Backend iniciado...")
        
        while True:
            # 1. Graba inteligentemente (espera a que hablen y para al detectar silencio)
            audio_data = audio_handler.grabar_segmento()
            
            if audio_data is not None:
                write(archivo_temp, 16000, audio_data)
                
                # 2. Transcribe (Voz a Texto)
                texto_detectado = transcribir_audio(archivo_temp)
                
                # Si detecta texto válido
                if hasattr(texto_detectado, 'text'):
                    texto_limpio = texto_detectado.text
                elif isinstance(texto_detectado, str):
                    texto_limpio = texto_detectado
                else:
                    texto_limpio = ""

                if texto_limpio and len(texto_limpio.strip()) > 5:
                    print(f"🎤 Escuchado: {texto_limpio}")
                    
                    # 3. Procesa con IA (Sugerencia)
                    respuesta_ia = procesar_con_ia(texto_limpio)
                    
                    # 4. Enviamos los datos a la interfaz de forma segura
                    self.nueva_respuesta.emit(texto_limpio, respuesta_ia)
                
                # Limpiar rastro
                if os.path.exists(archivo_temp):
                    os.remove(archivo_temp)
            
            time.sleep(0.1) # Respiro para el procesador

# --- LA APLICACIÓN PRINCIPAL (FRONTEND) ---
def ejecutar_lingopilot():
    app = QApplication(sys.argv)
    
    # Creamos la ventana flotante
    ventana = LingoPilotOverlay()
    ventana.show()
    
    # Configuramos los atajos de teclado
    configurar_atajos(ventana)
    
    # Creamos y lanzamos el hilo de audio
    worker = LingoWorker()
    worker.nueva_respuesta.connect(ventana.actualizar_texto)
    worker.start()
    
    print("✅ ¡LingoPilot AI activo! Atajos: [Ctrl+Alt+H] Ocultar/Mostrar | [Ctrl+Alt+L] Limpiar texto")
    sys.exit(app.exec_())

if __name__ == "__main__":
    ejecutar_lingopilot()