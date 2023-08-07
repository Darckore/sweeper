#
# Game board
#

import pygame

#
# A cell on a board
#
class cell :
  def __init__(self, centre : tuple[float, float], points : list) :
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
    self.__maxIdx = cols * rows
    self.dimensions = (self.cols * rect_field.cellSide, self.rows * rect_field.cellSide)

  # interface

  #
  # Inits the required number of cells
  #
  def make_cells(self) -> list[cell] :
    cells = []
    for row in range (0, self.rows) :
      top = row * self.cellSide
      shiftedRow = top + self.cellSide
      for col in range (0, self.cols) :
        left = col * self.cellSide
        shiftedCol = left + self.cellSide
        cells.append(cell((left + self.cellSide / 2, top + self.cellSide / 2),
          [
            (left, top),
            (shiftedCol, top),
            (left, shiftedRow),
            (shiftedCol, shiftedRow)
          ]))

    return self.__init_neighbours(cells)

  #
  # Draws the rectangular board
  #
  def draw(self, canvas : pygame.Surface, cells : list[cell],
                 boardColour : tuple[int, int, int], lineColour: tuple[int, int, int]) :
    for cell in cells :
      rect = pygame.Rect(cell.points[0][0], cell.points[0][1], self.cellSide, self.cellSide)
      pygame.draw.rect(canvas, boardColour, rect)
      pygame.draw.rect(canvas, lineColour, rect, 2)

  # implementation

  def __cell_at(self, cells : list[cell], col : int, row : int) -> cell :
    if row < 0 or col < 0 or row >= self.rows or col >= self.cols :
      return None
    idx = row * self.cols + col
    if idx < 0 or idx >= self.__maxIdx :
      return None
    return cells[idx]

  def __init_neighbours(self, cells : list[cell]) -> list[cell]:
    for cell in cells :
      col = int(cell.points[0][0] / self.cellSide)
      row = int(cell.points[0][1] / self.cellSide)
      for y in range (-1, 2) :
        for x in range (-1, 2) :
          if x == 0 and y == 0 :
            continue
          neighbour = self.__cell_at(cells, col + x, row + y)
          if neighbour != None :
            cell.neighbours.append(neighbour)

    return cells


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
    self.__init_cells()
    return self.minefield.dimensions

  #
  # Draws itself on the given surface
  #
  def draw(self, canvas : pygame.Surface) :
    canvas.fill(board.boardColour)
    if self.minefield == None :
      return
    
    self.minefield.draw(canvas, self.cells, self.boardColour, self.lineColour)

  #
  # Highlights the cell the mouse is over
  #
  def highlight(self, canvas : pygame.Surface, pos : tuple[int, int]) :
    pass

  # implementation

  def __init_cells(self) :
    self.cells = self.minefield.make_cells()