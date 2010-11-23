
from OpenGL.GL import *
import pygame
from pygame.locals import *


class	Font:
	def __init__(self):
		img = pygame.image.load('font.png')
		data = pygame.image.tostring(img, "RGBA", 1)

		self.tex = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.tex)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.get_width(), img.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

		scale_x = 8.0 / img.get_width()
		scale_y = 8.0 / img.get_height()

		self.chars = glGenLists(128)
		for i in range(128):
			glNewList(self.chars + i, GL_COMPILE)
			i -= 32
			if i >= 0 and i < 96:

				a, b = divmod(i, 8)
				tx = scale_x * b
				ty = scale_y * (11 - a)

				glBegin(GL_QUADS)
				glTexCoord2f(tx, ty)
				glVertex2d(-0, 8)
				glTexCoord2f(tx + scale_x, ty)
				glVertex2d(8, 8)
				glTexCoord2f(tx + scale_x, ty + scale_y)
				glVertex2d(8, -0)
				glTexCoord2f(tx, ty + scale_y)
				glVertex2d(-0, -0)
				glEnd()
			
			glTranslate(8, 0, 0)
			glEndList()

	def put(self, x, y, string):

		s = pygame.display.get_surface()
		glMatrixMode(GL_PROJECTION)
		glPushMatrix()
		glLoadIdentity()
		glOrtho(0, s.get_width(), s.get_height(), 0, -1, 1)
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()

		glBindTexture(GL_TEXTURE_2D, self.tex)
		glEnable(GL_TEXTURE_2D)
		glDisable(GL_LIGHTING)
		glTranslate(x, y, 0)
		glListBase(self.chars)
		glCallLists(string)
		glDisable(GL_TEXTURE_2D)
		glEnable(GL_LIGHTING)

		glPopMatrix()
		glMatrixMode(GL_PROJECTION)
		glPopMatrix()
		glMatrixMode(GL_MODELVIEW)

def init():
	global font
	font = Font()

def put(x, y, string):
	global font
	font.put(x, y, string)

