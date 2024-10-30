"""
Name: Chris Swezy and Dion Tryban
Date: October 30, 2024
Assignment: Assignment 4
Due Date: October 30, 2024
About this project: An online client/server Tic-Tac-Toe game that demonstrates
                    the usage of sockets to send data between machines over the
                    network.
Assumptions:
- The client connects to a server on the localhost.
- The server is started before the client using the same port.
- The first program argument is the port and is an integer.
- The client moves first.
- The client and server take turns making moves.
- Making out of order moves, client/server crashing/losing connection can be
  non-deterministic.

All work below was performed solely by Chris Swezy and Dion Tryban.
We did not use code generated by an AI tool.
"""
import socket
import swezy_c_tictactoegame as game

def updateBoard(board: list[list[str]], move: str, isServer: bool) -> list[list[str]] | str:
    """
    Returns an updated board using the given move, if possible.
    If the move is not possible, returns the reason.
    """
    move = move.strip()

    if len(move) != 2:
        return "Invalid move format."
    
    x, y = move[0], move[1]
    
    if x < 'A' or x > 'C':
        return "Move is out of bounds."
    
    x = ord(x) - ord('A')

    if y < '1' or y > '3':
        return "Move is out of bounds."
    
    y = int(y) - 1

    if board[x][y] == '.':
        if isServer:
            board[x][y] = 'O'
        else:
            board[x][y] = '#'
    else:
        return "Position is already occupied."

    return board


def runGameLoop(c: socket.socket) -> None:
    # Initialize board and send to client.
    board = game.createBoard()
    c.send(game.encodeBoard(board))
    game.printBoard(board)
    print("Waiting for opponent's first move. Don't type anything!")

    client_move = None
    while True:
        # Perform the client move.
        while True:
            # Get the move from the client.
            client_move = c.recv(4096).decode()
            result = updateBoard(board, client_move, False)

            # If the result is a str, it is an error reason and we send that.
            # Otherwise, the move is valid and we send the updated board.
            if type(result) is str:
                c.send(result.encode())
            else:
                board = result
                c.send(game.encodeBoard(board))
                break

        game.printBoard(board)

        if game.checkIsGameOver(board, False):
            break

        # Perform the server move.
        while True:
            # No need to send anything to the client until a valid move is made.
            move = game.getMoveFromUser(client_move)
            result = updateBoard(board, move, True)

            if type(result) is str:
                print(result)
            else:
                board = result
                break
        
        # Once a valid move is made, send the board and the move to the client.
        c.send(game.encodeBoard(board))
        c.send(move.encode())

        game.printBoard(board)

        if game.checkIsGameOver(board, True):
            break

        print("Wait for your opponent move (don't type anything)!")


if __name__ == "__main__":
    port = game.getPortFromArgv()
    if port is None:
        exit()

    s = socket.socket()
    s.bind(("", port))
    s.listen()

    while True:
        try:
            print("Waiting for opponent to connect....")
            c, addr = s.accept()
            print(f"Receive opponent connection from {addr}")

            runGameLoop(c)
        except BrokenPipeError:
            print("The client disconnected.")
            c.close()
    
    s.close()
