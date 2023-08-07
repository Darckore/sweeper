#
# Game board
#

import pygame

#
# A cell on a board
#
class cell :
  def __init__(self, centre : tuple[int, int], points : list) :
    self.points = points
    self.centre = centre
    self.neighbours = []


#
# Rectangular minefield
#
class rect_field :
  cellSide = 30

  def __init__(self, cols : int, rows : int) :
    self.cols = cols
    self.rows = rows
    self.dimensions = (self.cols * rect_field.cellSide, self.rows * rect_field.cellSide)

  # interface

  def make_cells(self) -> list :
    cells = []
    for row in range (0, self.rows) :
      top = row * self.cellSide
      shiftedRow = top + self.cellSide
      for col in range (0, self.cols) :
        left = col * self.cellSide
        shiftedCol = left + self.cellSide
        cells.append(cell((left + shiftedCol / 2, top + shiftedRow / 2),
          [
            (left, top),
            (shiftedCol, top),
            (left, shiftedRow),
            (shiftedCol, shiftedRow)
          ]))

    return cells

  def draw(self, canvas : pygame.Surface, cells : list[cell],
                 boardColour : tuple[int, int, int], lineColour: tuple[int, int, int]) :
    for cell in cells :
      rect = pygame.Rect(cell.points[0][0], cell.points[0][1], self.cellSide, self.cellSide)
      pygame.draw.rect(canvas, boardColour, rect)
      pygame.draw.rect(canvas, lineColour, rect, 2)


#
# Handles game logic
#
class board :
  boardColour = (0, 50, 50)
  lineColour  = (100, 100, 100)

  def __init__(self) :
    self.minefield = None
    self.cells = []

  # interface

  #
  # Inits a rectangular minefield
  #
  def make_rect(self, cols : int, rows : int) -> tuple[int, int] :
    self.minefield = rect_field(cols, rows)
    self.cells = self.minefield.make_cells()
    return self.minefield.dimensions

  #
  # Draws itself on the given surface
  #
  def draw(self, canvas : pygame.Surface) :
    canvas.fill(board.boardColour)
    if self.minefield == None :
      return
    
    self.minefield.draw(canvas, self.cells, self.boardColour, self.lineColour)