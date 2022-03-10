# Wordle Game Basis
from random import randint


def play_game():
    play = True
    guess = [None] * 6
    counter = 0
    total_words = get_correct_move("Wordle Answers.txt")
    correct_word = total_words[randint(0, len(total_words))]
    print(correct_word)

    # Initial instructions
    print("Welcome to Wordle!\nIn this game, you have 6 guesses to guess the correct 5 letter word!")
    print(
        "The following hints will be given after each move:\nCorrect letter and spot: %\nCorrect letter wrong spot: "
        "#\nLetter not in word: !\n")

    # Loop to play Wordle
    while play:
        # Get user input
        print("Guess:", end='')
        guess[counter] = input()
        temp = guess[counter]
        hint = (check_move(temp, correct_word))

        # check to see if hint is correct (meaning guess is correct word)
        if hint == "%%%%%":
            print("Your hint is:", hint)
            print("Congratulations! You win!")
            play = False

        # simply display hint if guess is incorrect
        else:
            print("Your hint is:", hint)
        counter = counter + 1

        # if counter == 6 then game is over
        if counter == 6:
            print("You lose! The correct word was:", correct_word)
            break


# checks move and constructs a hint to return to the user
def check_move(guess, correct_word):
    print(guess)
    print(correct_word)
    index = 0
    done_letters = [None] * 5
    hint = ["!"] * 5

    # loop to check if there are any letters in correct spot, add to array for comparison in second loop
    for g in guess:
        if index == 5:
            break
        if g == correct_word[index]:
            done_letters[index] = g
            hint[index] = "%"
        index = index + 1

    index = 0

    # loop to construct the hint, "%" if letter is in correct spot, "#" if letter is in wrong spot, "!"
    # if letter is incorrect
    for g in guess:
        if index == 5:
            break
        if g not in done_letters and g in correct_word:
            hint[index] = "#"
        index = index + 1
        """""
        if index == 5:
            break
        if g == correct_wrd[index]:
            hint = hint + "%"
        elif g in correct_word and g not in done_letters:
            hint = hint + "#"
        else:
            hint = hint + "!"
        index = index + 1
        """""
    if len(hint) < 5:
        for x in range(5 - len(hint)):
            hint = hint + "!"

    hint_str = ""
    for x in hint:
        hint_str = hint_str + x
    return hint_str


def get_correct_move(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    return lines


if __name__ == "__main__":
    play_game()
