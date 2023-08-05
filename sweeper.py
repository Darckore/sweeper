from internal.game import sweeper

def main() :
  game = sweeper()
  game.run()
  game.shutdown()

if __name__ == '__main__' :
  main()