"""Módulo para la pantalla de puntajes altos en Preguntados - Dragon Ball.

Este módulo gestiona la interfaz de la pantalla de puntajes altos, mostrando los 10 mejores resultados
guardados en el archivo partidas.json.
"""

from constantes import *
from funciones import *

def mostrar_puntajes(pantalla, eventos, datos_juego, fuente, fuente_game_over):
    """
    Muestra la pantalla de puntajes altos.
    
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
    fondo_puntajes = pygame.Surface((700, 400))
    fondo_puntajes.set_alpha(200)
    fondo_puntajes.fill(GRIS)
    pantalla.blit(fondo_puntajes, (50, 50))
    puntajes_altos = cargar_puntajes()
    for i, entrada in enumerate(puntajes_altos):
        texto = f"{i+1}. {entrada['nombre']} - {entrada['puntaje']} ({entrada['fecha']})"
        pantalla.blit(fuente.render(texto, True, NEGRO), (50, 50 + i * 40))
    dibujar_boton(pantalla, fuente, "Volver", 300, 500, 200, 50, GRIS, AZUL, lambda: datos_juego.update(estado=MENU))
    
    return datos_juego["estado"]