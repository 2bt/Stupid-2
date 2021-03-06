#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame, sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from stupid import Stupid, Entity
from vec import vec
from aufg3 import ObjObject


class Shade:
	def __init__(self, v_code, f_code):
		self.prog = glCreateProgram()
		for c, t in (v_code, GL_VERTEX_SHADER), (f_code, GL_FRAGMENT_SHADER):
			shader = glCreateShader(t)
			glShaderSource(shader, c)
			glCompileShader(shader)
			print glGetShaderInfoLog(shader)
			glAttachShader(self.prog, shader)
			glDeleteShader(shader)
		glLinkProgram(self.prog)
		self.locations = {}
	def get_location(self, name):
		if name not in self.locations:
			self.locations[name] = glGetUniformLocation(self.prog, name)
		return self.locations[name]
	def uniformf(self, name, *value):
		l = self.get_location(name)
		[glUniform1f, glUniform2f, glUniform3f, glUniform4f][len(value)-1](l, *value)
	def uniformi(self, name, *value):
		l = self.get_location(name)
		[glUniform1i, glUniform2i, glUniform3i, glUniform4i][len(value)-1](l, *value)
	def on(self): glUseProgram(self.prog)
	def off(self): glUseProgram(GL_NONE)

class Trick(Entity):
	def __init__(self, obj):
		Entity.__init__(self)
		self.obj = obj
		v = """
uniform vec3 light_pos;
varying vec3 pos, eye, normal, lpos, light_diff;
void main(void) {
	pos = gl_Vertex.xyz;
	lpos = vec3(gl_ModelViewMatrix * vec4(light_pos, 0.0));
	eye = vec3(gl_ModelViewMatrix * gl_Vertex);
	light_diff = pos - light_pos;
	normal = gl_NormalMatrix * gl_Normal;
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}"""
		self.toon = Shade(v, """
uniform bool blinn;
uniform float shininess, sections;
uniform vec4 color, diffuse, ambient, specular;
varying vec3 pos, normal, eye, light_diff;
void main(void) {
	vec3 n = normalize(normal);
	vec3 ldir = normalize(-light_diff);
	vec3 vdir = normalize(eye);
	vec3 lhalf = normalize(ldir - vdir);
	float intensity = max(dot(n, ldir), 0.0);
	float foo = max(blinn ? dot(n, lhalf) : dot(vdir, reflect(ldir, n)), 0.0);

	intensity = floor(intensity * sections) / sections;
	foo = pow(foo, shininess);
	foo = foo > 0.1 ? 1.0 : 0.0;
	vec4 cl = (color * ambient + specular * foo) * diffuse;
	gl_FragColor = vec4(cl.rgb * intensity, cl.a);
}""")

		self.phong = Shade(v, """
uniform bool blinn;
uniform float shininess;
uniform vec4 color, diffuse, ambient, specular;
varying vec3 pos, normal, eye, light_diff;
void main(void) {
	vec3 n = normalize(normal);
	vec3 ldir = normalize(-light_diff);
	vec3 vdir = normalize(eye);
	vec3 lhalf = normalize(ldir - vdir);
	float intensity = max(dot(n, ldir), 0.0);
	float foo = max(blinn ? dot(n, lhalf) : dot(vdir, reflect(ldir, n)), 0.0);
	foo = pow(foo, shininess);
	vec4 cl = (color * ambient + specular * foo) * diffuse;
	gl_FragColor = vec4(cl.rgb * intensity, cl.a);
}""")
		self.switch = 0
		self.blinn = 0
		self.sections = 5
		self.shininess = 30

	def render_sub(self):
		shade = [self.phong, self.toon][self.switch]
		shade.on()

		shade.uniformi("blinn", self.blinn)
		shade.uniformf("shininess", self.shininess)
		shade.uniformf("sections", self.sections)
		shade.uniformf("light_pos", 50, 50, 50)
		shade.uniformf("color", 1, 0, 1, 1)
		shade.uniformf("diffuse", 1, 1, 1, 1)
		shade.uniformf("ambient", 1, 1, 1, 1)
		shade.uniformf("specular", 1, 1, 1, 1)
		obj.render()
		shade.off()

	def update_sub(self, dt):
		self.switch ^= Stupid.key_state(K_c, True)
		self.blinn ^= Stupid.key_state(K_b, True)
		self.sections += Stupid.key_state(K_r, True)
		self.sections -= Stupid.key_state(K_f, True)
		self.shininess += Stupid.key_state(K_t, True)
		self.shininess -= Stupid.key_state(K_g, True)


class Normal(Entity):
	def __init__(self, obj):
		Entity.__init__(self)
		self.obj = obj
		self.shade = Shade("""
varying vec3 normal;
void main(void) {
	normal = gl_Normal;
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}""", """
varying vec3 normal;
void main(void) {
	vec3 h = vec3(0.5, 0.5, 0.5);
	gl_FragColor = vec4(normalize(normal.xyz) * h + h, 1);
}""")

	def render_sub(self):
		self.shade.on()
		self.obj.render()
		self.shade.off()


if __name__ == "__main__":
	stupid = Stupid("Stupid [ CGI - Aufgabe 5 ]")
	obj = ObjObject(sys.argv[1])
	stupid.add(Trick(obj))
	stupid.add(Normal(obj))
	stupid.mainloop()


