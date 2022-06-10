import numpy as np
from OpenGL.GL import *
from objloader import ObjLoader

class Model:

    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)


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
