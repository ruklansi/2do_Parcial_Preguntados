"""Módulo para la pantalla de configuración de música en Preguntados - Dragon Ball.

Este módulo gestiona la interfaz de configuración de música, permitiendo al usuario activar/desactivar
la música, ajustar el volumen y visualizar el nivel de volumen con un texto y una barra gráfica.
"""

from constantes import *
from funciones import *

def mostrar_config(pantalla, eventos, datos_juego, fuente, fuente_game_over):
    """
    Muestra la pantalla de configuración de música con el porcentaje de volumen y una barra visual.
    
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
    
    # Fondo para el área de configuración
    fondo_config = pygame.Surface((400, 400))
    fondo_config.set_alpha(200)
    fondo_config.fill(GRIS)
    pantalla.blit(fondo_config, (200, 100))
    
    # Mostrar estado de la música
    texto_musica = "Música: ON" if datos_juego["musica_sonando"] else "Música: OFF"
    dibujar_boton(pantalla, fuente, texto_musica, 300, 150, 200, 50, GRIS, AZUL, 
                  lambda: datos_juego.update(musica_sonando=alternar_musica(datos_juego)))
    
    # Mostrar porcentaje de volumen
    porcentaje_volumen = int(datos_juego["volumen_musica"] * 100)
    texto_volumen = fuente.render(f"Volumen: {porcentaje_volumen}%", True, NEGRO)
    pantalla.blit(texto_volumen, (300, 230))
    
    # Mostrar barra de volumen
    barra_ancho_max = 200
    barra_ancho_actual = barra_ancho_max * datos_juego["volumen_musica"]
    pygame.draw.rect(pantalla, VERDE, (300, 260, barra_ancho_actual, 10))  # Barra llena
    pygame.draw.rect(pantalla, NEGRO, (300, 260, barra_ancho_max, 10), 2)  # Borde
    
    # Botones de subir/bajar volumen
    dibujar_boton(pantalla, fuente, "Subir Volumen", 300, 300, 200, 50, GRIS, AZUL, 
                  lambda: datos_juego.update(volumen_musica=subir_volumen(datos_juego)[0]))
    dibujar_boton(pantalla, fuente, "Bajar Volumen", 300, 360, 200, 50, GRIS, AZUL, 
                  lambda: datos_juego.update(volumen_musica=bajar_volumen(datos_juego)[0]))
    
    # Botón de volver
    dibujar_boton(pantalla, fuente, "Volver", 300, 420, 200, 50, GRIS, AZUL, 
                  lambda: datos_juego.update(estado=MENU))
    
    return datos_juego["estado"]