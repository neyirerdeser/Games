import random

revealed = []
flagged = []


def print_game(brd):
    def horizontal():
        print()
        print('--+-', end='')
        for i in range(len(brd)):
            print('----', end='')
        print()

    print('  | ', end='')
    for i in range(len(brd)):
        print(i % 10, end='   ')
    horizontal()
    for i in range(len(brd)):
        print(i % 10, '| ', end='')
        for j in range(len(brd)):
            if (i, j) in revealed:
                if brd[i][j] == 9:
                    print('X', end=' | ')
                elif brd[i][j] == 0:
                    print('.', end=' | ')
                else:
                    print(brd[i][j], end=' | ')
            elif (i, j) in flagged:
                print('f', end=' | ')
            else:
                print(' ', end=' | ')
        horizontal()


def put_mines(lvl):
    size = 0
    mines = 0
    mine_rows = []
    mine_cols = []

    if lvl == 1:
        size = 8
        mines = 10
    if lvl == 2:
        size = 16
        mines = 40
    if lvl == 3:
        size = 24
        mines = 99

    for i in range(mines):
        mine_rows.append(random.randint(0, size - 1))
        valid = False
        c = 0
        while not valid:
            valid = True
            c = random.randint(0, size - 1)
            for j in range(len(mine_rows) - 1):
                if mine_rows[j] == mine_rows[i] and mine_cols[j] == c:
                    valid = False

        mine_cols.append(c)

    board = [[0] * size for _ in range(size)]
    for i in range(mines):
        board[mine_rows[i]][mine_cols[i]] = 9  # max number written on board can be 8, so 9 is a mine
    return board


def location_checks(board, i, j):
    def location():
        # corners: A C G I
        # borders: B D F H
        end = len(board) - 1
        if i == 0:
            # A B C
            if j == 0:
                return 'A'
            elif j == end:
                return 'C'
            else:
                return 'B'
        elif i == end:
            # G H I
            if j == 0:
                return 'G'
            elif j == end:
                return 'I'
            else:
                return 'H'
        elif j == 0:
            return 'D'
        elif j == end:
            return 'F'
        else:
            return 'E'

    a = []
    if location() == 'A':
        a = [5, 7, 8]
    if location() == 'B':
        a = [4, 5, 6, 7, 8]
    if location() == 'C':
        a = [4, 6, 7]
    if location() == 'D':
        a = [2, 3, 5, 7, 8]
    if location() == 'E':
        a = [1, 2, 3, 4, 5, 6, 7, 8]
    if location() == 'F':
        a = [1, 2, 4, 6, 7]
    if location() == 'G':
        a = [2, 3, 5]
    if location() == 'H':
        a = [1, 2, 3, 4, 5]
    if location() == 'I':
        a = [1, 2, 4]
    return a


def put_numbers(board):
    def check_increase(a):
        if 1 in a and board[i - 1][j - 1] == 9:
            board[i][j] += 1
        if 2 in a and board[i - 1][j] == 9:
            board[i][j] += 1
        if 3 in a and board[i - 1][j + 1] == 9:
            board[i][j] += 1
        if 4 in a and board[i][j - 1] == 9:
            board[i][j] += 1
        if 5 in a and board[i][j + 1] == 9:
            board[i][j] += 1
        if 6 in a and board[i + 1][j - 1] == 9:
            board[i][j] += 1
        if 7 in a and board[i + 1][j] == 9:
            board[i][j] += 1
        if 8 in a and board[i + 1][j + 1] == 9:
            board[i][j] += 1

    for i in range(len(board)):
        for j in range(len(board)):
            loc_keys = location_checks(board, i, j)
            if board[i][j] != 9:
                check_increase(loc_keys)


def play(board):
    def reveal(i, j):
        revealed.append((i, j))
        if board[i][j] == 0:
            a = location_checks(board, i, j)
            if 1 in a and (i - 1, j - 1) not in (revealed or flagged):
                reveal(i - 1, j - 1)
            if 2 in a and (i - 1, j) not in (revealed or flagged):
                reveal(i - 1, j)
            if 3 in a and (i - 1, j + 1) not in (revealed or flagged):
                reveal(i - 1, j + 1)
            if 4 in a and (i, j - 1) not in (revealed or flagged):
                reveal(i, j - 1)
            if 5 in a and (i, j + 1) not in (revealed or flagged):
                reveal(i, j + 1)
            if 6 in a and (i + 1, j - 1) not in (revealed or flagged):
                reveal(i + 1, j - 1)
            if 7 in a and (i + 1, j) not in (revealed or flagged):
                reveal(i + 1, j)
            if 8 in a and (i + 1, j + 1) not in (revealed or flagged):
                reveal(i + 1, j + 1)

    end = len(board) - 1
    print('coordinates: (row  column)\nto place a flag follow the format: f <row> <column> ')
    valid = False
    while not valid:
        coord = input()
        click = coord.split(' ')
        if len(click) == 2:
            # r, c = 0, 0
            try:
                r = int(click[0])
                c = int(click[1])
            except:
                print('coordinates must be integers')
                continue
            if r > end or c > end:
                print('location outside the game, careful first box is 0 0. choose a different box (row  column): ')
            elif (r, c) in revealed:
                print('box already open, choose a different box (row  column): ')
            elif (r, c) in flagged:
                print('box is flagged, to unflag enter the same command as flagging')
            else:
                valid = True
                reveal(r, c)
                if board[r][c] == 9:
                    return False
        elif len(click) == 3:
            if click[0] != 'f':
                print(
                    'please give two numbers seperated by space to enter coordinates\n'
                    'to place a flag follow the format: f <row> <column>')
                continue
            try:
                r = int(click[1])
                c = int(click[2])
            except:
                print('coordinates must be integers')
                continue
            if r > end or c > end:
                print('location outside the game, careful first box is 0 0. choose a different box (row  column): ')
            elif (r, c) in revealed:
                print('box already open, choose a different box (row  column): ')
            else:
                valid = True
                if (r, c) not in flagged:
                    flagged.append((r, c))
                else:
                    flagged.remove((r, c))
        else:
            print('please give two numbers seperated by space to enter coordinates')
    print_game(board)
    return True


def minesweeper():
    playing = True
    while playing:
        revealed.clear()
        flagged.clear()
        print('level of difficulty:\n'
              '1. Beginner\n2. Intermediate\n3. Expert\nYour choice: ')
        level = 0
        valid = False
        while not valid:
            try:
                level = int(input())
            except:
                print('level must be a number')
                continue
            if level not in (1, 2, 3):
                print('invalid answer entered')
            else:
                valid = True
        game = put_mines(level)
        mines = 0
        for i in range(len(game)):
            for j in range(len(game)):
                if game[i][j] == 9:
                    mines += 1
        put_numbers(game)
        print_game(game)
        print('mines left:', mines - len(flagged))
        while play(game):
            mines_left = mines - len(flagged)
            hidden = len(game) ** 2 - len(revealed) - len(flagged)
            if mines_left == 0 or hidden == mines_left:
                win = True
                for (a, b) in flagged:
                    if game[a][b] != 9:
                        win = False
                if win:
                    print('CONGRATULATIONS\nplay again? (Y/N)')
                    break
            print('mines left:', mines_left)
        else:
            mines_left = mines - len(flagged)
            for (a, b) in flagged:
                if game[a][b] != 9:
                    flagged.remove((a, b))
            for i in range(len(game)):
                for j in range(len(game)):
                    revealed.append((i, j))
            print_game(game)
            print('GAME OVER\nmines exploded: %d\nplay again? (Y/N)' % mines_left)
        valid = False
        while not valid:
            answer = input()
            if answer not in ('Y', 'N', 'y', 'n'):
                print('invalid answer entered\ndo you want to play again? (Y/N)')
            elif answer in ('N', 'n'):
                print('bye')
                playing = False
                valid = True
            else:
                valid = True


if __name__ == '__main__':
    minesweeper()
