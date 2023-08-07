#
# Game board
#

import pygame
import random

from internal.cell import cell
from internal.boards import rect_field
from internal.spritesheet import strip

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
    self.__minefield  = None
    self.__activeCell = None
    self.__cells = []
    self.__mouseBtns = (False, False, False)
    self.__going = False
    self.__mineCount = 0
    self.__sprites = None

  # interface

  #
  # Sets a spritesheet with number images
  #
  def attach_sprites(self, sprites : strip) :
    self.__sprites = sprites

  #
  # Inits a rectangular minefield
  #
  def make_rect(self, cols : int, rows : int, mines : int) -> tuple[int, int] :
    self.__mineCount = mines
    self.__minefield = rect_field(cols, rows)
    self.__init_cells()
    return self.__minefield.dimensions()

  #
  # Draws itself on the given surface
  #
  def draw(self, canvas : pygame.Surface) :
    canvas.fill(self.fillColour)
    minefield = self.__minefield
    if minefield is None :
      return

    for cell in self.__cells :
      minefield.draw_cell(canvas, cell, self.boardColour, self.lineColour)

    self.__highlight_active(canvas)

  #
  # Activates the cell the mouse is over
  #
  def make_active(self, pos : tuple[int, int]) :
    self.__activeCell = self.__minefield.cell_at(self.__cells, pos[0], pos[1])

  #
  # Stores mouse button state for later
  #
  def store_btns(self, btns : tuple[bool, bool, bool]) :
    self.__mouseBtns = btns

  #
  # Handles the click. This reacts to mouseup events
  #
  def on_click(self, canvas : pygame.Surface, btns : tuple[bool, bool, bool]) :
    if self.__activeCell is None :
      return

    if self.__released(0, btns) :
      self.__place_mines()
      self.__left_click(canvas)
    elif self.__released(1, btns) :
      pass
    elif self.__released(2, btns) :
      pass

    self.store_btns(btns)

  # implementation

  def __released(self, btn : int, btns : tuple[bool, bool, bool]) -> bool :
    prevState = self.__mouseBtns[btn]
    return prevState and prevState != btns[btn]


  def __place_mines(self) :
    totalCells = len(self.__cells)
    if totalCells == 0 or totalCells < self.__mineCount :
      return

    if self.__going or self.__activeCell is None :
      return

    minesLeft = self.__mineCount
    while minesLeft > 0 :
      rndIdx = random.randint(0, totalCells - 1)
      selectedCell = self.__cells[rndIdx]
      if selectedCell == self.__activeCell :
        continue
      if selectedCell.is_armed() :
        continue
      selectedCell.arm()
      minesLeft -= 1


  def __open_cell(self, canvas : pygame.Surface, target : cell) :
    if target.is_armed() :
      pass # todo : fail


  def __left_click(self, canvas : pygame.Surface) :
    if self.__activeCell is None :
      return
    self.__open_cell(canvas, self.__activeCell)


  def __init_cells(self) :
    self.__cells = self.__minefield.make_cells()


  def __highlight_active(self, canvas : pygame.Surface) :
    if self.__activeCell is None :
      return
    self.__minefield.draw_cell(canvas, self.__activeCell, self.highlightColour, self.lineColour)
    for heighbour in self.__activeCell.neighbours() :
      self.__minefield.draw_cell(canvas, heighbour, self.neighboutHighlightColour, self.lineColour)