from typing import List
import random
import math
import pygame


class Particle:
    def __init__(self, pos: List[int], vel: List[float], max_age: float, age_factor: float = 1.0):
        self.pos = pos.copy()
        self.vel = vel.copy()
        self.max_age = max_age
        self.age_factor = age_factor
        self.age = 0

    def update(self, dt: float):
        self.age += dt * self.age_factor
        self.pos[0] += dt * self.vel[0]
        self.pos[1] += dt * self.vel[1]

    @property
    def age_percent(self) -> float:
        return self.age / self.max_age
    
    @property
    def is_dead(self) -> bool:
        return self.age >= self.max_age
    

class Fire_Particle(Particle):
    def __init__(self, pos: List[int]):
        vel = [random.uniform(-17, 17), random.uniform(-30, -100)]
        max_age = random.uniform(1, 3)
        super().__init__(pos, vel, max_age, age_factor = 2.5)
        self.radius = 2
        self.palette = (
            (255, 255, 0),
            (255, 173, 51),
            (247, 117, 33), 
            (191, 74, 46),
            (115, 61, 56),
            (61, 38, 48),
        )

    def update(self, dt: float):
        super().update(dt)
        self.vel[0] += math.sin(self.age * 5) * 0.25
        self.radius += dt * 4.7

    def render(self, surface: pygame.Surface):
        i = min(int(self.age_percent * len(self.palette)), len(self.palette) - 1)
        a = max(0, int(255 * (1 - self.age_percent)))
        pygame.draw.circle(surface, (*self.palette[i], a), self.pos, self.radius)


if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((1280, 720), pygame.SRCALPHA)
    surface = pygame.Surface((320, 180), pygame.SRCALPHA)

    clock = pygame.time.Clock()

    living_particles: List[Particle] = []
    dead_particles: List[Particle] = []
    accumulator = 0

    mouse_btn = False
    mouse_pos = [0, 0]

    running = True
    while running:
        # event calls =====================
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse_btn = True
                
            if e.type == pygame.MOUSEBUTTONUP:
                mouse_btn = False
            
            if e.type == pygame.MOUSEMOTION:
                mouse_pos = list(pygame.mouse.get_pos())
        # =================================

        # update calls ====================
        dt = clock.tick(60) / 1000
 
        accumulator += dt
        while accumulator >= 1 / 120:
            accumulator -= 1 / 120
            if mouse_btn:
                living_particles.append(Fire_Particle([mouse_pos[0] / 4, mouse_pos[1] / 4]))
        # =================================

        #print(len(living_particles))

        # render calls ====================
        surface.fill((0, 0, 0))

        for p in living_particles:
            if p.is_dead:
                dead_particles.append(p)
                continue
            p.update(dt)
            p.render(surface)
        for p in dead_particles:
            living_particles.remove(p)
        dead_particles.clear()

        scaled = pygame.transform.scale(surface, (1280, 720))
        window.blit(scaled, (0, 0))
        pygame.display.flip()
        # =================================

    pygame.quit()