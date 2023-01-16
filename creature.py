import numpy as np
from types import SimpleNamespace
import pygame
def dist(p1, p2):
    return np.sqrt((p2.x-p1.x)**2+(p2.y-p1.y))
class Creature:
    def __init__(self, world, verts, x, y, size, c):
        self.x = x
        self.y = y
        self.world = world
        self.size = size
        self.max_size = size
        self.color = c
        self.verticies = verts
        self.angle=0
        self.speed = 5
        self.update_points()
    
    def draw(self):
        pygame.draw.polygon(self.world.window, self.color, self.points, width=0)
    
    def update_points(self):
        self.points = [(np.cos(x+self.angle)*self.size+self.x, np.sin(x+self.angle)*self.size+self.y) for x in np.arange(2*np.pi, step=2*np.pi/self.verticies)]
    
    def point_towards(self, point):
        try:
            self.angle = np.arctan((point[1]-self.y)/(point[0]-self.x))
        except ZeroDivisionError:
            pass
        if point[0]-self.x < 0:
            self.angle += np.pi
        self.update_points()
    
    def move_towards(self, point):
        self.point_towards(point)
        if dist(self, SimpleNamespace(x=point[0], y=point[1])) < self.speed:
            self.x = point[0]
            self.y = point[1]
        else:
            self.x += self.speed*np.cos(self.angle)
            self.y += self.speed*np.sin(self.angle)
    
    def reproduce(self):
        self.size /= 2
        x = np.random.randint(self.x-self.max_size*2, self.x+self.max_size*2)
        y = np.random.randint(self.y-self.max_size*2, self.y+self.max_size*2)
        if np.random.rand()>0.01:
            self.world.create_creature(self.verticies, (x, y))
        else:
            if self.verticies ==3:
                self.world.create_creature(self.verticies+1, (x, y))
            else:
                if np.random.rand() < 0.75:
                    self.world.create_creature(self.verticies+1, (x, y))
                else:
                    self.world.create_creature(self.verticies-1, (x, y))
    
    def update(self):
        f = self.find_closest_food()
        if f:
            self.move_towards((f.x, f.y))
            if self.world.isIntersecting(self, f):
                self.size += 2*self.verticies
                if self.size > self.max_size:
                    self.size = self.max_size
                    self.reproduce()
                if f.verticies == 1:
                    self.world.food.remove(f)
                else:
                    self.world.creatures.remove(f)
        else:
            self.move_towards(self.world.random_pos())
        if self.world.tick % 200 == 0:
            self.size -= 1*self.verticies
            if self.size <=0:
                self.world.creatures.remove(self)
    def find_closest_food(self):
        prey = []
        for p in self.world.creatures:
            if p.verticies < self.verticies:
                prey.append(p)
        return self.find_closest(prey+self.world.food)
    def find_closest(self, objs):
        min_dist = np.inf
        closest = False
        for o in objs:
            d = dist(o, self)
            if d !=0 and d<min_dist:
                min_dist = d
                closest = o
        return closest


class Food():
    def __init__(self, world, x, y):
        self.x, self.y = x, y
        self.size  = 5
        self.world = world
        self.verticies = 1
    def draw(self):
        pygame.draw.circle(self.world.window, (0, 255, 0), (self.x, self.y), self.size)