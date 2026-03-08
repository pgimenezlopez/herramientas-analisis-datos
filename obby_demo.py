import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 900, 600 # Ensanché un poco la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modern Obby: Escaleras y Matemáticas")
clock = pygame.time.Clock()

# --- Paleta Moderna ---
BG_COLOR = (30, 30, 34)
PLAYER_COLOR = (0, 255, 204)
PLATFORM_COLOR = (60, 60, 70)
CHECKPOINT_COLOR = (255, 0, 128)
LAVA_COLOR = (255, 80, 80)
TEXT_COLOR = (255, 255, 255)
MATH_COLOR = (255, 215, 0) # Dorado para el texto de matemáticas

# --- Variables del Jugador ---
player_rect = pygame.Rect(50, 450, 30, 30)
vel_y = 0
vel_x = 6
gravity = 0.5
jump_power = -11
is_jumping = False
respawn_pos = [50, 450]
trail = []

# --- Variables del Desafío Matemático ---
font = pygame.font.SysFont("Arial", 28, bold=True)
big_font = pygame.font.SysFont("Arial", 40, bold=True)

math_active = False
num1, num2 = 0, 0
player_answer = ""
math_solved_correctly = False
math_failed = False

# --- Definición del Nivel ---
# Añadimos más escalones y le damos 'id' a las plataformas especiales
platforms = [
    # Escalera inicial
    {"rect": pygame.Rect(0, 500, 100, 100), "type": "normal", "color": PLATFORM_COLOR},
    {"rect": pygame.Rect(150, 450, 60, 20), "type": "normal", "color": PLATFORM_COLOR},
    {"rect": pygame.Rect(250, 400, 60, 20), "type": "normal", "color": PLATFORM_COLOR},
    {"rect": pygame.Rect(350, 350, 60, 20), "type": "normal", "color": PLATFORM_COLOR},
    
    # Plataforma móvil donde ocurre la pregunta
    {"rect": pygame.Rect(450, 300, 100, 20), "type": "moving", "color": PLATFORM_COLOR, "id": "math_plat", "speed": 2, "dir": 1, "min_x": 450, "max_x": 550},
    
    # La plataforma trampa (El "escalón que viene")
    {"rect": pygame.Rect(650, 250, 80, 20), "type": "trap", "color": PLATFORM_COLOR, "id": "trap_plat", "speed": 4, "dir": 1, "min_x": 600, "max_x": 750, "is_moving": False},
    
    # Checkpoint final
    {"rect": pygame.Rect(800, 150, 80, 20), "type": "checkpoint", "color": CHECKPOINT_COLOR},
    
    # Lava
    {"rect": pygame.Rect(0, 580, WIDTH, 20), "type": "lava", "color": LAVA_COLOR}
]

running = True
while running:
    # 1. Eventos y Teclado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            # Salto
            if event.key == pygame.K_SPACE and not is_jumping:
                vel_y = jump_power
                is_jumping = True
                
            # Captura de respuesta matemática
            if math_active:
                if event.key == pygame.K_RETURN: # Presionó Enter
                    if player_answer.isdigit() and int(player_answer) == (num1 * num2):
                        math_solved_correctly = True
                        math_active = False
                    else:
                        math_failed = True
                        math_active = False
                        # Activar la trampa
                        for plat in platforms:
                            if plat.get("id") == "trap_plat":
                                plat["is_moving"] = True
                elif event.key == pygame.K_BACKSPACE: # Borrar número
                    player_answer = player_answer[:-1]
                elif event.unicode.isdigit(): # Ingresar número
                    player_answer += event.unicode

    # Movimiento horizontal
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_rect.x -= vel_x
    if keys[pygame.K_RIGHT]: player_rect.x += vel_x

    # 2. Lógica de Plataformas Móviles y Trampas
    for plat in platforms:
        if plat["type"] == "moving" or (plat["type"] == "trap" and plat.get("is_moving") == True):
            plat["rect"].x += plat["speed"] * plat["dir"]
            if plat["rect"].x > plat["max_x"] or plat["rect"].x < plat["min_x"]:
                plat["dir"] *= -1

    # 3. Físicas Modernas
    vel_y += gravity
    if vel_y > 4: vel_y = 4 
    player_rect.y += vel_y

    # 4. Colisiones
    is_jumping = True
    for plat in platforms:
        if player_rect.colliderect(plat["rect"]):
            if plat["type"] == "lava":
                # RESETEAR TODO AL MORIR
                player_rect.topleft = respawn_pos
                vel_y = 0
                trail.clear()
                math_active = False
                math_solved_correctly = False
                math_failed = False
                player_answer = ""
                for p in platforms:
                    if p.get("id") == "trap_plat":
                        p["is_moving"] = False
                break
                
            elif plat["type"] == "checkpoint":
                respawn_pos = [plat["rect"].x, plat["rect"].y - player_rect.height]
            
            # Frenar caída si aterriza
            if vel_y > 0 and player_rect.bottom <= plat["rect"].bottom + 10:
                player_rect.bottom = plat["rect"].top
                vel_y = 0
                is_jumping = False
                
                # Herencia de movimiento
                if plat["type"] == "moving" or (plat["type"] == "trap" and plat.get("is_moving") == True):
                    player_rect.x += plat["speed"] * plat["dir"]
                    
                # Disparador del problema matemático
                if plat.get("id") == "math_plat" and not math_solved_correctly and not math_failed:
                    if not math_active:
                        math_active = True
                        num1 = random.randint(2, 9) # Tablas del 2 al 9
                        num2 = random.randint(2, 9)
                        player_answer = ""

    # 5. Efecto de Estela
    trail.append(player_rect.center)
    if len(trail) > 12: trail.pop(0)

    # 6. Renderizado Visual
    screen.fill(BG_COLOR)

    # Dibujar plataformas
    for plat in platforms:
        color = CHECKPOINT_COLOR if plat["type"] == "checkpoint" else plat["color"]
        if plat["type"] == "lava": color = LAVA_COLOR
        # Si la trampa se activó, la pintamos un poco rojiza para avisar del peligro
        if plat.get("id") == "trap_plat" and plat.get("is_moving") == True:
            color = (200, 100, 100) 
            
        pygame.draw.rect(screen, color, plat["rect"], border_radius=10)

    # Dibujar la estela y el pañuelo
    for i, pos in enumerate(trail):
        size = (i / 12) * 25 
        r = pygame.Rect(0, 0, size, size)
        r.center = pos
        pygame.draw.rect(screen, PLAYER_COLOR, r, border_radius=6)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect, border_radius=8)

    # UI del Desafío Matemático
    if math_active:
        question_text = big_font.render(f"¿Cuánto es {num1} x {num2}?", True, MATH_COLOR)
        answer_text = big_font.render(player_answer + "_", True, TEXT_COLOR) # El guión bajo simula el cursor
        
        # Centrar el texto en la parte superior de la pantalla
        screen.blit(question_text, (WIDTH//2 - question_text.get_width()//2, 50))
        screen.blit(answer_text, (WIDTH//2 - answer_text.get_width()//2, 100))
        
        instruccion = font.render("(Escribe y presiona ENTER)", True, TEXT_COLOR)
        screen.blit(instruccion, (WIDTH//2 - instruccion.get_width()//2, 150))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()