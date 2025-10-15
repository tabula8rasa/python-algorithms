from itertools import batched
import pyglet
from pyglet import shapes
from math import cos, sin, pi
from typing import List, Tuple

# Create a window
window = pyglet.window.Window(width=1920, height=1080, caption='Pyglet Example')

# Create a batch for efficient drawing of multiple shapes
CLOCK= pyglet.graphics.Batch()


class Clock():

    def __init__(self, origin_x, origin_y, radius):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.radius = radius

    def create_circle(self):
        self.circle = shapes.Circle(x=self.origin_x, y=self.origin_y, radius=self.radius, color=(250, 250, 250), batch=CLOCK)

    def create_arrows(self):
        self.arrow_hour = shapes.Line(x=self.origin_x, y=self.origin_y, x2=self.origin_x + self.radius/2, y2=self.origin_y, thickness=4.8, color=(240, 20, 20), batch=CLOCK)
        self.arrow_min  = shapes.Line(x=self.origin_x, y=self.origin_y, x2=self.origin_x + self.radius, y2=self.origin_y, thickness=2.8, color=(20, 240, 20), batch=CLOCK)


objs = [Clock(origin_x=200 + 55 * i, origin_y=100 + 55 * j,  radius = 25) for j in range(6) for i in range(24)]
for i in objs:
    i.create_circle()
    i.create_arrows()
# print(objs)
#arrows = [shapes.Line(x=200+55*i,y=100+55*j,x2=225+55*i,y2=100+55*j,thickness=5.8,color=(240,20,20), batch=CLOCK) for j in range(6) for i in range(24)]
def update(dt):
    for i in objs:
        i.arrow_min.rotation += dt / 60 * 360

pyglet.clock.schedule_interval(update, 1)  # Call update 60 times per second


# Define the on_draw event handler
@window.event
def on_draw():
    window.clear()  # Clear the window to prepare for a new frame
    CLOCK.draw()    # Draw all shapes in the batch

# Run the Pyglet application
pyglet.app.run()

