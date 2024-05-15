import pygame

class Obstacle:
    def __init__(self, x, y, radius):
        self.position = pygame.math.Vector2(x, y)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), self.radius)