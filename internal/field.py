#
# Game board
#

import pygame

#
# Rectangular minefield
#
class rect_field :
  cellSide = 50

  def __init__(self, cols : int, rows : int) :
    self.cols = cols
    self.rows = rows
    self.dimensions = (self.cols * rect_field.cellSide, self.rows * rect_field.cellSide)

  # interface

  def draw(self, canvas : pygame.Surface) :
    self.__draw_grid(canvas)

  # implementation

  def __draw_grid(self, canvas : pygame.Surface) :
    for col in range (0, self.cols + rect_field.cellSide) :
      x = col * rect_field.cellSide
      pygame.draw.line(canvas, board.lineColour, (x, 0), (x, self.dimensions[1]))

    for row in range (0, self.rows + rect_field.cellSide) :
      y = row * rect_field.cellSide
      pygame.draw.line(canvas, board.lineColour, (0, y), (self.dimensions[0], y))


#
# Handles game logic
#
class board :
  boardColour = (128, 128, 128)
  lineColour  = (100, 100, 100)

  def __init__(self) :
    self.minefield = None

  # interface

  #
  # Inits a rectangular minefield
  #
  def make_rect(self, cols : int, rows : int) -> tuple[int, int] :
    self.minefield = rect_field(cols, rows)
    return self.minefield.dimensions

  #
  # Draws itself on the given surface
  #
  def draw(self, canvas : pygame.Surface) :
    canvas.fill(board.boardColour)
    if self.minefield == None :
      return
    
    self.minefield.draw(canvas)