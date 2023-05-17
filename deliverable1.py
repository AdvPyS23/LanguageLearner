# Load libraries 
import pandas as pd
import numpy as np

# Basic User imput (without UI)
keepgoing = True
i = 0
while keepgoing:
    word = input("Please input a word:")
    trans = input("Please input the translation:")
    additional = input("Would you like to add additonal information? (y/n)")
    if lower(additional) == y:
        pos = input("What is the part of speech of the word?")
        topic = input("What topic is this word part of?")
        difficuly = input("What difficulty level is this word?")
    else:
        pos,topic,diffculy = None/None/None
    # On  first iteration: create dataframe
    if i == 0:
        dictionary = pd.DataFrame({'word':word, 'translation': trans, 'Part of Speech': pos, 'Topic':topic, 'Difficulty': difficulty})
    else:
        # on each subsequent itteration, add a line to the df
        newline = pd.Series({'word': word, 'translation': trans, 'Part of Speech': pos, 'Topic':topic, 'Difficulty': difficulty})
        dictionary = dictionary.append(newline)
    i = i + 1
    check = input("Press any key to continue entering words, or q to quit")
    if lower(check) == q:
        keepgoing = False

# Arrange into dataframe:

