"""Módulo para la pantalla de Game Over en Preguntados - Dragon Ball.

Este módulo gestiona la interfaz de la pantalla de Game Over, mostrando un mensaje de fin de juego
y permitiendo al usuario continuar hacia la pantalla de ingreso de nombre.
"""

from constantes import *
from funciones import *

def mostrar_game_over(pantalla, eventos, datos_juego, fuente, fuente_game_over):
    """
    Muestra la pantalla de Game Over.
    
    Args:
        pantalla: Superficie donde se dibuja.
        eventos: Lista de eventos de Pygame.
        datos_juego: Diccionario con el estado del juego.
        fuente: Fuente para el texto del botón.
        fuente_game_over: Fuente para el texto "Game Over".
    
    Returns:
        str: Estado actualizado del juego.
    """
    pantalla.blit(datos_juego["juego_background"], (0, 0))
    fondo_game_over = pygame.Surface((400, 200))
    fondo_game_over.set_alpha(200)
    fondo_game_over.fill(GRIS)
    pantalla.blit(fondo_game_over, (200, 200))
    texto_game_over = fuente_game_over.render("Game Over", True, NEGRO)
    pantalla.blit(texto_game_over, (200 + (400 - texto_game_over.get_width()) // 2, 250))
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect_boton = pygame.Rect(300, 350, 200, 50)
    color_boton = VERDE if rect_boton.collidepoint(mouse) else GRIS
    pygame.draw.rect(pantalla, color_boton, rect_boton)
    texto_boton = fuente.render("Continuar", True, NEGRO)
    pantalla.blit(texto_boton, (300 + (200 - texto_boton.get_width()) // 2, 350 + (50 - texto_boton.get_height()) // 2))
    now = pygame.time.get_ticks()
    if rect_boton.collidepoint(mouse) and click[0] == 1 and now - datos_juego["ultimo_click_tiempo"] > 500:
        datos_juego["estado"] = FIN_JUEGO
        datos_juego["ultimo_click_tiempo"] = now
    
    return datos_juego["estado"]