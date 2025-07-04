import pygame
from constantes import *
from funciones import *
from PIL import Image

pygame.init()
pygame.mixer.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Preguntados - Dragon Ball")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)
fuente = pygame.font.SysFont("arial", 18)
fuente_game_over = pygame.font.SysFont("arial", 36)  # Fuente más grande para Game Over y animación
reloj = pygame.time.Clock()

try:
    musica_principal = pygame.mixer.Sound("dbz_principal.wav")
    volumen_musica = VOLUMEN_INICIAL
    musica_principal.set_volume(volumen_musica)
    musica_sonando = True
    musica_principal.play(-1)
except FileNotFoundError:
    musica_principal = None
    musica_sonando = False
    volumen_musica = VOLUMEN_INICIAL

try:
    musica_preguntas = pygame.mixer.Sound("dbz_preguntas.wav")
    musica_preguntas.set_volume(volumen_musica)
except FileNotFoundError:
    musica_preguntas = None

try:
    incorrect_sound = pygame.mixer.Sound("dbz_fallaste.wav")
except FileNotFoundError:
    incorrect_sound = None

try:
    correct_sound = pygame.mixer.Sound("dbz_correcto.wav")
except FileNotFoundError:
    correct_sound = None

try:
    game_over_sound = pygame.mixer.Sound("game_over.wav")
except FileNotFoundError:
    game_over_sound = None

try:
    comience_juego_sound = pygame.mixer.Sound("comience_el_juego.wav")
except FileNotFoundError:
    comience_juego_sound = None

musica_actual = musica_principal

preguntas = []
puntaje = PUNTAJE_INICIAL
vidas = DIFICULTADES["MEDIO"]["vidas"]
correctas_seguidas = CORRECTAS_SEGUIDAS_INICIAL
pregunta_actual = None
opciones = []
respuesta_correcta = ""
bomba_usada = False
x2_usado = X2_USADO_INICIAL
doble_chance_usado = DOBLE_CHANCE_USADO_INICIAL
doble_chance_activo = False
opciones_restantes = []
pasar_usado = PASAR_USADO_INICIAL
nombre_jugador = ""
entrada_nombre = ""
estado = MENU
juego_terminado_por_preguntas = False
mensaje_comodin = ""
mensaje_comodin_tiempo = 0
tiempo_inicio = 0
dificultad_seleccionada = "MEDIO"
cuenta_regresiva = 3  # Para la animación de inicio
cuenta_regresiva_tiempo = 0

# Carga de fondo_cell.gif para pantallas no relacionadas con el juego
try:
    gif = Image.open("fondo_cell.gif")
    gif_frames = []
    frame = gif.copy().convert("RGBA")
    frame = frame.resize((ANCHO, ALTO))
    gif_frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
    gif.seek(0)
    gif_frame_count = gif.n_frames
except Exception:
    gif_frames = [pygame.Surface((ANCHO, ALTO)).convert_alpha()]
    gif_frames[0].fill(BLANCO)
    gif_frame_count = 1

# Carga de pantalla_juego.png para el estado JUEGO
try:
    juego_background = pygame.image.load("pantalla_juego.png")
    juego_background = pygame.transform.scale(juego_background, (ANCHO, ALTO))
except FileNotFoundError:
    juego_background = pygame.Surface((ANCHO, ALTO)).convert_alpha()
    juego_background.fill(BLANCO)

# Carga de cell_dragon_ball.gif para el efecto Toasty
try:
    toasty_gif = Image.open("cell_dragon_ball.gif")
    toasty_frames = []
    frame = toasty_gif.copy().convert("RGBA")
    frame = frame.resize((100, 100))  # Tamaño pequeño para el efecto Toasty
    toasty_frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
    toasty_gif.seek(0)
    toasty_frame_count = toasty_gif.n_frames
except Exception:
    toasty_frames = [pygame.Surface((100, 100)).convert_alpha()]
    toasty_frames[0].fill(BLANCO)
    toasty_frame_count = 1

gif_frame_index = 0
gif_frame_delay = gif.info.get('duration', 100) if 'gif' in locals() else 100
toasty_frame_index = 0
toasty_frame_delay = toasty_gif.info.get('duration', 50) if 'toasty_gif' in locals() else 50
gif_last_update = pygame.time.get_ticks()
toasty_last_update = pygame.time.get_ticks()
toasty_active = False
toasty_type = None  # "correcto" o "incorrecto"
toasty_x = -100  # Posición inicial fuera de la pantalla (izquierda)
toasty_direction = "ida"  # "ida" o "vuelta"
toasty_start_time = 0
ultimo_click_tiempo = 0  # Para manejar clics en el botón Continuar

def principal():
    global ejecutando, estado, puntaje, vidas, correctas_seguidas, pregunta_actual, opciones, respuesta_correcta, bomba_usada, x2_usado, doble_chance_usado, doble_chance_activo, opciones_restantes, pasar_usado, nombre_jugador, entrada_nombre, musica_sonando, volumen_musica, gif_frame_index, gif_last_update, juego_terminado_por_preguntas, preguntas, mensaje_comodin, mensaje_comodin_tiempo, tiempo_inicio, musica_actual, dificultad_seleccionada, toasty_active, toasty_type, toasty_x, toasty_direction, toasty_frame_index, toasty_last_update, toasty_start_time, ultimo_click_tiempo, cuenta_regresiva, cuenta_regresiva_tiempo
    preguntas.extend(cargar_preguntas())
    ejecutando = True
    estado_anterior = None

    while ejecutando:
        now = pygame.time.get_ticks()
        # Actualizar fondo_cell.gif (solo para estados no JUEGO ni GAME_OVER)
        if estado not in [JUEGO, GAME_OVER] and now - gif_last_update > gif_frame_delay:
            gif_frame_index = (gif_frame_index + 1) % gif_frame_count
            gif_last_update = now

        # Actualizar animación Toasty
        if toasty_active:
            toasty_rect = pygame.Rect(toasty_x, ALTO//2, 100, 100)
            opciones_rect = pygame.Rect(200, 150, 400, 180)
            if toasty_direction == "ida":
                toasty_x += (ANCHO + 200) / (2.0 * FPS)
                if toasty_rect.colliderect(opciones_rect):
                    toasty_direction = "vuelta"
            else:
                toasty_x -= (ANCHO + 200) / (2.5 * FPS)
            if now - toasty_last_update > toasty_frame_delay:
                toasty_frame_index = (toasty_frame_index + 1) % toasty_frame_count
                toasty_last_update = now
            if toasty_frame_index >= len(toasty_frames):
                try:
                    toasty_gif.seek(toasty_frame_index)
                    frame = toasty_gif.copy().convert("RGBA")
                    frame = frame.resize((100, 100))
                    toasty_frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
                except Exception:
                    toasty_frames.append(toasty_frames[0])
            if toasty_direction == "vuelta" and toasty_x <= -100 or now - toasty_start_time > 4500:
                toasty_active = False
                toasty_x = -100
                toasty_direction = "ida"
                toasty_frame_index = 0

        if mensaje_comodin and now - mensaje_comodin_tiempo > 2000:
            mensaje_comodin = ""

        if estado != estado_anterior:
            if estado == JUEGO and musica_preguntas and musica_sonando:
                if musica_actual != musica_preguntas or not pygame.mixer.get_busy():
                    if musica_actual:
                        musica_actual.stop()
                    musica_actual = musica_preguntas
                    musica_actual.set_volume(volumen_musica)
                    musica_actual.play(-1)
            elif estado == GAME_OVER and game_over_sound:
                pygame.mixer.stop()
                game_over_sound.play()
            elif estado == INICIO_JUEGO and comience_juego_sound:
                pygame.mixer.stop()
                comience_juego_sound.play()
                cuenta_regresiva = 3
                cuenta_regresiva_tiempo = now
            elif musica_principal and musica_sonando:
                if musica_actual != musica_principal or not pygame.mixer.get_busy():
                    if musica_actual:
                        musica_actual.stop()
                    musica_actual = musica_principal
                    musica_actual.set_volume(volumen_musica)
                    musica_actual.play(-1)
            estado_anterior = estado

        # Carga dinámica de fotogramas para fondo_cell.gif
        if estado not in [JUEGO, GAME_OVER] and gif_frame_index >= len(gif_frames):
            try:
                gif.seek(gif_frame_index)
                frame = gif.copy().convert("RGBA")
                frame = frame.resize((ANCHO, ALTO))
                gif_frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
            except Exception:
                gif_frames.append(gif_frames[0])

        # Renderiza el fondo correspondiente
        pantalla.blit(juego_background if estado in [JUEGO, GAME_OVER] else gif_frames[gif_frame_index], (0, 0))

        if estado == MENU:
            botones_menu = [
                ("Jugar", GRIS, VERDE, lambda: globals().update(estado=INICIO_JUEGO)),
                ("RankingTop 10", GRIS, AZUL, lambda: globals().update(estado=PUNTAJES)),
                ("Configuración", GRIS, AZUL, lambda: globals().update(estado=CONFIG)),
                ("Opciones de Juego", GRIS, AZUL, lambda: globals().update(estado=CONFIG_JUEGO, dificultad_seleccionada="MEDIO")),
                ("Salir", GRIS, ROJO, lambda: globals().update(ejecutando=False)),
            ]
            ancho_boton = 200
            alto_boton = 50
            espacio = 25
            total_altura = len(botones_menu) * alto_boton + (len(botones_menu) - 1) * espacio
            y_inicial = (ALTO - total_altura) // 2

            for i, (texto, color_inactivo, color_activo, accion) in enumerate(botones_menu):
                y = y_inicial + i * (alto_boton + espacio)
                dibujar_boton(pantalla, fuente, texto, 300, y, ancho_boton, alto_boton, color_inactivo, color_activo, accion)
        
        elif estado == INICIO_JUEGO:
            if now - cuenta_regresiva_tiempo > 1000:  # Actualizar cada segundo
                cuenta_regresiva -= 1
                cuenta_regresiva_tiempo = now
            if cuenta_regresiva <= 0:
                estado = JUEGO
                puntaje = PUNTAJE_INICIAL
                vidas = DIFICULTADES[dificultad_seleccionada]["vidas"]
                correctas_seguidas = CORRECTAS_SEGUIDAS_INICIAL
                bomba_usada = False
                x2_usado = X2_USADO_INICIAL
                doble_chance_usado = DOBLE_CHANCE_USADO_INICIAL
                pasar_usado = PASAR_USADO_INICIAL
                juego_terminado_por_preguntas = False
                pregunta_actual = None
                opciones = []
                respuesta_correcta = ""
                doble_chance_activo = False
                opciones_restantes = []
                mensaje_comodin = ""
                tiempo_inicio = 0
            else:
                fondo_animacion = pygame.Surface((400, 200))
                fondo_animacion.set_alpha(200)
                fondo_animacion.fill(GRIS)
                pantalla.blit(fondo_animacion, (200, 200))
                texto_animacion = fuente_game_over.render(f"El juego comienza en {cuenta_regresiva}", True, NEGRO)
                pantalla.blit(texto_animacion, (200 + (400 - texto_animacion.get_width()) // 2, 250))
        
        elif estado == JUEGO:
            if not pregunta_actual:
                if not preguntas:
                    estado = FIN_JUEGO
                    juego_terminado_por_preguntas = True
                else:
                    pregunta_actual = random.choice(preguntas)
                    opciones = [pregunta_actual[f"opcion{i+1}"] for i in range(4)]
                    random.shuffle(opciones)
                    respuesta_correcta = pregunta_actual["correcta"]
                    preguntas.remove(pregunta_actual)
                    opciones_restantes = opciones.copy()
                    doble_chance_activo = False
                    tiempo_inicio = pygame.time.get_ticks()
            
            else:
                tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio) / 1000
                if tiempo_transcurrido > DIFICULTADES[dificultad_seleccionada]["tiempo_pregunta"]:
                    vidas -= 1
                    pregunta_actual = None
                    opciones_restantes = []
                    doble_chance_activo = False
                    mensaje_comodin = "Tiempo agotado: -1 vida"
                    mensaje_comodin_tiempo = pygame.time.get_ticks()
                    if incorrect_sound:
                        incorrect_sound.play()
                    toasty_active = True
                    toasty_type = "incorrecto"
                    toasty_x = -100
                    toasty_direction = "ida"
                    toasty_frame_index = 0
                    toasty_start_time = pygame.time.get_ticks()
                    if vidas <= 0:
                        estado = GAME_OVER
                else:
                    fondo_texto = pygame.Surface((700, 50))
                    fondo_texto.set_alpha(200)
                    fondo_texto.fill(GRIS)
                    pantalla.blit(fondo_texto, (50, 50))
                    texto_pregunta = fuente.render(pregunta_actual["pregunta"], True, NEGRO)
                    pantalla.blit(texto_pregunta, (50, 50))
                    
                    opciones_a_mostrar = opciones_restantes if doble_chance_activo else opciones
                    for i, opcion in enumerate(opciones_a_mostrar):
                        dibujar_boton(pantalla, fuente, opcion, 200, 150 + i * 60, 400, 50, GRIS, AZUL, lambda opt=opcion: seleccionar_opcion(opt, incorrect_sound, correct_sound))
                    
                    base_y_comodin = 410
                    base_x_comodin = 50
                    ancho_boton = 170
                    espacio = 20
                    idx = 0
                    if not bomba_usada:
                        dibujar_boton(pantalla, fuente, "Bomba", base_x_comodin + idx * (ancho_boton + espacio), base_y_comodin, ancho_boton, 50, GRIS, ROJO, lambda: globals().update(opciones=usar_bomba(opciones, respuesta_correcta, bomba_usada)[0], bomba_usada=usar_bomba(opciones, respuesta_correcta, bomba_usada)[1], opciones_restantes=usar_bomba(opciones_restantes, respuesta_correcta, bomba_usada)[0], mensaje_comodin=usar_bomba(opciones, respuesta_correcta, bomba_usada)[2], mensaje_comodin_tiempo=pygame.time.get_ticks()))
                        idx += 1
                    if not x2_usado:
                        dibujar_boton(pantalla, fuente, "X2", base_x_comodin + idx * (ancho_boton + espacio), base_y_comodin, ancho_boton, 50, GRIS, ROJO, lambda: globals().update(x2_usado=usar_x2(x2_usado)[0], mensaje_comodin=usar_x2(x2_usado)[1], mensaje_comodin_tiempo=pygame.time.get_ticks()))
                        idx += 1
                    if not doble_chance_usado:
                        dibujar_boton(pantalla, fuente, "Doble Chance", base_x_comodin + idx * (ancho_boton + espacio), base_y_comodin, ancho_boton, 50, GRIS, ROJO, lambda: globals().update(doble_chance_usado=usar_doble_chance(doble_chance_usado)[0], mensaje_comodin=usar_doble_chance(doble_chance_usado)[1], mensaje_comodin_tiempo=pygame.time.get_ticks()))
                        idx += 1
                    if not pasar_usado:
                        dibujar_boton(pantalla, fuente, "Pasar", base_x_comodin + idx * (ancho_boton + espacio), base_y_comodin, ancho_boton, 50, GRIS, ROJO, lambda: globals().update(pregunta_actual=usar_pasar(pregunta_actual, preguntas)[0], preguntas=usar_pasar(pregunta_actual, preguntas)[1], pasar_usado=True, mensaje_comodin=usar_pasar(pregunta_actual, preguntas)[2], mensaje_comodin_tiempo=pygame.time.get_ticks(), tiempo_inicio=pygame.time.get_ticks()))
                    
                    fondo_stats = pygame.Surface((200, 100))
                    fondo_stats.set_alpha(200)
                    fondo_stats.fill(GRIS)
                    pantalla.blit(fondo_stats, (50, 500))
                    pantalla.blit(fuente.render(f"Puntaje: {puntaje}", True, NEGRO), (50, 500))
                    pantalla.blit(fuente.render(f"Vidas: {vidas}", True, NEGRO), (50, 550))
                    fondo_tiempo = pygame.Surface((200, 50))
                    fondo_tiempo.set_alpha(200)
                    fondo_tiempo.fill(GRIS)
                    pantalla.blit(fondo_tiempo, (550, 500))
                    tiempo_restante = max(0, int(DIFICULTADES[dificultad_seleccionada]["tiempo_pregunta"] - tiempo_transcurrido))
                    pantalla.blit(fuente.render(f"Tiempo: {tiempo_restante}", True, NEGRO), (550, 500))
                    if mensaje_comodin or doble_chance_activo:
                        fondo_mensaje = pygame.Surface((700, 30))
                        fondo_mensaje.set_alpha(200)
                        fondo_mensaje.fill(GRIS)
                        pantalla.blit(fondo_mensaje, (50, 110))
                        mensaje_mostrar = mensaje_comodin if mensaje_comodin else "Doble Chance: Selecciona otra opción"
                        pantalla.blit(fuente.render(mensaje_mostrar, True, NEGRO), (50, 110))
        
        elif estado == GAME_OVER:
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
            if rect_boton.collidepoint(mouse) and click[0] == 1 and now - ultimo_click_tiempo > 500:
                estado = FIN_JUEGO
                ultimo_click_tiempo = now
        
        elif estado == PUNTAJES:
            fondo_puntajes = pygame.Surface((700, 400))
            fondo_puntajes.set_alpha(200)
            fondo_puntajes.fill(GRIS)
            pantalla.blit(fondo_puntajes, (50, 50))
            puntajes_altos = cargar_puntajes()
            for i, entrada in enumerate(puntajes_altos):
                texto = f"{i+1}. {entrada['nombre']} - {entrada['puntaje']} ({entrada['fecha']})"
                pantalla.blit(fuente.render(texto, True, NEGRO), (50, 50 + i * 40))
            dibujar_boton(pantalla, fuente, "Volver", 300, 500, 200, 50, GRIS, AZUL, lambda: globals().update(estado=MENU))
        
        elif estado == CONFIG:
            texto_musica = "Música: ON" if musica_sonando else "Música: OFF"
            dibujar_boton(pantalla, fuente, texto_musica, 300, 200, 200, 50, GRIS, AZUL, lambda: globals().update(musica_sonando=alternar_musica(musica_actual, musica_sonando)))
            dibujar_boton(pantalla, fuente, "Subir Volumen", 300, 300, 200, 50, GRIS, AZUL, lambda: globals().update(volumen_musica=subir_volumen(musica_actual, volumen_musica)))
            dibujar_boton(pantalla, fuente, "Bajar Volumen", 300, 400, 200, 50, GRIS, AZUL, lambda: globals().update(volumen_musica=bajar_volumen(musica_actual, volumen_musica)))
            dibujar_boton(pantalla, fuente, "Volver", 300, 500, 200, 50, GRIS, AZUL, lambda: globals().update(estado=MENU))
        
        elif estado == CONFIG_JUEGO:
            fondo_config = pygame.Surface((700, 400))
            fondo_config.set_alpha(200)
            fondo_config.fill(GRIS)
            pantalla.blit(fondo_config, (50, 50))
            pantalla.blit(fuente.render(f"Dificultad: {dificultad_seleccionada}", True, NEGRO), (50, 50))
            pantalla.blit(fuente.render(f"Puntos por acierto: {DIFICULTADES[dificultad_seleccionada]['puntos_aciertos']}", True, NEGRO), (50, 90))
            pantalla.blit(fuente.render(f"Puntos por error: {DIFICULTADES[dificultad_seleccionada]['puntos_errores']}", True, NEGRO), (50, 130))
            pantalla.blit(fuente.render(f"Vidas: {DIFICULTADES[dificultad_seleccionada]['vidas']}", True, NEGRO), (50, 170))
            pantalla.blit(fuente.render(f"Tiempo por pregunta: {DIFICULTADES[dificultad_seleccionada]['tiempo_pregunta']}s", True, NEGRO), (50, 210))
            dibujar_boton(pantalla, fuente, "Fácil", 200, 300, 150, 50, GRIS, VERDE, lambda: globals().update(dificultad_seleccionada="FACIL"))
            dibujar_boton(pantalla, fuente, "Medio", 375, 300, 150, 50, GRIS, VERDE, lambda: globals().update(dificultad_seleccionada="MEDIO"))
            dibujar_boton(pantalla, fuente, "Difícil", 550, 300, 150, 50, GRIS, VERDE, lambda: globals().update(dificultad_seleccionada="DIFICIL"))
            dibujar_boton(pantalla, fuente, "Volver", 300, 400, 200, 50, GRIS, AZUL, lambda: globals().update(estado=MENU))
        
        elif estado == FIN_JUEGO:
            fondo_fin = pygame.Surface((700, 150))
            fondo_fin.set_alpha(200)
            fondo_fin.fill(GRIS)
            pantalla.blit(fondo_fin, (50, 50))
            mensaje = "¡Felicidades! Respondiste todas las preguntas" if juego_terminado_por_preguntas else "Fin del juego. Ingresa tu nombre:"
            pantalla.blit(fuente.render(mensaje, True, NEGRO), (50, 50))
            pantalla.blit(fuente.render(entrada_nombre, True, NEGRO), (50, 100))
            dibujar_boton(pantalla, fuente, "Guardar", 300, 500, 200, 50, GRIS, VERDE, lambda: globals().update(**guardar_y_reiniciar(nombre_jugador, entrada_nombre, puntaje, vidas, correctas_seguidas, bomba_usada, estado, preguntas, juego_terminado_por_preguntas, x2_usado, doble_chance_usado, pasar_usado)))

        if toasty_active:
            pantalla.blit(toasty_frames[toasty_frame_index], (toasty_x, ALTO//2))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if estado == FIN_JUEGO and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and entrada_nombre.strip() and entrada_nombre.isalpha():
                    resultado = guardar_y_reiniciar(nombre_jugador, entrada_nombre, puntaje, vidas, correctas_seguidas, bomba_usada, estado, preguntas, juego_terminado_por_preguntas, x2_usado, doble_chance_usado, pasar_usado)
                    globals().update(**resultado)
                    pregunta_actual = None
                    opciones = []
                    respuesta_correcta = ""
                    opciones_restantes = []
                    doble_chance_activo = False
                    mensaje_comodin = ""
                    tiempo_inicio = 0
                elif evento.key == pygame.K_BACKSPACE:
                    entrada_nombre = entrada_nombre[:-1]
                elif len(entrada_nombre) < LIMITE_NOMBRE and evento.unicode.isalpha():
                    entrada_nombre += evento.unicode

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()

def seleccionar_opcion(opcion, incorrect_sound, correct_sound):
    global estado, puntaje, vidas, correctas_seguidas, pregunta_actual, x2_usado, doble_chance_usado, doble_chance_activo, opciones_restantes, mensaje_comodin, mensaje_comodin_tiempo, tiempo_inicio, toasty_active, toasty_type, toasty_x, toasty_direction, toasty_frame_index, toasty_start_time
    resultado = verificar_respuesta(
        opcion, respuesta_correcta, puntaje, vidas, correctas_seguidas, pregunta_actual, estado,
        x2_usado, doble_chance_usado, doble_chance_activo, opciones, incorrect_sound, correct_sound,
        preguntas, dificultad_seleccionada
    )
    globals().update(**resultado)
    mensaje_comodin = resultado["mensaje_comodin"]
    mensaje_comodin_tiempo = pygame.time.get_ticks()
    if resultado["pregunta_actual"] is None and not doble_chance_activo:
        toasty_active = True
        toasty_type = "correcto" if opcion == respuesta_correcta else "incorrecto"
        toasty_x = -100
        toasty_direction = "ida"
        toasty_frame_index = 0
        toasty_start_time = pygame.time.get_ticks()
    if resultado["pregunta_actual"] is None:
        tiempo_inicio = pygame.time.get_ticks()
    if resultado["vidas"] <= 0 and not doble_chance_activo:
        estado = GAME_OVER

if __name__ == "__main__":
    principal()