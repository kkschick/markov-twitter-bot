#!/usr/bin/env python

import sys
# import string
import random
import twitter
import twittercredentials

api = twitter.Api(consumer_key=twittercredentials.TWITTER_CONSUMER_KEY,
                  consumer_secret=twittercredentials.TWITTER_CONSUMER_SECRET,
                  access_token_key=twittercredentials.TWITTER_ACCESS_TOKEN_KEY,
                  access_token_secret=twittercredentials.TWITTER_ACCESS_TOKEN_SECRET)


def make_chains(corpus, markov_dict, n):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    # Taking text input, stripping leading/trailing chars, 
    list_of_words = corpus.strip().split()
    
    # Looping through the list until you get to n from the end
    for i in range(len(list_of_words) - n):

        # Creating a tuple with n number of values
        tup = tuple(list_of_words[i + x] for x in range(n))

        # If tuple doesn't already exist, add it to the dict along with its value
        if tup not in markov_dict:
            markov_dict[tup] = [list_of_words[i + n]]

        # If it does exist, append it, along with its value
        else:
            markov_dict[tup].append(list_of_words[i + n])

    return markov_dict

def make_text(chains, n):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""

    # Create a list of the keys in the dict
    list_of_keys = chains.keys()

    # Create an empty list to put the random text into
    list_of_strings = []

    # Create an empty list of words that start sentences
    starting_words = []

    # Loop through the dict keys and find the starting words and add them to the starting_words list
    for item in list_of_keys:
        if item[0] == 'I' or item[0] == 'The' or item[0] == 'There' or item[0] == 'It':
            starting_words.append(item)

    #chooses one of the tuples from starting_words to use as first key
    key = random.choice(starting_words)

    #finds value associated with that key
    value = chains[key]

    #randomly chooses one of the items in the list of values (if only one, chooses that one)
    select_value = random.choice(value)

    #adds the words in key to list_of_strings
    for i in range(len(key)):
        list_of_strings.append(key[i])

    #adds the value to end of list_of_strings
    list_of_strings.append(select_value)
    random_string = " ".join(list_of_strings)

    #finds length of random_string
    length = len(random_string)

    while length <= 140:       #makes sure final string is short enough for Twitter
        #defines the key based on last n words in list_of_strings
        key = tuple(list_of_strings[(-n + x)] for x in range(n))        
        #finds key in dictionary.  If key exists, returns value.  Else, returns None
        value = chains.get(key, None) 
        if value == None: #exits loop if None
            break
        #randomly chooses one of the items in the list of values
        select_value = random.choice(value) 
        list_of_strings.append(select_value) #adds select_value to list_of_strings
        #defines new_string that is select_value added to random_string
        new_string = random_string + " " + select_value 
        length = len(new_string) #finds length of new_string
        if length <= 140: #assigns random_string to new_string if new_string <= 140 char
            random_string = new_string

    return random_string

def write_tweets(random_text):

    status = api.PostUpdate(random_text)


def open_files(filename, markov_dict, n):

    # Open and read files into a string called 'text'
    text = open(filename)
    text = text.read()

    # Strips out punctuation
    # input_text = ''
    # for char in text:
    #     if char not in string.punctuation:
    #         input_text += char

    input_text = text

    # Runs the function make_chains on the file and adds output to dict_of_words
    dict_of_words = make_chains(input_text, markov_dict, n)

    return dict_of_words

def main():
    args = sys.argv

    # Creates empty dictionary
    markov_dict = {}

    # Iterates through files and runs open_files on each file; adds returned dict to markov_dict
    for item in args[1:]:
        markov_dict = open_files(item, markov_dict, 2)

    # Runs make_text on the markov_dict
    random_text = make_text(markov_dict, 2)

    # Prints randomly generated text
    print random_text

    write_tweets(random_text)

if __name__ == "__main__":
    main()
