#
# Game board
#

import pygame

from enum import Enum

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
      pygame.draw.line(canvas, (0,0,0), (x, 0), (x, self.dimensions[1]), 3)

    for row in range (0, self.rows + rect_field.cellSide) :
      y = row * rect_field.cellSide
      pygame.draw.line(canvas, (0,0,0), (0, y), (self.dimensions[0], y), 3)


#
# Handles game logic
#
class board :
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
    canvas.fill((128, 128, 128))
    self.minefield.draw(canvas)