import numpy as np


def painter_algorithm(edges, viewpoint=(0, 0, 0)):
  view_coord = np.array(viewpoint)    
  sorted_edges = sorted(edges, key=lambda p: __point_plane_dist(view_coord, p), reverse=True)
  return sorted_edges


def __point_plane_dist(point, plane):
  p1, p2, p3 = tuple(np.array(p) for p in plane)
  u = p2 - p1
  v = p3 - p1
  n = np.cross(u, v)
  nn = n / np.linalg.norm(n)
  p = point - p1
  return np.dot(p, nn)
