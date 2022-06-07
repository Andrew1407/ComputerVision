from OpenGL.GLUT import *
import sys
from bearing import Bearing, BearingShape, ObjPosition


WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
POSITION_WIDTH, POSITION_HEIGHT = 600, 300

SKY_BLUE = (102 / 255, 178 / 255, 1, 1)
GREY_1 = (80 / 255, 80 / 255, 80 / 255, 1)
GREY_2 = (127 / 255, 127 / 255, 127 / 255, 1)

def mk_bearing():
  shape = BearingShape(
    radius_1=1,
    radius_2=1.5,
    radius_3=3,
    radius_4=4,
    width_1=3,
    width_2=2
  )
  return Bearing(
    rotation=ObjPosition(x=1, y=1, z=0),
    position=ObjPosition(y=15),
    bkg_color=SKY_BLUE,
    light_position=ObjPosition(rotation=5, x=5, y=10, z=0),
    shape_colors=(GREY_1, GREY_2),
    shape_params=shape
  )

if __name__ == '__main__':
  bearing = mk_bearing()
  glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
  glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
  glutInitWindowPosition(POSITION_WIDTH, POSITION_HEIGHT)
  glutInit(sys.argv)
  glutCreateWindow(b"Bearing conveyor")
  bearing.setup()
  glutDisplayFunc(bearing.draw)
  glutReshapeFunc(bearing.reshape)
  glutMainLoop()
