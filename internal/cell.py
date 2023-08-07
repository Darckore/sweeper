#
# A board cell
#

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

  # interface

  def arm(self) :
    self.__armed = True

  def is_armed(self) :
    return self.__armed

  def visit(self) :
    self.__visited = True

  def is_visited(self) :
    return self.__visited

  def points(self) :
    return self.__points

  def neighbours(self) :
    return self.__neighbours

  def centre(self) :
    return self.__centre

  def mines_around(self) :
    mineCount = 0
    for neighbour in self.__neighbours :
      if neighbour.is_armed() :
        mineCount += 1
    return mineCount