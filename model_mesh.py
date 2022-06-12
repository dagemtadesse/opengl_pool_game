import numpy as np
from OpenGL.GL import *
import pyrr
from objloader import ObjLoader


class Model:

    def __init__(self, position, eulers, mesh=None, texture=None):
        # The objects location in space
        self.position = np.array(position, dtype=np.float32)
        # euler angles for rotation
        self.eulers = np.array(eulers, dtype=np.float32)
        # tranformation on the model
        self.modelTranformations = pyrr.matrix44.create_identity(
            dtype=np.float32)
        # holds the models vertices, texture coordinated and other stuff
        self.mesh = mesh
        # hold the texture for the model
        self.texture = texture

    def addTransformation(self, tranformation_matrices):
        # addes a series of tranformation to the object
        self.modelTranformations = pyrr.matrix44.create_identity(
            dtype=np.float32)
        for tranformationMatrix in tranformation_matrices:
            self.modelTranformations = pyrr.matrix44.multiply(
                m1=self.modelTranformations,
                m2=tranformationMatrix
            )

    def draw(self, modelTransformationMatrixLocation):
        """draw the object"""
        # apply the model tranformation matrix
        glUniformMatrix4fv(modelTransformationMatrixLocation,
                           1, GL_FALSE, self.modelTranformations)
        # bind the vertex array object of the mesh
        glBindVertexArray(self.mesh.vao)
        # bind the texuture if the mesh has one
        if not self.texture is None:
            self.texture.use()
        # draw the faces of the mesh
        glDrawArrays(GL_TRIANGLES, 0, self.mesh.vertexCount)


class ModelMesh():

    def __init__(self, modelPath):
        self.meshVertices, self.meshBuffer = ObjLoader.load_model(modelPath)
        self.vertexCount = len(self.meshVertices)

        self.vertexData = np.array(self.meshBuffer, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.meshBuffer.nbytes,
                     self.meshBuffer, GL_STATIC_DRAW)

        # vertex
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              self.meshBuffer.itemsize * 8, ctypes.c_void_p(0))

        # textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                              self.meshBuffer.itemsize * 8, ctypes.c_void_p(12))

        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
                              self.meshBuffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)
