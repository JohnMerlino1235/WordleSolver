# Wordle Game Basis
import collections
from random import randint


def online_play():
    print("Please enter your first guess:", end='')
    guess = input()
    print("Please enter the received hint:", end='')
    hint = input()
    total_words = load_words("Wordle Answers.txt")
    correct_word_dic, has_to_contain, bad_letters = get_correct_word_counter(guess, hint, {}, {}, [])
    total_words = get_total_word_list(total_words, correct_word_dic, has_to_contain, bad_letters)
    prev_guess = guess
    counter = 1
    while True:
        correct_word_dic, has_to_contain, bad_letters = get_correct_word_counter(prev_guess, hint,
                                                                                 correct_word_dic,
                                                                                 has_to_contain, bad_letters)
        # print("TotalWords Before:", len(total_words))
        total_words = get_total_word_list(total_words, correct_word_dic, has_to_contain, bad_letters)
        prev_guess = minimax(correct_word_dic, has_to_contain, bad_letters, 0, total_words)
        if prev_guess in total_words:
            total_words.remove(prev_guess)

        # print("TotalWords After:", len(total_words))
        print("Here is the best word to use based off of your hint:", prev_guess)

        print("Please print your hint:", end='')
        hint = input()
        counter += 1
        if counter == 7:
            break


def get_total_word_list(total_words, correct_word_dic, has_to_contain, bad_letters):
    final_list = []

    for word in total_words:
        for index in range(len(word)):
            if index in correct_word_dic and correct_word_dic[index] == word[index]:
                final_list.append(word)
                break
            if word[index] in has_to_contain and index not in has_to_contain[word[index]]:
                final_list.append(word)
                break
            """
            if index in correct_word_dic and word[index] != correct_word_dic[index]:
                total_words.remove(word)
                break
            elif word[index] in correct_word_dic.values() and index in correct_word_dic and index != get_key(word[index], correct_word_dic):
                total_words.remove(word)
                break
                """

            """
            elif word[index] not in bad_letters:
                final_list.append(word)
                break
    for word in final_list:
        for index in range(len(word)):
            if word[index] in bad_letters:
                final_list.remove(word)
                break
                """
            """
        if word in final_list:
            for index in range(len(word)):
                if word[index] in bad_letters:
                    final_list.remove(word)
                    break
                elif index in correct_word_dic and correct_word_dic[index] != word[index]:
                    final_list.remove(word)
                    break
                    """


    return total_words


def get_key(val, correct_word_dic):
    for key, value in correct_word_dic.items():
        if val == value:
            return key


def analyze_heuristic(guess, correct_word_dic, has_to_contain, bad_letters):
    score = 0
    for index in range(len(guess)):
        if index in correct_word_dic and guess[index] == correct_word_dic[index]:
            score += 1006
        elif index in correct_word_dic and guess[index] != correct_word_dic[index]:
            score = -999999999999999
            break
        elif guess[index] in has_to_contain and index in has_to_contain[guess[index]]:
            print("gets here", guess)
            score = -99999999999999
            break
        elif guess[index] in has_to_contain and index not in has_to_contain[guess[index]]:
            score += 201
        elif guess[index] in bad_letters and guess[index] not in correct_word_dic:
            score = -999999999999
            break
        else:
            score += 1
    return score


def get_correct_word_counter(guess, hint, correct_word_dic, has_to_contain, bad_letters):
    for index in range(len(hint)):
        if hint[index] == "%" and index not in correct_word_dic:
            correct_word_dic[index] = guess[index]
            """
            if guess[index] not in frequency:
                frequency[guess[index]] = 1
            else:
                frequency[guess[index]] += 1
            """
        elif hint[index] == "!" and guess[index] not in bad_letters:
            bad_letters.append(guess[index])
        elif hint[index] == "#" and guess[index] not in has_to_contain and guess[
            index] not in correct_word_dic.values():
            has_to_contain[guess[index]] = [index]
        elif hint[index] == "#" and guess[index] in has_to_contain and guess[index] not in correct_word_dic.values() and guess[index] not in has_to_contain[guess[index]] and guess[index] not in bad_letters:
            has_to_contain[guess[index]].append(index)

            """
            if guess[index] not in frequency:
                frequency[guess[index]] = 1
            else:
                frequency[guess[index]] += 1
            """

    return correct_word_dic, has_to_contain, bad_letters


def minimax(correct_word_dic, has_to_contain, bad_letters, index, word_list):
    min_val = -999999999999
    best_word = word_list[0]
    for word in word_list:
        val = analyze_heuristic(word, correct_word_dic, has_to_contain, bad_letters)
        if min_val < val:
            min_val = val
            best_word = word

    return best_word


def play_game():
    play = True
    guess = [None] * 6
    hints = ["!!!!!"] * 6
    counter = 0
    total_words = load_words("Wordle Answers.txt")
    correct_word = total_words[randint(0, len(total_words))]

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
            guess[counter] = random_guess(total_words)
        else:
            guess[counter] = get_user_guess()

        temp_guess = guess[counter]
        print("Your guess is:", temp_guess)
        temp_hint = check_move(temp_guess, correct_word)
        hints[counter] = temp_hint
        # check to see if hint is correct (meaning guess is correct word)
        if check_hint(hints[counter]):
            break
        temp_index = 0
        print(len(total_words))
        for h in temp_hint:
            if h == "!":
                total_words = cannot_contain(temp_guess[temp_index], total_words)
                # print("!:", len(total_words))
                # print(total_words)
            elif h == "#":
                total_words = must_contain(temp_guess[temp_index], total_words)
                # print("#:", len(total_words))
                # print(total_words)

            elif h == "%":
                total_words = correct_position(temp_guess[temp_index], total_words, temp_index)
                # print("%:", len(total_words))
                # print(total_words)

            temp_index += 1
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


def correct_position(character, word_list, index):
    new_list = []
    for word in word_list:
        if word[index] == character:
            new_list.append(word)
    return new_list


def must_contain(character, word_list):
    new_list = []
    for word in word_list:
        if character in word:
            new_list.append(word)
    return new_list


def cannot_contain(character, word_list):
    new_list = []
    for word in word_list:
        if character not in word:
            new_list.append(word)
    return new_list


"""
def correct_position(guess, hint, word_list):
    new_list = []
    index = 0
    for h in hint:
        if h == "%":
            for word in word_list:
                if word[index] == guess[index]:
                    new_list.append(word)
        index += 1

    return new_list

def must_contain(guess, hint, word_list):
    new_list = word_list
    index = 0
    for h in hint:
        if h == "#":
            for word in word_list:
                if guess[index] not in word:
                    new_list.remove(word)
        index += 1

    return new_list

def cannot_contain(guess, hint, word_list):
    new_list = word_list
    index = 0
    for h in hint:
        if h == "!":
            for word in word_list:
                if guess[index] in word:
                    new_list.remove(word)
        index += 1

    return new_list
"""

"""
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
"""


def get_updated_words(necessary_letters, bad_letters, word_list):
    new_list = []
    for word in word_list:
        for character in word:
            if character not in bad_letters:
                new_list.append(word)
                break

    for word in new_list:
        for character in word:
            if character not in necessary_letters:
                new_list.remove(word)
                break
    print(new_list)
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


"""
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
"""


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
    # play_game()
    # correct word is snake
    """
    guess = "snaaa"
    hint = "%%%!!"
    total_words = load_words("Wordle Answers.txt")

    correct_word_dic, has_to_contain, bad_letters = get_correct_word_counter(guess, hint, {},
                                                                             [], [])

    total_words = get_total_word_list(total_words, correct_word_dic, has_to_contain)
    prev_guess = minimax(correct_word_dic, has_to_contain, bad_letters, 0, total_words)
    """
    online_play()
