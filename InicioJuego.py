"""Módulo para la pantalla de inicio del juego en Preguntados - Dragon Ball.

Este módulo gestiona la pantalla de inicio con una cuenta regresiva antes de comenzar el juego,
inicializando las variables del juego y mostrando una animación de fondo.
"""

from constantes import *
from funciones import *

def mostrar_inicio_juego(pantalla, eventos, datos_juego, fuente, fuente_game_over):
    """
    Muestra la animación de inicio con cuenta regresiva.
    
    Args:
        pantalla: Superficie donde se dibuja.
        eventos: Lista de eventos de Pygame.
        datos_juego: Diccionario con el estado del juego.
        fuente: No usada en este estado.
        fuente_game_over: Fuente para el texto de la animación.
    
    Returns:
        str: Estado actualizado del juego.
    """
    now = pygame.time.get_ticks()
    pantalla.blit(datos_juego["gif_frames"][datos_juego["gif_frame_index"]], (0, 0))
    if now - datos_juego["cuenta_regresiva_tiempo"] > 1000:
        datos_juego["cuenta_regresiva"] -= 1
        datos_juego["cuenta_regresiva_tiempo"] = now
    if datos_juego["cuenta_regresiva"] <= 0:
        datos_juego["estado"] = JUEGO
        datos_juego["puntaje"] = PUNTAJE_INICIAL
        datos_juego["vidas"] = DIFICULTADES[datos_juego["dificultad_seleccionada"]]["vidas"]
        datos_juego["correctas_seguidas"] = CORRECTAS_SEGUIDAS_INICIAL
        datos_juego["bomba_usada"] = False
        datos_juego["x2_usado"] = X2_USADO_INICIAL
        datos_juego["doble_chance_usado"] = DOBLE_CHANCE_USADO_INICIAL
        datos_juego["pasar_usado"] = PASAR_USADO_INICIAL
        datos_juego["juego_terminado_por_preguntas"] = False
        datos_juego["pregunta_actual"] = None
        datos_juego["opciones"] = []
        datos_juego["respuesta_correcta"] = ""
        datos_juego["doble_chance_activo"] = False
        datos_juego["opciones_restantes"] = []
        datos_juego["mensaje_comodin"] = ""
        datos_juego["tiempo_inicio"] = 0
    else:
        fondo_animacion = pygame.Surface((400, 200))
        fondo_animacion.set_alpha(200)
        fondo_animacion.fill(GRIS)
        pantalla.blit(fondo_animacion, (200, 200))
        texto_animacion = fuente_game_over.render(f"El juego comienza en {datos_juego['cuenta_regresiva']}", True, NEGRO)
        pantalla.blit(texto_animacion, (200 + (400 - texto_animacion.get_width()) // 2, 250))
    
    return datos_juego["estado"]