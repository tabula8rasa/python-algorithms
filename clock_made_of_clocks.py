from itertools import batched

import pyglet
from pyglet import shapes
from math import cos, sin, pi

# Create a window
window = pyglet.window.Window(width=1920, height=1080, caption='Pyglet Example')

# Create a batch for efficient drawing of multiple shapes
CLOCK= pyglet.graphics.Batch()


Clock = {
    'radius': 50,

}


#circle = shapes.Circle(x=400, y=300, radius=Clock['radius'], color=(250, 250, 250), batch=CLOCK)
#hour_arrow = shapes.Line(x=400,y=300,x2=400,y2=300,thickness=100.8,color=(240,20,20), batch=CLOCK)

objs = [shapes.Circle(x=400+110*i, y=300+110*j, radius=Clock['radius'], color=(250, 250, 250), batch=CLOCK) for j in range(3) for i in range(8)]
arrows = [shapes.Line(x=400+110*i,y=300+110*j,x2=450+110*i,y2=300+110*j,thickness=10.8,color=(240,20,20), batch=CLOCK) for j in range(3) for i in range(8)]
def update(dt):
    for i in arrows:
        i.rotation += dt / 60 * 360

pyglet.clock.schedule_interval(update, 1)  # Call update 60 times per second


# Define the on_draw event handler
@window.event
def on_draw():
    window.clear()  # Clear the window to prepare for a new frame
    CLOCK.draw()    # Draw all shapes in the batch

# Run the Pyglet application
pyglet.app.run()

