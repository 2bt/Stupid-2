
from OpenGL.GL import *
from vec import vec
import math

class Savage:

	def __init__(self):

		self.verts = []
		self.polys = []

	def render_raw(self):
		for p in self.polys:
			glBegin(GL_TRIANGLE_FAN)
			a, b, c = (self.verts[i] for i in p[:3])
			ab = b - a
			ac = c - a
			try:
				n = ab.cross(ac).normalize()
				glNormal(*n)
			except ZeroDivisionError: pass
			for i in p: glVertex(self.verts[i])
			glEnd()

	def render(self):
		glCallList(self.display_list)


	def gen_list(self):
		self.display_list = glGenLists(1)
		glNewList(self.display_list, GL_COMPILE)
		self.render_raw()
		glEndList()
		return self.display_list


	def render_shadow_raw(self):
		# render normal first
		self.render_raw()
		# calculate normals
		normals = []
		for p in self.polys:
			a, b, c = (self.verts[i] for i in p[:3])
			ab = b - a
			ac = c - a
			normals.append( ab.cross(ac).normalize() )
		# render quad for each shared edge
		edges = {}
		for p, normal in zip(self.polys, normals):
			for i in range(len(p)):
				a, b = p[i], p[(i + 1) % len(p)]
				if (b, a) in edges:
					glBegin(GL_QUADS)
					glNormal(*normal)
					glVertex(self.verts[b])
					glVertex(self.verts[a])
					glNormal(*edges[(b, a)])
					glVertex(self.verts[a])
					glVertex(self.verts[b])
					glEnd()
					del edges[(b, a)]
				else: edges[(a, b)] = normal

	def render_shadow(self):
		glCallList(self.shadow_display_list)


	def gen_shadow_list(self):
		self.shadow_display_list = glGenLists(1)
		glNewList(self.shadow_display_list, GL_COMPILE)
		self.render_shadow_raw()
		glEndList()
		return self.shadow_display_list




	def translate(self, x, y, z):
		d = vec(x, y, z)
		for i, v in enumerate(self.verts):
			self.verts[i] = v + d
		return self

	def rotate(self, angle, x, y, z):
		s = math.sin(angle * math.pi / 180.0)
		c = math.cos(angle * math.pi / 180.0)
		omc = 1 - c
		mat1 = (c + x*x*omc, x*y*omc - z*s, x*z*omc + y*s)
		mat2 = (y*x*omc + z*s, c + y*y*omc, x*z*omc - x*s)
		mat3 = (z*x*omc - y*s, z*y*omc + x*s, c + z*z*omc)

		for i, v in enumerate(self.verts):
			self.verts[i] = vec(
				mat1[0] * v.x + mat1[1] * v.y + mat1[2] * v.z,
				mat2[0] * v.x + mat2[1] * v.y + mat2[2] * v.z,
				mat3[0] * v.x + mat3[1] * v.y + mat3[2] * v.z)
		return self

	def scale(self, x, y, z):
		for i, v in enumerate(self.verts):
			self.verts[i] = vec(v.x * x, v.y * y, v.z * z)
		return self

	def __iadd__(self, other):
		n = len(self.verts)
		for p in other.polys:
			self.polys.append(tuple(i + n for i in p))
		self.verts += other.verts
		return self

	def __add__(self, other):
		res = Savage()
		res += self
		res += other
		return res


class Brick(Savage):
	def __init__(self, *size):
		s = [(i * -0.5, i * 0.5) for i in size]
		self.verts = [vec(x, y, z) for x in s[0] for y in s[1] for z in s[2]]
		self.polys = [(0, 1, 3, 2), (6, 7, 5, 4), (4, 5, 1, 0),
					(2, 3, 7, 6), (5, 7, 3, 1), (0, 2, 6, 4)]


class Can(Savage):
	def __init__(self, height, diameter, detail=12):
		d = 2 * math.pi / detail
		r = diameter * 0.5
		vs = [(math.sin(i * d) * r, math.cos(i * d) * r) for i in range(detail)]
		self.verts  = [vec(v[0], height *  0.5, v[1]) for v in vs]
		self.verts += [vec(v[0], height * -0.5, v[1]) for v in vs]
		self.polys = [(i, i + detail, (i+1) % detail + detail, (i+1) % detail) for i in range(detail)]
		self.polys.append(range(detail))
		self.polys.append(range(detail, detail*2)[::-1])


class Orb(Savage):
	def __init__(self, diameter, detail=2):
		r = 0.5 * diameter
		i = (1/3.0 ** 0.5) * r
		q = [(vec(i, i, i), vec(-i, i, i), vec(-i, -i, i), vec(i, -i, i)),
			(vec(i, i, -i), vec(i, -i, -i), vec(-i, -i, -i), vec(-i, i, -i)),
			(vec(i, i, i), vec(i, -i, i), vec(i, -i, -i), vec(i, i, -i)),
			(vec(-i, i, i), vec(-i, i, -i), vec(-i, -i, -i), vec(-i, -i, i)),
			(vec(i, i, i), vec(i, i, -i), vec(-i, i, -i), vec(-i, i, i)),
			(vec(i, -i, i), vec(-i, -i, i), vec(-i, -i, -i), vec(i, -i, -i))]
		for _ in range(detail):
			w, q = q, []
			for a, b, c, d in w:
				e = ((a + b) * 0.5).normalize() * r
				f = ((b + c) * 0.5).normalize() * r
				g = ((c + d) * 0.5).normalize() * r
				h = ((d + a) * 0.5).normalize() * r
				i = ((a + b + c + d) * 0.25).normalize() * r
				q.append((a, e, i, h))
				q.append((e, b, f, i))
				q.append((h, i, g, d))
				q.append((i, f, c, g))

		self.verts = list(set(v for p in q for v in p))
		self.polys = [[self.verts.index(v) for v in p] for p in q]


