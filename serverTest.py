import socket
import swezy_c_tictactoegame as game

def updateBoard(board, move, isServer) -> list[list[str]] | None:
    move = move.strip()

    if len(move) != 2:
        return
    
    x, y = move[0], move[1]
    
    if x < 'A' or x > 'C':
        return
    
    x = ord(x) - ord('A')

    if y < '1' or y > '3':
        return
    
    y = int(y) - 1

    if board[x][y] == '*':
        if isServer:
            board[x][y] = 'O'
        else:
            board[x][y] = '#'
    else:
        return

    return board

if __name__ == "__main__":
    s = socket.socket()

    port = 12345  # TODO: Get from sys.argv

    s.bind(('', port))
    s.listen(1)

    board = game.createBoard()
    c, addr = s.accept()

    c.send(game.encodeBoard(board))
    game.printBoard(board)

    client_move = None

    print("Waiting for opponent's first move. Don't type anything!")

    while True:
        # Client Move
        while True:
            
            client_move = c.recv(4096).decode()
            result = updateBoard(board, client_move, False)

            if result is not None:
                board = result
                c.send(game.encodeBoard(board))
                break
            else:
                c.send("error".encode())


        game.printBoard(board)

        if game.checkWin(board):
            print("Your opponent won the game!")
            break

        if game.checkTie(board):
            print("The game is a tie.")
            break

        # Server Move
        while True:
            move = game.getMoveFromUser(client_move)
            result = updateBoard(board, move, True)

            if result is not None:
                board = result
                break
        
        c.send(game.encodeBoard(board))
        c.send(move.encode())

        game.printBoard(board)

        if game.checkWin(board):
            print("Congratulations, you won!")
            break

        if game.checkTie(board):
            print("The game is a tie.")
            break

        print("Wait for your opponent move (don't type anything)!")
