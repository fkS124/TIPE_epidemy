import pygame
import random

# Paramètres de la simulation
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_PERSONS = 100
INFECTION_RATE = 0.03
INFECTION_RADIUS = 10
INFECTION_DURATION = 7000
HEALTHY_COLOR = (0, 255, 0)
INFECTED_COLOR = (255, 0, 0)
RECOVERED_COLOR = (0, 0, 255)

class Person:
    def __init__(self, x, y, status):
        self.x = x
        self.y = y
        self.dx = random.randint(-1, 1)
        self.dy = random.randint(-1, 1)
        self.status = status
        self.infection_timer = INFECTION_DURATION if status == "infected" else 0

    def update(self, persons):
        if self.status == "infected":
            self.infection_timer -= 1
            if self.infection_timer <= 0:
                self.status = "recovered"

        if self.status == "healthy":
            for person in persons:
                if person.status == "infected":
                    distance = ((self.x - person.x)**2 + (self.y - person.y)**2)**0.5
                    if distance < INFECTION_RADIUS:
                        if random.random() < INFECTION_RATE:
                            self.status = "infected"
                            self.infection_timer = INFECTION_DURATION
                            break

        self.x += self.dx
        self.y += self.dy

        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.dx *= -1
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.dy *= -1

    def draw(self, screen):
        if self.status == "healthy":
            color = HEALTHY_COLOR
        elif self.status == "infected":
            color = INFECTED_COLOR
        else:
            color = RECOVERED_COLOR

        pygame.draw.circle(screen, color, (self.x, self.y), 5)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Epidemic Simulation")

persons = [Person(random.randint(0, SCREEN_WIDTH), 
                  random.randint(0, SCREEN_HEIGHT),
                  "healty" if random.randint(0, 100) > 20 else "infected") for _ in range(NUM_PERSONS)]

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for person in persons:
        person.update(persons)
        person.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()