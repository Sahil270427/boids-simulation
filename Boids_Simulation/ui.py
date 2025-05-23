import pygame
from constants import *
from tools import *

class Button:
    def __init__(self, text, position=(Width-230, 700), w=100, h=50, border=10, color=(60, 60, 60), borderColor=(100, 150, 255)):
        self.text = text
        self.position = position
        self.w = w
        self.h = h
        self.border = border
        self.temp = color
        self.color = color
        self.borderColor = borderColor
        self.font = 'freesansbold.ttf'
        self.fontSize = 25
        self.textColor = (255, 255, 255)
        self.state = False
        self.action = None

    def HandleMouse(self, HoverColor=(100, 100, 100)):
        m = pygame.mouse.get_pos()
        self.state = False
        if self.position[0] <= m[0] <= self.position[0] + self.w and self.position[1] <= m[1] <= self.position[1] + self.h:
            self.color = HoverColor
            if pygame.mouse.get_pressed()[0]:
                self.color = (200, 200, 200)
                if self.action is None:
                    self.state = True
        else:
            self.color = self.temp

    def Render(self, screen):
        self.HandleMouse()
        font = pygame.font.Font(self.font, self.fontSize)
        text = font.render(self.text, True, self.textColor)
        textRect = text.get_rect(center=(self.position[0] + self.w // 2, self.position[1] + self.h // 2))
        if self.border > 0:
            pygame.draw.rect(screen, self.borderColor, pygame.Rect(self.position[0] - self.border // 2, self.position[1] - self.border // 2, self.w + self.border, self.h + self.border))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.w, self.h))
        screen.blit(text, textRect)

class Panel:
    def __init__(self, position=(Width-350, 100), w=345, h=500, color=(40, 40, 40), alpha=128):
        self.position = position
        self.w = w
        self.h = h
        self.color = color
        self.alpha = alpha

    def Render(self, screen):
        s = pygame.Surface((self.w, self.h))
        s.set_alpha(self.alpha)
        s.fill(self.color)
        screen.blit(s, self.position)

class ToggleButton:
    def __init__(self, position=((Width-200, 400)), w=30, h=30, state=False, color=(60, 60, 60), activeColor=(100, 150, 255)):
        self.position = position
        self.w = w
        self.h = h
        self.clicked = False
        self.state = state
        self.temp = (activeColor, color)
        self.activeColor = activeColor
        self.color = color

    def HandleMouse(self, HoverColor=(150, 120, 40)):
        m = pygame.mouse.get_pos()
        if self.position[0] <= m[0] <= self.position[0] + self.w and self.position[1] <= m[1] <= self.position[1] + self.h:
            self.color = HoverColor
            self.activeColor = HoverColor
            if self.clicked:
                self.state = not self.state
                self.color = (255, 255, 255)
        else:
            self.color = self.temp[1]
            self.activeColor = self.temp[0]

    def Render(self, screen, clicked):
        self.HandleMouse()
        self.clicked = clicked
        if self.state:
            pygame.draw.rect(screen, self.activeColor, pygame.Rect(self.position[0], self.position[1], self.w, self.h))
        else:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.w, self.h))
        return self.state

class TextUI:
    def __init__(self, text, position, fontColor):
        self.position = position
        self.text = text
        self.font = 'freesansbold.ttf'
        self.fontSize = 18
        self.fontColor = fontColor

    def Render(self, screen):
        font = pygame.font.Font(self.font, self.fontSize)
        text = font.render(self.text, True, self.fontColor)
        textRect = text.get_rect(center=self.position)
        screen.blit(text, textRect)

class DigitInput:
    def __init__(self, startingValue, position=(Width-320, 100), w=80, h=30, color=(60, 60, 60)):
        self.position = position
        self.text = str(startingValue)
        self.fontColor = (255, 255, 255)
        self.fontSize = 18
        self.font = 'freesansbold.ttf'
        self.w = w
        self.h = h
        self.color = color
        self.value = int(self.text)
        self.hoverEnter = False

    def Check(self, backspace, val):
        if self.hoverEnter:
            if backspace:
                self.value = int(str(self.value)[:-1]) if len(str(self.value)) > 1 else 0
            else:
                if self.text.isdigit():
                    self.value = int(str(self.value) + str(self.text))
                else:
                    self.text = ''.join(filter(str.isdigit, self.text))
        backspace = False
        self.text = ""

    def updateText(self, val, pressed):
        m = pygame.mouse.get_pos()
        self.hoverEnter = self.position[0] <= m[0] <= self.position[0] + self.w and self.position[1] <= m[1] <= self.position[1] + self.h
        if self.hoverEnter and pressed:
            self.text += val

    def Render(self, screen, val, backspace, pressed):
        self.updateText(val, pressed)
        self.Check(backspace, val)
        font = pygame.font.Font(self.font, self.fontSize)
        text = font.render(str(self.value), True, self.fontColor)
        textRect = text.get_rect(center=(self.position[0] + self.w // 2, self.position[1] + self.h // 2))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], self.w, self.h))
        screen.blit(text, textRect)

class Slider:
    def __init__(self, x, y, val, min1, max1, length, h, max=500):
        self.value = val
        self.x = x
        self.y = y
        self.h = h
        self.min1 = min1
        self.max1 = max1
        self.length = length
        self.lineColor = (20, 10, 20)
        self.rectradius = 10
        self.temp_radius = self.rectradius
        self.rectColor = (255, 255, 255)
        self.v = 0.4
        self.temp = self.lineColor
        self.max = max

    def Calculate(self, val):
        self.v = (val - self.x) / self.length
        self.value = self.v * self.max

    def HandleMouse(self):
        mx, my = pygame.mouse.get_pos()
        if self.x <= mx <= self.x + self.length and self.y <= my <= self.y + self.h:
            self.rectradius = 15
            if pygame.mouse.get_pressed()[0]:
                self.Calculate(mx)
        else:
            self.lineColor = self.temp
            self.rectradius = self.temp_radius

    def Render(self, screen):
        self.HandleMouse()
        pygame.draw.rect(screen, self.lineColor, pygame.Rect(self.x, self.y, self.length, self.h))
        x = int(self.v * self.length + self.x)
        pygame.draw.rect(screen, self.rectColor, pygame.Rect(self.x, self.y, int(self.v * self.length), self.h))
        pygame.draw.circle(screen, (130, 213, 151), (x, self.y + self.rectradius // 2), self.rectradius)
        return self.value