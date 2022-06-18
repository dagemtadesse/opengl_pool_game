import pygame
import numpy as np
from OpenGL.GL import *
import pyrr
from event_handler import EventHandler
from motion_controller import MotionController

from progress_bar import ProgressBar
from utils import createShader
from transformations import tableTransformation, cueTransformation

WIDTH, HEIGHT = 960, 540


class GameApp:

    def __init__(self):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                        pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.set_mode(
            (WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

        self.clock = pygame.time.Clock()
        self.shader = createShader(
            'shaders/vertex.shader',
            'shaders/fragment.shader')

        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, 'imageTexture'), 0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(.13, .16, 0.19, 1)  # rgb(34,40,49)

        self.progressBar = ProgressBar()

        import items

        self.whiteBall = items.whiteBall
        self.balls = items.balls
        self.ball8 = items.balls[0]
        self.plane = items.plane
        self.table = items.table
        self.poolCue = items.poolCue
        
        print(self.whiteBall.position)
        print(self.ball8.position)

        self.motionController = MotionController(self.balls + [self.whiteBall])

        projection_transorm = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=WIDTH/HEIGHT,
            near=0.1, far=10, dtype=np.float32
        )

        glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"),
                           1, GL_FALSE, projection_transorm)
        self.modeMatrixLocation = glGetUniformLocation(self.shader, "model")
        self.viewMatrixLocation = glGetUniformLocation(self.shader, 'view')

        self.addEventListeners()
        self.mainloop()

    def addEventListeners(self):
        def handleKeypress(event):
            if event.key == pygame.K_UP:
                self.progressBar.updateValue()
            if event.key == pygame.K_DOWN:
                self.progressBar.updateValue(decrement=True)
                
            if event.key == pygame.K_SPACE:
                direction = self.ball8.position - self.whiteBall.position
                direction /= np.linalg.norm(direction)
                
                self.whiteBall.velocity = (direction * self.progressBar.value) * 0.01

        self.eventListener = EventHandler()
        # listen for quit event
        self.eventListener.on(pygame.QUIT, lambda _: self.quit())

        self.eventListener.on(pygame.KEYDOWN, handleKeypress)

    def mainloop(self):
        while True:
            self.eventListener.listen()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)

            glUniformMatrix4fv(self.viewMatrixLocation, 1,
                               GL_FALSE, self.setupCamera())

            self.whiteBall.addTransformation([])
            

            self.plane.addTransformation(tableTransformation)
            self.table.addTransformation(tableTransformation)
            self.poolCue.addTransformation(
                cueTransformation(self.whiteBall, self.ball8))

            twoDModel = glGetUniformLocation(self.shader, 'twoDMode')
            glUniform1i(twoDModel, 0)
                

            self.whiteBall.draw(self.modeMatrixLocation)
            # self.ball8.draw(self.modeMatrixLocation)
            self.table.draw(self.modeMatrixLocation)
            self.plane.draw(self.modeMatrixLocation)
            self.poolCue.draw(self.modeMatrixLocation)

            for ball in self.balls:
                ball.addTransformation([pyrr.matrix44.create_from_x_rotation(theta=np.radians(-45)),])
                ball.draw(self.modeMatrixLocation)
                
            self.progressBar.draw(self.shader)
            
            self.motionController.updatePosition()
            self.motionController.updatePoolCue(self.poolCue, self.whiteBall)
            
            pygame.display.flip()
            self.clock.tick(100)

    def setupCamera(self, position=[1, 1, 2], ):
        return pyrr.matrix44.create_from_x_rotation(theta=np.radians(-45))
    
    def quit(self):
        pygame.quit()


if __name__ == "__main__":
    game = GameApp()
