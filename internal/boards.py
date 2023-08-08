#
# A collection of game boards and impl-level stuff
#

import pygame

from internal.cell import cell

#
# Rectangular minefield
#
class rect_field :
  cellSide = 30

  def __init__(self, cols : int, rows : int) :
    self.__cols = cols
    self.__rows = rows
    self.__maxIdx = cols * rows
    self.__dimensions = (self.__cols * rect_field.cellSide, self.__rows * rect_field.cellSide)

  # interface

  #
  # Returns the fitting canvas size
  #
  def dimensions(self) :
    return self.__dimensions

  #
  # Inits the required number of cells
  #
  def make_cells(self) -> list[cell] :
    cells = []
    for row in range (0, self.__rows) :
      top = row * self.cellSide
      shiftedRow = top + self.cellSide
      for col in range (0, self.__cols) :
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
  # Draws a single cell
  #
  def draw_cell(self, canvas : pygame.Surface, cell : cell,
                boardColour : tuple[int, int, int], lineColour: tuple[int, int, int]) :
    rect = pygame.Rect(cell.points()[0][0], cell.points()[0][1], self.cellSide, self.cellSide)
    pygame.draw.rect(canvas, boardColour, rect)
    pygame.draw.rect(canvas, lineColour, rect, 2)

  #
  # Gets the cell at the specified coordinates
  #
  def cell_at(self, cells : list[cell], col : int, row : int) -> cell :
    x = int(col / self.cellSide)
    y = int(row / self.cellSide)
    return self.__cell_at(cells, x, y)

  #
  # Gets a rect for the given cell
  #
  def get_rect(self, cell : cell) -> pygame.Rect :
    points = cell.points()
    return pygame.Rect(points[0][0], points[0][1], self.cellSide, self.cellSide)

  # implementation

  def __cell_at(self, cells : list[cell], col : int, row : int) -> cell :
    if row < 0 or col < 0 or row >= self.__rows or col >= self.__cols :
      return None
    idx = row * self.__cols + col
    if idx < 0 or idx >= self.__maxIdx :
      return None
    return cells[idx]

  def __init_neighbours(self, cells : list[cell]) -> list[cell]:
    for cell in cells :
      col = int(cell.points()[0][0] / self.cellSide)
      row = int(cell.points()[0][1] / self.cellSide)
      for y in range (-1, 2) :
        for x in range (-1, 2) :
          if x == 0 and y == 0 :
            continue
          neighbour = self.__cell_at(cells, col + x, row + y)
          if not neighbour is None :
            cell.neighbours().append(neighbour)

    return cells
