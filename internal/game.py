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
  def __init__(self) :
    initialSize = (500, 500)
    self.__board = board()
    self.__canvas = self.__initial_setup(initialSize)
    self.__sprites = None

  # interface

  #
  # Runs the main loop
  #
  def run(self) :
    canvasSz = self.__board.make_rect(32, 18, 100)
    self.__canvas = self.__set_canvas_size(canvasSz)
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
  # Loads resources
  #
  def __load_res(self) :
    self.__sprites = strip('assets/field_sprites.png')

  #
  # Inits the window and returns the resulting surface
  #
  def __initial_setup(self, params : tuple[int, int]) :
    pygame.init()
    pygame.display.set_caption('Derpsweeper')
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
    for evt in pygame.event.get() :
      if evt.type == pygame.QUIT :
        return False

      if evt.type == pygame.MOUSEMOTION :
        self.__board.make_active(pygame.mouse.get_pos())
      elif evt.type == pygame.MOUSEBUTTONDOWN :
        self.__board.make_active(pygame.mouse.get_pos())
        self.__board.store_btns(pygame.mouse.get_pressed())
      elif evt.type == pygame.MOUSEBUTTONUP :
        self.__board.make_active(pygame.mouse.get_pos())
        self.__board.on_click(pygame.mouse.get_pressed())

    return True

  #
  # Draws the board
  #
  def __present(self) :
    self.__board.draw(self.__canvas)
    pygame.display.flip()