# Wordle Analysis Tool

## Intro

Everyone's addicted to Wordle! I wrote this because I was curiuos about a few things.

1. What is the best word to start with?
2. How many steps does it take before the large list of words (~13,000) get pared down to something small?
3. Given a dictionary of words, how many steps would it take on average to solve a Wordle?
4. After a couple of steps, is there a good subset of words to know that will ensure success?
5. Assuming the author of Wordle tried to pick well known words, and assuming that most people don't know 13,000 5-letter words, what is the most realistic number of solving steps? In other words, should an average person be able to solve every Wordl in 6 tries?

This tool isn't design to help you make your next guess. It's designed to run through many wordle rounds in order to do analysis on the overall game.

## Caveats

Wordle's *answer key* and *dictionary of allowed words* are both freely available online and easily viewable in Chrome's developer console. These two lists are included in this repo, but they've been alphabetized in the hopes that they aren't too much of a spoiler. Still, **don't look if you don't want to know**. I'm using these word lists as part of the solving algorithm.

As you can see from the code, I'm not an expert Python developer. I've been learning both Python and Data Science, and this seemed like a fun real-world exercise. As with any language, you have to program in it for a while to become fluent. If you see areas where I could have coded something in a more python-like way, please make an issue or leave a pull request.

Finally, this is work in progress.

## The Solving Algorithm

You feed the guess algorithm with 1) your word guess, 2) the answer word, and a 3) dictionary of words that contains all allowable word guesses and answer words. The guess algorithm does these steps:

1. Mark the guess word with "2" for exact matches (right letter, right spot), aka green squares. Mark the guess word with "1" for inexact matches (right letter, wrong spot) matches, aka yellow squares. As with the real Wordle game, if an inexact matching letter appears in multiple places in a word, the first place is the one marked.
2. Filter the dictionary of words based on the exact letter placements. For both debugging purposes and for Step 3, two dictionaries are created. The first is the filtered word list. The second is the filtered word list with "-" in place of the exact character matches.
3. Filter the dictionary of words based on the remaining inexact letters, the yellow squares. This filtering uses the word list from Step 2 with the "-" in place of the exact letter matches so that if you have two of the same letter, the exact matches are removed so that they don't also count as inexact matches.
4. Finally, remove words from the dictionary that contain unmatched letters, the black squares. One caveat here is if a letter is in both a yelllow square and a black square, we don't try and remove words that contain only one instance of that letter, rather than two (or more). This was for implementation expediency, but it technically means that there could be a very few number of words left that aren't actually good guesses because they contain one or more inexact matching letters. I will go back and fix this at some point. I believe this impact to be very small relative to the stats I'm trying to gather.

So this guess algorithm represents one guess. To run the algorithm repeatedly towards a solution, you have to keep making guesses, each time feeding the further-reduced list of words. In the code currently, this is done by started with a seed word that represents the highest frequency of letters and then having the algorithm randomly pick the next word guess from the filtered dictionary produced by the previous guess. The algorithm quickly converges to a small list of words, but we're at the mercy of the random guesses made by the computer at that point.

## --------------- SPOILERS BELOW ----------------

## Learnings So Far

### What is the best word to start with?

This was the first surprise. Let's take a look at two histograms. The first histogram shows the distribution of letters in the entire word list (allowable guesses + answers). The second shows a histogram of only the answer list. Based on this information, you would choose AROSE with the first list and ORATE with the second. Of cousre, we only care about the answers, so ORATE is the world we'll start with in the rest of the simualtions.

You might wonder why these are different, though. The short answer is that the allowable guesses list has a shockingly high number of words that that most people, msylef included, have never heard of. The guess list wasn't intended to be only common words. It was apparently intended to cover most 5-letter words in a dictionary. I'll look into this in more detail later.

![](FullHistogram.png)
![](AnswersHistogram.png)

### How many steps does it take to get to a manangeable list?

TODO

### How many steps would it take on average to solve a Wordle?

TODO

### After a couple of steps, is there a good subset of words to know that will ensure success?

TODO

### How much of a difference does a smaller dictionary make?

TODO
