from itertools import batched
import pyglet
from pyglet import shapes
from math import cos, sin, pi
from typing import List, Tuple
import random

# Create a window
window = pyglet.window.Window(width=1920, height=1080, caption='Pyglet Example')

# Create a batch for efficient drawing of multiple shapes
CLOCK= pyglet.graphics.Batch()

class Clock:

    def __init__(self, origin_x: int, origin_y: int, radius: int):
        self.circle = shapes.Circle(x=origin_x, y=origin_y, radius=radius, color=(250, 250, 250), batch=CLOCK)
        self.arrow_hour = shapes.Line(x=origin_x, y=origin_y, x2=origin_x + radius, y2=origin_y, thickness=4.8, color=(240, 20, 20), batch=CLOCK)
        self.arrow_min = shapes.Line(x=origin_x, y=origin_y, x2=origin_x + radius, y2=origin_y, thickness=4.8, color=(20, 240, 20), batch=CLOCK)
        self.states = {'H':[0, 180],
                       'V':[270,90],
                       'TL':[180,270],
                       'TR':[0,270],
                       'BL':[180,90],
                       'BR':[0,90],
                       'E':[135,135]}


    def rotate(self, position_to: str):
        self.arrow_hour.rotation += self.states[position_to][0] - self.arrow_hour.rotation
        self.arrow_min.rotation += self.states[position_to][1] - self.arrow_min.rotation



obj = Clock(origin_x=500, origin_y=500, radius=150)

print(obj.arrow_hour.rotation)
# objs = [Clock(origin_x=200 + 55 * i, origin_y=100 + 55 * j,  radius = 25) for j in range(6) for i in range(24)]


def update(dt):
    l = ['H','V','TL','TR','BL','BR','E']
    obj.rotate(l[random.randint(0, 6)])


pyglet.clock.schedule_interval(update, 3)  # Call update 60 times per second


# Define the on_draw event handler
@window.event
def on_draw():
    window.clear()  # Clear the window to prepare for a new frame
    CLOCK.draw()    # Draw all shapes in the batch

# Run the Pyglet application
pyglet.app.run()

