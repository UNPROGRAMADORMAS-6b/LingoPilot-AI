import sys
import numpy

# --- EL PARCHE DEFINITIVO (INYECCIÓN DE MÓDULO) ---
# Esto arregla el error de 'fromstring' incluso dentro de otras librerías
if not hasattr(numpy, 'fromstring'):
    numpy.fromstring = numpy.frombuffer

# Forzamos a que cualquier librería que importe numpy use nuestra versión parchada
sys.modules['numpy'] = numpy
# --------------------------------------------------

import soundcard as sc
import numpy as np

def obtener_grabadora():
    """Busca el dispositivo de Loopback para capturar audio interno."""
    try:
        # En Windows, buscamos el altavoz que permite capturar lo que suena
        speakers = sc.all_microphones(include_loopback=True)
        if not speakers:
            print("❌ No se encontraron dispositivos de Loopback.")
            return None
            
        # Usualmente el índice 0 es el altavoz principal (Realtek)
        loopback = speakers[0] 
        return loopback
    except Exception as e:
        print(f"❌ Error al detectar dispositivos: {e}")
        return None

def grabar_segmento(silencio_maximo=1.5, limite_tiempo=20):
    """
    Graba de forma inteligente: espera a que hablen, graba la frase completa,
    y se detiene automáticamente cuando detecta 'silencio_maximo' segundos de pausa.
    """
    recorder = obtener_grabadora()
    if not recorder: 
        return None
    
    fs = 16000
    chunk_size = int(fs * 0.5) # Escuchamos en bloques de medio segundo
    umbral_volumen = 0.005 # SENSIBILIDAD: Si no te detecta, bájalo. Si corta muy rápido, súbelo.
    
    audio_acumulado = []
    segundos_silencio = 0.0
    hablando = False
    
    print("👂 LingoPilot: Esperando voz...")
    
    try:
        with recorder.recorder(samplerate=fs) as mic:
            # Límite máximo de seguridad para que no grabe al infinito (ej. 20 segs)
            for _ in range(int(limite_tiempo / 0.5)):
                chunk = mic.record(numframes=chunk_size)
                mono_chunk = chunk[:, 0].astype(np.float32)
                
                # Calculamos el nivel de energía/volumen del bloque actual
                volumen = np.sqrt(np.mean(mono_chunk**2))
                
                if volumen > umbral_volumen:
                    # ¡Alguien está hablando!
                    hablando = True
                    segundos_silencio = 0.0
                    audio_acumulado.append(mono_chunk)
                    
                elif hablando:
                    # Estaba hablando, pero ahora hay silencio
                    segundos_silencio += 0.5
                    audio_acumulado.append(mono_chunk)
                    
                    if segundos_silencio >= silencio_maximo:
                        print("🔇 Fin de la frase detectado. Procesando...")
                        break # Rompemos el bucle para enviar el audio a la IA
                        
            # Si acumulamos audio, lo unimos todo en un solo archivo
            if audio_acumulado:
                return np.concatenate(audio_acumulado)
            else:
                return None
                
    except Exception as e:
        print(f"❌ Error durante la grabación: {e}")
        return None

if __name__ == "__main__":
    # Prueba rápida de funcionamiento
    print("Prueba de VAD: Pon algún audio o habla...")
    audio = grabar_segmento()
    if audio is not None:
        print(f"🎤 ¡Éxito! Capturados {len(audio)} frames de audio.")