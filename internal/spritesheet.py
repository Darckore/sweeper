#
# A basic spritesheet
#

import pygame

#
# Stores a spritesheet and provides access to its pieces
#
class strip :
  spriteSide = 64

  def __init__(self, filename) :
    try :
      self.__sheet = pygame.image.load(filename).convert()
    except pygame.error as e:
      print(f"Unable to load spritesheet image: {filename}")
      raise SystemExit(e)

  # interface

  def image_at(self, pos : int) :
    rect = pygame.Rect(pos + self.spriteSide, 0, self.spriteSide, self.spriteSide)
    img  = pygame.Surface(rect.size).convert()
    img.blit(self.__sheet, (0, 0), rect)
    chroma = img.get_at((0, 0))
    img.set_colorkey(chroma, pygame.RLEACCEL)
    return img