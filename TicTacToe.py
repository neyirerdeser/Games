def draw_board(board):
    n = len(board)

    def draw_stripe():
        for i in range(2 * n + 1):
            if i % 2 == 0:
                print('+', end='')
            else:
                print('--', end='')
        print()

    for i in range(n):
        draw_stripe()
        for j in range(n):
            char = ' '
            if board[i][j] == 1: char = 'X'
            if board[i][j] == 2: char = 'O'
            print('|', char, end='')
        print('|')

    draw_stripe()


def check_winner(board):
    def row(i):  # i-th row
        rowl = []
        for x in range(0, len(board)):
            rowl.append(board[i][x])
        return rowl

    def col(i):  # i-th column
        coll = []
        for x in range(0, len(board)):
            coll.append(board[x][i])
        return coll

    def dia(i):  # 1 for negative sloped diagonal, 2 for positive
        dial = []
        for x in range(0, len(board)):
            if i == 1:
                dial.append(board[x][x])
            elif i == 2:
                dial.append(board[x][len(board) - 1 - x])
        return dial

    def match(line):
        for i in range(0, len(line) - 1):
            if line[i] != line[i + 1]:
                return False
        return True

    winner = 0
    line = []
    for i in range(0, len(board)):
        if match(row(i)):
            line = row(i)
            break
        elif match(col(i)):
            line = col(i)
            break
        elif match(dia(1)):
            line = dia(1)
            break
        elif match(dia(2)):
            line = dia(2)
            break

    if line:
        if line[0] == 1:
            winner = 1
        elif line[0] == 2:
            winner = 2

    return winner


def create_board(n):
    return [[0 for i in range(n)] for j in range(n)]


def get_move(board, player):
    print('Player %d please enter your move in format (row,column): ' % player)
    valid = False
    while not valid:
        coord = input()
        move = coord.split(',')
        move[0] = int(move[0])-1
        move[1] = int(move[1])-1
        if board[move[0]][move[1]] != 0:
            print('the spot it occupied, please enter a valid move (row,column): ')
        else:
            valid = True
            if player == 1: board[move[0]][move[1]] = 1
            if player == 2: board[move[0]][move[1]] = 2


def full(board):
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            if board[i][j] == 0:
                return False
    return True


if __name__ == '__main__':
    play = True
    while play:
        size = int(input('size pls (3 is suggested) : '))
        game = create_board(size)
        count = 1
        while not full(game) and check_winner(game) == 0:
            draw_board(game)
            count += 1
            get_move(game, count % 2 + 1)
        draw_board(game)
        if check_winner(game) == 0:
            print('no more valid mores. its a tie')
        elif check_winner(game) == 1:
            print('Player 1 wins!')
        elif check_winner(game) == 2:
            print('Player 2 wins!')

        response = input('to exit enter exit. to play again press enter')
        if response == 'exit':
            play = False
