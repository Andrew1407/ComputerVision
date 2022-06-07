def get_contour_lines(intersections):
  pairs = list()
  for p1 in intersections:
    for p2 in intersections:
      if p1 is p2: continue
      if p1[1] == p2[1]:
        pair = (p1, p2)
        if not __pair_exists(pairs, (p2, p1)):
          pairs.append(pair)
  return pairs


def __pair_exists(arr, pair):
  for p in arr:
    if p == pair: return True
  return False
