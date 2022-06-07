from dataclasses import dataclass
from OpenGL.GL import *
from OpenGL.GLUT import *
from hollow_cylinder import hollow_cylinder


@dataclass
class ObjPosition:
  x: float = 0
  y: float = 0
  z: float = 0
  rotation: float = 0

  def astuple(self, coords_only: bool = True) -> tuple[float, ...]:
    coords = (self.x, self.y, self.z)
    return coords if coords_only else (self.rotation, *coords)


@dataclass
class BearingShape:
  radius_1: float = 0
  radius_2: float = 0
  radius_3: float = 0
  radius_4: float = 0
  width_1: float = 0
  width_2: float = 0


class Bearing:
  def __init__(
    self,
    shape_colors,
    bkg_color=(1, 1, 1, 1),
    rotation=ObjPosition(),
    position=ObjPosition(),
    light_position=ObjPosition(),
    shape_params=BearingShape()
  ):
    self.__rotation = rotation
    self.__position = position
    self.__shape_colors = shape_colors
    self.__light_position = light_position
    self.__shape_params = shape_params
    self.__bkg_color = bkg_color
    self.__obj_container = None


  def setup(self):
    light_pos = self.__light_position.astuple(coords_only=False)
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glClearColor(*self.__bkg_color)
    self.__obj_container = glGenLists(1)
    glNewList(self.__obj_container, GL_COMPILE)
    self.__draw_components()    
    glEndList()
    glEnable(GL_NORMALIZE)

  
  def draw(self):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    self.__move_obj()
    glCallList(self.__obj_container)
    glPopMatrix()
    glutSwapBuffers()
    glutPostRedisplay()


  def reshape(self, width, height):
    h = height / width
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1.0, 1.0, -h, h, 5.0, 60.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -40.0)


  def __draw_components(self):
    shape = self.__shape_params
    color1, color2 = self.__shape_colors
    cylinders = [
      dict(r1=shape.radius_1, r2=shape.radius_2, width=shape.width_1, color=color1),
      dict(r1=shape.radius_2, r2=shape.radius_3, width=shape.width_2, color=color2),
      dict(r1=shape.radius_3, r2=shape.radius_4, width=shape.width_1, color=color1),
    ]
    for args in cylinders: hollow_cylinder(**args)


  def __move_obj(self):
    move_angle = 3
    move_y_position = -0.1
    rotation = self.__rotation.astuple(coords_only=False)
    glTranslatef(*self.__position.astuple())
    glRotatef(*rotation)
    self.__rotation.rotation += move_angle
    self.__position.y += move_y_position
    if self.__rotation.rotation > 360:
      self.__rotation.rotation = 0
    if self.__position.y < -13:
      self.__position.y = 15
