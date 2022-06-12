from OpenGL.GL import *
import pygame

class Material:

    def __init__(self, filepath):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = pygame.image.load(filepath).convert_alpha()
        image_width, image_height = image.get_rect().size
        image_data = pygame.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width,
                     image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        # glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        # glActiveTexture(GL_TEXTURE0,)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destory(self):
        glDeleteTextures(1, (self.texture,))


