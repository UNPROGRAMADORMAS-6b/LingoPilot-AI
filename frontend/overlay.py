import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QDesktopWidget
from PyQt5.QtCore import Qt

class LingoPilotOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 1. Configuración de Ventana Fantasma
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 2. Diseño (Layout)
        self.layout = QVBoxLayout()
        self.label_pregunta = QLabel("Esperando audio...")
        self.label_respuesta = QLabel("")
        
        # --- LA MAGIA PARA QUE NO SE VAYA A LA DERECHA ---
        # Obligamos al texto a saltar a la siguiente línea si es muy largo
        self.label_pregunta.setWordWrap(True)
        self.label_respuesta.setWordWrap(True)
        
        # Estilo CSS más refinado
        estilo_base = "color: white; font-size: 18px; font-weight: bold; background-color: rgba(0, 0, 0, 180); border-radius: 10px; padding: 12px;"
        self.label_pregunta.setStyleSheet(estilo_base + "color: #00FFCC;") 
        self.label_respuesta.setStyleSheet(estilo_base + "font-size: 20px; border: 2px solid #FFCC00;") 
        
        self.layout.addWidget(self.label_pregunta)
        self.layout.addWidget(self.label_respuesta)
        self.setLayout(self.layout)

        # 3. Posición inicial
        self.centrar_ventana()

    def centrar_ventana(self):
        # Fijamos un ANCHO MÁXIMO para que tus ojos no se muevan de lado a lado
        ancho_ventana = 700 
        self.setFixedWidth(ancho_ventana)
        
        # Obtenemos la resolución de TU pantalla automáticamente
        pantalla = QDesktopWidget().screenGeometry()
        x_centro = int((pantalla.width() - ancho_ventana) / 2)
        y_arriba = 20 # A 20 píxeles del borde superior (justo pegado a tu cámara)
        
        # Movemos la ventana a ese punto exacto
        self.move(x_centro, y_arriba)

    def actualizar_texto(self, pregunta, respuesta):
        self.label_pregunta.setText(f"🤔 Entrevistador: {pregunta}")
        self.label_respuesta.setText(f"💡 Sugerencia:\n{respuesta}")
        
        # Hacemos que la ventana crezca hacia ABAJO si hay mucho texto, no hacia los lados
        self.adjustSize()