import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import math

from model_mesh import Model, ModelMesh
from texture import Material

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
        self.shader = self.createShader(
            'shaders/vertex.shader', 'shaders/fragment.shader')
        glUseProgram(self.shader)

        glUniform1i(glGetUniformLocation(self.shader, 'imageTexture'), 0)
        glEnable(GL_DEPTH_TEST)

        # glEnable(GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(.5, .5, 1.0, 1)

        self.ball4 = Model(
            position=[0, 0, -1],
            eulers=[0, 0, 0, ],
            mesh=ModelMesh("models/ball.obj"),
            texture=Material('textures/4.png')
        )

        self.ball8 = Model(
            position=[-0.5, 0, -1],
            eulers=[0, 0, 0, ],
            mesh=ModelMesh("models/ball.obj"),
            texture=Material('textures/8.png')
        )

        self.plane = Model(
            position=[0, 0, -5],
            eulers=[0,0,0],
            mesh=ModelMesh("models/plane.obj"),
            texture=Material('textures/felt.bmp')
        )

        self.table = Model(
            position=[0, 0, -5],
            eulers=[0, 0, 0],
            mesh=ModelMesh("models/table.obj"),
            texture=Material('textures/leather.jpg')
        )

        projection_transorm = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=WIDTH/HEIGHT,
            near=0.1, far=10, dtype=np.float32
        )

        glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"),
                           1, GL_FALSE, projection_transorm)

        self.modeMatrixLocation = glGetUniformLocation(self.shader, "model")
        self.viewMatrixLocation = glGetUniformLocation(self.shader, 'view')

        self.mainloop()

    def createShader(self, vertexShaderPath, fragmentShaderPath):
        with open(vertexShaderPath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentShaderPath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            self.ball4.eulers[2] += 1
            if self.ball4.eulers[2] > 360:
                self.ball4.eulers[2] -= 360

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # glUseProgram(self.shader)

            glUniformMatrix4fv(self.viewMatrixLocation, 1,
                               GL_FALSE, self.setupCamera())

            self.ball4.addTransformation([
                pyrr.matrix44.create_from_scale(
                    scale=np.array((2, 2, 2)), dtype=np.float32
                ),
                pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.ball4.eulers), dtype=np.float32),
                pyrr.matrix44.create_from_translation(
                    vec=self.ball4.position, dtype=np.float32
                )
            ])

            self.ball8.addTransformation([
                pyrr.matrix44.create_from_scale(
                    scale=np.array((2, 2, 2)), dtype=np.float32
                ),
                pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.ball4.eulers), dtype=np.float32),
                pyrr.matrix44.create_from_translation(
                    vec=self.ball8.position, dtype=np.float32
                )
            ])

            self.plane.addTransformation([
                pyrr.matrix44.create_from_x_rotation(theta=np.radians(-60)),
                pyrr.matrix44.create_from_translation(
                    vec=self.plane.position, dtype=np.float32
                ),
            ])

            self.table.addTransformation([
                # pyrr.matrix44.create_from_scale(
                #     scale=np.array((.25, .25, .5)), dtype=np.float32
                # ),
                # pyrr.matrix44.create_from_eulers(
                #     eulers=np.radians(self.ball4.eulers), dtype=np.float32),
                pyrr.matrix44.create_from_x_rotation(theta=np.radians(-60)),
                pyrr.matrix44.create_from_translation(
                    vec=self.table.position, dtype=np.float32
                ),
            ])

            # self.ball4.draw(self.modeMatrixLocation)
            # self.ball8.draw(self.modeMatrixLocation)
            self.table.draw(self.modeMatrixLocation)
            self.plane.draw(self.modeMatrixLocation)
            pygame.display.flip()
            self.clock.tick(60)

    def setupCamera(self, position=[1, 1, 2], ):
        
        # cameraPos = pyrr.Vector3([1, 1, 1])
        # cameraTarget = pyrr.Vector3([0, 0, 0])
        
        # normal = cameraPos - cameraTarget
        
        # up = pyrr.vector.normalise(normal)
        
        # return pyrr.matrix44.create_look_at(
        #     eye=np.array(position),
        #     target=np.array([.0, .0, .0]),
        #     up=np.array([.0, .0, .1])
        # )

        return pyrr.matrix44.create_identity()

    def quit(self):
        pygame.quit()


if __name__ == "__main__":
    game = GameApp()
