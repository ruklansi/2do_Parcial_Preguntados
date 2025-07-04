"""Funciones de soporte para el juego Preguntados - Dragon Ball.

Este módulo contiene funciones utilitarias para cargar preguntas, gestionar puntajes, dibujar botones,
verificar respuestas, manejar comodines, controlar el volumen de la música y reiniciar el juego.
Estas funciones son utilizadas por los módulos de los diferentes estados del juego para mantener
la lógica centralizada y modular.
"""

import pygame
import csv
import json
import random
from datetime import datetime
from constantes import *

def cargar_preguntas():
    """Carga las preguntas desde el archivo preguntas.csv.

    Lee el archivo CSV que contiene las preguntas del juego y sus opciones, y devuelve una lista
    de diccionarios con las preguntas.

    Returns:
        list: Lista de diccionarios, cada uno representando una pregunta con sus opciones y respuesta correcta.
    """
    with open("preguntas.csv", "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)

def guardar_resultado(nombre, puntaje):
    """Guarda el resultado de una partida en el archivo partidas.json.

    Agrega un nuevo registro con el nombre del jugador, su puntaje y la fecha actual al archivo JSON.

    Args:
        nombre (str): Nombre del jugador.
        puntaje (int): Puntaje obtenido en la partida.
    """
    with open("partidas.json", "r") as archivo:
        datos = json.load(archivo)
    datos.append({"nombre": nombre, "puntaje": puntaje, "fecha": datetime.now().strftime("%Y-%m-%d")})
    with open("partidas.json", "w") as archivo:
        json.dump(datos, archivo, indent=4)

def cargar_puntajes():
    """Carga los 10 mejores puntajes desde el archivo partidas.json.

    Lee el archivo JSON, ordena los resultados por puntaje de mayor a menor y devuelve los 10 primeros.

    Returns:
        list: Lista de los 10 mejores resultados, cada uno con nombre, puntaje y fecha.
    """
    with open("partidas.json", "r") as archivo:
        datos = json.load(archivo)
    return sorted(datos, key=lambda x: x["puntaje"], reverse=True)[:10]

def dibujar_boton(pantalla, fuente, texto, x, y, ancho, alto, color_inactivo, color_activo, accion=None):
    """
    Dibuja un botón interactivo con texto centrado.
    
    Args:
        pantalla: Superficie donde se dibuja.
        fuente: Fuente para el texto.
        texto: Texto del botón.
        x, y: Posición del botón.
        ancho, alto: Dimensiones del botón.
        color_inactivo: Color cuando el ratón no está encima.
        color_activo: Color cuando el ratón está encima.
        accion: Función a ejecutar al hacer clic.
    """
    raton = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()
    rect_boton = pygame.Rect(x, y, ancho, alto)
    color = color_activo if rect_boton.collidepoint(raton) else color_inactivo
    boton_surface = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    boton_surface.set_alpha(200)
    boton_surface.fill(color)
    pantalla.blit(boton_surface, (x, y))
    texto_surf = fuente.render(texto, True, NEGRO)
    texto_rect = texto_surf.get_rect(center=rect_boton.center)
    pantalla.blit(texto_surf, texto_rect)
    if clic[0] == 1 and rect_boton.collidepoint(raton) and accion:
        pygame.time.wait(200)
        accion()

def verificar_respuesta(opcion_seleccionada, datos_juego, incorrect_sound, correct_sound):
    """
    Verifica si la opción seleccionada es correcta y actualiza el estado del juego.
    
    Args:
        opcion_seleccionada: Opción elegida por el jugador.
        datos_juego: Diccionario con el estado del juego.
        incorrect_sound, correct_sound: Sonidos para respuestas incorrectas/correctas.
    
    Returns:
        dict: Estado actualizado del juego.
    """
    mensaje_comodin = ""
    opciones_restantes = datos_juego["opciones"].copy()
    
    if opcion_seleccionada == datos_juego["respuesta_correcta"]:
        puntos_ganados = DIFICULTADES[datos_juego["dificultad_seleccionada"]]["puntos_aciertos"] * (2 if datos_juego["x2_usado"] else 1)
        datos_juego["puntaje"] += puntos_ganados
        datos_juego["correctas_seguidas"] += 1
        if datos_juego["correctas_seguidas"] >= 5:
            datos_juego["vidas"] += 1
            datos_juego["correctas_seguidas"] = 0
        datos_juego["pregunta_actual"] = None
        datos_juego["doble_chance_activo"] = False
        datos_juego["opciones_restantes"] = []
        mensaje_comodin = f"¡Correcto! +{puntos_ganados} puntos" + (" (X2 activado)" if datos_juego["x2_usado"] else "")
        if correct_sound:
            correct_sound.play()
    else:
        if datos_juego["doble_chance_usado"] and not datos_juego["doble_chance_activo"]:
            datos_juego["doble_chance_activo"] = True
            datos_juego["opciones_restantes"].remove(opcion_seleccionada)
            mensaje_comodin = "Doble Chance: Selecciona otra opción"
        else:
            datos_juego["puntaje"] += DIFICULTADES[datos_juego["dificultad_seleccionada"]]["puntos_errores"]
            datos_juego["vidas"] -= 1
            datos_juego["correctas_seguidas"] = 0
            datos_juego["pregunta_actual"] = None
            datos_juego["doble_chance_activo"] = False
            datos_juego["opciones_restantes"] = []
            mensaje_comodin = f"Incorrecto: {DIFICULTADES[datos_juego['dificultad_seleccionada']]['puntos_errores']} puntos, -1 vida"
            if incorrect_sound:
                incorrect_sound.play()
    
    datos_juego["mensaje_comodin"] = mensaje_comodin
    return datos_juego

def usar_bomba(datos_juego):
    """Aplica el comodín Bomba, eliminando opciones incorrectas.

    Si no se ha usado la bomba, elimina todas las opciones incorrectas excepto una (si está disponible),
    dejando la respuesta correcta y una incorrecta. Actualiza el estado del juego.

    Args:
        datos_juego (dict): Diccionario con el estado del juego.

    Returns:
        dict: Estado actualizado del juego.
    """
    if datos_juego["bomba_usada"]:
        datos_juego["mensaje_comodin"] = "Ya usaste la bomba"
        return datos_juego
    opciones_incorrectas = [op for op in datos_juego["opciones"] if op != datos_juego["respuesta_correcta"]]
    if len(opciones_incorrectas) >= 1:
        datos_juego["opciones"] = [datos_juego["respuesta_correcta"], opciones_incorrectas[0]]
        datos_juego["opciones_restantes"] = datos_juego["opciones"].copy()
    else:
        datos_juego["opciones"] = [datos_juego["respuesta_correcta"]]
        datos_juego["opciones_restantes"] = datos_juego["opciones"].copy()
    random.shuffle(datos_juego["opciones"])
    datos_juego["bomba_usada"] = True
    datos_juego["mensaje_comodin"] = "¡Bomba activada!"
    return datos_juego

def usar_x2(datos_juego):
    """Aplica el comodín X2 para duplicar los puntos de la siguiente respuesta correcta.

    Si no se ha usado X2, lo activa y actualiza el estado del juego.

    Args:
        datos_juego (dict): Diccionario con el estado del juego.

    Returns:
        dict: Estado actualizado del juego.
    """
    if not datos_juego["x2_usado"]:
        datos_juego["x2_usado"] = True
        datos_juego["mensaje_comodin"] = "X2 usado: Siguiente respuesta correcta dará el doble de puntos"
    else:
        datos_juego["mensaje_comodin"] = "Ya usaste X2"
    return datos_juego

def usar_doble_chance(datos_juego):
    """Aplica el comodín Doble Chance para permitir un segundo intento tras un error.

    Si no se ha usado Doble Chance, lo activa y actualiza el estado del juego.

    Args:
        datos_juego (dict): Diccionario con el estado del juego.

    Returns:
        dict: Estado actualizado del juego.
    """
    if not datos_juego["doble_chance_usado"]:
        datos_juego["doble_chance_usado"] = True
        datos_juego["mensaje_comodin"] = "Doble Chance usado: Tendrás un segundo intento si fallas"
    else:
        datos_juego["mensaje_comodin"] = "Ya usaste Doble Chance"
    return datos_juego

def usar_pasar(datos_juego):
    """Aplica el comodín Pasar para saltar la pregunta actual sin afectar puntos ni vidas.

    Si no se ha usado Pasar, elimina la pregunta actual y pasa a la siguiente.

    Args:
        datos_juego (dict): Diccionario con el estado del juego.

    Returns:
        dict: Estado actualizado del juego.
    """
    if datos_juego["pregunta_actual"] in datos_juego["preguntas"]:
        datos_juego["preguntas"].remove(datos_juego["pregunta_actual"])
    datos_juego["pregunta_actual"] = None
    datos_juego["mensaje_comodin"] = "Pasar usado: Pregunta saltada"
    return datos_juego

def alternar_musica(datos_juego):
    """Alterna entre reproducir y pausar la música del juego.

    Cambia el estado de la música (encendido/apagado) y reproduce o detiene la música actual.

    Args:
        datos_juego (dict): Diccionario con el estado del juego.

    Returns:
        bool: Estado actual de la música (True si está sonando, False si está pausada).
    """
    datos_juego["musica_sonando"] = not datos_juego["musica_sonando"]
    if datos_juego["musica_sonando"] and datos_juego["musica_actual"]:
        datos_juego["musica_actual"].play(-1)
    elif datos_juego["musica_actual"]:
        datos_juego["musica_actual"].stop()
    return datos_juego["musica_sonando"]

def subir_volumen(datos_juego):
    """Sube el volumen de la música en un 10% y devuelve el valor actual y el porcentaje.

    Aumenta el volumen hasta un máximo de 1.0 y lo aplica a la música actual.

    Args:
        datos_juego (dict): Diccionario con el estado del juego.

    Returns:
        tuple: (volumen_musica, porcentaje_volumen) con el valor del volumen (0.0 a 1.0) y el porcentaje (0 a 100).
    """
    datos_juego["volumen_musica"] = min(1.0, datos_juego["volumen_musica"] + 0.1)
    if datos_juego["musica_actual"]:
        datos_juego["musica_actual"].set_volume(datos_juego["volumen_musica"])
    porcentaje = int(datos_juego["volumen_musica"] * 100)
    return datos_juego["volumen_musica"], porcentaje

def bajar_volumen(datos_juego):
    """Baja el volumen de la música en un 10% y devuelve el valor actual y el porcentaje.

    Disminuye el volumen hasta un mínimo de 0.0 y lo aplica a la música actual.

    Args:
        datos_juego (dict): Diccionario con el estado del juego.

    Returns:
        tuple: (volumen_musica, porcentaje_volumen) con el valor del volumen (0.0 a 1.0) y el porcentaje (0 a 100).
    """
    datos_juego["volumen_musica"] = max(0.0, datos_juego["volumen_musica"] - 0.1)
    if datos_juego["musica_actual"]:
        datos_juego["musica_actual"].set_volume(datos_juego["volumen_musica"])
    porcentaje = int(datos_juego["volumen_musica"] * 100)
    return datos_juego["volumen_musica"], porcentaje

def guardar_y_reiniciar(datos_juego):
    """Guarda el resultado del juego y reinicia las variables para una nueva partida.

    Si el nombre del jugador es válido, guarda el resultado y reinicia el estado del juego,
    incluyendo puntaje, vidas, comodines y preguntas.

    Args:
        datos_juego (dict): Diccionario con el estado del juego.

    Returns:
        dict: Estado actualizado del juego.
    """
    if datos_juego["entrada_nombre"].strip() and datos_juego["entrada_nombre"].isalpha():
        datos_juego["nombre_jugador"] = datos_juego["entrada_nombre"]
        guardar_resultado(datos_juego["nombre_jugador"], datos_juego["puntaje"])
        datos_juego["estado"] = MENU
        datos_juego["preguntas"].clear()
        datos_juego["preguntas"].extend(cargar_preguntas())
        datos_juego["puntaje"] = PUNTAJE_INICIAL
        datos_juego["vidas"] = DIFICULTADES[datos_juego["dificultad_seleccionada"]]["vidas"]
        datos_juego["correctas_seguidas"] = CORRECTAS_SEGUIDAS_INICIAL
        datos_juego["bomba_usada"] = False
        datos_juego["x2_usado"] = X2_USADO_INICIAL
        datos_juego["doble_chance_usado"] = DOBLE_CHANCE_USADO_INICIAL
        datos_juego["pasar_usado"] = PASAR_USADO_INICIAL
        datos_juego["entrada_nombre"] = ""
        datos_juego["nombre_jugador"] = ""
        datos_juego["juego_terminado_por_preguntas"] = False
    return datos_juego