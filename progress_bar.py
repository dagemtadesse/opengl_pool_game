from matplotlib import projections
import pyrr
import numpy as np
from OpenGL.GL import *


class ProgressBar():
    def __init__(self) -> None:

        # b	rgb(255, 81, 47) -> gb	rgb(240, 152, 25)
        baseQuad = [0.0, 0.0, 0.0, 1.0, 0.32, 0.18,
                    0.2, 0.0, 0.0, 0.94, 0.6, 0.09,
                    0.0, 0.0, 0.1, 1.0, 0.32, 0.18,
                    0.2, 0.0, 0.1, 0.94, 0.6, 0.09,]

        self.baseQuad = np.array(baseQuad, dtype=np.float32)

        self.value = 1
        self.createVerticies()
    
    def updateValue(self, decrement = False):
        if not decrement:
            self.value += 1
            if(self.value >= 7): self.value = 7
            return
        
        self.value -= 1
        if(self.value <= 1): self.value = 1

    def createVerticies(self):
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, self.baseQuad.nbytes,
                     self.baseQuad, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              24, ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                            24, ctypes.c_void_p(12))

    def draw(self, shader):
        
        self.addTransformation([
            pyrr.matrix44.create_from_x_rotation(theta=np.radians(90)),
            pyrr.matrix44.create_from_scale(scale=[self.value,1,1]),
            pyrr.matrix44.create_from_translation(
                vec=np.array([-2.85, 1.4, -4], dtype=np.float32), dtype=np.float32
            ),
        ])

        transformLoc = glGetUniformLocation(shader, 'model')
        twoDModel = glGetUniformLocation(shader, 'twoDMode')

        glUniformMatrix4fv(transformLoc, 1, GL_FALSE,
                            self.modelTranformations)


        glUniform1i(twoDModel, 1)
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)


    def addTransformation(self, tranformation_matrices):
        # addes a series of tranformation to the object
        self.modelTranformations = pyrr.matrix44.create_identity(
            dtype=np.float32)
        
        for tranformationMatrix in tranformation_matrices:
            self.modelTranformations = pyrr.matrix44.multiply(
                m1=self.modelTranformations,
                m2=tranformationMatrix
            )
