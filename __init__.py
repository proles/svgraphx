"""
__init__.py

Created by Andres Bastidas on 2011-11-07.
"""
import math
import random
from nodebox.graphics import Context
_ctx = Context
_palette = []
_tilt_range = []
_round_range = []
SINE_PERIOD_DEG = 180.0
ATAN_PERIOD_DEG = 90.0

def init():
  set_tilt_range()
  set_round_range()

def set_palette(palette):
  """ set color palette
  """
  global _palette
  _palette = palette
  return
  
def set_tilt_range(tilt_range=range(-2,2,1)):
  """ set tilt range
  """
  global _tilt_range
  _tilt_range = tilt_range
  return

def set_round_range(round_range=range(0,5,1)):
  global _round_range
  _round_range = make_fractional(round_range)
  return

def make_fractional(contents, denominator = 10.0):
  """
  helper function to get franctional ranges
  """
  return map(lambda x: x/denominator, contents)

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
  return (-x,-y), (w,h)

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

def get_natan_width(width):
  """ return normalized theta coefficient based on canvas width for standard period
  """
  global ATAN_PERIOD_DEG
  return 1 / (_ctx.WIDTH * width / ATAN_PERIOD_DEG)

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

def draw_sine(amplitude=0, width=1, step=1, xzero=0, yzero=0, variation=True,tilt=False,roundness=True):
  """ creates discrete sine wave with given amplitude,
  half-period(degrees), and increment steps
  """
  global _palette
  global _tilt_range
  global _round_range
  yzero = get_nyzero(yzero)
  atheta = get_nsine_width(width)
  namplitude = get_namplitude(amplitude)
  _ctx.push()
  if tilt:
    _ctx.rotate(random.choice(_tilt_range))
  for angle in range(step,int(SINE_PERIOD_DEG/atheta),step):
    x = angle + xzero
    h = namplitude * math.sin(atheta*math.radians(angle))
    clr = random.choice(_palette)
    clr.a = 1.0 - amplitude
    _ctx.fill(_ctx.color(clr.r, clr.g, clr.b, clr.a))
    if variation:
      h = h * random.choice(range(80,100,5))/100
    y = yzero - h
    if roundness:
      radius = random.choice(_round_range)
    _ctx.rect(x, y, step, h, radius)
  _ctx.pop()
  return

def plane_path(amplitude=1, scale=1, width=1, xzero=0, yzero=0, endstep=100,plane=None,clr=None):
  """ draw plane paths using log()
  """
  yzero = get_nyzero(yzero)
  xzero = xzero * _ctx.WIDTH
  width = _ctx.WIDTH * width
  amplitude = amplitude * _ctx.HEIGHT
  #p1
  p1a = random.choice(make_fractional(range(1,3)))
  p1x = width * p1a + xzero
  p1y = _ctx.HEIGHT - amplitude * math.log(p1x) / math.log(width)
  #p2
  p2a = random.choice(make_fractional(range(3,7)))
  p2x = width * p2a + xzero
  p2y = _ctx.HEIGHT - amplitude * math.log(p2x) / math.log(width)
  
  print 'width: ' + str(width)
  print 'p1a: ' + str(p1a)
  print 'p1x: ' + str(p1x)
  print 'p1y: ' + str(p1y)
  print 'p2a: ' + str(p2a)
  print 'p2x: ' + str(p2x)
  print 'p2y: ' + str(p2y)

  _ctx.nofill()
  _ctx.beginpath(xzero, yzero)
  _ctx.curveto(p1x, p1y, p2x, p2y, width, p2y)
  _ctx.endpath()
  
  if plane:
    _ctx.push()
    (resetx, resety), (w, h) = zero_translate(plane)
    if clr:
      _ctx.fill(clr)
    _ctx.translate(resetx,resety)
    _ctx.translate(width,p2y-h*0.6)
    _ctx.rotate(math.degrees(math.atan((p2y-p1y)/(p2x-p1x)))-15)
    _ctx.scale(scale)
    for path in plane:
      _ctx.drawpath(path.copy())
    _ctx.pop()

  return

def draw_clouds():
  """ draw clouds using union sample from 
  http://nodebox.net/code/index.php/Compound_paths
  """
  compound = None
  for i in range(50):
      r = random.choice(range(350))
      path = _ctx.oval(random.choice(range(_ctx.WIDTH)), random.choice(range(_ctx.HEIGHT)), r, r, draw=False)
      if not compound:
          compound = path
      compound = compound.union(path)
  _ctx.drawpath(compound)
  return

def draw_globe(x,y,w,h,a=1.0):
  """ draw globe with params as fraction of canvas HEIGHT, WIDTH
  """
  global _palette
  clr = random.choice(_palette)
  clr.a = a
  _ctx.fill(_ctx.color(clr.r, clr.g, clr.b, clr.a))
  _ctx.oval(x*_ctx.WIDTH, y*_ctx.HEIGHT, w*_ctx.WIDTH, h*_ctx.HEIGHT, True)
  return