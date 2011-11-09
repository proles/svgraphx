"""
__init__.py

Created by Andres Bastidas on 2011-11-07.
"""

def bounds(paths=[]):
  """ Returns (x,y), (width, height) bounds for a group of paths
	- originally provided as sample at
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

def make_grid(paths=[],xoffset=0,yoffset=0,xcount=1,ycount=1,xpad=0,ypad=0):
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
