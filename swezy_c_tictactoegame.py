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
import sys

def getPortFromArgv() -> int | None:
    """Gets the port from the sys.argv and handles errors."""
    if len(sys.argv) == 2:
        try:
            return int(sys.argv[1])
        except ValueError:
            print("The port must be an integer.")
    else:
        print(f"Usage: python3 {sys.argv[0]} <port>")


def createBoard() -> list[list[str]]:
    """Initializes a board as a 3x3 grid of '.' strings."""
    return [['.' for x in range(3)] for y in range(3)]


def encodeBoard(board: list[list[str]]) -> bytes:
    """Encodes a board as a flattened string."""
    return "".join(["".join(x) for x in board]).encode()


def decodeBoard(board_bytes: bytes) -> list[list[str]] | str:
    """Decodes an encoded board back to a 3x3 grid."""
    flat_board = board_bytes.decode()

    if set(flat_board) >= set(".#0") or len(flat_board) != 9:
        return flat_board

    board = [[' ' for x in range(3)] for y in range(3)]
    counter = 0
    for i in range(3):
        for j in range(3):
            board[i][j] = flat_board[counter]
            counter += 1

    return board


def printBoard(board: list[list[str]]) -> None:
    print("  1 2 3")
    print(f"A {board[0][0]} {board[0][1]} {board[0][2]}")
    print(f"B {board[1][0]} {board[1][1]} {board[1][2]}")
    print(f"C {board[2][0]} {board[2][1]} {board[2][2]}")


def getMoveFromUser(prevMove: str | None) -> str:
    if prevMove == None:
        move = input("Enter a move([ABC][123]): ")
    else:
        move = input(f"Your opponent played {prevMove}, your move ([ABC][123]): ")
    
    return move


def checkWin(board: list[list[str]]) -> bool:
    # Check columns
    for x in range(3):
        row = set(board[x])
        if len(row) == 1 and row.pop() != '.':
            return True
    
    # Check rows
    for y in range(3):
        col = set([board[0][y], board[1][y], board[2][y]])
        if len(col) == 1 and col.pop() != '.':
            return True
    
    # Check left diagonal
    if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] != '.':
        return True

    # Check right diagonal
    if board[2][0] == board[1][1] and board[2][0] == board[0][2] and board[2][0] != '.':
        return True
    
    return False


def checkTie(board: list[list[str]]) -> bool:
    for x in range(3):
        for y in range(3):
            if board[x][y] == '.':
                return False
    
    return True


def checkIsGameOver(board: list[list[str]], wasJustYourTurn: bool) -> bool:
    """Checks for a win or tie and prints the respective mesage."""
    if checkWin(board):
        if wasJustYourTurn:
            print("Congratulations, you won!")
        else:
            print("Your opponent won the game!")
        return True
    
    if checkTie(board):
        print("The game is a tie.")
        return True

    return False
