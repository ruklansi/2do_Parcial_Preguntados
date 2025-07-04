"""Módulo principal para Preguntados - Dragon Ball.

Este módulo inicializa el juego, carga recursos multimedia (imágenes, sonidos, GIFs), y ejecuta el bucle
principal que delega el manejo de los estados a los módulos correspondientes (menú, juego, configuración, etc.).
"""

import pygame
from PIL import Image
from constantes import *
from funciones import *
from Menu import mostrar_menu
from InicioJuego import mostrar_inicio_juego
from Juego import mostrar_juego
from GameOver import mostrar_game_over
from Puntajes import mostrar_puntajes
from Configuracion import mostrar_config
from ConfigJuego import mostrar_config_juego
from FinJuego import mostrar_fin_juego

pygame.init()
pygame.mixer.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Preguntados - Dragon Ball")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)
fuente = pygame.font.SysFont("arial", 18)
fuente_game_over = pygame.font.SysFont("arial", 36)
reloj = pygame.time.Clock()

def cargar_recursos():
    """Carga recursos multimedia (imágenes, sonidos, GIFs) con todos los fotogramas pre-cargados.

    Carga los sonidos, el fondo del juego, el GIF de fondo y la animación Toasty. Si un recurso no está
    disponible, utiliza valores predeterminados (superficies blancas o sonidos nulos).

    Returns:
        dict: Diccionario con los recursos cargados, incluyendo sonidos, imágenes y fotogramas de GIFs.
    """
    recursos = {}
    try:
        recursos["musica_principal"] = pygame.mixer.Sound("dbz_principal.wav")
        recursos["musica_principal"].set_volume(VOLUMEN_INICIAL)
        recursos["musica_preguntas"] = pygame.mixer.Sound("dbz_preguntas.wav")
        recursos["musica_preguntas"].set_volume(VOLUMEN_INICIAL)
        recursos["incorrect_sound"] = pygame.mixer.Sound("dbz_fallaste.wav")
        recursos["correct_sound"] = pygame.mixer.Sound("dbz_correcto.wav")
        recursos["game_over_sound"] = pygame.mixer.Sound("game_over.wav")
        recursos["comience_juego_sound"] = pygame.mixer.Sound("comience_el_juego.wav")
    except FileNotFoundError:
        recursos["musica_principal"] = None
        recursos["musica_preguntas"] = None
        recursos["incorrect_sound"] = None
        recursos["correct_sound"] = None
        recursos["game_over_sound"] = None
        recursos["comience_juego_sound"] = None

    try:
        gif = Image.open("fondo_cell.gif")
        gif_frames = []
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_img = gif.copy().convert("RGBA")
            frame_img = frame_img.resize((ANCHO, ALTO))
            gif_frames.append(pygame.image.fromstring(frame_img.tobytes(), frame_img.size, frame_img.mode))
        recursos["gif_frame_count"] = gif.n_frames
        recursos["gif_frame_delay"] = gif.info.get('duration', 100)
        recursos["gif_frames"] = gif_frames
    except Exception:
        gif_frames = [pygame.Surface((ANCHO, ALTO)).convert_alpha()]
        gif_frames[0].fill(BLANCO)
        recursos["gif_frame_count"] = 1
        recursos["gif_frame_delay"] = 100
        recursos["gif_frames"] = gif_frames

    try:
        toasty_gif = Image.open("cell_dragon_ball.gif")
        toasty_frames = []
        for frame in range(toasty_gif.n_frames):
            toasty_gif.seek(frame)
            frame_img = toasty_gif.copy().convert("RGBA")
            frame_img = frame_img.resize((100, 100))
            toasty_frames.append(pygame.image.fromstring(frame_img.tobytes(), frame_img.size, frame_img.mode))
        recursos["toasty_frame_count"] = toasty_gif.n_frames
        recursos["toasty_frame_delay"] = toasty_gif.info.get('duration', 50)
        recursos["toasty_frames"] = toasty_frames
    except Exception:
        toasty_frames = [pygame.Surface((100, 100)).convert_alpha()]
        toasty_frames[0].fill(BLANCO)
        recursos["toasty_frame_count"] = 1
        recursos["toasty_frame_delay"] = 50
        recursos["toasty_frames"] = toasty_frames

    try:
        recursos["juego_background"] = pygame.transform.scale(pygame.image.load("pantalla_juego.png"), (ANCHO, ALTO))
    except FileNotFoundError:
        recursos["juego_background"] = pygame.Surface((ANCHO, ALTO)).convert_alpha()
        recursos["juego_background"].fill(BLANCO)

    return recursos

def principal():
    """Bucle principal del juego, delega el manejo de estados a módulos específicos.

    Inicializa el estado del juego, carga recursos, y ejecuta el bucle principal que actualiza la pantalla,
    maneja eventos, y controla la animación de GIFs y Toasty.
    """
    datos_juego = {
        "ejecutando": True,
        "estado": MENU,
        "puntaje": PUNTAJE_INICIAL,
        "vidas": DIFICULTADES["MEDIO"]["vidas"],
        "correctas_seguidas": CORRECTAS_SEGUIDAS_INICIAL,
        "pregunta_actual": None,
        "opciones": [],
        "respuesta_correcta": "",
        "bomba_usada": False,
        "x2_usado": X2_USADO_INICIAL,
        "doble_chance_usado": DOBLE_CHANCE_USADO_INICIAL,
        "doble_chance_activo": False,
        "opciones_restantes": [],
        "pasar_usado": PASAR_USADO_INICIAL,
        "nombre_jugador": "",
        "entrada_nombre": "",
        "juego_terminado_por_preguntas": False,
        "mensaje_comodin": "",
        "mensaje_comodin_tiempo": 0,
        "tiempo_inicio": 0,
        "dificultad_seleccionada": "MEDIO",
        "cuenta_regresiva": 3,
        "cuenta_regresiva_tiempo": 0,
        "gif_frame_index": 0,
        "gif_last_update": 0,
        "toasty_active": False,
        "toasty_type": None,
        "toasty_x": -100,
        "toasty_direction": "ida",
        "toasty_frame_index": 0,
        "toasty_last_update": 0,
        "ultimo_click_tiempo": 0,
        "musica_sonando": True,
        "volumen_musica": VOLUMEN_INICIAL,
        "musica_actual": None,
        "preguntas": cargar_preguntas(),
    }
    datos_juego.update(cargar_recursos())
    datos_juego["musica_actual"] = datos_juego["musica_principal"]
    if datos_juego["musica_actual"]:
        datos_juego["musica_actual"].play(-1)

    estado_funciones = {
        MENU: mostrar_menu,
        INICIO_JUEGO: mostrar_inicio_juego,
        JUEGO: mostrar_juego,
        GAME_OVER: mostrar_game_over,
        PUNTAJES: mostrar_puntajes,
        CONFIG: mostrar_config,
        CONFIG_JUEGO: mostrar_config_juego,
        FIN_JUEGO: mostrar_fin_juego
    }

    while datos_juego["ejecutando"]:
        now = pygame.time.get_ticks()
        # Actualizar índice de GIF de fondo
        if datos_juego["estado"] not in [JUEGO, GAME_OVER] and now - datos_juego["gif_last_update"] > datos_juego["gif_frame_delay"]:
            datos_juego["gif_frame_index"] = (datos_juego["gif_frame_index"] + 1) % datos_juego["gif_frame_count"]
            datos_juego["gif_last_update"] = now
        
        # Actualizar animación de Toasty
        if datos_juego["toasty_active"]:
            toasty_rect = pygame.Rect(datos_juego["toasty_x"], ALTO//2, 100, 100)
            opciones_rect = pygame.Rect(200, 150, 400, 180)
            if datos_juego["toasty_direction"] == "ida":
                datos_juego["toasty_x"] += (ANCHO + 200) / (2.0 * FPS)  # ~2s para ida
                if toasty_rect.colliderect(opciones_rect):
                    datos_juego["toasty_direction"] = "vuelta"
            else:
                datos_juego["toasty_x"] -= (ANCHO + 200) / (2.5 * FPS)  # ~2.5s para vuelta
            if now - datos_juego["toasty_last_update"] > datos_juego["toasty_frame_delay"]:
                datos_juego["toasty_frame_index"] = (datos_juego["toasty_frame_index"] + 1) % datos_juego["toasty_frame_count"]
                datos_juego["toasty_last_update"] = now
            if datos_juego["toasty_direction"] == "vuelta" and datos_juego["toasty_x"] <= -100 or now - datos_juego["toasty_start_time"] > 4500:
                datos_juego["toasty_active"] = False
                datos_juego["toasty_x"] = -100
                datos_juego["toasty_direction"] = "ida"
                datos_juego["toasty_frame_index"] = 0

        # Limpiar mensaje de comodín después de 2 segundos
        if datos_juego["mensaje_comodin"] and now - datos_juego["mensaje_comodin_tiempo"] > 2000:
            datos_juego["mensaje_comodin"] = ""

        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                datos_juego["ejecutando"] = False

        estado_anterior = datos_juego["estado"]
        datos_juego["estado"] = estado_funciones[datos_juego["estado"]](pantalla, eventos, datos_juego, fuente, fuente_game_over)
        
        # Manejo de transiciones de estado y audio
        if datos_juego["estado"] != estado_anterior:
            if datos_juego["estado"] == JUEGO and datos_juego["musica_preguntas"] and datos_juego["musica_sonando"]:
                if datos_juego["musica_actual"] != datos_juego["musica_preguntas"] or not pygame.mixer.get_busy():
                    if datos_juego["musica_actual"]:
                        datos_juego["musica_actual"].stop()
                    datos_juego["musica_actual"] = datos_juego["musica_preguntas"]
                    datos_juego["musica_actual"].set_volume(datos_juego["volumen_musica"])
                    datos_juego["musica_actual"].play(-1)
            elif datos_juego["estado"] == GAME_OVER and datos_juego["game_over_sound"]:
                pygame.mixer.stop()
                datos_juego["game_over_sound"].play()
            elif datos_juego["estado"] == INICIO_JUEGO and datos_juego["comience_juego_sound"]:
                pygame.mixer.stop()
                datos_juego["comience_juego_sound"].play()
                datos_juego["cuenta_regresiva"] = 3
                datos_juego["cuenta_regresiva_tiempo"] = now
            elif datos_juego["musica_principal"] and datos_juego["musica_sonando"]:
                if datos_juego["musica_actual"] != datos_juego["musica_principal"] or not pygame.mixer.get_busy():
                    if datos_juego["musica_actual"]:
                        datos_juego["musica_actual"].stop()
                    datos_juego["musica_actual"] = datos_juego["musica_principal"]
                    datos_juego["musica_actual"].set_volume(datos_juego["volumen_musica"])
                    datos_juego["musica_actual"].play(-1)

        # Dibujar Toasty si está activo
        if datos_juego["toasty_active"]:
            pantalla.blit(datos_juego["toasty_frames"][datos_juego["toasty_frame_index"]], (datos_juego["toasty_x"], ALTO//2))

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    principal()