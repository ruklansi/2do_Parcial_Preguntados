import pygame
import csv
import json
import random
from datetime import datetime
from constantes import *

pygame.init()
pygame.mixer.init()

# Configuración de la ventana y reloj
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Preguntados")
fuente = pygame.font.SysFont("arial", 24, bold=True)
reloj = pygame.time.Clock()

# Cargar música
musica_background = pygame.mixer.Sound("background_music.wav")
volumen_musica = 0.5
musica_background.set_volume(volumen_musica)
musica_sonando = True
musica_background.play(-1) # Reproducción en bucle

# Variables del juego
preguntas = []
puntaje = 0
vidas = 3
correctas_seguidas = 0
pregunta_actual = None
opciones = []
respuesta_correcta = ""
bomba_usada = False
nombre_jugador = ""
entrada_nombre = ""

# Cargar preguntas desde CSV
def cargar_preguntas():
    with open("preguntas.csv", "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)

# Guardar resultado en JSON
def guardar_resultado(nombre, puntaje):
    with open("partidas.json", "r") as archivo:
        datos = json.load(archivo)
    datos.append({"nombre": nombre, "puntaje": puntaje, "fecha": datetime.now().strftime("%d-%m-%Y")})
    with open("partidas.json", "w") as archivo:
        json.dump(datos, archivo, indent=4)

# Cargar puntajes altos
def cargar_puntajes():
    with open("partidas.json", "r") as archivo:
        datos = json.load(archivo)
    return sorted(datos, key=lambda x: x["puntaje"], reverse=True)[:10]

# Dibujar botón
def dibujar_boton(texto, x, y, ancho, alto, color_inactivo, color_activo, accion=None):
    raton = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()
    rect_boton = pygame.Rect(x, y, ancho, alto)
    color = color_activo if rect_boton.collidepoint(raton) else color_inactivo
    pygame.draw.rect(pantalla, color, rect_boton)
    texto_surf = fuente.render(texto, True, NEGRO)
    texto_rect = texto_surf.get_rect(center=rect_boton.center)
    pantalla.blit(texto_surf, texto_rect)
    if clic[0] == 1 and rect_boton.collidepoint(raton) and accion:
        pygame.time.wait(200)  # Evitar clics múltiples
        accion()

# Bucle principal
def principal():
    global estado, puntaje, vidas, correctas_seguidas, pregunta_actual, opciones, respuesta_correcta, bomba_usada, nombre_jugador, entrada_nombre
    preguntas = cargar_preguntas()
    ejecutando = True

    while ejecutando:
        pantalla.fill(BLANCO)
        
        if estado == MENU:
            dibujar_boton("Jugar", 300, 200, 200, 50, GRIS, VERDE, lambda: globals().update(estado=JUEGO, puntaje=0, vidas=3, correctas_seguidas=0, bomba_usada=False))
            dibujar_boton("Top 10", 300, 300, 200, 50, GRIS, AZUL, lambda: globals().update(estado=PUNTUACION))
            dibujar_boton("Configuración", 300, 400, 200, 50, GRIS, AZUL, lambda: globals().update(estado=CONFIGURACION))
        
        elif estado == JUEGO:
            if not pregunta_actual:
                if preguntas:  # Si quedan preguntas
                    pregunta_actual = random.choice(preguntas)
                    preguntas.remove(pregunta_actual)  # Eliminar la pregunta usada
                    opciones = [pregunta_actual[f"opcion{i+1}"] for i in range(4)]
                    random.shuffle(opciones)
                    respuesta_correcta = pregunta_actual["correcta"]
                else:
                    estado = FIN_JUEGO  # Si no quedan preguntas, termina el juego
            
            # Dibujar pregunta
            texto_pregunta = fuente.render(pregunta_actual["pregunta"], True, NEGRO)
            pantalla.blit(texto_pregunta, (50, 50))
            
            # Dibujar opciones
            for i, opcion in enumerate(opciones):
                dibujar_boton(opcion, 50, 150 + i * 60, 700, 50, GRIS, AZUL, lambda opt=opcion: verificar_respuesta(opt))
            
            # Dibujar botón Bomba
            if not bomba_usada:
                dibujar_boton("Bomba", 600, 450, 150, 50, GRIS, ROJO, usar_bomba)
            
            # Dibujar estadísticas
            pantalla.blit(fuente.render(f"Puntaje: {puntaje}", True, NEGRO), (50, 500))
            pantalla.blit(fuente.render(f"Vidas: {vidas}", True, NEGRO), (50, 550))
        
        elif estado == PUNTUACION:
            puntajes_altos = cargar_puntajes()
            for i, entrada in enumerate(puntajes_altos):
                texto = f"{i+1}. {entrada['nombre']} - {entrada['puntaje']} ({entrada['fecha']})"
                pantalla.blit(fuente.render(texto, True, NEGRO), (50, 50 + i * 40))
            dibujar_boton("Volver", 300, 500, 200, 50, GRIS, AZUL, lambda: globals().update(estado=MENU))
        
        elif estado == CONFIGURACION:
            texto_musica = "Música: ON" if musica_sonando else "Música: OFF"
            dibujar_boton(texto_musica, 300, 200, 200, 50, GRIS, AZUL, alternar_musica)
            dibujar_boton("Subir Volumen", 300, 300, 200, 50, GRIS, AZUL, subir_volumen)
            dibujar_boton("Bajar Volumen", 300, 400, 200, 50, GRIS, AZUL, bajar_volumen)
            dibujar_boton("Volver", 300, 500, 200, 50, GRIS, AZUL, lambda: globals().update(estado=MENU))
        
        elif estado == FIN_JUEGO:
            pantalla.blit(fuente.render("Fin del juego. Ingresa tu nombre:", True, NEGRO), (50, 50))
            pantalla.blit(fuente.render(entrada_nombre, True, NEGRO), (50, 100))
            dibujar_boton("Guardar", 300, 500, 200, 50, GRIS, VERDE, guardar_y_reiniciar)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if estado == FIN_JUEGO and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and entrada_nombre.strip():
                    guardar_y_reiniciar()
                elif evento.key == pygame.K_BACKSPACE:
                    entrada_nombre = entrada_nombre[:-1]
                elif len(entrada_nombre) < 20:
                    entrada_nombre += evento.unicode

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

# Verificar respuesta
def verificar_respuesta(opcion_seleccionada):
    global puntaje, vidas, correctas_seguidas, pregunta_actual, estado
    if opcion_seleccionada == respuesta_correcta:
        puntaje += 10
        correctas_seguidas += 1
        if correctas_seguidas >= 5:
            vidas += 1
            correctas_seguidas = 0
    else:
        puntaje -= 5
        vidas -= 1
        correctas_seguidas = 0
    pregunta_actual = None
    if vidas <= 0:
        estado = FIN_JUEGO

# Comodín Bomba
def usar_bomba():
    global opciones, bomba_usada
    if not bomba_usada:
        opciones_incorrectas = [opt for opt in opciones if opt != respuesta_correcta]
        random.shuffle(opciones_incorrectas)
        opciones = [respuesta_correcta, opciones_incorrectas[0]]  # Deja correcta y una incorrecta
        bomba_usada = True

# Controles de música
def alternar_musica():
    global musica_sonando
    musica_sonando = not musica_sonando
    if musica_sonando:
        musica_background.play(-1)
    else:
        musica_background.stop()

def subir_volumen():
    global volumen_musica
    volumen_musica = min(1.0, volumen_musica + 0.1)
    musica_background.set_volume(volumen_musica)

def bajar_volumen():
    global volumen_musica
    volumen_musica = max(0.0, volumen_musica - 0.1)
    musica_background.set_volume(volumen_musica)

# Guardar y reiniciar
def guardar_y_reiniciar():
    global nombre_jugador, entrada_nombre, estado, puntaje, vidas, correctas_seguidas, bomba_usada
    if entrada_nombre.strip():
        nombre_jugador = entrada_nombre
        guardar_resultado(nombre_jugador, puntaje)
        estado = MENU
        puntaje = 0
        vidas = 3
        correctas_seguidas = 0
        bomba_usada = False
        entrada_nombre = ""

if __name__ == "__main__":
    principal()