import pygame
import csv
import json
import random
from datetime import datetime
from constantes import *

def cargar_preguntas():
    with open("preguntas.csv", "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)

def guardar_resultado(nombre, puntaje):
    with open("partidas.json", "r") as archivo:
        datos = json.load(archivo)
    datos.append({"nombre": nombre, "puntaje": puntaje, "fecha": datetime.now().strftime("%Y-%m-%d")})
    with open("partidas.json", "w") as archivo:
        json.dump(datos, archivo, indent=4)

def cargar_puntajes():
    with open("partidas.json", "r") as archivo:
        datos = json.load(archivo)
    return sorted(datos, key=lambda x: x["puntaje"], reverse=True)[:10]

def dibujar_boton(pantalla, fuente, texto, x, y, ancho, alto, color_inactivo, color_activo, accion=None):
    raton = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()
    rect_boton = pygame.Rect(x, y, ancho, alto)
    color = color_activo if rect_boton.collidepoint(raton) else color_inactivo
    boton_surface = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    color_con_alpha = color + (120,) if len(color) == 3 else color
    boton_surface.fill(color_con_alpha)
    pantalla.blit(boton_surface, (x, y))
    texto_surf = fuente.render(texto, True, NEGRO)
    texto_rect = texto_surf.get_rect(center=rect_boton.center)
    pantalla.blit(texto_surf, texto_rect)
    if clic[0] == 1 and rect_boton.collidepoint(raton) and accion:
        pygame.time.wait(200)
        accion()

def verificar_respuesta(opcion_seleccionada, respuesta_correcta, puntaje, vidas, correctas_seguidas, pregunta_actual, estado, x2_usado, doble_chance_usado, doble_chance_activo, opciones, incorrect_sound, correct_sound, preguntas, dificultad):
    mensaje_comodin = ""
    opciones_restantes = opciones.copy()
    
    if opcion_seleccionada == respuesta_correcta:
        puntos_ganados = DIFICULTADES[dificultad]["puntos_aciertos"] * (2 if x2_usado else 1)
        puntaje += puntos_ganados
        correctas_seguidas += 1
        if correctas_seguidas >= 5:
            vidas += 1
            correctas_seguidas = 0
        pregunta_actual = None
        doble_chance_activo = False
        opciones_restantes = []
        mensaje_comodin = f"¡Correcto! +{puntos_ganados} puntos" + (" (X2 activado)" if x2_usado else "")
        if correct_sound:
            correct_sound.play()
    else:
        if doble_chance_usado and not doble_chance_activo:
            doble_chance_activo = True
            opciones_restantes.remove(opcion_seleccionada)
            mensaje_comodin = "Doble Chance: Selecciona otra opción"
        else:
            puntaje += DIFICULTADES[dificultad]["puntos_errores"]
            vidas -= 1
            correctas_seguidas = 0
            pregunta_actual = None
            doble_chance_activo = False
            opciones_restantes = []
            mensaje_comodin = f"Incorrecto: {DIFICULTADES[dificultad]['puntos_errores']} puntos, -1 vida"
            if incorrect_sound:
                incorrect_sound.play()
    
    if vidas <= 0:
        estado = FIN_JUEGO
    
    return {
        "puntaje": puntaje,
        "vidas": vidas,
        "correctas_seguidas": correctas_seguidas,
        "pregunta_actual": pregunta_actual,
        "estado": estado,
        "x2_usado": False if x2_usado else False,
        "doble_chance_activo": doble_chance_activo,
        "opciones_restantes": opciones_restantes,
        "mensaje_comodin": mensaje_comodin
    }

def usar_bomba(opciones, respuesta_correcta, bomba_usada):
    if bomba_usada:
        return opciones, bomba_usada, "Ya usaste la bomba"
    opciones_incorrectas = [op for op in opciones if op != respuesta_correcta]
    if len(opciones_incorrectas) >= 1:
        opciones = [respuesta_correcta, opciones_incorrectas[0]]
    else:
        opciones = [respuesta_correcta]
    random.shuffle(opciones)
    bomba_usada = True
    return opciones, bomba_usada, "¡Bomba activada!"

def usar_x2(x2_usado):
    if not x2_usado:
        x2_usado = True
        mensaje_comodin = "X2 usado: Siguiente respuesta correcta dará el doble de puntos"
    else:
        mensaje_comodin = "Ya usaste X2"
    return x2_usado, mensaje_comodin

def usar_doble_chance(doble_chance_usado):
    if not doble_chance_usado:
        doble_chance_usado = True
        mensaje_comodin = "Doble Chance usado: Tendrás un segundo intento si fallas"
    else:
        mensaje_comodin = "Ya usaste Doble Chance"
    return doble_chance_usado, mensaje_comodin

def usar_pasar(pregunta_actual, preguntas):
    if pregunta_actual in preguntas:
        preguntas.remove(pregunta_actual)
    pregunta_actual = None
    mensaje_comodin = "Pasar usado: Pregunta saltada"
    return pregunta_actual, preguntas, mensaje_comodin

def alternar_musica(musica, musica_sonando):
    musica_sonando = not musica_sonando
    if musica and musica_sonando:
        musica.play(-1)
    elif musica:
        musica.stop()
    return musica_sonando

def subir_volumen(musica, volumen_musica):
    volumen_musica = min(1.0, volumen_musica + 0.1)
    if musica:
        musica.set_volume(volumen_musica)
    return volumen_musica

def bajar_volumen(musica, volumen_musica):
    volumen_musica = max(0.0, volumen_musica - 0.1)
    if musica:
        musica.set_volume(volumen_musica)
    return volumen_musica

def guardar_y_reiniciar(nombre_jugador, entrada_nombre, puntaje, vidas, correctas_seguidas, bomba_usada, estado, preguntas, juego_terminado_por_preguntas, x2_usado, doble_chance_usado, pasar_usado):
    if entrada_nombre.strip() and entrada_nombre.isalpha():
        nombre_jugador = entrada_nombre
        guardar_resultado(nombre_jugador, puntaje)
        estado = MENU
        preguntas.clear()
        preguntas.extend(cargar_preguntas())
        puntaje = PUNTAJE_INICIAL
        vidas = DIFICULTADES["MEDIO"]["vidas"]
        correctas_seguidas = CORRECTAS_SEGUIDAS_INICIAL
        bomba_usada = False
        x2_usado = X2_USADO_INICIAL
        doble_chance_usado = DOBLE_CHANCE_USADO_INICIAL
        pasar_usado = PASAR_USADO_INICIAL
        entrada_nombre = ""
        nombre_jugador = ""
        juego_terminado_por_preguntas = False
    return {
        "nombre_jugador": nombre_jugador,
        "entrada_nombre": entrada_nombre,
        "puntaje": puntaje,
        "vidas": vidas,
        "correctas_seguidas": correctas_seguidas,
        "bomba_usada": bomba_usada,
        "estado": estado,
        "preguntas": preguntas,
        "juego_terminado_por_preguntas": juego_terminado_por_preguntas,
        "x2_usado": x2_usado,
        "doble_chance_usado": doble_chance_usado,
        "pasar_usado": pasar_usado
    }