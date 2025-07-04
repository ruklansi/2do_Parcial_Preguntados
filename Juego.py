"""Módulo para el estado principal del juego en Preguntados - Dragon Ball.

Este módulo gestiona la interfaz y la lógica del estado de juego, incluyendo la visualización de preguntas,
opciones de respuesta, comodines, puntaje, vidas, tiempo restante, y la animación Toasty que aparece tras
una respuesta correcta o incorrecta.
"""

from constantes import *
from funciones import *

def seleccionar_opcion(opcion, datos_juego, incorrect_sound, correct_sound):
    """
    Maneja la selección de una opción en el juego.
    
    Args:
        opcion (str): Opción seleccionada por el jugador.
        datos_juego (dict): Diccionario con el estado del juego.
        incorrect_sound (pygame.mixer.Sound): Sonido para respuesta incorrecta.
        correct_sound (pygame.mixer.Sound): Sonido para respuesta correcta.
    
    Returns:
        dict: Estado actualizado del juego.
    """
    datos_juego = verificar_respuesta(opcion, datos_juego, incorrect_sound, correct_sound)
    datos_juego["mensaje_comodin_tiempo"] = pygame.time.get_ticks()
    if datos_juego["pregunta_actual"] is None and not datos_juego["doble_chance_activo"]:
        datos_juego["toasty_active"] = True
        datos_juego["toasty_type"] = "correcto" if opcion == datos_juego["respuesta_correcta"] else "incorrecto"
        datos_juego["toasty_x"] = -100
        datos_juego["toasty_direction"] = "ida"
        datos_juego["toasty_frame_index"] = 0
        datos_juego["toasty_start_time"] = pygame.time.get_ticks()
    if datos_juego["pregunta_actual"] is None:
        datos_juego["tiempo_inicio"] = pygame.time.get_ticks()
    if datos_juego["vidas"] <= 0 and not datos_juego["doble_chance_activo"]:
        datos_juego["estado"] = GAME_OVER
    return datos_juego

def mostrar_juego(pantalla, eventos, datos_juego, fuente, fuente_game_over):
    """
    Muestra el estado del juego con preguntas y comodines.
    
    Args:
        pantalla: Superficie donde se dibuja.
        eventos: Lista de eventos de Pygame.
        datos_juego: Diccionario con el estado del juego.
        fuente: Fuente para el texto.
        fuente_game_over: No usada en este estado.
    
    Returns:
        str: Estado actualizado del juego.
    """
    pantalla.blit(datos_juego["juego_background"], (0, 0))
    if not datos_juego["pregunta_actual"]:
        if not datos_juego["preguntas"]:
            datos_juego["estado"] = FIN_JUEGO
            datos_juego["juego_terminado_por_preguntas"] = True
        else:
            datos_juego["pregunta_actual"] = random.choice(datos_juego["preguntas"])
            datos_juego["opciones"] = [datos_juego["pregunta_actual"][f"opcion{i+1}"] for i in range(4)]
            random.shuffle(datos_juego["opciones"])
            datos_juego["respuesta_correcta"] = datos_juego["pregunta_actual"]["correcta"]
            datos_juego["preguntas"].remove(datos_juego["pregunta_actual"])
            datos_juego["opciones_restantes"] = datos_juego["opciones"].copy()
            datos_juego["doble_chance_activo"] = False
            datos_juego["tiempo_inicio"] = pygame.time.get_ticks()
    else:
        tiempo_transcurrido = (pygame.time.get_ticks() - datos_juego["tiempo_inicio"]) / 1000
        if tiempo_transcurrido > DIFICULTADES[datos_juego["dificultad_seleccionada"]]["tiempo_pregunta"]:
            datos_juego["vidas"] -= 1
            datos_juego["pregunta_actual"] = None
            datos_juego["opciones_restantes"] = []
            datos_juego["doble_chance_activo"] = False
            datos_juego["mensaje_comodin"] = "Tiempo agotado: -1 vida"
            datos_juego["mensaje_comodin_tiempo"] = pygame.time.get_ticks()
            if datos_juego["incorrect_sound"]:
                datos_juego["incorrect_sound"].play()
            datos_juego["toasty_active"] = True
            datos_juego["toasty_type"] = "incorrecto"
            datos_juego["toasty_x"] = -100
            datos_juego["toasty_direction"] = "ida"
            datos_juego["toasty_frame_index"] = 0
            datos_juego["toasty_start_time"] = pygame.time.get_ticks()
            if datos_juego["vidas"] <= 0:
                datos_juego["estado"] = GAME_OVER
        else:
            fondo_texto = pygame.Surface((700, 50))
            fondo_texto.set_alpha(200)
            fondo_texto.fill(GRIS)
            pantalla.blit(fondo_texto, (50, 50))
            texto_pregunta = fuente.render(datos_juego["pregunta_actual"]["pregunta"], True, NEGRO)
            pantalla.blit(texto_pregunta, (50, 50))
            
            opciones_a_mostrar = datos_juego["opciones_restantes"] if datos_juego["doble_chance_activo"] else datos_juego["opciones"]
            for i, opcion in enumerate(opciones_a_mostrar):
                dibujar_boton(pantalla, fuente, opcion, 200, 150 + i * 60, 400, 50, GRIS, AZUL, 
                              lambda opt=opcion: datos_juego.update(seleccionar_opcion(opt, datos_juego, datos_juego["incorrect_sound"], datos_juego["correct_sound"])))
            
            base_y_comodin = 410
            base_x_comodin = 50
            ancho_boton = 170
            espacio = 20
            idx = 0
            if not datos_juego["bomba_usada"]:
                dibujar_boton(pantalla, fuente, "Bomba", base_x_comodin + idx * (ancho_boton + espacio), base_y_comodin, ancho_boton, 50, GRIS, ROJO, 
                              lambda: datos_juego.update(usar_bomba(datos_juego), mensaje_comodin_tiempo=pygame.time.get_ticks()))
                idx += 1
            if not datos_juego["x2_usado"]:
                dibujar_boton(pantalla, fuente, "X2", base_x_comodin + idx * (ancho_boton + espacio), base_y_comodin, ancho_boton, 50, GRIS, ROJO, 
                              lambda: datos_juego.update(usar_x2(datos_juego), mensaje_comodin_tiempo=pygame.time.get_ticks()))
                idx += 1
            if not datos_juego["doble_chance_usado"]:
                dibujar_boton(pantalla, fuente, "Doble Chance", base_x_comodin + idx * (ancho_boton + espacio), base_y_comodin, ancho_boton, 50, GRIS, ROJO, 
                              lambda: datos_juego.update(usar_doble_chance(datos_juego), mensaje_comodin_tiempo=pygame.time.get_ticks()))
                idx += 1
            if not datos_juego["pasar_usado"]:
                dibujar_boton(pantalla, fuente, "Pasar", base_x_comodin + idx * (ancho_boton + espacio), base_y_comodin, ancho_boton, 50, GRIS, ROJO, 
                              lambda: datos_juego.update(usar_pasar(datos_juego), tiempo_inicio=pygame.time.get_ticks(), mensaje_comodin_tiempo=pygame.time.get_ticks()))
            
            fondo_stats = pygame.Surface((200, 100))
            fondo_stats.set_alpha(200)
            fondo_stats.fill(GRIS)
            pantalla.blit(fondo_stats, (50, 500))
            pantalla.blit(fuente.render(f"Puntaje: {datos_juego['puntaje']}", True, NEGRO), (50, 500))
            pantalla.blit(fuente.render(f"Vidas: {datos_juego['vidas']}", True, NEGRO), (50, 550))
            fondo_tiempo = pygame.Surface((200, 50))
            fondo_tiempo.set_alpha(200)
            fondo_tiempo.fill(GRIS)
            pantalla.blit(fondo_tiempo, (550, 500))
            tiempo_restante = max(0, int(DIFICULTADES[datos_juego["dificultad_seleccionada"]]["tiempo_pregunta"] - tiempo_transcurrido))
            pantalla.blit(fuente.render(f"Tiempo: {tiempo_restante}", True, NEGRO), (550, 500))
            if datos_juego["mensaje_comodin"] or datos_juego["doble_chance_activo"]:
                fondo_mensaje = pygame.Surface((700, 30))
                fondo_mensaje.set_alpha(200)
                fondo_mensaje.fill(GRIS)
                pantalla.blit(fondo_mensaje, (50, 110))
                mensaje_mostrar = datos_juego["mensaje_comodin"] if datos_juego["mensaje_comodin"] else "Doble Chance: Selecciona otra opción"
                pantalla.blit(fuente.render(mensaje_mostrar, True, NEGRO), (50, 110))
    
    return datos_juego["estado"]