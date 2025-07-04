"""Módulo para la pantalla de configuración de dificultad en Preguntados - Dragon Ball.

Este módulo gestiona la interfaz de selección de dificultad, mostrando los parámetros de la dificultad
seleccionada (puntos, vidas, tiempo por pregunta) y permitiendo al usuario cambiar entre las opciones
de dificultad (Fácil, Medio, Difícil).
"""

from constantes import *
from funciones import *

def mostrar_config_juego(pantalla, eventos, datos_juego, fuente, fuente_game_over):
    """
    Muestra la pantalla de configuración de juego (dificultad).
    
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
    fondo_config = pygame.Surface((700, 400))
    fondo_config.set_alpha(200)
    fondo_config.fill(GRIS)
    pantalla.blit(fondo_config, (50, 50))
    pantalla.blit(fuente.render(f"Dificultad: {datos_juego['dificultad_seleccionada']}", True, NEGRO), (50, 50))
    pantalla.blit(fuente.render(f"Puntos por acierto: {DIFICULTADES[datos_juego['dificultad_seleccionada']]['puntos_aciertos']}", True, NEGRO), (50, 90))
    pantalla.blit(fuente.render(f"Puntos por error: {DIFICULTADES[datos_juego['dificultad_seleccionada']]['puntos_errores']}", True, NEGRO), (50, 130))
    pantalla.blit(fuente.render(f"Vidas: {DIFICULTADES[datos_juego['dificultad_seleccionada']]['vidas']}", True, NEGRO), (50, 170))
    pantalla.blit(fuente.render(f"Tiempo por pregunta: {DIFICULTADES[datos_juego['dificultad_seleccionada']]['tiempo_pregunta']}s", True, NEGRO), (50, 210))
    dibujar_boton(pantalla, fuente, "Fácil", 200, 300, 150, 50, GRIS, VERDE, 
                  lambda: datos_juego.update(dificultad_seleccionada="FACIL"))
    dibujar_boton(pantalla, fuente, "Medio", 375, 300, 150, 50, GRIS, VERDE, 
                  lambda: datos_juego.update(dificultad_seleccionada="MEDIO"))
    dibujar_boton(pantalla, fuente, "Difícil", 550, 300, 150, 50, GRIS, VERDE, 
                  lambda: datos_juego.update(dificultad_seleccionada="DIFICIL"))
    dibujar_boton(pantalla, fuente, "Volver", 300, 400, 200, 50, GRIS, AZUL, 
                  lambda: datos_juego.update(estado=MENU))
    
    return datos_juego["estado"]