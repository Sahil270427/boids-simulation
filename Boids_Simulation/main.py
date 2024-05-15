import pygame
from boid import Boid
from tools import Vector
from obstacle import Obstacle
import math
import random
from matrix import *
from constants import *
from uiParameters import *
from deap import base, creator, tools, algorithms
import numpy as np


pygame.init()
window = pygame.display.set_mode(size, pygame.FULLSCREEN)
clock = pygame.time.Clock()
fps = 60

scale = 40
Distance = 5
speed = 0.0005

flock = []
obstacles = []

#number of boids
n = 50


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=3)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
	for boid in flock:
		boid.weights = individual
	
	for _ in range(100):
		for boid in flock:
			boid.behaviour(flock, obstacles)
			boid.update()
	
	alignment_sum = sum(boid.alignment(flock) for boid in flock)
	cohesion_sum = sum(boid.cohesion(flock) for boid in flock)
	separation_sum = sum(boid.separation(flock) for boid in flock)
	
	fitness = alignment_sum + cohesion_sum + separation_sum
	return (fitness,)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=50)
hof = tools.HallOfFame(3)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)


population, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, stats=stats, halloffame=hof, verbose=True)

best_weights = hof[0]
for boid in flock:
	boid.weights = best_weights

for i in range(n):
	boid = Boid(random.randint(20, Width-20), random.randint(20, Height-20))
	boid.weights = best_weights
	flock.append(boid)


textI = "10"
reset = False
SpaceButtonPressed = False
backSpace = False
keyPressed = False
showUI = False
clicked = False
run = True
while run:
	clock.tick(fps)
	window.fill((10, 10, 15))

	n = numberInput.value
	scale = sliderScale.value

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				run = False
			if event.key == pygame.K_r:
				reset = True
			if event.key == pygame.K_SPACE:
				SpaceButtonPressed = True

			textI = pygame.key.name(event.key)
			keyPressed = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_BACKSPACE:
				backSpace = True
			if event.key == pygame.K_u:
				showUI = not showUI
		if event.type == pygame.MOUSEBUTTONDOWN and pygame.key.get_mods() & pygame.KMOD_SHIFT:
			mouse_pos = pygame.mouse.get_pos()
			obstacles.append(Obstacle(mouse_pos[0], mouse_pos[1], 10))


	if reset == True or resetButton.state == True:
		flock = []
		obstacles = []
		for boid in flock:
        		boid.trace = []
		for i in range(n):
			flock.append(Boid(random.randint(20, Width-20), random.randint(20, Height-20)))
		reset = False


	for boid in flock:
		boid.toggles = {"separation": toggleSeparation.state, "alignment": toggleAlignment.state,"cohesion": toggleCohesion.state}
		boid.values = {"separation": separationInput.value/100, "alignment": alignmentInput.value/100,"cohesion": cohesionInput.value/100}
		boid.radius = scale
		boid.limits(Width, Height)
		boid.behaviour(flock, obstacles)
		boid.update(Width, Height)
		boid.hue += speed
		boid.Draw(window, Distance, scale, showTrace.state, showPerceptionCircle.state)

	for obstacle in obstacles:
		obstacle.draw(window)


	if showUI == True:
		panel.Render(window)
		resetButton.Render(window)
		Behaviours.Render(window)
		Separation.Render(window)
		Alignment.Render(window)
		Cohesion.Render(window)
		Trace.Render(window)
		Perception.Render(window)
		SeparationValue.Render(window)
		AlignmentValue.Render(window)
		CohesionValue.Render(window)
		NumberOfBoids.Render(window)
		ScaleText.Render(window)
		toggleSeparation.Render(window, clicked)
		toggleAlignment.Render(window, clicked)
		toggleCohesion.Render(window, clicked)
		separationInput.Render(window, textI, backSpace, keyPressed)
		alignmentInput.Render(window, textI, backSpace, keyPressed)
		cohesionInput.Render(window, textI, backSpace, keyPressed)
		numberInput.Render(window, textI, backSpace, keyPressed)
		showTrace.Render(window, clicked)
		showPerceptionCircle.Render(window, clicked)

		sliderScale.Render(window)
	else:
		UItoggle.Render(window)
	backSpace = False
	keyPressed = False
	pygame.display.flip()
	clicked = False
pygame.quit()
