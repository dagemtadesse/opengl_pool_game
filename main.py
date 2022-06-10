import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from model_mesh import Model, ModelMesh
import pyrr

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
        glClearColor(1.0, 1.0, 1.0, 1)

        self.wood_texture = Material('textures/8.png')
        self.cube_mesh = ModelMesh("models/8.obj")
        self.cube = Model(
            position=[0, 0, -1],
            eulers=[0, 0, 0, ]
        )


        projection_transorm=pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = WIDTH/HEIGHT,
            near = 0.1, far = 10, dtype = np.float32
        )
        
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"),
                           1, GL_FALSE, projection_transorm)

        self.modeMatrixLocation = glGetUniformLocation(self.shader, "model")
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
                    
            self.cube.eulers[2] += 0.25
            if self.cube.eulers[2] > 360:
                self.cube.eulers[2] -= 360;
                
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)
            
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            
            model_transform = pyrr.matrix44.multiply(
                m1 = model_transform, 
                m2 = pyrr.matrix44.create_from_scale(
                    scale=np.array((2, 2, 2)), dtype=np.float32
                ))
            
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(eulers=np.radians(self.cube.eulers), dtype=np.float32)
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=self.cube.position,dtype=np.float32
                )
            )
            
            glUniformMatrix4fv(self.modeMatrixLocation, 1, GL_FALSE, model_transform)
            self.wood_texture.use()
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertexCount)
            pygame.display.flip()
            self.clock.tick(60)

    def quit(self):
        pygame.quit()

if __name__ == "__main__":
    game = GameApp()
