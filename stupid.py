
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from time import time as get_time, sleep

import math
import font
from vec import vec


class Entity:
	"""the base for stupid objects"""

	chain = []
	count = 0

	def __init__(self):
		self.chain.append(self)
		self.id = self.count
		self.active = not self.id
		Entity.count += 1

	def update(self, time_dif):
		if Stupid.key_state(K_1 + self.id, True):
			for e in self.chain: e.active = False
			self.active = True
		if self.active:
			self.update_sub(time_dif)

	def render(self):
		if self.active:
			self.render_sub()

	def update_sub(self, time_dif): pass
	def render_sub(self): pass


class Candle:
	"""light"""

	def __init__(self, stupid):
		self.stupid = stupid

		glEnable(GL_COLOR_MATERIAL)
		glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 128);
		glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, (0.5, 0.5, 0.5))
		glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.7, 0.7, 0.7))
		glLight(GL_LIGHT0, GL_AMBIENT, (0.05, 0.05, 0.05))

		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)
		glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0, 0, 0, 0))
	
		self.pos = vec(2, 4, 5)
	
	def update(self, time_dif):
		pass

	def render(self):
		glLight(GL_LIGHT0, GL_POSITION, (self.pos.x, self.pos.y, self.pos.z))
#		glDisable(GL_LIGHTING)
#		glColor(1, 1, 1)
#		glPointSize(10)
#		glBegin(GL_POINTS)
#		glVertex(self.pos)
#		glEnd()
#		glEnable(GL_LIGHTING)

class Eye:

	def __init__(self, stupid):
		self.stupid = stupid

		fullscreen = False
		self.width, self.height = 1280, 800

		self.ratio = float(self.width) / self.height

		pygame.display.gl_set_attribute(GL_STENCIL_SIZE, 4)
		pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 4)
		pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, 1)

		pygame.display.set_mode((self.width, self.height), OPENGL | DOUBLEBUF | (fullscreen and FULLSCREEN))
		pygame.mouse.set_visible(False)
		glEnable(GL_MULTISAMPLE)
		glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

		glEnable(GL_LINE_SMOOTH)
		glEnable(GL_BLEND)
		glEnable(GL_ALPHA_TEST)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		glDepthFunc(GL_LEQUAL)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_CULL_FACE)
		glShadeModel(GL_SMOOTH)

		glClearColor(0.2, 0.2, 0.2, 0)

		self.pos = vec(0, 5, 10)
		self.ang_y = 0
		self.ang_x = 0.1

		self.fps = 0
		self.frame = 0
		self.time = get_time()

	def update(self, time_dif):
		self.ang_y += (Stupid.key_state(K_RIGHT) - Stupid.key_state(K_LEFT)) * time_dif
		self.ang_x += (Stupid.key_state(K_DOWN) - Stupid.key_state(K_UP)) * time_dif
		x = Stupid.key_state(K_d) - Stupid.key_state(K_a)
		y = Stupid.key_state(K_SPACE) - Stupid.key_state(K_LSHIFT)
		z = Stupid.key_state(K_s) - Stupid.key_state(K_w)

		cy = math.cos(self.ang_y)
		sy = math.sin(self.ang_y)
		cx = math.cos(self.ang_x)
		sx = math.sin(self.ang_x)

		move = vec()
		move.y = y * cx + z * sx
		move.x = x * cy - z * sy * cx + sy * sx * y
		move.z = x * sy + z * cy * cx - cy * sx * y

		if not Stupid.key_state(K_RCTRL):
			self.pos += time_dif * move * 5
		else:
			self.stupid.candle.pos += time_dif * move * 5

		# frame rate
		self.frame += 1
		t = get_time()
		if t - self.time > 2:
			self.fps = self.frame / (t - self.time)
			self.time = t
			self.frame = 0

	def render(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45, self.ratio, 0.1, 1000)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		glRotate(self.ang_x * (180 / math.pi), 1, 0, 0)
		glRotate(self.ang_y * (180 / math.pi), 0, 1, 0)
		glTranslate(-self.pos.x, -self.pos.y, -self.pos.z)

		glColor(1, 1, 1)
		font.put(5, 5, "FPS: %3.2f" % self.fps)


class Stupid:

	keys = {}
	@classmethod
	def key_state(cls, key, kill=False):
		if type(key) == str: key = ord(key)
		c = cls.keys.get(key, 0)
		if kill: cls.keys[key] = 0
		return c

	def __init__(self, title):
		pygame.display.init()
		pygame.display.set_caption(title)
		pygame.key.set_repeat(300, 100)

		self.eye = Eye(self)
		self.candle = Candle(self)
		self.objects = [self.eye, self.candle]
		font.init()

	def add(self, entity):
		self.objects.append(entity)

	def mainloop(self):
		time = get_time()

		while 1:
			# event handling
			for event in pygame.event.get():
				if event.type == QUIT: return
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE: return
					self.keys[event.key] = 1
				elif event.type == KEYUP:
					self.keys[event.key] = 0

			# update
			time_new = get_time()
			time_dif = time_new - time
			time = time_new
			for o in self.objects: o.update(time_dif)

			# render
			for o in self.objects: o.render()

			pygame.display.flip()
			sleep(0.005)

