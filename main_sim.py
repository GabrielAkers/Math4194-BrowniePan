import pygame
import random
import os

# run it and then hit n to spawn a new shape

pygame.init()
SIZE = [500, 500]
SCREEN = pygame.display.set_mode(SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# some predefined polygons for easy testing
EQ_TRI = [(3/4*SIZE[0], 1/4*SIZE[1]),
          (SIZE[0]/2, 3/4*SIZE[1]),
          (1/4*SIZE[0], 1/4*SIZE[1])]
SQ = [(1/4*SIZE[0], 1/4*SIZE[1]),
      (3/4*SIZE[0], 1/4*SIZE[1]),
      (3/4*SIZE[0], 3/4*SIZE[1]),
      (1/4*SIZE[0], 3/4*SIZE[1])]
PENT = [(250, 100),
        (107, 204),
        (162, 371),
        (338, 371),
        (393, 204)]  # got lazy generalizing to variable height/width
HEX = [(325, 120),
       (175, 120),
       (100, 250),
       (175, 380),
       (325, 380),
       (400, 250)]


class Shape:
    def __init__(self, vertices, shape_type, radius=.8):
        # vertices := list of tuples (x,y)
        # this is flatting the 2d list vertices and then scaling the coords then turning back into vertices
        coords = [i for j in vertices for i in j]
        it = iter(coords)
        self.vertices = list(zip(it, it))
        self.radius = radius  # this is for rounded rect or 'rr' flagged shapes, 0<=r<=1 : 0=>square and 1=>circle

        self.shape_type = shape_type
        self.create_self()

        self.area = self.calc_area()

    def create_self(self):
        if self.shape_type == 'poly':
            pygame.draw.polygon(SCREEN, WHITE, self.vertices)
        elif self.shape_type == 'rr':
            r = pygame.Rect(SQ[0][0], SQ[0][1], 250, 250)
            self.aa_filled_rounded_rect(SCREEN, r, WHITE, self.radius)

    def calc_area(self):
        # arbitrary polygon area algorithm found here: https://www.mathopenref.com/coordpolygonarea2.html
        j = len(self.vertices) - 1
        a = 0
        for i in range(len(self.vertices)):
            a += ((self.vertices[j][0]+self.vertices[i][0]) * (self.vertices[j][1]-self.vertices[i][1]))
            j = i

        return abs(a)/2

    # found here: https://www.pygame.org/project-AAfilledRoundedRect-2349-.html
    def aa_filled_rounded_rect(self, surface, rect, color, radius=.6):

        """
        AAfilledRoundedRect(surface,rect,color,radius=0.4)

        surface : destination
        rect    : rectangle
        color   : rgb or rgba
        radius  : 0 <= radius <= 1
        """

        rect = pygame.Rect(rect)
        color = pygame.Color(*color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0, 0
        rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

        circle = pygame.Surface([min(rect.size)*3]*2, pygame.SRCALPHA)
        pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        circle = pygame.transform.smoothscale(circle, [int(min(rect.size)*radius)]*2)

        radius = rectangle.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

        rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

        surface.blit(rectangle, pos)


class Sim:
    def __init__(self):
        self.play = True
        self.shape = None

    def new_sim(self, shape_type='rr', radius=0.7):
        SCREEN.fill(BLACK)
        self.shape = Shape(SQ, shape_type=shape_type, radius=radius)

    def run(self):
        while self.play:
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.new_sim()


os.chdir(os.path.dirname(__file__))
if __name__ == "__main__":
    sim = Sim()
    sim.run()
