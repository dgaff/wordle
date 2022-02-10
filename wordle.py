from hashlib import new
import random
from collections import OrderedDict
import string

def by_size(words, size):
    return [word for word in words if len(word) == size]

def count_letters(word_list):

    histogram = OrderedDict((c,0) for c in string.ascii_lowercase)

    for word in word_list:
        for c in word:
            if c in string.ascii_letters:
                histogram[c.lower()] += 1

    return histogram

def next_guess(guess, word_chosen, word_list):
    """
    This function reduces the word list based on the guess and actual word.
    """
    # Local vars
    guess_copy = list(guess)
    word_copy = list(word_chosen)
    print("Guess: ", guess_copy)
    print("Answer:", word_copy)
    print("\n")

    # Step 1: Mark exact (right letter, right spot) and inexact (right letter, wrong spot) matches.
    # As with the real game, the first inexact match is marked if there is more than one inexact match.

    for i, letter in enumerate(guess):
        if letter == word_chosen[i]: 
            word_copy[i] = " "
            guess_copy[i] = "2"

    for i, letter in enumerate(guess_copy):
        if guess_copy[i] in word_copy:
            index = word_copy.index(guess_copy[i])
            word_copy[index] = " "
            guess_copy[i] = "1" 

    print("Exact matches mnarked with '2'. Inexact matches marked with '1'")
    print("Guess: ", guess_copy)
    print("Guess: ", guess)
    print("Answer:", word_copy)
    print("\n")

    # Step 2: Filter words by exact letter placements. Create a parallel filtered words list
    # that has matched letters removed in prep for the last step. Matched letters contain "-".

    chosen_words = list(word_list)
    chosen_wordsfilt = list(word_list) 

    while "2" in guess_copy:
        index = guess_copy.index("2")
        letter = guess[index]

        # Create a new word list of words that only match this letter in this position
        new_chosen_words = [word for word in chosen_words if word[index] == letter]
        new_chosen_wordsfilt = [word for word in chosen_wordsfilt if word[index] == letter]

        # Now cross out the matched letter in the filtered list
        for i, word in enumerate(new_chosen_wordsfilt):
            new_chosen_wordsfilt[i] = word[0:index] + "-" + word[index+1:len(word)]

        # Prep for the next iteration of the loop and remove this matching letter from the guess
        chosen_words = new_chosen_words
        chosen_wordsfilt = new_chosen_wordsfilt
        guess_copy[index] = "-"

        # print("Exact matches pass:")
        # print(len(chosen_words))
        # print(guess_copy)

    print("\n Filtered word list after exact letter matches.")
    the_words = list(zip(chosen_words, chosen_wordsfilt))
    # print(the_words)
    print(len(the_words))
    print("\n")

    # Step 3: Filter by words that contain the remaining matched letters. We've already filtered out the exact 
    # letter matches in the previous step, so this will find words whose remaining unmatched letters fully
    # contain the inexact matched guess letters.

    if "1" in guess_copy:

        # We're going to rebuild the word guess list by adding words that have all inexact matches.
        new_words = list()
        new_wordsfilt = list()

        # Make a list of the letters that must be present for the word to be a good guess.
        letters = list()
        for i, letter in enumerate(guess_copy):
            if letter == '1':
                letters.append(guess[i])
        print("Inexact letters", letters)

        # Now we need to go through every filtered word from the previous steps and pick the matches
        for i, word in enumerate(chosen_wordsfilt):
            temp_word = list(word)

            if all(item in temp_word for item in letters):
                new_words.append(chosen_words[i])
                new_wordsfilt.append(chosen_wordsfilt[i])

        # Now we have a new word list. We still need the filtered word list to remove unique non-matching 
        # letters
        chosen_words = new_words
        chosen_wordsfilt = new_wordsfilt

    print("\n Filtered word list after inexact letter matches.")
    the_words = list(zip(chosen_words, chosen_wordsfilt))
    # print(the_words)
    print(len(the_words))
    print("\n")

    # Step 4: Remove words containing unique letters that did not match anything. If the letters are inexact 
    # matches, leave those words in the list, since we don't know which position those inexact matches are.

    # Again, we're going to use a copy to modify.
    final_chosen_words = list(chosen_words)

    # Get a list of the inexact letter matches
    inexact_letters = list()
    for i, letter in enumerate(guess_copy):
        if letter == "1":
            inexact_letters.append(guess[i])

    # Now build a list of unique letters that are not inexact matches
    unique_letters = list()
    for letter in guess_copy:
        if letter != "1" and letter != "2" and letter != '-' and letter not in inexact_letters:
            unique_letters.append(letter)
    print("Unique non-matching letters", unique_letters)

    # Go through the filtered word list and only pull out the words with unique non-matching letters. 
    for i, word in enumerate(chosen_wordsfilt):
        for letter in unique_letters:
            if letter in word:
                final_chosen_words.remove(chosen_words[i])
                break

    print("\n Filtered word list after bad letter guesses.")
    # print(final_chosen_words)
    print(len(final_chosen_words))
    print("\n")

    return final_chosen_words

def iterate_until_solved(guess, word_chosen, word_list):
    """
    This iterates starting with the seed word and choosing randomly until the word is found.
    """
    # Keep track so we don't repeat guesses on each pass
    guess_list = list()
    guess_list.append(guess)

    # Loop through and reduce the word list until we get the answer
    passcount = 1
    while guess != word_chosen:
        # Make our first simplification
        print("PASS #",passcount)
        print("\n")
        chosen_words = next_guess(guess, word_chosen, word_list)

        # New subset of words
        word_list = chosen_words
        # Make a random new guess and make sure we didn't guess it already
        guess = random.choice(word_list)
        while guess in guess_list:
            guess = random.choice(word_list)
        
        # Loop back around to try the next guess
        guess_list.append(guess)
        print("Next guess:",guess)
        passcount += 1

    return passcount

# This is a link to the wordl allowed guesses and answers (alphabatized)
# https://www.reddit.com/r/wordle/comments/s4tcw8/a_note_on_wordles_word_list/
# https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c
# https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b 

# The purpose of this was to see if there are better starting guesses for solving worlde quickly. What this does
# currently is to iterate based on a starting guess and the known answer. 
#
# To adapt this for an analysis of all solutions:
#   (DONE) 1. Pick a starting word like "irate" or do an histogram on the dictionary to find other good starting words.
#   2. Btree on each wordle solution. 
#       Start with a single solution
#       Run every possible second guess after seed word
#       Record the words that produce the fewest words for the next step
#       Run those words through to see how many more steps it takes to solve
#   3. Repeat for each wordle solution.
#   4. Process the list to see if there are a subset of words that get you to a solution faster

def main():
    """
    This contains a variety of code blocks that do different things with the word list. 
    Uncomment the desired block to test things out.
    """
    # Dictionary of guesses. The worlde list does not contain the answers, just the guesses. This strips \n.
    # wordBank = "/usr/share/dict/words"
    word_bank_file = "wordle-allowed-guesses.txt"
    with open(word_bank_file) as f:
        word_guess_list = f.read().splitlines() 

    # List of all answers
    word_answers_bank_file = "wordle-answers-alphabetical.txt"
    with open(word_answers_bank_file) as f:
        word_answer_list = f.read().splitlines() 

    # Master word list, includes answers and guesses
    word_list = word_guess_list + word_answer_list
    word_list.sort()

    print("\n\n---------------- Wordle Analyzer ----------------\n\n")

    # ------------------------------------------------------------------------------------------------
    # Histogram of letters from the answer list. ORATE has the higest frequency of letters
    # ------------------------------------------------------------------------------------------------
    # print("Histogram of letters in answer key")
    # histogram = count_letters(word_answer_list)
    # histogram = dict(sorted(histogram.items(), key=lambda item: item[1], reverse=True))
    # print(histogram)
    # print("\n")

    # ------------------------------------------------------------------------------------------------
    # Algorithm test words
    # ------------------------------------------------------------------------------------------------
    # # No letter overlap
    # guess = "orate"
    # word_chosen = "biddy"
    # # Exact letter matches only
    # guess = "brand"
    # word_chosen = "frank"
    # # Inexact letter matches only
    # guess = "orate"
    # word_chosen = "tides"
    # # All types of matches
    # guess = "orate"
    # word_chosen = "trade"
    # next_guess(guess, word_chosen, word_list)

    # ------------------------------------------------------------------------------------------------
    # Single pass through the solver
    # ------------------------------------------------------------------------------------------------
    # guess = "orate"
    # word_chosen = "trade"
    # numguesses = iterate_until_solved(guess, word_chosen, word_list)
    # print("Guesses to solve: ", numguesses)

    # ------------------------------------------------------------------------------------------------
    # Test seed word against entire list
    # ------------------------------------------------------------------------------------------------
    # guess = "orate"
    # numguesses = list()
    # for answerword in word_answer_list:
    #     num = iterate_until_solved(guess, answerword, word_list)
    #     numguesses.append(num)
    # print(numguesses)

    # ------------------------------------------------------------------------------------------------
    # Test seed word against a sample of the entire list
    # ------------------------------------------------------------------------------------------------
    shorter_word_list = random.sample(word_guess_list, 2000)
    new_word_list = shorter_word_list + word_answer_list
    guess = "orate"
    numguesses = list()
    for answerword in word_answer_list:
        num = iterate_until_solved(guess, answerword, new_word_list)
        numguesses.append(num)
    print(numguesses)


if __name__ == "__main__":
    main()


# Misc code I didn't use, but don't want to forget

# This brings in \n line endings
# word_guess_list = open(wordBank).readlines()

# One way to get 5 letter words from entire dictionary
# fiveletterwords = by_size(word_guess_list, 5)
# print(fiveletterwords)
# print(len(fiveletterwords))

# Another way to pick a radmon 5 letter word
# Pick a random 5-letter word
# while True:
#     word_chosen = random.choice(word_guess_list)
#     if len(word_chosen) == 5: 
#         break
# print (word_chosen)
