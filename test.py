
import pyglet

from pyglet.window import key
from pyglet import shapes

import datetime


# Create a window
window = pyglet.window.Window(width=1750, height=500,caption='Pyglet Example')

keys = key.KeyStateHandler()
window.push_handlers(keys)

# Create a batch for efficient drawing of multiple shapes
CLOCK= pyglet.graphics.Batch()
SYMBOL = None

class Clock:

    def __init__(self, origin_x: int, origin_y: int, radius: int):

        self.border_circle = shapes.Circle(x=origin_x, y=origin_y, segments = 500, radius=radius+5, color=(168, 168, 168), batch=CLOCK)
        self.circle = shapes.Circle(x=origin_x, y=origin_y, segments=500, radius=radius, color=(250, 250, 250), batch=CLOCK)
        self.arrow_hour = shapes.Line(x=origin_x, y=origin_y, x2=origin_x + radius, y2=origin_y, thickness=6, color=(0,0, 0), batch=CLOCK)
        self.arrow_min = shapes.Line(x=origin_x, y=origin_y, x2=origin_x + radius, y2=origin_y, thickness=6, color=(0, 0, 0), batch=CLOCK)
        self.states = {'H':[0, 180],
                       'V':[270,90],
                       'TL':[180,270],
                       'TR':[0,270],
                       'BL':[180,90],
                       'BR':[0,90],
                       'E':[135,135]}
        self.position = 'E'
        self.arrow_hour.rotation = self.states[self.position][0]
        self.arrow_min.rotation = self.states[self.position][1]


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

t = datetime.datetime.now()
delta = datetime.timedelta(seconds=1/60)

def wtfamidoing(obj, state):

    if obj.arrow_hour.rotation % 360  != obj.states[state][0] or obj.arrow_min.rotation % 360 != obj.states[state][1]:
        h, m = 0, 0
        if obj.arrow_hour.rotation % 360 == obj.states[state][0] and h == 0:
            obj.arrow_hour.rotation = obj.states[state][0]
            h = 1
        if obj.arrow_min.rotation % 360 == obj.states[state][1] and m == 0:
            obj.arrow_min.rotation = obj.states[state][1]
            m = 1
        if h == 0:
            obj.arrow_hour.rotation += 15
        if m == 0:
            obj.arrow_min.rotation += 15
        if h + m == 2:
            SYMBOL = None

# objs = [Clock(origin_x=200 + 55 * i, origin_y=100 + 55 * j,  radius = 25) for j in range(6) for i in range(24)]
h_f_digit = [Clock(origin_x=200 + 55 * i, origin_y=375 - 55 * j,  radius = 25) for j in range(6) for i in range(4)]
h_s_digit = [Clock(origin_x=210 + 55 * i, origin_y=375 - 55 * j,  radius = 25) for j in range(6) for i in range(4,8)]
m_f_digit = [Clock(origin_x=240 + 55 * i, origin_y=375 - 55 * j,  radius = 25) for j in range(6) for i in range(8,12)]
m_s_digit = [Clock(origin_x=250 + 55 * i, origin_y=375 - 55 * j,  radius = 25) for j in range(6) for i in range(12,16)]
s_f_digit = [Clock(origin_x=280 + 55 * i, origin_y=375 - 55 * j,  radius = 25) for j in range(6) for i in range(16,20)]
s_s_digit = [Clock(origin_x=290 + 55 * i, origin_y=375 - 55 * j,  radius = 25) for j in range(6) for i in range(20,24)]
objs =[h_f_digit,h_s_digit,m_f_digit,m_s_digit,s_f_digit,s_s_digit]

def update(dt):
    global SYMBOL, t
    t += delta

    if len(str(t.hour)) == 1:
        hour_f = '0'
        hour_s = str(t.hour)[0]
    else:
        hour_f = str(t.hour)[0]
        hour_s = str(t.hour)[1]
    if len(str(t.minute)) == 1:
        minute_f = '0'
        minute_s = str(t.minute)[0]
    else:
        minute_f = str(t.minute)[0]
        minute_s = str(t.minute)[1]
    if len(str(t.second)) == 1:
        second_f = '0'
        second_s = str(t.second)[0]
    else:
        second_f = str(t.second)[0]
        second_s = str(t.second)[1]

    # print(second_f)
    i=0
    j=0
    ii=0
    jj=0
    iii=0
    jjj=0

    for clock in objs[-1]:
        wtfamidoing(clock, digits[int(second_s)][i])
        i+=1
    for clock in objs[-2]:
        wtfamidoing(clock, digits[int(second_f)][j])
        j += 1
    for clock in objs[-3]:
        wtfamidoing(clock, digits[int(minute_s)][ii])
        ii += 1
    for clock in objs[-4]:
        wtfamidoing(clock, digits[int(minute_f)][jj])
        jj += 1
    for clock in objs[-5]:
        wtfamidoing(clock, digits[int(hour_s)][iii])
        iii += 1
    for clock in objs[-6]:
        wtfamidoing(clock, digits[int(hour_f)][jjj])
        jjj += 1


pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_key_press(symbol, modifiers):
    global SYMBOL
    SYMBOL = symbol
    print(symbol)

# Define the on_draw event handler
@window.event
def on_draw():
    window.clear()  # Clear the window to prepare for a new frame
    CLOCK.draw()    # Draw all shapes in the batch

# Run the Pyglet application
pyglet.app.run()

