from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *

def createShader( vertexShaderPath, fragmentShaderPath):
    with open(vertexShaderPath, 'r') as f:
        vertex_src = f.readlines()

    with open(fragmentShaderPath, 'r') as f:
        fragment_src = f.readlines()

    shader = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )

    return shader