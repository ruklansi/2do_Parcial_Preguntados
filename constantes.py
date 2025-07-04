"""Constantes globales para el juego Preguntados - Dragon Ball.

Este módulo define las constantes utilizadas en el juego, incluyendo colores, dimensiones de la pantalla,
estados del juego, configuraciones iniciales y parámetros de las dificultades. Estas constantes son utilizadas
por otros módulos para mantener consistencia en la configuración del juego.
"""

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (150, 150, 150)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Estados del juego
MENU = "menu"
JUEGO = "juego"
GAME_OVER = "game_over"
PUNTAJES = "puntajes"
CONFIG = "config"
FIN_JUEGO = "fin_juego"
CONFIG_JUEGO = "config_juego"
INICIO_JUEGO = "inicio_juego"

# Configuraciones iniciales
PUNTAJE_INICIAL = 0
VIDAS_INICIALES = 3
CORRECTAS_SEGUIDAS_INICIAL = 0
VOLUMEN_INICIAL = 0.5
LIMITE_NOMBRE = 20
X2_USADO_INICIAL = False
DOBLE_CHANCE_USADO_INICIAL = False
PASAR_USADO_INICIAL = False
FPS = 30

# Dificultades
DIFICULTADES = {
    "FACIL": {"puntos_aciertos": 15, "puntos_errores": -3, "vidas": 5, "tiempo_pregunta": 45},
    "MEDIO": {"puntos_aciertos": 10, "puntos_errores": -5, "vidas": 3, "tiempo_pregunta": 30},
    "DIFICIL": {"puntos_aciertos": 20, "puntos_errores": -10, "vidas": 2, "tiempo_pregunta": 20}
}