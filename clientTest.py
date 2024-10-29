import socket
import swezy_c_tictactoegame as game

s = socket.socket()

port = 12345

s.connect(('localhost', port))

board = game.decodeBoard(s.recv(4096))
game.printBoard(board)

server_move = None

while True:
    # Client Move
    while True:
        move = game.getMoveFromUser(server_move)
        s.send(move.encode())

        board = game.decodeBoard(s.recv(4096))

        if board is not None:
            break
    
    game.printBoard(board)

    if game.checkWin(board):
        print("Congratulations, you won!")
        break

    if game.checkTie(board):
        print("The game is a tie.")
        break

    print("Wait for your opponent move (don't type anything)!")
    
    # Server Move
    board = game.decodeBoard(s.recv(4096))
    server_move = s.recv(4096).decode()

    game.printBoard(board)

    if game.checkWin(board):
        print("Your opponent won the game!")
        break

    if game.checkTie(board):
        print("The game is a tie.")
        break
    

s.close()