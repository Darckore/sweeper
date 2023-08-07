#
# Game entry point
#

import pygame

from internal.field import board

#
# Inits things and runs the main loop
#
class sweeper :
  def __init__(self) :
    initialSize = (500, 500)
    self.board = board()
    self.canvas = self.__initial_setup(initialSize)

  # interface

  #
  # Runs the main loop
  #
  def run(self) :
    canvasSz = self.board.make_rect(32, 18)
    self.canvas = self.__set_canvas_size(canvasSz)
    while self.__poll_events() :
      self.__present()

  #
  # I'm outta here
  #
  def shutdown(self) :
    pygame.quit()

  # implementation

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
    
    return True

  #
  # Draws the board
  #
  def __present(self) :
    self.board.draw(self.canvas)
    pygame.display.flip()