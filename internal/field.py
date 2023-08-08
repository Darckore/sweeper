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
  flagImageIdx = 8
  bombImageIdx = 9
  okImageIdx   = 10
  failImageIdx = 11

  fillColour  = (128, 128, 128)
  boardColour = (0, 50, 50)
  lineColour  = (100, 100, 100)
  highlightColour = (0, 100, 30)
  neighboutHighlightColour = (0, 60, 30)
  detonatedBombColour = (255, 0, 0)

  def __reset(self) :
    self.__minefield  = None
    self.__activeCell = None
    self.__cells = []
    self.__mouseBtns = (False, False, False)
    self.__going = False
    self.__boom  = False
    self.__won   = False
    self.__cellsLeft = 0
    self.__mineCount = 0
    self.__minesLeft = 0
    self.__minesLeftPrev = 0
    self.__sprites = None

  def __init__(self, baseCaption) :
    self.__reset()
    self.__baseCaption = baseCaption

  # interface

  #
  # Called every frame after dispatching all the events
  #
  def ping(self) :
    if self.__game_done() :
      return
    if not self.__game_done() and self.__minesLeft != self.__minesLeftPrev :
      gameCaption = '{} - {} mines left'.format(self.__baseCaption, self.__minesLeft)
      pygame.display.set_caption(gameCaption)
      self.__minesLeftPrev = self.__minesLeft
    if self.__cellsLeft == self.__mineCount :
      self.__win()

  #
  # Sets a spritesheet with number images
  #
  def attach_sprites(self, sprites : strip) :
    self.__sprites = sprites

  #
  # Inits a rectangular minefield
  #
  def make_rect(self, cols : int, rows : int, mines : int) -> tuple[int, int] :
    self.__reset()
    self.__mineCount = mines
    self.__minesLeft = mines
    self.__cellsLeft = cols * rows
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
      if not cell.is_visited() :
        minefield.draw_cell(canvas, cell, self.boardColour, self.lineColour)
        self.__draw_flag(canvas, cell)
      else :
        if not cell.is_armed() :
          minefield.draw_cell(canvas, cell, self.fillColour, self.lineColour)
        else :
          minefield.draw_cell(canvas, cell, self.detonatedBombColour, self.lineColour)
        self.__draw_mine_count(canvas, cell)

    self.__highlight_active(canvas)
    if self.__game_done() :
      for cell in self.__cells :
        self.__draw_mine(canvas, cell)

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
  def on_click(self, btns : tuple[bool, bool, bool]) :
    if self.__activeCell is None :
      return

    if self.__released(0, btns) :
      self.__place_mines()
      self.__left_click()
    elif self.__released(1, btns) :
      self.__middle_click()
    elif self.__released(2, btns) :
      self.__right_click()

    self.store_btns(btns)

  #
  # Is the game failed?
  #
  def failed(self) :
    return self.__boom

  #
  # Is the game won?
  #
  def won(self) :
    return self.__won

  # implementation

  def __game_done(self) :
    return self.__boom or self.__won

  def __released(self, btn : int, btns : tuple[bool, bool, bool]) -> bool :
    prevState = self.__mouseBtns[btn]
    return prevState and prevState != btns[btn]

  def __place_mines(self) :
    if self.__game_done() :
      return

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
    self.__going = True

  def __win(self) :
    pygame.display.set_caption("{} - WIN".format(self.__baseCaption))
    self.__won = True

  def __go_boom(self) :
    pygame.display.set_caption("{} - FAIL".format(self.__baseCaption))
    self.__boom  = True

  def __visit_cell(self, cell : cell) :
    if cell.is_visited() :
      return
    cell.visit()
    self.__cellsLeft -= 1

  def __expand_neighbours(self, target : cell, goBoom : bool) :
    for neighbour in target.neighbours() :
      if not neighbour.is_armed() and neighbour.mines_around() == 0 :
        self.__open_cell(neighbour)
        continue
      if neighbour.is_armed() :
        if not goBoom or neighbour.has_flag() :
          continue
        self.__visit_cell(neighbour)
        self.__go_boom()
      if neighbour.has_flag() :
        continue
      self.__visit_cell(neighbour)

  def __open_cell(self, target : cell) :
    if target.is_visited() :
      return

    self.__visit_cell(target)
    if target.is_armed() :
      self.__go_boom()
      return

    if target.mines_around() != 0 :
      return
    self.__expand_neighbours(target, False)

  def __left_click(self) :
    actCell = self.__activeCell
    if actCell is None or self.__game_done() :
      return
    if actCell.has_flag() :
      return
    self.__open_cell(actCell)

  def __middle_click(self) :
    actCell = self.__activeCell
    if actCell is None or self.__game_done() :
      return
    if not actCell.is_visited() :
      return
    if actCell.flags_around() != actCell.mines_around() :
      return
    self.__expand_neighbours(actCell, True)

  def __right_click(self) :
    actCell = self.__activeCell
    if actCell is None or self.__game_done() :
      return
    if actCell.is_visited() :
      self.__middle_click()
      return
    actCell.flip_flag()
    if actCell.has_flag() :
      self.__minesLeft -= 1
    else :
      self.__minesLeft += 1

  def __init_cells(self) :
    self.__cells = self.__minefield.make_cells()

  def __draw_image_at_index(self, canvas : pygame.Surface, idx : int, target : pygame.Rect) :
    img = self.__sprites.image_at(idx)
    img = pygame.transform.scale(img, (target.width, target.height))
    canvas.blit(img, target)

  def __draw_mine(self, canvas : pygame.Surface, curCell : cell) :
    armed = curCell.is_armed()
    flagged = curCell.has_flag()
    if not (armed or flagged) :
      return
    if not flagged :
      self.__draw_image_at_index(canvas, self.bombImageIdx, self.__minefield.get_rect(curCell))
    elif not armed :
      self.__draw_image_at_index(canvas, self.failImageIdx, self.__minefield.get_rect(curCell))
    else :
      self.__draw_image_at_index(canvas, self.okImageIdx, self.__minefield.get_rect(curCell))

  def __draw_mine_count(self, canvas : pygame.Surface, curCell : cell) :
    if curCell.is_armed() :
      return
    mineCount = curCell.mines_around()
    if mineCount == 0 :
      return
    self.__draw_image_at_index(canvas, mineCount - 1, self.__minefield.get_rect(curCell))

  def __draw_flag(self, canvas : pygame.Surface, target : cell) :
    if not target.has_flag() :
      return
    self.__draw_image_at_index(canvas, self.flagImageIdx, self.__minefield.get_rect(target))

  def __highlight_active(self, canvas : pygame.Surface) :
    actCell = self.__activeCell
    if actCell is None :
      return
    if not actCell.is_visited() :
      self.__minefield.draw_cell(canvas, actCell, self.highlightColour, self.lineColour)
      self.__draw_flag(canvas, actCell)
    
    for neighbour in actCell.neighbours() :
      if neighbour.is_visited() :
        continue
      self.__minefield.draw_cell(canvas, neighbour, self.neighboutHighlightColour, self.lineColour)
      self.__draw_flag(canvas, neighbour)