import random


class Game:
    revealed = []
    flagged = []
    board = []
    level = None
    size = None
    mines = None

    def __init__(self, level):
        self.revealed.clear()
        self.flagged.clear()
        self.board = []
        self.level = level
        self.size = self.set_level()[0]
        self.mines = self.set_level()[1]
        self.put_mines()
        self.put_numbers()

    def set_level(self):
        if self.level == 1:
            return tuple((8, 10))
        if self.level == 2:
            return tuple((16, 40))
        if self.level == 3:
            return tuple((24, 99))

    def put_mines(self):
        mine_rows = []
        mine_cols = []

        for i in range(self.mines):
            mine_rows.append(random.randint(0, self.size - 1))
            valid = False
            c = 0
            while not valid:
                valid = True
                c = random.randint(0, self.size - 1)
                for j in range(len(mine_rows) - 1):
                    if mine_rows[j] == mine_rows[i] and mine_cols[j] == c:
                        valid = False

            mine_cols.append(c)

        mined = [[0] * self.size for _ in range(self.size)]
        for i in range(self.mines):
            mined[mine_rows[i]][mine_cols[i]] = 9  # max number written on board can be 8, so 9 is a mine
        self.board.extend(mined)

    def put_numbers(self):
        for i in range(self.size):
            for j in range(self.size):
                location_keys = self.location_checks(i, j)
                if self.board[i][j] != 9:
                    self.check_increase(location_keys, i, j)

    def location_checks(self, i, j):
        # corners: A C G I
        # borders: B D F H
        end = self.size - 1
        if i == 0:
            if j == 0:
                return [5, 7, 8]  # A
            elif j == end:
                return [4, 6, 7]  # C
            else:
                return [4, 5, 6, 7, 8]  # B
        elif i == end:
            if j == 0:
                return [2, 3, 5]  # G
            elif j == end:
                return [1, 2, 4]  # I
            else:
                return [1, 2, 3, 4, 5]  # H
        elif j == 0:
            return [2, 3, 5, 7, 8]  # D
        elif j == end:
            return [1, 2, 4, 6, 7]  # F
        else:
            return [1, 2, 3, 4, 5, 6, 7, 8]  # E

    def check_increase(self, a, i, j):
        if 1 in a and self.board[i - 1][j - 1] == 9:
            self.board[i][j] += 1
        if 2 in a and self.board[i - 1][j] == 9:
            self.board[i][j] += 1
        if 3 in a and self.board[i - 1][j + 1] == 9:
            self.board[i][j] += 1
        if 4 in a and self.board[i][j - 1] == 9:
            self.board[i][j] += 1
        if 5 in a and self.board[i][j + 1] == 9:
            self.board[i][j] += 1
        if 6 in a and self.board[i + 1][j - 1] == 9:
            self.board[i][j] += 1
        if 7 in a and self.board[i + 1][j] == 9:
            self.board[i][j] += 1
        if 8 in a and self.board[i + 1][j + 1] == 9:
            self.board[i][j] += 1

    def flag(self, i, j):
        if (i, j) not in self.flagged:
            self.flagged.append((i, j))
        else:
            self.flagged.remove((i, j))

    def reveal(self, i, j):
        self.revealed.append((i, j))
        if self.board[i][j] == 0:
            a = self.location_checks(i, j)
            if 1 in a and (i - 1, j - 1) not in (self.revealed or self.flagged):
                self.reveal(i - 1, j - 1)
            if 2 in a and (i - 1, j) not in (self.revealed or self.flagged):
                self.reveal(i - 1, j)
            if 3 in a and (i - 1, j + 1) not in (self.revealed or self.flagged):
                self.reveal(i - 1, j + 1)
            if 4 in a and (i, j - 1) not in (self.revealed or self.flagged):
                self.reveal(i, j - 1)
            if 5 in a and (i, j + 1) not in (self.revealed or self.flagged):
                self.reveal(i, j + 1)
            if 6 in a and (i + 1, j - 1) not in (self.revealed or self.flagged):
                self.reveal(i + 1, j - 1)
            if 7 in a and (i + 1, j) not in (self.revealed or self.flagged):
                self.reveal(i + 1, j)
            if 8 in a and (i + 1, j + 1) not in (self.revealed or self.flagged):
                self.reveal(i + 1, j + 1)

    def reveal_all(self):
        for (a, b) in self.flagged:
            if self.board[a][b] != 9:
                self.flagged.remove((a, b))
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) not in self.flagged:
                    self.reveal(i, j)

    def play(self, test, mode, i, j):
        move = self.get_move(test, mode, i, j)
        key = move[0]
        i = move[1]
        j = move[2]
        if key == 'open':
            self.reveal(i, j)
            if self.board[i][j] == 9:
                return False
        if key == 'flag':
            self.flag(i, j)
        if not test:
            self.print_game()
        return True

    def get_move(self, test, mode, i, j):
        end = self.size - 1
        if not test:
            print('coordinates in format <row>  <column>\nto place a flag follow the format: f <row> <column> ')
            while True:
                coord = input()
                click = coord.split(' ')
                if len(click) == 2:
                    try:
                        r = int(click[0])
                        c = int(click[1])
                    except (TypeError, ValueError):
                        print('both coordinates must be integers')
                        continue
                    if r > end or c > end:
                        print('location outside the game, careful first box is 0 0. '
                              'choose a different box (row  column): ')
                    elif (r, c) in self.revealed:
                        print('box already open, choose a different box (row  column): ')
                    elif (r, c) in self.flagged:
                        print('box is flagged, to unflag enter the same command as flagging')
                    else:
                        return tuple(('open', r, c))
                elif len(click) == 3:
                    if click[0] != 'f':
                        print(
                            'please give two numbers seperated by space to enter coordinates\n'
                            'to place a flag follow the format: f <row> <column>')
                        continue
                    try:
                        r = int(click[1])
                        c = int(click[2])
                    except (TypeError, ValueError):
                        print('both coordinates must be integers')
                        continue
                    if r > end or c > end:
                        print('location outside the game, careful first box is 0 0. '
                              'choose a different box (row  column): ')
                    elif (r, c) in self.revealed:
                        print('box already open, choose a different box (row  column): ')
                    else:
                        return tuple(('flag', r, c))
                else:
                    print('please give two numbers separated by space to enter coordinates')
        else:  # in test
            return tuple((mode, i, j))

    def print_game(self):
        def horizontal(length):
            print()
            print('--+-', end='')
            for l in range(length):
                print('----', end='')
            print()
        print('  | ', end='')
        for i in range(self.size):
            print(i % 10, end='   ')
        horizontal(self.size)
        for i in range(self.size):
            print(i % 10, '| ', end='')
            for j in range(self.size):
                char = ' '
                if (i, j) in self.revealed:
                    if self.board[i][j] == 9:
                        char = 'X'
                    elif self.board[i][j] == 0:
                        char = '.'
                    else:
                        char = self.board[i][j]
                elif (i, j) in self.flagged:
                    char = 'f'
                print(char, end=' | ')
            horizontal(self.size)
        print('mines left:', self.mines - len(self.flagged))

    @classmethod
    def intro(cls):
        print('Welcome to minesweeper\n'
              'some notes for after you choose the level you want to play\n'
              '* to open a box, you will enter your coordinates in the format:'
              ' <row> <column> of your desired number (eg. 2 5)\n'
              '* to (un)flag a box put an 'f' in front of your coordinates (eg. f 4 3)\n'
              '* game ends when all unopened or flagged boxes are mines\n'
              '* empty boxes are shown with a . in them for convenience\n'
              '* keep in mind that the upper left corner has coordinates 0 0\n'
              '  and that numbers on the side repeat for each 10 rows/column,'
              ' you should type the real number that would be there\n'
              'lets start :)\n')

    @classmethod
    def get_level(cls, test, lvl=None):
        if not test:
            print('level of difficulty:\n'
                  '1. Beginner\n2. Intermediate\n3. Expert\nYour choice: ')
        level = 0
        valid = False
        while not valid:
            try:
                if lvl is None:
                    level = int(input())
                else:
                    level = lvl
            except (TypeError, ValueError):
                print('level must be a number')
                continue
            if level not in (1, 2, 3):
                print('invalid answer entered')
            else:
                valid = True
        return level

    def lost(self):
        mines_left = self.mines - len(self.flagged)
        self.reveal_all()
        self.print_game()
        print('GAME OVER\nmines exploded: %d\nplay again? (Y/N)' % mines_left)

    def won(self, test):
        for (a, b) in self.flagged:
            if self.board[a][b] != 9:
                return False
        if not test:
            print('CONGRATULATIONS\nplay again? (Y/N)')
        return True

    @classmethod
    def minesweeper(cls, test, mode=None, i=None, j=None, lvl=None):
        playing = True
        while playing:
            level = cls.get_level(test, lvl)
            game = Game(level)
            game.print_game()
            turn = 0
            curr_mode = None
            curr_i = None
            curr_j = None
            if test:
                if mode[turn] is None or mode[turn] not in ('open', 'flag'):
                    raise Exception('mode must be open or flag')
                elif i[turn] is None or j[turn] is None:
                    raise Exception('test mode needs coordinates')
                else:
                    curr_mode = mode[turn]
                    curr_i = i[turn]
                    curr_j = j[turn]

            while game.play(test, curr_mode, curr_i, curr_j):

                mines_left = game.mines - len(game.flagged)
                hidden = game.size ** 2 - len(game.revealed) - len(game.flagged)
                if (mines_left == 0 or hidden == mines_left) and game.won(test):
                    break
                turn += 1
                if test:
                    if turn >= len(mode):
                        curr_mode = 'open'
                        while True:
                            curr_i = random.randint(0, game.size - 1)
                            curr_j = random.randint(0, game.size - 1)
                            if (curr_i, curr_j) not in game.revealed:
                                break
                            elif hidden == 0:
                                # then coordinates must be in game.flagged
                                # then unflag and play
                                game.flag(curr_i, curr_j)
                                break
                    else:
                        if mode[turn] is None or mode[turn] not in ('open', 'flag'):
                            raise Exception('mode must be open or flag')
                        elif i[turn] is None or j[turn] is None:
                            raise Exception('test mode needs coordinates')
                        else:
                            curr_mode = mode[turn]
                            curr_i = i[turn]
                            curr_j = j[turn]
            else:
                game.lost()
            valid = False
            while not valid:
                answer = 'N'
                if not test:
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
    Game.intro()
    Game.minesweeper(False)
