from dataclasses import dataclass
from graphics import *
import numpy as np


@dataclass
class FaceContainer:
  """ Contains face points, its plane normal vector and figue center coords. """
  edges: np.ndarray
  normal: np.ndarray
  center: np.ndarray


@dataclass
class PlaneParams:
  """ Container for projection axis params. """
  position: int
  coords: tuple[float, float]


def parser (values: np.ndarray, coords: tuple[float, ...]) -> tuple[tuple[float, ...], ...]:
  """ Parses nupmy arrays as tuples with neccessary coords only """
  parsed = list()
  for row in values:
    parsed.append(tuple(row[i] for i in coords))
  return tuple(parsed)


PLANES_TRANSFORMS: dict[str, PlaneParams] = dict(
  xy = PlaneParams(position=2, coords=(0, 1)),
  xz = PlaneParams(position=1, coords=(0, 2)),
  yz = PlaneParams(position=0, coords=(2, 1)),
)

def orthogonal_projection(figure: np.ndarray, plane: str = 'xy', parse: bool = False):
  """
    Perrforms projection for each point in matrix
    (figure) to the passed axis with optional parsing.
  """
  projection_mtx = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
  ])
  params = PLANES_TRANSFORMS[plane]
  projection_mtx[params.position, params.position] = 0
  result = np.round(figure.dot(projection_mtx), decimals=2)
  return parser(result, params.coords) if parse else result


def calc_shape_center(points):
  """ Calculates the center of points for each axis. """
  center_fn = lambda axis: sum(p[axis] for p in points) / len(points)
  return np.array([round(center_fn(i), 2) for i in range(len(points[0]))])


def mk_faces_containers(edges_container) -> list[FaceContainer]:
  """
    Takes edges witj approximate plane normal direction
    (in case of opposite direction of result normal)
    and returns boxed faces values containing the given points with
    its face (plane) normal and center point.
  """
  result = list()
  unit = lambda vec: vec / np.linalg.norm(vec)

  for edges, direction in edges_container:
    center = calc_shape_center(edges)
    [p1, p2] = edges[:2]
    v1 = center - p1
    v2 = center - p2
    normal = unit(np.cross(v1, v2))
    angle = np.dot(direction, normal)
    angle = np.arccos(angle)
    # check for vector opposite direction case (direction inside figure instead of outside)
    if angle >= 90: normal *= -1
    result.append(FaceContainer(edges, normal, center))

  return result


def group_faces(face_containers: list[FaceContainer], view_point = [0, 0, 0]):
  """
    Categorizes given faces as visible and hidden ones
    checking an angle between viewpoint vector and its normal
    (by default view_point = [0, 0, 0]); returns tuple of the groups.
  """
  visible = list()
  hidden = list()
  for c in face_containers:
    n = c.normal
    l = view_point - c.center
    dot = np.dot(l, n)
    container = hidden if dot < 0 else visible
    container.append(c.edges)
  return visible, hidden


def define_hidden_edges(faces):
  """
    Searches hidden egdes among hidden faces by checking
    two common points in two hidden faces that are not visible
    and groups them as an egde.
  """
  edges = list()
  f_len = len(faces)
  for i in range(f_len):
    if i == (len(faces) - 1): break
    face_i = faces[i]

    for u in range(i + 1, f_len):
      face_u = faces[u]
      points = list()
      for p1 in face_i:
        for p2 in face_u:
          if p1 is p2: points.append(p1)

      if len(points) == 2:
        edges.append(tuple(points))

  return edges


def draw_figue(faces):
  """ Draws given visible faces in the graphics window. """
  width, height = 800, 800
  title = 'Visible faces'
  bkg_color = 'yellow'
  fill_color = 'aqua'

  faces_arr = tuple(np.array([[*p, 1] for p in ps]) for ps in faces)
  projected = tuple(orthogonal_projection(points, plane='xy', parse=True) for points in faces_arr)
  wnd = GraphWin(title, width, height)
  wnd.setBackground(bkg_color)
  for points in projected:
    pl = Polygon([Point(p[0], p[1]) for p in points])
    pl.setFill(fill_color)
    pl.setWidth(3)
    pl.draw(wnd)
  wnd.getMouse()
  wnd.close()


if __name__ == '__main__':
  # initializing square pyramid points where
  # a, b, c, d - square base
  # e - pyramid top
  a = np.array([200, 470, 10])
  b = np.array([230, 450, 100])
  c = np.array([450, 450, 100])
  d = np.array([400, 470, 10])
  e = np.array([300, 300, 60])

  # initializing a tuple of pyramid faces
  # with approximate outside normal direction
  # for the Roberts algorithm (normals should have
  # direction out of figure)
  faces_with_norm_direction = (
    ((a, b, c, d), [0, 1, 0]),
    ((a, b, e), [-1, 0, 0]),
    ((b, c, e), [0, 0, 1]),
    ((c, d, e), [1, 0, 0]),
    ((a, d, e), [0, 0, -1]),
  )

  faces_containers = mk_faces_containers(faces_with_norm_direction)
  f_visible, f_hidden = group_faces(faces_containers)
  print('Hidden faces:')
  for f in f_hidden: print(f)
  hidden_edges = define_hidden_edges(f_hidden)
  print('\nHidden edges:')
  for e in hidden_edges: print(e)
  draw_figue(f_visible)
