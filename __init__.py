"""
__init__.py

Created by Andres Bastidas on 2011-11-07.
"""
import math
import random
from nodebox.graphics import Context
_ctx = Context
_palette = []
SINE_PERIOD_DEG = 180.0

def set_palette(palette):
  """ set color palette
  """
  global _palette
  _palette = palette
  return

def bounds(paths=[]):
  """ Returns (x,y), (width, height) bounds for a group of paths
  - originally provided as sample at http://nodebox.net/code/index.php/SVG
  """
  if len(paths) == 0:
    return (0, 0), (0, 0)

  l = t = float("inf")
  r = b = float("-inf")

  for path in paths:
    (x, y), (w, h) = path.bounds
    l = min(l, x)
    t = min(t, y)
    r = max(r, x+w)
    b = max(b, y+h)

  return (l, t), (r-l, b-t)

def zero_translate(paths=[]):
  """ return offset to get path corner to (0,0)
  """
  (x,y), (w,h) = bounds(paths)
  return (-x,-y)

def make_grid(paths=[], xoffset=0, yoffset=0, xcount=1, ycount=1, xpad=0, ypad=0):
  """ creates a grid using the provided path
  """
  g_paths = []
  (x,y), (w,h) = bounds(paths)
  zero_x = -x + xoffset
  zero_y = -y + yoffset

  for path in paths:
    for i in range(0, xcount):
      row = []
      for j in range(0, ycount):
        _x = zero_x + i * (w + xpad)
        _y = zero_y + j * (h + ypad)
        row.append({'path':path.copy(),'x':_x, 'y':_y})
      g_paths.append(row)

  return g_paths

def draw_grid(grid=[]):
  """ draws provided grid to screen, expects output of make_grid
  """
  for row in grid:
    for item in row:
      _ctx.push()
      _ctx.translate(item['x'],item['y'])
      _ctx.drawpath(item['path'].copy())
      _ctx.pop()
      
  return
  
def get_nsine_width(width):
  """ return normalized theta coefficient based on canvas width for standard period
  """
  global SINE_PERIOD_DEG
  return 1 / (_ctx.WIDTH * width / SINE_PERIOD_DEG)

def get_nyzero(factor):
  """ return y-axis location
  """
  if not factor:
    return _ctx.HEIGHT
  return int(_ctx.HEIGHT*factor)

def get_namplitude(factor):
  """ return normalized amplitude based on canvas height
  """
  if not factor:
    return _ctx.HEIGHT
  return int(_ctx.HEIGHT * factor)

def draw_sine(amplitude=0, width=1, step=1, xzero=0, yzero=0, variation=True):
  """ creates discrete sine wave with given amplitude,
  half-period(degrees), and increment steps
  """
  global _palette
  yzero = get_nyzero(yzero)
  atheta = get_nsine_width(width)
  amplitude = get_namplitude(amplitude)
  for angle in range(step,int(SINE_PERIOD_DEG/atheta),step):
    x = angle + xzero
    h = amplitude * math.sin(atheta*math.radians(angle))
    _ctx.fill(random.choice(_palette))
    if variation:
      h = h * random.choice(range(80,100,5))/100
    y = yzero - h
    _ctx.rect(x, y, step, h)
  
  return

