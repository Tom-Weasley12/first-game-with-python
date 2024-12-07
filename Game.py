import pygame
import sys
import random

pygame.init()

pygame.mixer.music.load("musica_fondo.mp3")
pygame.mixer.music.play(-1)
sonido_powerup = pygame.mixer.Sound("powerup.mp3")
sonido_meta = pygame.mixer.Sound("victoria.mp3")
sonido_perder = pygame.mixer.Sound("derrota.mp3")

ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laberinto")

COLOR_FONDO = (30, 30, 30)
COLOR_JUGADOR = (50, 200, 50)
COLOR_PARED = (200, 50, 50)
COLOR_META = (50, 50, 200)
COLOR_ENEMIGO = (200, 0, 0)
COLOR_POWERUP = (255, 223, 0)

tamaño_jugador = 40
x_jugador, y_jugador = ANCHO // 2, ALTO // 2
velocidad = 5
velocidad_normal = 5

paredes = [
    pygame.Rect(150, 100, 500, 20),
    pygame.Rect(150, 200, 20, 300),
    pygame.Rect(630, 200, 20, 300),
    pygame.Rect(150, 500, 500, 20)
]

meta = pygame.Rect(700, 550, 50, 50)

enemigo = pygame.Rect(300, 300, 40, 40)
velocidad_enemigo = 3

powerup = pygame.Rect(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 50), 30, 30)
powerup_activo = False
duracion_powerup = 3000  # 3 segundos
tiempo_powerup = 0

reloj = pygame.time.Clock()


def mostrar_texto(texto):
    """Muestra un texto centrado en la pantalla durante 2 segundos."""
    ventana.fill(COLOR_FONDO)
    fuente = pygame.font.SysFont(None, 75)
    mensaje = fuente.render(texto, True, (255, 255, 255))
    ventana.blit(mensaje, ((ANCHO - mensaje.get_width()) // 2, (ALTO - mensaje.get_height()) // 2))
    pygame.display.flip()
    pygame.time.wait(2000)


def pantalla_inicio():
    """Pantalla de inicio que espera a que el usuario presione ENTER."""
    mostrar_texto("Presiona ENTER para empezar")
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False


pantalla_inicio()
jugando = True
while jugando:
    tiempo_actual = pygame.time.get_ticks()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    teclas = pygame.key.get_pressed()
    jugador_rect = pygame.Rect(x_jugador, y_jugador, tamaño_jugador, tamaño_jugador)

    # Desactivar powerup después de su duración
    if powerup_activo and tiempo_actual - tiempo_powerup > duracion_powerup:
        velocidad = velocidad_normal
        powerup_activo = False

    # Movimiento del jugador
    if teclas[pygame.K_LEFT] and x_jugador > 0:
        nuevo_rect = jugador_rect.move(-velocidad, 0)
        if not any(nuevo_rect.colliderect(pared) for pared in paredes):
            x_jugador -= velocidad

    if teclas[pygame.K_RIGHT] and x_jugador < ANCHO - tamaño_jugador:
        nuevo_rect = jugador_rect.move(velocidad, 0)
        if not any(nuevo_rect.colliderect(pared) for pared in paredes):
            x_jugador += velocidad

    if teclas[pygame.K_UP] and y_jugador > 0:
        nuevo_rect = jugador_rect.move(0, -velocidad)
        if not any(nuevo_rect.colliderect(pared) for pared in paredes):
            y_jugador -= velocidad

    if teclas[pygame.K_DOWN] and y_jugador < ALTO - tamaño_jugador:
        nuevo_rect = jugador_rect.move(0, velocidad)
        if not any(nuevo_rect.colliderect(pared) for pared in paredes):
            y_jugador += velocidad

    # Movimiento del enemigo (vertical)
    enemigo.y += velocidad_enemigo
    if enemigo.top <= 0 or enemigo.bottom >= ALTO:
        velocidad_enemigo *= -1

    # Verificar colisión con la meta
    if jugador_rect.colliderect(meta):
        sonido_meta.play()
        mostrar_texto("¡HAS GANADO!")
        jugando = False

    # Verificar colisión con el enemigo
    if jugador_rect.colliderect(enemigo):
        sonido_perder.play()
        mostrar_texto("HAS PERDIDO!")
        jugando = False

    # Verificar colisión con el powerup
    if jugador_rect.colliderect(powerup):
        sonido_powerup.play()
        powerup_activo = True
        tiempo_powerup = tiempo_actual
        velocidad = 10
        powerup.x, powerup.y = random.randint(50, ANCHO - 50), random.randint(50, ALTO - 50)

    # Dibujar elementos en pantalla
    ventana.fill(COLOR_FONDO)
    pygame.draw.rect(ventana, COLOR_JUGADOR, (x_jugador, y_jugador, tamaño_jugador, tamaño_jugador))

    for pared in paredes:
        pygame.draw.rect(ventana, COLOR_PARED, pared)

    pygame.draw.rect(ventana, COLOR_META, meta)
    pygame.draw.rect(ventana, COLOR_ENEMIGO, enemigo)

    if not powerup_activo:
        pygame.draw.rect(ventana, COLOR_POWERUP, powerup)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
