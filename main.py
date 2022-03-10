# Wordle Game Basis


def play_game():
    play = True
    guess = [None] * 5
    counter = 0
    correct_word = "snake"
    print(correct_word[0])
    # correct_move = random word

    # Initial instructions
    print("Welcome to Wordle!\nIn this game, you have 6 guesses to guess the correct 5 letter word!")
    print(
        "The following hints will be given after each move:\nCorrect letter and spot: %\nCorrect letter wrong spot: "
        "#\nLetter not in word: !\n")

    # Loop to play Wordle
    while play:
        print("Guess:", end='')
        guess[counter] = input()
        temp = guess[counter]
        hint = (check_move(temp, correct_word))
        if hint == "%%%%%":
            print("Your hint is:", hint)
            print("Congratulations! You win!")
            play = False
        else:
            print("Your hint is:", hint)
        counter = counter + 1
        if counter == 6:
            play = False


def check_move(guess, correct_word):
    duplicate_flag = True
    index = 0
    hint = ""
    done_letters = [None] * 4
    for g in guess:
        if index > 3:
            break
        if g == correct_word[index]:
            done_letters.append(g)
        index = index + 1
    print(done_letters)
    index = 0
    for g in guess:
        if index > 4:
            break
        print(g, correct_word[index])
        if g == correct_word[index]:
            hint = hint + "%"
        elif g in correct_word and g not in done_letters:
            hint = hint + "#"
        else:
            hint = hint + "!"
        index = index + 1
    if len(hint) != 5:
        for x in range(4 - len(hint)):
            hint = hint + "!"
    return hint


if __name__ == "__main__":
    play_game()
