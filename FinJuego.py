"""Módulo para la pantalla de fin de juego en Preguntados - Dragon Ball.

Este módulo gestiona la interfaz de fin de juego, permitiendo al usuario ingresar su nombre para guardar
el resultado de la partida y reiniciar el juego.
"""

from constantes import *
from funciones import *

def mostrar_fin_juego(pantalla, eventos, datos_juego, fuente, fuente_game_over):
    """
    Muestra la pantalla de fin de juego para ingresar el nombre.
    
    Args:
        pantalla: Superficie donde se dibuja.
        eventos: Lista de eventos de Pygame.
        datos_juego: Diccionario con el estado del juego.
        fuente: Fuente para el texto.
        fuente_game_over: No usada en este estado.
    
    Returns:
        str: Estado actualizado del juego.
    """
    pantalla.blit(datos_juego["gif_frames"][datos_juego["gif_frame_index"]], (0, 0))
    fondo_fin = pygame.Surface((700, 150))
    fondo_fin.set_alpha(200)
    fondo_fin.fill(GRIS)
    pantalla.blit(fondo_fin, (50, 50))
    mensaje = "¡Felicidades! Respondiste todas las preguntas" if datos_juego["juego_terminado_por_preguntas"] else "Fin del juego. Ingresa tu nombre:"
    pantalla.blit(fuente.render(mensaje, True, NEGRO), (50, 50))
    pantalla.blit(fuente.render(datos_juego["entrada_nombre"], True, NEGRO), (50, 100))
    dibujar_boton(pantalla, fuente, "Guardar", 300, 500, 200, 50, GRIS, VERDE, 
                  lambda: datos_juego.update(guardar_y_reiniciar(datos_juego)))

    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN and datos_juego["entrada_nombre"].strip() and datos_juego["entrada_nombre"].isalpha():
                datos_juego = guardar_y_reiniciar(datos_juego)
                datos_juego["pregunta_actual"] = None
                datos_juego["opciones"] = []
                datos_juego["respuesta_correcta"] = ""
                datos_juego["opciones_restantes"] = []
                datos_juego["doble_chance_activo"] = False
                datos_juego["mensaje_comodin"] = ""
                datos_juego["tiempo_inicio"] = 0
            elif evento.key == pygame.K_BACKSPACE:
                datos_juego["entrada_nombre"] = datos_juego["entrada_nombre"][:-1]
            elif len(datos_juego["entrada_nombre"]) < LIMITE_NOMBRE and evento.unicode.isalpha():
                datos_juego["entrada_nombre"] += evento.unicode

    return datos_juego["estado"]