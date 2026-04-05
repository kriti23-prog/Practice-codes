'''import pygame
import math

pygame.init()

# 🎨 Colors
Red = [255, 0, 0]
Green = [0, 255, 0]
White = [255, 255, 255]

# 🖥️ Window setup
WIDTH, HEIGHT = 500, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Simulation")

# 🌌 Constants
FPS = 60
MASS=345
PLANET_SIZE = 50
OBJ_SIZE = 9
VEL_SCALE = 0.1 
G=6.77 # Adjust for visible motion

# 🖼️ Background and planet (placeholder graphics)
BG =pygame.transform.scale(pygame.image.load("universe.png"), (WIDTH, HEIGHT))
PLANET =pygame.transform.scale(pygame.image.load("jupiter.png"), (PLANET_SIZE*2, PLANET_SIZE*2))


# 🚀 Ship class
class Ship:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(win, Green, (int(self.x), int(self.y)), OBJ_SIZE)

def move(self,planet=None):
    distance = math.sqrt((self.x - WIDTH // 2) ** 2 + (self.y - HEIGHT // 2) ** 2)
    force=G*( MASS / (distance)**2)
    acceleration = force / self.MASS
    angle =math.atan2(self.y - HEIGHT // 2, self.x - WIDTH // 2)
    self.vx -= acceleration * math.cos(angle)
    self.vy -= acceleration * math.sin(angle)
    


    self.x += self.vx
    self.y += self.vy
# 🧠 Main loop
def main():
    clock = pygame.time.Clock()
    running = True
    ships = []

    temp_obj_pos = None
    dragging = False

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                temp_obj_pos = mouse_pos
                dragging = True

            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                dragging = False
                if temp_obj_pos:
                    dx = mouse_pos[0] - temp_obj_pos[0]
                    dy = mouse_pos[1] - temp_obj_pos[1]
                    vx = dx * VEL_SCALE
                    vy = dy * VEL_SCALE
                    ships.append(Ship(temp_obj_pos[0], temp_obj_pos[1], vx, vy))
                    temp_obj_pos = None

        # 🎨 Draw background and planet
        win.blit(BG, (0, 0))
        win.blit(PLANET, (WIDTH // 2 - PLANET_SIZE, HEIGHT // 2 - PLANET_SIZE))

        # 🚀 Draw dragging arrow
        if dragging and temp_obj_pos:
            pygame.draw.circle(win, Red, temp_obj_pos, OBJ_SIZE)
            pygame.draw.line(win, White, temp_obj_pos, mouse_pos, 2)

        # 🛰️ Update and draw ships
        for ship in ships:
            ship.update()
            ship.draw(win)
            move(ship)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()'''

import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect")

PLANET_MASS = 100
SHIP_MASS = 60
G = 0.1
FPS = 30
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100

BG = pygame.transform.scale(pygame.image.load("universe.png"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("jupiter.png"), (PLANET_SIZE * 2, PLANET_SIZE * 2))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        win.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))

class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G * self.mass * planet.mass) / distance ** 2
        
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y
    
    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)

def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)
    return obj

def main():
    running = True
    clock = pygame.time.Clock()

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        win.blit(BG, (0, 0))

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)
        
        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_SIZE
            if off_screen or collided:
                objects.remove(obj)

        planet.draw()

        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()