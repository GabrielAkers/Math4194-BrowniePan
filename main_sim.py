import pygame
import random
import os
import colour
from colour import Color

# run it and then hit n to spawn a new shape

pygame.init()
SIZE = [500, 500]
SCREEN = pygame.display.set_mode(SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
TRANS = (1, 1, 1)

BLUE = (0, 0, 255)
YELLOW = (0, 122, 122)
GREEN = (0, 255, 0)
ORANGE = (200, 100, 50)
RED = (255, 0, 0)



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
Z = [(125, 125), (375, 125),
     (375, 170), (140, 170),
     (140, 185), (375, 185),
     (375, 230), (140, 230),
     (140, 245), (375, 245),
     (375, 290), (140, 290),
     (140, 305), (375, 305),
     (375, 350), (140, 350),
     (140, 365), (375, 365),
     (375, 380), (125, 380),
     (125, 335), (360, 335),
     (360, 320), (125, 320),
     (125, 275), (360, 275),
     (360, 260), (125, 260),
     (125, 215), (360, 215),
     (360, 200), (125, 200),
     (125, 155), (360, 155),
     (360, 140), (125, 140)]


class Shape:
    def __init__(self, vertices, shape_type, radius=.8):
        # vertices := list of tuples (x,y)
        # this is flatting the 2d list vertices and then scaling the coords then turning back into vertices
        coords = [i for j in vertices for i in j]
        it = iter(coords)
        self.vertices = list(zip(it, it))
        self.radius = radius  # this is for rounded rect or 'rr' flagged shapes, 0<=r<=1 : 0=>square and 1=>circle

        self.shape_type = shape_type
        self.shape = None
        self.create_self()

        self.area = self.calc_area()

    def create_self(self):
        if self.shape_type == 'poly':
            self.shape = pygame.draw.polygon(SCREEN, WHITE, self.vertices)
        elif self.shape_type == 'rr':
            r = pygame.Rect(SQ[0][0], SQ[0][1], 250, 250)
            self.shape = self.aa_filled_rounded_rect(SCREEN, r, WHITE, self.radius)

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
        rectangle.fill((255, 255, 255), special_flags=pygame.BLEND_RGBA_MIN)

        return surface.blit(rectangle, pos)


# slider stuff borrowed from here: https://www.dreamincode.net/forums/topic/401541-buttons-and-sliders-in-pygame/
font = pygame.font.SysFont("Verdana", 12)


class Slider:
    def __init__(self, name, val, maxi, mini, pos):
        self.val = val  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.xpos = pos  # x-location on screen
        self.ypos = 450
        self.surf = pygame.Surface((100, 50))
        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction

        self.txt_surf = font.render(name, 1, WHITE)
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))

        # Static graphics - slider background #
        self.surf.fill((100, 100, 100))
        pygame.draw.rect(self.surf, GREY, [0, 0, 100, 50], 3)
        pygame.draw.rect(self.surf, ORANGE, [10, 10, 80, 10], 0)
        pygame.draw.rect(self.surf, WHITE, [10, 30, 80, 5], 0)

        self.surf.blit(self.txt_surf, self.txt_rect)  # this surface never changes

        # dynamic graphics - button surface #
        self.button_surf = pygame.Surface((20, 20))
        self.button_surf.fill(TRANS)
        self.button_surf.set_colorkey(TRANS)
        pygame.draw.circle(self.button_surf, WHITE, (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, ORANGE, (10, 10), 4, 0)

    def draw(self):
        """ Combination of static and dynamic graphics in a copy of
    the basic slide surface
    """
        # static
        surf = self.surf.copy()

        # dynamic
        pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # move of button box to correct screen position

        # screen
        SCREEN.blit(surf, (self.xpos, self.ypos))

    def move(self):
        """
    The dynamic part; reacts to movement of the slider button.
    """
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi


class Sim:
    def __init__(self, shape_type, shape_coords):
        self.play = True
        self.shape_type = shape_type
        self.shape_coords = shape_coords

        self.radius_slider = Slider("Radius", 0.6, 1.0, 0.0, 0)
        self.cook_time_slider = Slider("Time", 200, 200, 10, 100)
        self.slides = [self.radius_slider, self.cook_time_slider]

        self.color_grades = 8
        self.colors = list(Color("blue").range_to(Color("red"), self.color_grades))
        print(self.colors)
        self.rgb_colors = [colour.hex2rgb(i.hex) for i in self.colors]
        temp = [int(255*i) for j in self.rgb_colors for i in j]
        it = iter(temp)
        self.rgb_colors = list(zip(it, it, it))
        print(self.rgb_colors)
        self.diffusing = False
        self.current_diffuse_time = 0
        self.cook_time = self.cook_time_slider.val
        self.max_diffuse_time = self.cook_time
        self.cleanup = True
        self.forward = True

        self.shape = None

        for s in self.slides:
            s.draw()
        self.draw_text()
        pygame.display.update()

    def new_sim(self):
        SCREEN.fill(BLACK)
        if self.shape_type == 'rr':
            self.shape = Shape(SQ, shape_type=self.shape_type, radius=self.radius_slider.val)
        elif self.shape_type == 'poly':
            self.shape = Shape(self.shape_coords, shape_type=self.shape_type, radius=self.radius_slider.val)
        self.diffusing = True
        self.current_diffuse_time = 0
        self.cleanup = True

    def draw_text(self):
        # just display the value of the radius
        txt_surf = font.render(str(self.radius_slider.val) + " :: " + str(self.cook_time_slider.val), 1, WHITE)
        txt_rect = txt_surf.get_rect(center=(50, 15))
        SCREEN.fill(BLACK, pygame.Rect(0, 0, 100, 30))
        SCREEN.blit(txt_surf, txt_rect)

    def diffuse(self):
        # check middle pixel for doneness
        middle_pix = (250, 250)
        temp_increment = (350-75)/self.color_grades
        final_amount = (160-75)/temp_increment
        if SCREEN.get_at(middle_pix) in self.rgb_colors and self.rgb_colors.index(SCREEN.get_at(middle_pix)) >= final_amount:
            self.diffusing = False
            print('done cooking')
        # color correction stuff from the anti-aliasing
        if self.cleanup:
            for x in range(100, 400):
                for y in range(100, 400):
                    # this is a really bad way to handle this. consider refactoring to define a notion of closeness
                    fake_white = (252, 252, 252, 255)
                    other_fake_white = (191, 191, 191, 255)
                    fake_black = (8, 8, 8, 255)
                    middle_black = (120, 120, 120, 255)
                    if SCREEN.get_at((x, y)) == fake_white or SCREEN.get_at((x, y)) == other_fake_white:
                        SCREEN.set_at((x, y), WHITE)
                    elif SCREEN.get_at((x, y)) == fake_black or SCREEN.get_at((x, y)) == middle_black:
                        SCREEN.set_at((x, y), BLACK)
        self.cleanup = False
        if self.forward:
            for x in range(100, 400):
                for y in range(100, 400):
                    if SCREEN.get_at((x, y)) == BLACK or SCREEN.get_at((x, y)) in self.rgb_colors:
                        direction = self.pick_random_direction()
                        direction = tuple(item1 + item2 for item1, item2 in zip(direction, (x, y)))
                        direction_color = SCREEN.get_at(direction)
                        if direction_color == WHITE:
                            SCREEN.set_at(direction, self.rgb_colors[0])
                        elif direction_color in self.rgb_colors:
                            start_index = self.rgb_colors.index(direction_color)
                            if start_index < len(self.colors)-1:
                                new = self.rgb_colors[start_index+1]
                            else:
                                new = self.rgb_colors[start_index]
                            SCREEN.set_at(direction, new)

                        # heat exiting the pan happens here
                        if SCREEN.get_at((x, y)) in self.rgb_colors and SCREEN.get_at(direction) == BLACK:
                            ind = self.rgb_colors.index(SCREEN.get_at((x, y)))
                            if ind >= 1:
                                SCREEN.set_at((x, y), self.rgb_colors[ind-1])
                            else:
                                SCREEN.set_at((x, y), WHITE)
        else:
            for x in range(100, 400):
                for y in range(100, 400):
                    if SCREEN.get_at((500-x, 500-y)) == BLACK or SCREEN.get_at((500-x, 500-y)) in self.rgb_colors:
                        direction = self.pick_random_direction()
                        direction = tuple(item1 + item2 for item1, item2 in zip(direction, (500-x, 500-y)))
                        direction_color = SCREEN.get_at(direction)
                        if direction_color == WHITE:
                            SCREEN.set_at(direction, self.rgb_colors[0])
                        elif direction_color in self.rgb_colors:
                            start_index = self.rgb_colors.index(direction_color)
                            if start_index < len(self.colors) - 1:
                                new = self.rgb_colors[start_index + 1]
                            else:
                                new = self.rgb_colors[start_index]
                            SCREEN.set_at(direction, new)

                        # heat exiting the pan happens here
                        if SCREEN.get_at((500-x, 500-y)) in self.rgb_colors and SCREEN.get_at(direction) == BLACK:
                            ind = self.rgb_colors.index(SCREEN.get_at((500-x, 500-y)))
                            if ind >= 1:
                                SCREEN.set_at((500-x, 500-y), self.rgb_colors[ind - 1])
                            else:
                                SCREEN.set_at((500-x, 500-y), WHITE)
        self.forward = not self.forward

    def pick_random_direction(self):
        choices = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        return random.choice(choices)

    def gather_data(self):
        red_dots = 0
        for x in range(100, 400):
            for y in range(100, 400):
                if SCREEN.get_at((x, y)) == RED:
                    red_dots += 1
        print('current shape type: ' + self.shape_type)
        print('num vertices: ' + str(len(self.shape.vertices)))
        print('num red dots: ' + str(red_dots))
        print('cook time: ' + str(self.current_diffuse_time))
        print('area: ' + str(self.shape.area))

    def run(self):
        while self.play:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n and not self.diffusing:
                        self.new_sim()
                    elif event.key == pygame.K_s and self.diffusing:
                        self.diffusing = False
                    elif event.key == pygame.K_g and not self.diffusing:
                        self.gather_data()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for s in self.slides:
                        if s.button_rect.collidepoint(pos):
                            s.hit = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    for s in self.slides:
                        s.hit = False

            if not self.diffusing:
                for s in self.slides:
                    if s.hit:
                        s.move()
                for s in self.slides:
                    s.draw()
                self.draw_text()

            pygame.display.update()

            if self.diffusing and self.current_diffuse_time < self.max_diffuse_time:
                self.diffuse()
                self.current_diffuse_time += 1


os.chdir(os.path.dirname(__file__))
if __name__ == "__main__":
    sim = Sim('poly', Z)
    sim.run()
