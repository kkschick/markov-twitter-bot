#!/usr/bin/env python

import sys
import string
import random

def make_chains(corpus, markov_dict):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    list_of_words = corpus.strip().split()
    

    for i in range(len(list_of_words)-2):
        if (list_of_words[i], list_of_words[i + 1]) not in markov_dict:
            markov_dict[(list_of_words[i], list_of_words[i + 1])] = [list_of_words[i + 2]]
        else:
            markov_dict[(list_of_words[i], list_of_words[i + 1])].append(list_of_words[i + 2])

    return markov_dict

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    list_of_keys = chains.keys()

    list_of_strings = []

    key = random.choice(list_of_keys)
    value = chains[key]
    select_value = random.choice(value)

    list_of_strings.extend([key[0], key[1], select_value])

    while True:
        key = (list_of_strings[-2], list_of_strings[-1])
        value = chains.get(key, "None")
        if value == "None":
            break
        select_value = random.choice(value)
        list_of_strings.append(select_value)

    random_string = ''

    for item in list_of_strings:
        random_string += item + ' '

    random_string = random_string.rstrip().capitalize() + '.'
    return random_string

def open_files(filename, markov_dict):

    text = open(filename)
    text = text.read()
    
    dict_of_words = make_chains(text, markov_dict)


    # input_text = ''
    # for char in text:
    #     if char not in string.punctuation:
    #         input_text += char
    return dict_of_words

def main():
    args = sys.argv
    markov_dict = {}
    # Change this to read input_text from a file
    for item in args[1:]:
        markov_dict = open_files(item, markov_dict)

    random_text = make_text(markov_dict)
    print random_text

if __name__ == "__main__":
    main()
