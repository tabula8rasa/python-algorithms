import pyglet
from pyglet.window import key
from pyglet import shapes
from datetime import datetime

WIN_W, WIN_H = 1850, 500
RADIUS = 25
LINE_THICK = 7
CIRCLE_SEG = 60

STATE_ANGLES = {
    'H':  (0, 180),
    'V':  (270, 90),
    'TL': (180, 270),
    'TR': (0, 270),
    'BL': (180, 90),
    'BR': (0, 90),
    'E':  (135, 135),
}

DIGITS = [
  [
    'BR', 'H',  'H',  'BL',
    'V',  'BR', 'BL', 'V',
    'V',  'V',  'V',  'V',
    'V',  'V',  'V',  'V',
    'V',  'TR', 'TL', 'V',
    'TR', 'H',  'H',  'TL',
  ],
  [
    'BR', 'H',  'BL', 'E',
    'TR', 'BL', 'V',  'E',
    'E',  'V',  'V',  'E',
    'E',  'V',  'V',  'E',
    'BR', 'TL', 'TR', 'BL',
    'TR', 'H',  'H',  'TL',
  ],
  [
    'BR', 'H',  'H',  'BL',
    'TR', 'H',  'BL', 'V',
    'BR', 'H',  'TL', 'V',
    'V',  'BR', 'H',  'TL',
    'V',  'TR', 'H',  'BL',
    'TR', 'H',  'H',  'TL',
  ],
  [
    'BR', 'H',  'H',  'BL',
    'TR', 'H',  'BL', 'V',
    'E',  'BR', 'TL', 'V',
    'E',  'TR', 'BL', 'V',
    'BR', 'H',  'TL', 'V',
    'TR', 'H',  'H',  'TL',
  ],
  [
    'BR', 'BL', 'BR', 'BL',
    'V',  'V',  'V',  'V',
    'V',  'TR', 'TL', 'V',
    'TR', 'H',  'BL', 'V',
    'E',  'E',  'V',  'V',
    'E',  'E',  'TR', 'TL',
  ],
  [
    'BR', 'H',  'H',  'BL',
    'V',  'BR', 'H',  'TL',
    'V',  'TR', 'H',  'BL',
    'TR', 'H',  'BL', 'V',
    'BR', 'H',  'TL', 'V',
    'TR', 'H',  'H',  'TL',
  ],
  [
    'BR', 'H',  'H',  'BL',
    'V',  'BR', 'H',  'TL',
    'V',  'TR', 'H',  'BL',
    'V',  'BR', 'BL', 'V',
    'V',  'TR', 'TL', 'V',
    'TR', 'H',  'H',  'TL',
  ],
  [
    'BR', 'H',  'H',  'BL',
    'TR', 'H',  'BL', 'V',
    'E',  'E',  'V',  'V',
    'E',  'E',  'V',  'V',
    'E',  'E',  'V',  'V',
    'E',  'E',  'TR', 'TL',
  ],
  [
    'BR', 'H',  'H',  'BL',
    'V',  'BR', 'BL', 'V',
    'V',  'TR', 'TL', 'V',
    'V',  'BR', 'BL', 'V',
    'V',  'TR', 'TL', 'V',
    'TR', 'H',  'H',  'TL',
  ],
  [
    'BR', 'H',  'H',  'BL',
    'V',  'BR', 'BL', 'V',
    'V',  'TR', 'TL', 'V',
    'TR', 'H',  'BL', 'V',
    'BR', 'H',  'TL', 'V',
    'TR', 'H',  'H',  'TL',
  ]]

window = pyglet.window.Window(width=WIN_W, height=WIN_H,caption='Clock_by_clocks')
pyglet.gl.glClearColor(0.8, 0.85, 0.85, 1.0)
keys = key.KeyStateHandler()
window.push_handlers(keys)
CLOCK = pyglet.graphics.Batch()

# Dots between hours, minutes and seconds
dots = [shapes.Circle(x=x,y=y,segments=CIRCLE_SEG, radius=8, color=(0,0,0), batch=CLOCK) for x in [675,1195] for y in [195,255]]

class Clock:
    def __init__(self, origin_x: int, origin_y: int, radius: int):

        self.border_circle = shapes.Circle(x=origin_x, y=origin_y, segments=CIRCLE_SEG, radius=radius+4, color=(250, 250, 250), batch=CLOCK)
        self.circle = shapes.Circle(x=origin_x, y=origin_y, segments=CIRCLE_SEG, radius=radius, color=(230, 230, 230), batch=CLOCK)
        self.arrow_hour = shapes.Line(x=origin_x, y=origin_y, x2=origin_x + radius, y2=origin_y, thickness=LINE_THICK, color=(0,0, 0), batch=CLOCK)
        self.arrow_min = shapes.Line(x=origin_x, y=origin_y, x2=origin_x + radius, y2=origin_y, thickness=LINE_THICK, color=(0, 0, 0), batch=CLOCK)

        self.arrow_hour.rotation = STATE_ANGLES['E'][0]
        self.arrow_min.rotation = STATE_ANGLES['E'][1]


def func_rotation(obj, state):
    """Rotate both arrows to given position

    Args:
        obj: Single clock
        state: Position which rotate to

    Returns:
        None
    """
    if obj.arrow_hour.rotation % 360  != STATE_ANGLES[state][0] or obj.arrow_min.rotation % 360 != STATE_ANGLES[state][1]:
        h, m = 0, 0
        if obj.arrow_hour.rotation % 360 == STATE_ANGLES[state][0]:
            obj.arrow_hour.rotation = STATE_ANGLES[state][0]
            h = 1
        if obj.arrow_min.rotation % 360 == STATE_ANGLES[state][1]:
            obj.arrow_min.rotation = STATE_ANGLES[state][1]
            m = 1
        if h == 0:
            obj.arrow_hour.rotation += 15
        if m == 0:
            obj.arrow_min.rotation += 15

def make_digit(origin_x: int, origin_y: int = 375, w: int = 4, h: int = 6, dx: int = 60, dy: int = 60):
    return [Clock(origin_x + i*dx, origin_y - j*dy, RADIUS)
            for j in range(h) for i in range(w)]

objs = [make_digit(200 + (i*4)*60 + (i % 2) *(i * 20 - 10) - (i % 2 - 1) * (i * 20), 375 ) for i in range(6)]

DX = 60            # width of a single clock cell
BLOCK = 4*DX       # width of one digit
GAP = 10           # regular gap between digits
COLON_GAP = 30     # extra gap before the ":" separator
x0 = 200           # starting x position

digit_x = [
    x0,
    x0 + GAP + BLOCK,
    x0 + GAP + 2*BLOCK + COLON_GAP,
    x0 + 2*GAP + 3*BLOCK + COLON_GAP,
    x0 + 2*GAP + 4*BLOCK + 2*COLON_GAP,
    x0 + 3*GAP + 5*BLOCK + 2*COLON_GAP
]

digits = [make_digit(x) for x in digit_x]

def update(dt):

    current_time = list(datetime.now().strftime("%H%M%S"))

    for i, obj in enumerate(digits):
        for j, clock in enumerate(obj):
            func_rotation(clock, DIGITS[int(current_time[i])][j])

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    CLOCK.draw()

pyglet.app.run()

