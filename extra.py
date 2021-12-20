from chessboard import display

validfen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'

# Initialization
display.start()

# Position change/update
display.update(validfen)

# Checking GUI window for QUIT event. (Esc or GUI CANCEL)
display.checkForQuit()

# Close window
display.terminate()