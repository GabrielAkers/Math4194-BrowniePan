import pygame
import random
import os
import numpy as np
import pandas as pd


pygame.init()
SIZE = [500, 500]
SCREEN = pygame.display.set_mode(SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# some predefined polygons for easy testing
EQ_TRI = [(.1, .55), (.1, .1), (.55, .1)]


class Polygon:
    def __init__(self, vertices):
        # vertices := list of tuples (x,y)
        # multiply by half the screen width.
        # when making a polygon just pass in numbers normalized
        half_size = SIZE[0]/2
        # this is flatting the 2d list vertices and then scaling the coords then turning back into vertices
        coords = [half_size * i for j in vertices for i in j]
        it = iter(coords)
        self.vertices = list(zip(it, it))
        self.rect = self.create_self()
        self.area = self.calc_area()

    def create_self(self):
        return pygame.draw.polygon(SCREEN, WHITE, self.vertices)

    def calc_area(self):
        # arbitrary polygon area algorithm found here: https://www.mathopenref.com/coordpolygonarea2.html
        j = len(self.vertices) - 1
        a = 0
        for i in range(len(self.vertices)):
            a += ((self.vertices[j][0]+self.vertices[i][0]) * (self.vertices[j][1]-self.vertices[i][1]))
            j = i

        return abs(a)/2


class Sim:
    def __init__(self, shape):
        self.play = True
        self.shape = shape.rect

    def run(self):
        while self.play:
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


os.chdir(os.path.dirname(__file__))
if __name__ == "__main__":
    tri = Polygon(EQ_TRI)
    sim = Sim(tri)
    sim.run()