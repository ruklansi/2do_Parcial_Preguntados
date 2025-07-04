"""Módulo para el menú principal de Preguntados - Dragon Ball.

Este módulo gestiona la interfaz del menú principal, mostrando botones interactivos para iniciar el juego,
ver puntajes, configurar música, ajustar opciones de juego o salir.
"""

from constantes import *
from funciones import *

def mostrar_menu(pantalla, eventos, datos_juego, fuente, fuente_game_over):
    """
    Muestra el menú principal con botones interactivos.
    
    Args:
        pantalla: Superficie donde se dibuja.
        eventos: Lista de eventos de Pygame.
        datos_juego: Diccionario con el estado del juego.
        fuente: Fuente para el texto de los botones.
        fuente_game_over: No usada en este estado.
    
    Returns:
        str: Estado actualizado del juego.
    """
    pantalla.blit(datos_juego["gif_frames"][datos_juego["gif_frame_index"]], (0, 0))
    botones_menu = [
        ("Jugar", GRIS, VERDE, lambda: datos_juego.update(estado=INICIO_JUEGO)),
        ("RankingTop 10", GRIS, AZUL, lambda: datos_juego.update(estado=PUNTAJES)),
        ("Configuración", GRIS, AZUL, lambda: datos_juego.update(estado=CONFIG)),
        ("Opciones de Juego", GRIS, AZUL, lambda: datos_juego.update(estado=CONFIG_JUEGO, dificultad_seleccionada="MEDIO")),
        ("Salir", GRIS, ROJO, lambda: datos_juego.update(ejecutando=False)),
    ]
    ancho_boton, alto_boton, espacio = 200, 50, 25
    total_altura = len(botones_menu) * alto_boton + (len(botones_menu) - 1) * espacio
    y_inicial = (ALTO - total_altura) // 2

    for i, (texto, color_inactivo, color_activo, accion) in enumerate(botones_menu):
        y = y_inicial + i * (alto_boton + espacio)
        dibujar_boton(pantalla, fuente, texto, 300, y, ancho_boton, alto_boton, color_inactivo, color_activo, accion)

    return datos_juego["estado"]