from hashlib import new
import random
from collections import OrderedDict
import string
from textwrap import wrap
from this import d
import matplotlib.pyplot as plt
import numpy as np
import statistics

def by_size(words, size):
    return [word for word in words if len(word) == size]

def count_letters(word_list):

    histogram = OrderedDict((c,0) for c in string.ascii_lowercase)

    for word in word_list:
        for c in word:
            if c in string.ascii_letters:
                histogram[c.lower()] += 1

    return histogram

# Global for next_guess function
verbose_print = True
# verbose_print = False

def next_guess(guess, word_chosen, word_list):
    """
    This function reduces the word list based on the guess and actual word.

    Definitions
    exact match = green square = right letter, right spot
    inexact match = yellow square = right letter, wrong spot
    unmatched = black square and not a green or yellow square
    overmatched = black square but letter already marked in other green or yellow squares
    """
    # Local vars
    guess_copy = list(guess)
    word_copy = list(word_chosen)

    # Step 1: Mark up the word with matches.

    # Mark green with "2" and the yellow squares with "1". As with the real game, the first yellow 
    # match is marked if there is more than one instance of that letter. 

    for i, letter in enumerate(guess):
        if letter == word_chosen[i]: 
            word_copy[i] = " "
            guess_copy[i] = "2"

    for i, letter in enumerate(guess_copy):
        if guess_copy[i] in word_copy:
            index = word_copy.index(guess_copy[i])
            word_copy[index] = " "
            guess_copy[i] = "1" 

    # Build a dictionary of unmatched letters and overmatched letters, e.g. { "e": 1, "j": 2 }
    # Letters with a count of 1 are unmatched. Letters with a count > 1 are overmatched. See Step 4.

    tempguess = list(guess)
    word_delete_list = {}

    for i, letter in enumerate(guess_copy):
        if letter != "1" and letter != "2" and letter not in word_delete_list.keys():
            word_delete_list[letter] = 1

    for i, letter in enumerate(guess_copy):
        if letter == "1" and tempguess[i] in word_delete_list.keys():
            word_delete_list[tempguess[i]] += 1

    # Debug info for this step.

    print("Exact matches marked with '2'. Inexact matches marked with '1'")
    print("Guess: ", list(guess))
    print("Guess: ", guess_copy)
    print("Answer:", list(word_chosen))
    print("Answer:", word_copy)
    print("Delete counts:", word_delete_list)
    print("\nCount of initial word list:", len(word_list))

    # Step 2: Filter words by green letter placements. Create a parallel filtered words list
    # that has green letters removed in prep for Step 3. Green letters replaced with "-".

    chosen_words = list(word_list)
    chosen_wordsfilt = list(word_list) 

    exact_matches = False
    while "2" in guess_copy:
        index = guess_copy.index("2")
        letter = guess[index]
        exact_matches = True

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

        # print("Exact matches pass:",len(chosen_words))
        # print(guess_copy)

    if verbose_print and exact_matches:
        the_words = list(zip(chosen_words, chosen_wordsfilt))
        print("\nCount of filtered word list after exact letter matches:",len(the_words))
        # print(the_words)

    # Step 3: Filter by words for yellow letters. We've already filtered out and removed the green letter
    # matches, so if there's a repeat letter that was both green and yellow, this step will keep that
    # word in the list. 

    inexact_matches = False
    if "1" in guess_copy:
        inexact_matches = True

        # We're going to rebuild the word guess list by adding words that have all inexact matches.
        new_words = list()
        new_wordsfilt = list()

        # Make a list of the letters that must be present for the word to be a good guess.
        letters = list()
        for i, letter in enumerate(guess_copy):
            if letter == '1':
                letters.append(guess[i])
        # print("Inexact letters", letters)

        # Now we need to go through every filtered word from the previous steps and pick the matches
        for i, word in enumerate(chosen_wordsfilt):
            temp_word = list(word)

            if all(item in temp_word for item in letters):
                new_words.append(chosen_words[i])
                new_wordsfilt.append(chosen_wordsfilt[i])

        # New word list
        chosen_words = new_words
        chosen_wordsfilt = new_wordsfilt

    if verbose_print and inexact_matches:
        the_words = list(zip(chosen_words, chosen_wordsfilt))
        print("\nCount of filtered word list after inexact letter matches:",len(the_words))
        # print(the_words)

    # Step 4: Remove words containing unmatched and overmatched letters. Again we're using the filtered list for
    # this, which has green letters removed. In Step 1, we built a dictionary of unmatched letters (count = 1) and
    # overmatched letters (count = yelow letters + black letters that are the same). 
    # 
    # For example, let's say my guess has 1 "z" and 2 "e" in it. The "z" is a black square. One "e" is marked yellow,
    # and the other "e" is marked black. This means that any dictionary word with a "z" has to be removed, and any 
    # dictionary word with two or more "e" has to be removed. In this case, my removal dictionary looks like:
    # word_delete_list = { "z" : 1, "e" : 2 }

    # Again, we're going to use a copy to modify the word lists.
    final_chosen_words = list(chosen_words)
    final_chosen_wordsfilt = list(chosen_wordsfilt)

    # Go through the filtered word list and only pull out the words with unique non-matching letters. 
    for i, word in enumerate(chosen_wordsfilt):
        for key in word_delete_list:
            if word.count(key) >= word_delete_list[key]:
                final_chosen_words.remove(chosen_words[i])
                final_chosen_wordsfilt.remove(chosen_wordsfilt[i])
                break

    if verbose_print:
        the_words = list(zip(final_chosen_words, final_chosen_wordsfilt))
        print("\nCount of filter word list after non-matching letters and too many inexact matching letters:",len(the_words))
        # print(the_words)

    if verbose_print:
       removed_words = np.setdiff1d(word_list, final_chosen_words).tolist()
       print("\nTotal words removed in this step:", len(removed_words))
       print(removed_words)

    return final_chosen_words

def iterate_until_solved(guess, word_chosen, word_list):
    """
    This iterates starting with the seed word and choosing randomly until the word is found.
    It returns a count of the words at each step.
    """
    # Keep track so we don't repeat guesses on each pass
    guess_list = list()
    word_count_per_step = list()
    guess_list.append(guess)

    # Initialize the random number generator. This just ensures we get the same randomness each time we
    # run the algorithm, which helps check for mistakes.
    random.seed(100)

    # The first wordcount is the entire list
    word_count_per_step.append(len(word_list))

    # Loop through and reduce the word list until we get the answer
    print("----------------------------------------------")
    passcount = 1
    while guess != word_chosen:
        # Make our first simplification
        print("PASS #",passcount)
        # print("\n")
        chosen_words = next_guess(guess, word_chosen, word_list)

        # New subset of words
        word_list = chosen_words
        # Make a random new guess and make sure we didn't guess it already
        guess = random.choice(word_list)
        while guess in guess_list:
            guess = random.choice(word_list)
        
        # Loop back around to try the next guess
        guess_list.append(guess)
        word_count_per_step.append(len(word_list))
        print("Next guess:",guess)
        passcount += 1

    return word_count_per_step

# This is a link to the wordl allowed guesses and answers (alphabatized)
# https://www.reddit.com/r/wordle/comments/s4tcw8/a_note_on_wordles_word_list/
# https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c
# https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b 

def plot_words_per_step(words_per_step):
    """
    Plots min, max, mean curves for each step
    """

    # words_per_step is a list with rows of different lengths. We need to make the rows the same length
    # in order to subset a numpy array.
    row_lengths = []
    for row in words_per_step:
        row_lengths.append(len(row))
    max_length = max(row_lengths)

    for row in words_per_step:
        while (len(row) < max_length):
            row.append(0)

    words_per_step_array = np.array(words_per_step)

    # Init the plot lines
    means = [0] * max_length
    mins = [0] * max_length
    maxes = [0] * max_length
    x = list(range(1, max_length+1))

    # Calculate the stats on guesses at each step
    for i in range(0, len(means)):
        mins[i] = min(words_per_step_array[:,i])
        maxes[i] = max(words_per_step_array[:,i])
        means[i] = statistics.mean(words_per_step_array[:,i])

    # Print the values
    print(x)
    print("Mins: ", mins)
    print("Maxes:", maxes)
    print("Means:", means)

    # Plot the three curves. Skip the first step because it's the entire dictionary
    plt.plot(x[1:], mins[1:], label = "min")
    plt.plot(x[1:], maxes[1:], label = "max")
    plt.plot(x[1:], means[1:], label = "mean")
    plt.legend()
    plt.title("Words in dictionary at each guess")
    plt.xlabel("Step")
    plt.ylabel("Word Count")
    plt.show()

def plot_numguess(numguesses):
    """
    Plots histogram of guesses
    """

    print("Number of guesses per word:",numguesses)

    bins=list(range(1,max(numguesses)+1))
    ticks = list(range(1,max(numguesses)))

    histogram = np.histogram(numguesses, bins=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    histogram = np.histogram(numguesses, bins)
    print(histogram)

    plt.bar(histogram[1][0:max(numguesses)-1], histogram[0], width=0.5, color='g')
    plt.title("Histogram of number of steps to solve each word")
    plt.xticks(ticks)
    plt.xlabel("Steps")
    plt.ylabel("Count")
    plt.show()


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
    # Histogram of letters from the total word list. 
    # ------------------------------------------------------------------------------------------------
    
    # print("Histogram of letters in full word list")
    # histogram = count_letters(word_list)
    # histogram = dict(sorted(histogram.items(), key=lambda item: item[1], reverse=True))
    # print(histogram)
    # print("\n")

    # plt.bar(histogram.keys(), histogram.values(), width=0.5, color='g')
    # plt.title('Histogram of letters in full word list')
    # plt.ylim(ymax=7000)
    # plt.show()

    # ------------------------------------------------------------------------------------------------
    # Histogram of letters from the answer list. 
    # ------------------------------------------------------------------------------------------------
    
    # print("Histogram of letters in answer key")
    # histogram = count_letters(word_answer_list)
    # histogram = dict(sorted(histogram.items(), key=lambda item: item[1], reverse=True))
    # print(histogram)
    # print("\n")

    # plt.bar(histogram.keys(), histogram.values(), width=0.5, color='g')
    # plt.title('Histogram of letters in answer key')
    # plt.show()

    # ------------------------------------------------------------------------------------------------
    # Algorithm test words - single pass through solver
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
    # # Too many inexact matching letters
    # guess = "ezzze"
    # word_chosen = "hoped"
    # next_guess(guess, word_chosen, word_list)

    # ------------------------------------------------------------------------------------------------
    # Algorithm test - full solve
    # ------------------------------------------------------------------------------------------------
    
    # guess = "orate"
    # word_chosen = "hoped"
    # numguesses = iterate_until_solved(guess, word_chosen, word_list)
    # print("Guesses to solve: ", numguesses)

    # ------------------------------------------------------------------------------------------------
    # Test seed word against entire list. Count number of guessed per word and also number
    # of words at the end of each guess step.
    # ------------------------------------------------------------------------------------------------

    # guess = "orate"
    # numguesses = list()
    # words_per_step = list()

    # for answerword in word_answer_list:
    #     word_count_per_step = iterate_until_solved(guess, answerword, word_list)
    #     words_per_step.append(word_count_per_step)
    #     numguesses.append(len(word_count_per_step))

    # plot_words_per_step(words_per_step)
    # plot_numguess(numguesses)

    # ------------------------------------------------------------------------------------------------
    # Test seed word against a sample of the entire list
    # ------------------------------------------------------------------------------------------------

    shorter_word_list = random.sample(word_guess_list, 2000)
    new_word_list = shorter_word_list + word_answer_list
    guess = "orate"
    numguesses = list()
    words_per_step = list()

    for answerword in word_answer_list:
        word_count_per_step = iterate_until_solved(guess, answerword, new_word_list)
        words_per_step.append(word_count_per_step)
        numguesses.append(len(word_count_per_step))

    plot_words_per_step(words_per_step)
    plot_numguess(numguesses)

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

# d = np.random.laplace(loc=15, scale=3, size=500)
# n, bins, patches = plt.hist(x=d, bins='auto', color='#0504aa',
#                             alpha=0.7, rwidth=0.85)
# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.title('Histogram of letters in full word list')
# plt.text(23, 45, r'$\mu=15, b=3$')
# maxfreq = n.max()
# # Set a clean upper y-axis limit.
# plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
# plt.show()
#
# How to manually initialize a 2D array
#    words_per_step = [[0 for x in range(20)] for y in range(len(word_answer_list))]
