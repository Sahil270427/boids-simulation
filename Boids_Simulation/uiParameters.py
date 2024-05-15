from ui import *

panel = Panel(color=(40, 40, 40))
resetButton = Button("Reset", color=(60, 60, 60), borderColor=(100, 150, 255))

Behaviours = TextUI("BEHAVIOURS", (Width-180, 60), (200, 200, 200))
UItoggle = TextUI("Press 'U' to show parameter panel", (Width-180, 90), (100, 150, 255))

Separation = TextUI("Separation: ", (Width-245, 140), (200, 200, 200))
Alignment = TextUI("Alignment: ", (Width-245, 180), (200, 200, 200))
Cohesion = TextUI("Cohesion: ", (Width-245, 220), (200, 200, 200))

Trace = TextUI("Trace Lines: ", (Width-245, 260), (200, 200, 200))
Perception = TextUI("Perception Circle: ", (Width-245, 300), (200, 200, 200))

SeparationValue = TextUI("separationValue: ", (Width-245, 365), (200, 200, 200))
AlignmentValue = TextUI("alignmentValue: ", (Width-245, 415), (200, 200, 200))
CohesionValue = TextUI("cohesionValue: ", (Width-245, 465), (200, 200, 200))
NumberOfBoids = TextUI("Number of Boids: ", (Width-245, 515), (200, 200, 200))
ScaleText = TextUI("Boid-Scale (radius): ", (Width-200, 570), (200, 200, 200))

toggleSeparation = ToggleButton((Width-160, 130), 20, 20, True, (60, 60, 60), (100, 150, 255))
toggleAlignment = ToggleButton((Width-160, 170), 20, 20, True, (60, 60, 60), (100, 150, 255))
toggleCohesion = ToggleButton((Width-160, 210), 20, 20, True, (60, 60, 60), (100, 150, 255))

showTrace = ToggleButton((Width-160, 250), 20, 20, True, (60, 60, 60), (100, 150, 255))

showPerceptionCircle = ToggleButton((Width-160, 290), 20, 20, True, (60, 60, 60), (100, 150, 255))

separationInput = DigitInput(10, (Width-160, 340), 80, 30, (60, 60, 60))
alignmentInput = DigitInput(10, (Width-160, 390), 80, 30, (60, 60, 60))
cohesionInput = DigitInput(10, (Width-160, 440), 80, 30, (60, 60, 60))
numberInput = DigitInput(50, (Width-160, 490), 80, 30, (60, 60, 60))

sliderScale = Slider(Width-280, 610, 40, 0, 100, 180, 10, 80)
