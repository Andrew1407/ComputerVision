from graphics import Polygon, Point


parse_hex = lambda color: tuple(int(d, 16) for d in (color[1:3], color[3:5], color[5:]))
stringify_hex = lambda container: '#%02x%02x%02x' % container

def define_drawing_layers(points: tuple[Point, ...]) -> tuple[tuple[Polygon, ...], ...]:
  fill_bkg = __define_fill_bkg(points)
  carcass = __define_carcass(points)
  layers = (fill_bkg, carcass)
  return tuple(__polygon_mapper(l) for l in layers)


def figure_cleanup(layers: tuple[tuple[Polygon, ...], ...]):
  for l in layers:
    for p in l: p.undraw()


__polygon_mapper = lambda container: tuple(Polygon(*ps) for ps in container)

def __define_fill_bkg(points: tuple[Point, ...]) -> tuple[tuple[Point, ...], ...]:
  a, b, c, d = points
  bkg_components = (a, b, c), (a, c, d), (a, b, d), (b, c, d)
  return bkg_components


def __define_carcass(points: tuple[Point, ...]) -> tuple[tuple[Point, ...], ...]:
  a, b, c, d = points
  carcass = a, d, b, a, c, d, b, c
  return (carcass,)
