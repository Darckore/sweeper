from internal.game import sweeper

def main() :
  game = sweeper((500, 500)) # todo: don't hard-code
  game.run()
  game.shutdown()

if __name__ == '__main__' :
  main()