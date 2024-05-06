import pygame
import random
import math

# Paramètres de la fenêtre
WIDTH = 800
HEIGHT = 600
FPS = 60

# Paramètres des boules
BALL_RADIUS = 20
BALL_COLOR = (255, 0, 0)
NUM_BALLS = 10

# Classe pour représenter une boule
class Ball:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    # Mettre à jour la position de la boule
    def update(self, balls):
        self.x += self.dx
        self.y += self.dy

        # Rebondir sur les bords
        if self.x - BALL_RADIUS < 0 or self.x + BALL_RADIUS > WIDTH:
            self.dx *= -1
        if self.y - BALL_RADIUS < 0 or self.y + BALL_RADIUS > HEIGHT:
            self.dy *= -1

        # Rebondir sur les autres boules
        for ball in balls:
            if ball != self:
                distance = math.sqrt((self.x - ball.x)**2 + (self.y - ball.y)**2)
                if distance <= 2 * BALL_RADIUS:
                    self.dx *= -1
                    self.dy *= -1
                    ball.dx *= -1
                    ball.dy *= -1

    # Dessiner la boule sur l'écran
    def draw(self, screen):
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)

# Initialiser Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls")
clock = pygame.time.Clock()

balls = []
# Ajouter des boules initiales
for _ in range(NUM_BALLS):
    x = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
    y = random.randint(BALL_RADIUS, HEIGHT - BALL_RADIUS)
    dx = random.randint(-5, 5)
    dy = random.randint(-5, 5)
    balls.append(Ball(x, y, dx, dy))

# Boucle principale
running = True
while running:
    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mettre à jour la position de chaque boule
    for ball in balls:
        ball.update(balls)

    # Dessiner l'arrière-plan
    screen.fill((255, 255, 255))

    # Dessiner les boules
    for ball in balls:
        ball.draw(screen)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter le FPS
    clock.tick(FPS)

# Quitter Pygame
pygame.quit()
