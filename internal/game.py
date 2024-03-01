#
# Game entry point
#

import pygame

from internal.field import board
from internal.spritesheet import strip

#
# Inits things and runs the main loop
#
class sweeper :
  captionBase = 'Derpsweeper'

  def __init__(self) :
    initialSize = (500, 500)
    self.__board = board(self.captionBase)
    self.__canvas = self.__initial_setup(initialSize)
    self.__sprites = None
    self.__endSprites = None
    self.__restart = False

  # interface

  #
  # Runs the main loop
  #
  def run(self) :
    self.__new_game()
    self.__load_res()
    self.__board.attach_sprites(self.__sprites)
    while self.__poll_events() :
      self.__present()

  #
  # I'm outta here
  #
  def shutdown(self) :
    pygame.quit()

  # implementation

  #
  # Inits the field for the new game
  #
  def __new_game(self) :
    canvasSz = self.__board.make_rect(32, 18, 100)
    self.__canvas = self.__set_canvas_size(canvasSz)

  #
  # Loads resources
  #
  def __load_res(self) :
    self.__sprites = strip(64, 64, 'assets/field_sprites.png')
    self.__endSprites = strip(256, 256, 'assets/win_fail.png')

  #
  # Inits the window and returns the resulting surface
  #
  def __initial_setup(self, params : tuple[int, int]) :
    pygame.init()
    pygame.display.set_caption(self.captionBase)
    return self.__set_canvas_size(params)
  
  #
  # Sets the display size and returns the resulting surface
  #
  def __set_canvas_size(self, size : tuple[int, int]) :
    return pygame.display.set_mode(size)

  #
  # Listens to events and dispatches them
  #
  def __poll_events(self) :
    board = self.__board
    for evt in pygame.event.get() :
      if evt.type == pygame.QUIT :
        return False

      clicked = False
      if evt.type == pygame.MOUSEMOTION :
        board.make_active(pygame.mouse.get_pos())
      elif evt.type == pygame.MOUSEBUTTONDOWN :
        board.make_active(pygame.mouse.get_pos())
        board.store_btns(pygame.mouse.get_pressed())
      elif evt.type == pygame.MOUSEBUTTONUP :
        board.make_active(pygame.mouse.get_pos())
        board.on_click(pygame.mouse.get_pressed())
        clicked = True

      if clicked and self.__restart :
        self.__new_game()
        self.__restart = False

    board.ping()
    if board.failed() or board.won() :
      self.__restart = True

    return True

  #
  # Draws an overlayed image
  #
  def __overlay(self, img : pygame.Surface) :
    canvas = self.__canvas
    canvasCX = canvas.get_width() / 2
    canvasCY = canvas.get_height() / 2
    imgCX = img.get_width() / 2
    imgCY = img.get_height() / 2
    canvas.blit(img, (canvasCX - imgCX, canvasCY - imgCY))


  #
  # Draws the board
  #
  def __present(self) :
    board = self.__board
    board.draw(self.__canvas)

    if board.won() :
      self.__overlay(self.__endSprites.image_at(0))
    elif board.failed() :
      self.__overlay(self.__endSprites.image_at(1))

    pygame.display.flip()