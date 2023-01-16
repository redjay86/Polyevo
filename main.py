import pygame
from pygame.locals import *
import numpy as np
from world import World
import matplotlib.pyplot as plt
from  matplotlib.animation import FuncAnimation

def get_population(world):
    pops = {}
    verts_seen = []
    for c in world.creatures:
        if c.verticies in verts_seen:
            pops[c.verticies][0]+=1
        else:
            pops[c.verticies] = [1, c.color]
            verts_seen.append(c.verticies)
    return pops, world.tick
pygame.init()
fig = plt.figure()
lines = []
created_lines = []
Xs = {}
Ys = {}
def animate(i):
    for i in range(1):
        main_loop()
    graph_data, x = get_population(world)
    for creat_pop in graph_data:
        if creat_pop not in created_lines:
            Xs[creat_pop] = [x]
            Ys[creat_pop] = [graph_data[creat_pop][0]]
            lines.append(plt.plot([],[], color=np.array(graph_data[creat_pop][1])/255)[0])
            created_lines.append(creat_pop)
        else:
            Xs[creat_pop].append(x)
            Ys[creat_pop].append(graph_data[creat_pop][0])
        lines[created_lines.index(creat_pop)].set_data(Xs[creat_pop], Ys[creat_pop])
    fig.gca().relim()
    fig.gca().autoscale_view() 
    return lines,

window = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)

run = True
world = World(window)
pos = (0, 0)
[world.create_creature(3, world.random_pos(), size=25) for i in range(1)]
[world.create_food(world.random_pos()) for i in range(100)]
animation = FuncAnimation(fig, animate, interval=1)

def main_loop():
    window.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            return False
        elif event.type == MOUSEBUTTONDOWN:
            world.create_creature(3, event.pos, 25)
            pass
        elif event.type == MOUSEMOTION:
            pos = event.pos
    world.update()
    world.display()
    pygame.display.update()
plt.show()

