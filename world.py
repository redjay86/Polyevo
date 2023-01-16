from creature import Creature, Food, dist
import numpy as np
import pygame.display
class World:
    def __init__(self, window):
        self.window = window
        self.creatures = []
        self.food = []
        self.color_index = []
        self.tick = 0
    
    def create_creature(self, verts, pos, size=25):
        while len(self.color_index) < verts:
            self.color_index.append((np.random.randint(255), np.random.randint(255), np.random.randint(255)))
        c = self.color_index[verts-1]
        self.creatures.append(Creature(self, verts, pos[0], pos[1], size, c))
    
    def create_food(self, pos):
        self.food.append(Food(self, pos[0], pos[1]))
    
    def display(self):
        [c.draw() for c in self.creatures]
        [f.draw() for f in self.food]
    
    def update(self):
        [c.update() for c in self.creatures]
        # CREATE FOOD
        if self.tick % 10 == 0:
            for i in range(2):
                self.create_food(self.random_pos())
        self.tick+=1
    @staticmethod
    def random_pos():
        w, h = pygame.display.get_window_size()
        return (np.random.rand()*w, np.random.rand()*h)

    @staticmethod
    def isIntersecting(c1, c2):
        return dist(c2, c1) <= c1.size + c2.size
