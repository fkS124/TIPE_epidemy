import pygame as pg 

v = pg.Vector2

class Car:

    def __init__(self, display, x, y):
        self.display = display
        self.image = pg.Surface((20, 20), pg.SRCALPHA)
        self.rect = pg.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = v(x, y)
        self.angle = 0
        self.vel = 10
        self.rotated_image = self.image.copy()
        self.last_frame_angle = 0

        self.draw()

    def draw(self):
        w, h = self.rect.size
        pg.draw.polygon(self.image, (255, 0, 0), [
            (0, h), (w, h), (w//2,0)
        ])

    def rotate(self):
        self.rotated_image = pg.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_image.get_rect(center=self.rect.center)

    def update(self):
        if self.last_frame_angle != self.angle:
            self.last_frame_angle = self.angle
            self.rotate()
        self.display.blit(self.rotated_image, self.rect)

        self.rect.topleft += self.vel*(v(0, -1).rotate(-self.angle)).normalize()

pg.init()
W, H = 500, 500
display = pg.display.set_mode((W, H))
running = True
clock = pg.time.Clock()
car = Car(display, 250, 250)
pts = []
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

    display.fill((255, 255, 255))
    try:
        pg.draw.lines(display, (0, 0, 0), False, pts)
    except:
        pass
    car.update()
    car.angle += 5
    pts.append(car.rect.center)

    pg.display.update()
    clock.tick(30)