#
# Game board
#

import pygame

from internal.boards import rect_field

#
# Handles game logic
#
class board :
  fillColour  = (128, 128, 128)
  boardColour = (0, 50, 50)
  lineColour  = (100, 100, 100)
  highlightColour = (0, 100, 30)
  neighboutHighlightColour = (0, 60, 30)

  def __init__(self) :
    self.minefield  = None
    self.activeCell = None
    self.cells = []

  # interface

  #
  # Inits a rectangular minefield
  #
  def make_rect(self, cols : int, rows : int) -> tuple[int, int] :
    self.minefield = rect_field(cols, rows)
    self.__init_cells()
    return self.minefield.dimensions

  #
  # Draws itself on the given surface
  #
  def draw(self, canvas : pygame.Surface) :
    canvas.fill(self.fillColour)
    if self.minefield == None :
      return
    
    self.minefield.draw(canvas, self.cells, self.boardColour, self.lineColour)
    self.__highlight_active(canvas)

  #
  # Highlights the cell the mouse is over
  #
  def highlight(self, pos : tuple[int, int]) :
    self.activeCell = self.minefield.cell_at(self.cells, pos[0], pos[1])

  # implementation

  def __init_cells(self) :
    self.cells = self.minefield.make_cells()

  def __highlight_active(self, canvas : pygame.Surface) :
    if self.activeCell == None :
      return
    self.minefield.draw_cell(canvas, self.activeCell, self.highlightColour, self.lineColour)
    for heighbour in self.activeCell.neighbours :
      self.minefield.draw_cell(canvas, heighbour, self.neighboutHighlightColour, self.lineColour)