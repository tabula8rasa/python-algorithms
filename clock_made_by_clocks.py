import pyglet
from pyglet.window import key
from pyglet import shapes
import datetime

window = pyglet.window.Window(width=1850, height=500,caption='Clock_by_clocks')
pyglet.gl.glClearColor(0.8, 0.85, 0.85, 1.0)
keys = key.KeyStateHandler()
window.push_handlers(keys)

CLOCK = pyglet.graphics.Batch()

# Dots between hours, minutes and seconds
dots = [shapes.Circle(x=x,y=y,segments=50, radius=8, color=(0,0,0), batch=CLOCK) for x in [675,1195] for y in [195,255]]

class Clock:
    def __init__(self, origin_x: int, origin_y: int, radius: int):

        self.border_circle = shapes.Circle(x=origin_x, y=origin_y, segments=500, radius=radius+4, color=(250, 250, 250), batch=CLOCK)
        self.circle = shapes.Circle(x=origin_x, y=origin_y, segments=500, radius=radius, color=(230, 230, 230), batch=CLOCK)
        self.arrow_hour = shapes.Line(x=origin_x, y=origin_y, x2=origin_x + radius, y2=origin_y, thickness=7, color=(0,0, 0), batch=CLOCK)
        self.arrow_min = shapes.Line(x=origin_x, y=origin_y, x2=origin_x + radius, y2=origin_y, thickness=7, color=(0, 0, 0), batch=CLOCK)
        self.states = {'H':[0, 180],
                       'V':[270,90],
                       'TL':[180,270],
                       'TR':[0,270],
                       'BL':[180,90],
                       'BR':[0,90],
                       'E':[135,135]}
        self.arrow_hour.rotation = self.states['E'][0]
        self.arrow_min.rotation = self.states['E'][1]

digits = [
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

def func_rotation(obj, state):
    """Rotate both arrows to given position

    Args:
        obj: Single clock
        state: Position which rotate to

    Returns:
        None
    """
    if obj.arrow_hour.rotation % 360  != obj.states[state][0] or obj.arrow_min.rotation % 360 != obj.states[state][1]:
        h, m = 0, 0
        if obj.arrow_hour.rotation % 360 == obj.states[state][0]:
            obj.arrow_hour.rotation = obj.states[state][0]
            h = 1
        if obj.arrow_min.rotation % 360 == obj.states[state][1]:
            obj.arrow_min.rotation = obj.states[state][1]
            m = 1
        if h == 0:
            obj.arrow_hour.rotation += 15
        if m == 0:
            obj.arrow_min.rotation += 15

h_f_digit = [Clock(origin_x=200 + 60 * i, origin_y=375 - 60 * j,  radius = 25) for j in range(6) for i in range(4)]
h_s_digit = [Clock(origin_x=210 + 60 * i, origin_y=375 - 60 * j,  radius = 25) for j in range(6) for i in range(4,8)]
m_f_digit = [Clock(origin_x=240 + 60 * i, origin_y=375 - 60 * j,  radius = 25) for j in range(6) for i in range(8,12)]
m_s_digit = [Clock(origin_x=250 + 60 * i, origin_y=375 - 60 * j,  radius = 25) for j in range(6) for i in range(12,16)]
s_f_digit = [Clock(origin_x=280 + 60 * i, origin_y=375 - 60 * j,  radius = 25) for j in range(6) for i in range(16,20)]
s_s_digit = [Clock(origin_x=290 + 60 * i, origin_y=375 - 60 * j,  radius = 25) for j in range(6) for i in range(20,24)]

objs =[h_f_digit,h_s_digit,m_f_digit,m_s_digit,s_f_digit,s_s_digit]

def update(dt):

    t = datetime.datetime.now()
    h = str(t.hour)
    m = str(t.minute)
    s = str(t.second)

    hour_f = '0' if len(h) == 1 else h[0]
    hour_s = h[0] if len(h) == 1 else h[1]

    minute_f = '0' if len(m) == 1 else m[0]
    minute_s = m[0] if len(m) == 1 else m[1]

    second_f = '0' if len(s) == 1 else s[0]
    second_s = s[0] if len(s) == 1 else s[1]

    status =[hour_f,hour_s,minute_f,minute_s,second_f,second_s]

    for i, obj in enumerate(objs):
        for j, clock in enumerate(obj):
            func_rotation(clock, digits[int(status[i])][j])

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    CLOCK.draw()

pyglet.app.run()

