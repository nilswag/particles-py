
class Particle:
    def __init__(self):
        pass

def main():
    import pygame
    import imgui

    window = pygame.display.set_mode((800, 800))
    surf = pygame.Surface((400, 400))
    clock = pygame.time.Clock()
    framerate = 60 # 60 fps

    running = True
    while running:
        dt = max(clock.tick(framerate), 0.05) # clamp dt to 20 fps

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        surf.fill((0, 0, 0))
        pygame.transform.scale(surf, window.get_size(), window)
        pygame.display.flip()

if __name__ == "__main__":
    main()