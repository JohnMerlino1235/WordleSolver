# Wordle Game Basis
from random import randint


def play_game():
    play = True
    guess = [None] * 6
    hints = ["!!!!!"] * 6
    counter = 0
    total_words = load_words("Wordle Answers.txt")
    correct_word = total_words[randint(0, len(total_words))]

    # print(correct_word)

    guesses_list = total_words
    letter_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r""s", "t",
                   "u", "v", "w", "x", "y", "z"]

    constructed_word = "!!!!!"

    # Initial instructions
    print("Welcome to Wordle!\nIn this game, you have 6 guesses to guess the correct 5 letter word!")
    print(
        "The following hints will be given after each move:\nCorrect letter and spot: %\nCorrect letter wrong spot: "
        "#\nLetter not in word: !\n")

    # Loop to play Wordle
    while play:
        # Get user input
        print("Would you like to randomly generate a guess? Y/N", end='')
        if input() is "Y":
            if counter is 0:
                guess[counter] = random_guess(guesses_list)
            else:
                letter_list = get_updated_letters(guess[counter - 1], hints[counter - 1], letter_list)
                print(len(guesses_list))
                guesses_list = get_updated_words(letter_list, guesses_list)
                print(len(guesses_list))
                guess[counter] = random_guess(guesses_list)


        else:
            guess[counter] = get_user_guess()

        temp = guess[counter]
        print("Your guess is:", temp)
        hints[counter] = (check_move(temp, correct_word))

        # check to see if hint is correct (meaning guess is correct word)
        if check_hint(hints[counter]):
            break
        """""
        if hint == "%%%%%":
            print("Your hint is:", hint)
            print("Congratulations! You win!")
            play = False

        # simply display hint if guess is incorrect
        else:
            print("Your hint is:", hint)
        """
        # add one to your counter, resembles the amount of guesses user has used
        counter = counter + 1

        # if counter == 6 then game is over
        play = check_counter(counter, correct_word)


# checks counter to see if user has reached maximum amount of guesses
def check_counter(counter, correct_word):
    if counter == 6:
        print("You lose! The correct word was:", correct_word)
        return False
    else:
        return True


# gets updated possible letters
def get_updated_letters(guess, hint, letter_list):
    index = 0
    new_list = letter_list
    for h in hint:
        if h == "!" and guess[index] in new_list:
            new_list.remove(guess[index])
        index += 1

    return new_list


def construct_correct_word(guess, hint):
    index = 0
    new_string = ""
    for h in hint:
        if h == "%":
            new_string = new_string + guess[index]
        else:
            new_string = new_string + "!"
        index += 1
    return new_string


def get_updated_words(letter_list, word_list):
    new_list = []
    for letter in letter_list:
        for word in word_list:
            if letter in word and word not in new_list:
                new_list.append(word)

    return new_list


# checks hint and outputs information based on correctness
def check_hint(hint):
    if hint == "%%%%%":
        print("Your hint is:", hint)
        print("Congratulations! You win!")
        return True
    else:
        print("Your hint is:", hint)
        return False


# asks the user to input a guess
def get_user_guess():
    print("Guess:", end='')
    guess = input()
    return guess


# simple algorithm that cycles through
def simple_algorithm(previous_guess, valid_guesses, hint):
    # remove guess from valid guess array
    valid_guesses.remove(previous_guess)

    if hint == "!!!!!":
        return valid_guesses

    char_index = 0
    new_guesses = []
    done_words = []
    for valid in valid_guesses:
        index = 0
        for char_guess in previous_guess:
            if char_guess == valid[index]:
                done_words.append(valid)
                break

    for char in hint:
        if char == "%":
            for guess in valid_guesses:
                if previous_guess[char_index] == guess[char_index]:
                    new_guesses.append(guess)
            char_index = char_index + 1
        elif char == "#":
            for guess in valid_guesses:
                if previous_guess[char_index] in guess and guess not in done_words:
                    new_guesses.append(guess)
            char_index = char_index + 1
        else:
            char_index = char_index + 1
    return new_guesses


# checks move and constructs a hint to return to the user
def check_move(guess, correct_word):
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


# total possible words array
def load_words(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    for x in range(len(lines)):
        lines[x] = lines[x].strip("\n")

    # remove first and last index
    del lines[0]
    del lines[-1]
    return lines


# algorithm to get random guess each time
def random_guess(word_list):
    return word_list[randint(0, len(word_list))]


if __name__ == "__main__":
    play_game()
