import random

def by_size(words, size):
    return [word for word in words if len(word) == size]

def next_guess(guess, wordChosen, wordList):
    """
    This function reduces the word list based on the guess and actual word.
    """

    # The guess and answer are marked up as we search. Make copies.
    guessCopy = list(guess)
    wordCopy = list(wordChosen)
    print("Guess and answer word:")
    print(guessCopy)
    print(wordCopy)
    print("\n")

    # Mark the correct guesses. "2" for exact match, "1" for an inexact match (right letter, wrong spot).
    # The exact matches are removed first. Then additional matches are marked sequentially.

    for i, letter in enumerate(guess):
        if (letter == wordChosen[i]): 
            wordCopy[i] = ""
            guessCopy[i] = "2"
    print("Exact matches marked with 2:")
    print(guessCopy)
    print(wordCopy)
    print("\n")

    for i, letter in enumerate(guessCopy):
        if (guessCopy[i] in wordCopy):
            index = wordCopy.index(guessCopy[i])
            wordCopy[index] = ""
            guessCopy[i] = "1" 
    print("Inexact matches marked with 1:")
    print(guessCopy)
    print(wordCopy)
    print("\n")

    # First filter acceptable words by exact letter placements

    chosenWords = wordList      # Word list we're going to subset based on matches
    chosenWordsFilt = wordList  # Same word list, but we're going to remove matched letters to prevent dupe matches

    while "2" in guessCopy:
        index = guessCopy.index("2")
        letter = guess[index]

        newChosenWords = [word for word in chosenWords if word[index] == letter]
        newChosenWordsFilt = [word for word in chosenWordsFilt if word[index] == letter]

        for i, word in enumerate(newChosenWordsFilt):
            newChosenWordsFilt[i] = word[0:index] + "-" + word[index+1:len(word)]

        chosenWords = newChosenWords
        chosenWordsFilt = newChosenWordsFilt
        guessCopy[index] = "-"

        print("Exact matches pass:")
        print(len(chosenWords))
        print(guessCopy)

    print("\n Filtered word list after exact letter matches.")
    thewords = list(zip(chosenWords,chosenWordsFilt))
    print(thewords)
    print(len(thewords))
    print("\n")

    # Then filter by words that contain the remaining matched letters. We've already filtered exact letter matches, so
    # if we find a matching letter that's in the exact location, it's not a viable word.

    newwords = list()
    newwordsfilt = list()
    while "1" in guessCopy:
        index = guessCopy.index("1")
        letter = guess[index]

        for i, word in enumerate(newChosenWordsFilt):
            if letter in word:
                j = word.index(letter)

                if j != index:
                    newwords.append(newChosenWords[i])
                    newwordsfilt.append(word[0:j] + "-" + word[j+1:len(word)])
        
        chosenWords = newwords
        chosenWordsFilt = newwordsfilt
        guessCopy[index] = "-"

        print("Inexact matches pass:")
        print(len(chosenWordsFilt))
        print(guessCopy)

    print("\n Filtered word list after inexact letter matches.")
    thewords = list(zip(chosenWords,chosenWordsFilt))
    print(thewords)
    print(len(thewords))
    print("\n")

    return chosenWords, chosenWordsFilt

# This is a link to the wordl allowed guesses and answers (alphabatized)
# https://www.reddit.com/r/wordle/comments/s4tcw8/a_note_on_wordles_word_list/
# https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c
# https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b 

# The purpose of this was to see if there are better starting guesses for solving worlde quickly. What this does
# currently is to iterate based on a starting guess and the known answer. 
#
# To adapt this for an analysis of all solutions:
#   1. Pick a starting word like "irate" or do an histogram on the dictionary to find other good starting words.
#   2. Btree on each wordle solution. 
#       Start with a single solution
#       Run every possible second guess after "irate"
#       Record the words that produce the fewest words for the next step
#       Run those words through to see how many more steps it takes to solve
#   3. Repeat for each wordle solution.
#   4. Process the list to see if there are a subset of words that get you to a solution faster


def main():
    """
    Main Code
    """

    # Dictionary of guesses. The worlde list does not contain the answers, just the guesses. This strips \n.
    # wordBank = "/usr/share/dict/words"
    wordBank = "wordle-allowed-guesses.txt"
    with open(wordBank) as f:
        wordGuessList = f.read().splitlines() 

    # List of all answers
    wordAnswersBank = "wordle-answers-alphabetical.txt"
    with open(wordAnswersBank) as f:
        wordAnswerList = f.read().splitlines() 

    # Master word list, includes answers and guesses
    wordList = wordGuessList + wordAnswerList
    wordList.sort()

    # Choose first guess and indicate answer word
    guess = "prank"
    wordChosen = "frame"

    # Keep track so we don't repeat guesses on each pass
    guessList = list()
    guessList.append(guess)

    # Loop through and reduce the word list until we get the answer
    passcount = 1
    while guess != wordChosen:
        # Make our first simplification
        print("PASS #",passcount)
        chosenWords, chosenWordsFilt =  next_guess(guess, wordChosen, wordList)

        # New subset of words
        wordList = chosenWords

        # Make a random new guess and make sure we didn't guess it already
        guess = random.choice(wordList)
        while guess in guessList:
            guess = random.choice(wordList)
        
        # Loop back around to try the next guess
        guessList.append(guess)
        print("Guess:",guess)
        passcount += 1

if __name__ == "__main__":
    main()


# Misc code I didn't use, but don't want to forget

# This brings in \n line endings
# wordGuessList = open(wordBank).readlines()

# One way to get 5 letter words from entire dictionary
# fiveletterwords = by_size(wordGuessList, 5)
# print(fiveletterwords)
# print(len(fiveletterwords))

# Another way to pick a radmon 5 letter word
# Pick a random 5-letter word
# while True:
#     wordChosen = random.choice(wordGuessList)
#     if len(wordChosen) == 5: 
#         break
# print (wordChosen)
