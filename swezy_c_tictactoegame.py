def createBoard() -> list[list[str]]:
    return [['*' for x in range(3)] for y in range(3)]

def encodeBoard(board: list[list[str]]) -> bytes:
    return "".join(["".join(x) for x in board]).encode()

def decodeBoard(board_bytes: bytes) -> list[list[str]] | None:
    flat_board = board_bytes.decode()

    if flat_board == "error" or len(flat_board) != 9:
        return

    board = [[' ' for x in range(3)] for y in range(3)]
    counter = 0
    for i in range(3):
        for j in range(3):
            board[i][j] = flat_board[counter]
            counter += 1

    return board

def printBoard(board: list[list[str]]):
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
        if len(row) == 1 and row.pop() != '*':
            return True
    
    # Check rows
    for y in range(3):
        col = set([board[0][y], board[1][y], board[2][y]])
        if len(col) == 1 and col.pop() != '*':
            return True
    
    # Check left diagonal
    if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] != '*':
        return True

    # Check right diagonal
    if board[2][0] == board[1][1] and board[2][0] == board[0][2] and board[2][0] != '*':
        return True
    
    return False

def checkTie(board: list[list[str]]) -> bool:
    for x in range(3):
        for y in range(3):
            if board[x][y] == '*':
                return False
    
    return True
