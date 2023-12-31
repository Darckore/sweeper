#
# A board cell
#

from math import sqrt

#
# A cell on a board
#
class cell :
  def __init__(self, centre : tuple[float, float], points : list) :
    self.__points = points
    self.__centre = centre
    self.__neighbours = []
    self.__armed = False
    self.__visited = False
    self.__flagged = False
    self.__minesAround = None

  # interface

  def distance_to(self, dest) :
    scrCentre = self.centre()
    dstCentre = dest.centre()
    return sqrt((dstCentre[0] - scrCentre[0]) ** 2 +
                (dstCentre[1] - scrCentre[1]) ** 2)

  def arm(self) :
    self.__armed = True

  def is_armed(self) :
    return self.__armed

  def visit(self) :
    self.__visited = True

  def is_visited(self) :
    return self.__visited

  def flip_flag(self) :
    self.__flagged = not self.__flagged

  def has_flag(self) :
    return self.__flagged

  def points(self) :
    return self.__points

  def neighbours(self) :
    return self.__neighbours

  def centre(self) :
    return self.__centre

  def mines_around(self) :
    if not self.__minesAround is None :
      return self.__minesAround
    mineCount = 0
    for neighbour in self.__neighbours :
      if neighbour.is_armed() :
        mineCount += 1
    self.__minesAround = mineCount
    return mineCount

  def flags_around(self) :
    flagCount = 0
    for neighbour in self.__neighbours :
      if neighbour.has_flag() :
        flagCount += 1
    return flagCount
