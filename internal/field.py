#
# Game board
#

import pygame

#
# Handles game logic
#
class board :
  def __init__(self, width : int, height : int) :
    self.width   = width
    self.height  = height
    self.columns = 0
    self.rows    = 0

  #
  # Sets the field mode, i.e. the number of cells and mines
  #
  def set_mode(self, cols : int, rows : int) :
    self.columns = cols
    self.rows = rows

  #
  # Draws itself on the given surface
  #
  def draw(self, canvas : pygame.Surface) :
    canvas.fill((0, 128, 0))
    pygame.draw.circle(canvas, (200, 200, 200), (200, 300), 100)