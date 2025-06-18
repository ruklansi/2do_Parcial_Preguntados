import pygame
import csv
import json
import random
from datetime import datetime

pygame.init()
pygame.mixer.init()

# Configuración de la pantalla y reloj
ANCHO, ALTO = 800, 600
FPS = 60
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.set_caption("Juego de Preguntas")
fuente = pygame.font.SysFont("arial", 24)
reloj = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (150, 150, 150)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Cargar música y sonidos(.mp3)
musica = pygame.mixer.Sound("background.mp3")
volumen_musica = 0.5
musica.set_volume(volumen_musica)
musica_sonando = True
musica.play(-1)  # Reproducir en bucle

# Estados del juego
MENU = 0
JUEGO = 1
PUNTUACION = 2
CONFIGURACION = 3
FIN_JUEGO = 4
estado = MENU

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

# Cargar preguntas desde un archivo CSV
def cargar_preguntas():
    with open("preguntas.csv", "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)
    
# Guardar puntuación en un archivo JSON
def guardar_resultado(nombre, puntaje):
    with open("partidas.json", "r") as archivo:
        datos = json.load(archivo)
    datos.append({"nombre": nombre, "puntaje": puntaje, "fecha": datetime.now().strftime("%d-%m-%Y %H:%M:%S")})
    with open("partidas.json", "w") as archivo:
        json.dump(datos, archivo, indent=4)
