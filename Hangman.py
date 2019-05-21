import random


def pick_word(filename):
    text = ''
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            text += line
            line = f.readline()

    words = text.split()
    n = len(words)
    return words[random.randint(0, n - 1)]

clue = ''
guessed_letters = []

def guessed(c):
    return c in guessed_letters



def get_letter(mistake):
    letter = input('letter : ')
    if letter not in clue and letter not in guessed_letters:
        mistake += 1
    guessed_letters.append(letter)

    return mistake


def display_word():
    for x in clue:
        if guessed(x):
            print(x, end=' ')
        else:
            print('_', end=' ')
    print()


def win():
    for x in clue:
        if x not in guessed_letters:
            return False
    return True


def game():
    mistake = 0
    print('Welcome to Hangman. You can have at most 6 mistakes (use capital letters). Good luck!')
    display_word()
    while not win():
        mistake = get_letter(mistake)
        print_man(mistake)
        display_word()
        if mistake >= 6:
            print('you killed the man. better luck next time')
            return
    print('congratulations!')

def print_man(mistake):
    man = [['o o'],
           [' - '],
           [' |'],
           ['-|-'],
           [' |'],
           ['/ \\']]
    if mistake <= 0:
        return
    for i in range(mistake):
        print(man[i][0])

if __name__ == '__main__':
    playing = True
    while playing:
        clue = pick_word('sowpods.txt')
        game()
        response = input('to exit enter exit. to play press enter')
        if response == 'exit':
            playing = False
        else:
            guessed_letters = []