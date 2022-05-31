import pygame
import numpy as np
from OpenGL.GL import *

class GameApp:

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((960, 540), pygame.OPENGL|pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        glClearColor(1.0, 1.0, 1.0, 1)
        self.mainloop()

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            pygame.display.flip()
            self.clock.tick(60)

    def quit(self):
        pygame.quit()

if __name__ == "__main__":
    game = GameApp()
