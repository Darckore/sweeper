#
# Game entry point
#

import pygame

from internal.field import board

#
# Inits things and runs the main loop
#
class sweeper :
  def __init__(self, canvasSize : tuple[int, int]) :
    self.canvas = self.__initial_setup(canvasSize)
    self.board = board(canvasSize[0], canvasSize[1])

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

  #
  # Runs the main loop
  #
  def run(self) :
    self.board.set_mode(15, 10)
    while self.__poll_events() :
      self.__present()

  #
  # I'm outta here
  #
  def shutdown(self) :
    pygame.quit()