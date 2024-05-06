import pygame as pg 
from random import randint

v = pg.math.Vector2

class Human:

    def __init__(self, x, y, infecte, dt_infection, dt_contagion):
        self.pos = v(x, y)
        self.vel = v(1, 0).rotate(randint(0, 360))

        self.infecte = infecte
        self.contagieux = infecte
        self.dt_contagion = dt_contagion
        self.dt_infection = dt_infection

        self.debut_infect = pg.time.get_ticks()
        self.change_vel = 0
        self.radius = 20
        self.next_frame_vel = v(0, 0)

    def update_vel(self, all_humans):
        if self.next_frame_vel != v(0, 0):
            self.vel = self.next_frame_vel.copy()
            self.next_frame_vel = v(0, 0)

        if self.pos.x + self.vel.x - self.radius < 0 or self.pos.x + self.radius + self.vel.x > 500:
            self.vel.x = -self.vel.x
        if self.pos.y + self.vel.y - self.radius < 0 or self.pos.y + self.radius + self.vel.y > 500:
            self.vel.y = -self.vel.y

        for cobaye in all_humans:
            if cobaye is not self:
                new_pos_cob = cobaye.pos + cobaye.vel
                new_pos_self = self.pos + self.vel
                if (d := new_pos_cob.distance_to(new_pos_self)) < self.radius + cobaye.radius:
                    self.next_frame_vel = -(new_pos_cob-new_pos_self).normalize()*self.vel.magnitude()
                    self.vel = self.vel.normalize()*d/2
                    cobaye.vel = cobaye.vel.normalize()*d/2
                    

    def update(self, all_humans):
        # Mouvement
        self.update_vel(all_humans)
        self.pos += self.vel

        # Gérer la contagion
        if self.contagieux and pg.time.get_ticks() - self.debut_infect > self.dt_contagion:
            self.contagieux = False
        if self.infecte and pg.time.get_ticks() - self.debut_infect > self.dt_infection:
            self.infecte = False


if __name__ == "__main__":
    pg.init()
    clock = pg.time.Clock()
    display = pg.display.set_mode((500, 500))
    cobayes = [Human(randint(100, 400), randint(100, 400), randint(0, 1), 1000, 1500)
                for _ in range(5)]

    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit

        display.fill((255, 255, 255))
        for cobaye in cobayes:
            cobaye.update(cobayes)
            pg.draw.circle(
                display,
                (255, 0, 0) if cobaye.infecte else (0, 255, 0),
                cobaye.pos,
                cobaye.radius
            )

        clock.tick(120)
        pg.display.update()