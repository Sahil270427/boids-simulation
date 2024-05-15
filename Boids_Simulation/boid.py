import pygame
from tools import *
from random import uniform
import colorsys
from matrix import *
from math import pi,sin,cos


class Boid:
	def __init__(self, x, y):
		self.position = Vector(x, y)
		vec_x = uniform(-1, 1)
		vec_y = uniform(-1, 1)
		self.velocity = Vector(vec_x, vec_y)
		self.velocity.normalize()
		#set a random magnitude
		self.velocity = self.velocity * uniform(1.5, 4)
		self.acceleration = Vector()
		self.color = (255, 255,255)
		self.temp = self.color
		self.secondaryColor = (70, 70, 70)
		self.max_speed = 5
		self.max_length = 1
		self.size = 2
		self.stroke = 5
		self.angle = 0
		self.hue = 0
		self.toggles = {"separation":True, "alignment":True, "cohesion":True}
		self.values = {"separation":0.1, "alignment":0.1, "cohesion":0.1}
		self.radius = 40
		self.trace = []
		self.trace_length = 50
		self.weights = [1.0, 1.0, 1.0]

	def limits(self, width , height):
		if self.position.x > width:
			self.position.x = 0
		elif self.position.x < 0:
			self.position.x = width

		if self.position.y > height:
			self.position.y = 0
		elif self.position.y < 0:
			self.position.y = height

	def update_radius(self):
		# We can adjust the perception radius based on the boid's velocity
		speed = self.velocity.magnitude()
		self.radius = max(20, min(100, speed * 10))

	def avoid_obstacles(self, obstacles):
		total = 0
		steering = Vector()
		
		for obstacle in obstacles:
			dist = getDistance(self.position, obstacle.position)
			if dist < self.radius + obstacle.radius:
				temp = SubVectors(self.position, obstacle.position)
				temp = temp / (dist ** 2)
				steering.add(temp)
				total += 1
		
		if total > 0:
			steering = steering / total
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity
			steering.limit(self.max_length)

		return steering

	def behaviour(self, flock, obstacles):
		self.acceleration.reset()

		avoid_obs = self.avoid_obstacles(obstacles)
		avoid_obs = avoid_obs * 0.5  
		self.acceleration.add(avoid_obs)

		if self.toggles["separation"] == True:
			separation = self.separation(flock) * self.weights[0]
			self.acceleration.add(separation)

		if self.toggles["cohesion"]== True:
			cohesion = self.cohesion(flock) * self.weights[2]
			self.acceleration.add(cohesion)

		if self.toggles["alignment"] == True:
			alignment = self.alignment(flock) * self.weights[1]
			self.acceleration.add(alignment)
			


	def separation(self, flockMates):
		total = 0
		steering = Vector()

		for mate in flockMates:
			dist = getDistance(self.position, mate.position)
			if mate is not self and dist < self.radius:
				temp = SubVectors(self.position,mate.position)
				temp = temp/(dist ** 2)
				steering.add(temp)
				total += 1

		
		if total > 0:
			steering = steering / total
			# steering = steering - self.position
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity
			steering.limit(self.max_length)

		return steering

	def alignment(self, flockMates):
		total = 0
		steering = Vector()
		for mate in flockMates:
			dist = getDistance(self.position, mate.position)
			if mate is not self and dist < self.radius:
				vel = mate.velocity.Normalize()
				steering.add(vel)
				mate.color = hsv_to_rgb( self.hue ,1, 1)

				total += 1


		if total > 0:
			steering = steering / total
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity.Normalize()
			steering.limit(self.max_length)
		return steering

	def cohesion(self, flockMates):
		total = 0
		steering = Vector()

		for mate in flockMates:
			dist = getDistance(self.position, mate.position)
			if mate is not self and dist < self.radius:
				steering.add(mate.position)
				total += 1

		if total > 0:
			steering = steering / total
			steering = steering - self.position
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity
			steering.limit(self.max_length)

		return steering

	def update(self, Width, Height):

		self.position = self.position + self.velocity
		self.velocity = self.velocity + self.acceleration
		self.velocity.limit(self.max_speed)
		self.angle = self.velocity.heading() + pi/2
		self.update_radius()

		self.limits(Width, Height)
	
		self.trace.append((int(self.position.x), int(self.position.y)))
		if len(self.trace) > self.trace_length:
			self.trace.pop(0)

	def limits(self, width, height):
		if self.position.x > width:
			self.position.x = 0
			self.trace = [] 
		elif self.position.x < 0:
			self.position.x = width
			self.trace = []  
	
		if self.position.y > height:
			self.position.y = 0
			self.trace = []  
		elif self.position.y < 0:
			self.position.y = height
			self.trace = [] 

	def Draw(self, screen, distance, scale, show_trace, show_perception):
		ps = []
		points = [None for _ in range(3)]

		points[0] = [[0],[-self.size],[0]]
		points[1] = [[self.size//2],[self.size//2],[0]]
		points[2] = [[-self.size//2],[self.size//2],[0]]

		for point in points:
			rotated = matrix_multiplication(rotationZ(self.angle) , point)
			z = 1/(distance - rotated[2][0])

			projection_matrix = [[z, 0, 0], [0, z, 0]]
			projected_2d = matrix_multiplication(projection_matrix, rotated)

			x = int(projected_2d[0][0] * scale) + self.position.x
			y = int(projected_2d[1][0] * scale) + self.position.y
			ps.append((x, y))

		pygame.draw.polygon(screen, self.secondaryColor, ps)
		pygame.draw.polygon(screen, self.color, ps, self.stroke)

		
		if show_trace:
			points = [(int(pos[0]), int(pos[1])) for pos in self.trace]
			if len(points) > 1:
				pygame.draw.lines(screen, self.color, False, points)

		if show_perception:
			pygame.draw.circle(screen, (0, 255, 0), (int(self.position.x), int(self.position.y)), int(self.radius), 1)

