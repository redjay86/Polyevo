import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
 
fig = plt.figure(figsize=(6, 3))
x = [0]
ys = []
 
lines = []

 
def update(frame):
    if frame%20==0:
        ys.append([0]*len(x))
        lines.append(plt.plot(x, ys[-1], '-')[0])
    x.append(x[-1] + 1)
    for i in range(len(ys)):
        ys[i].append(np.random.rand())
        lines[i].set_data(x, ys[i]) 
    fig.gca().relim()
    fig.gca().autoscale_view() 
    return lines,
 
animation = FuncAnimation(fig, update, interval=500)
plt.show()