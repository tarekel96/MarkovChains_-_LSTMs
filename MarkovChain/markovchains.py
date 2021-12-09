# -*- coding: utf-8 -*-
"""MarkovChains.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qAY7uIiM5cXAXvRDFmj9UIfwrUkAKa98
"""

import pandas as pd
import numpy as np
import random # used to randomly choose a word from list of words
import string # needed to remove punctation from words

def remove_punc(word, punc_set = string.punctuation):
  return ''.join(ch for ch in word if ch not in punc_set)

"""Preprocess File"""

def parse_txt_file(filename="/content/nursery_rhymes.txt"):
  words = []
  
  with open(filename) as file:
    line = file.read()
    # replacing line breaks and carriage return with a space char
    line = line.replace('\r', ' ').replace('\n', ' ').strip()
    
    # splitting line str into list of words
    new_words = line.split(' ')
    # filter out empty and space chars
    new_words = [word.lower() for word in new_words if word not in ['', ' ']]
    new_words = [remove_punc(word) for word in new_words]
    # assign new words to words list
    words = words + new_words
  return words

words = parse_txt_file()

# Show count of many words there are
print(f'Corpus size: {len(words)} words.')
# print a few words to show parsing worked
print(words[slice(10)])

"""Build the transition probabilities


*   Represent transitions as a dictionary where the keys are the distinct words and the value is the list of words that appear after that respective key

1st order Markov Chain method
"""

def gen_1st_order_chain(words):
  chain = {}  
  n_words = len(words)  
  for i, key in enumerate(words):  
      if n_words > (i + 1):
          word = words[i + 1]
          if key not in chain:
              chain[key] = [word]
          else:
              chain[key].append(word)
  return chain

chain = gen_1st_order_chain(words)
print('Chain size: {0} distinct words.'.format(len(chain)))

"""Why duplicates are not a problem:

*   If a word appears multiple times in the list, and take a random sample from the list during a transition, there’s a higher likelihood that word would be picked proportional to the number of times it appeared after the key relative to all the other words in the corpus that appeared after that key

Generating rhyme from the Markov Chain requires only a starting word and a phrase length. To generate a phrase:


1.   Randomly select a starting word from the corpus
2.   Make rhyme length 20 words long
3.   Repeat until have 30 lines of these.

First order Markov Chain rhyme method
"""

# First order rhyme generator
def gen_1st_order_rhyme(words, chain):
  rand_rhyme = ""
  rand_word_1 = random.choice(words)
  rand_rhyme = rand_word_1  
  rhyme = []
  rhyme.append(rand_word_1)
  for i in range(19):  
      rand_word_2 = random.choice(chain[rand_word_1])
      rhyme.append(rand_word_2)
      rand_rhyme += ' ' + rand_word_2
      rand_word_1 = rand_word_2
  print(rhyme)
  print(f"There are {len(rhyme)} many words.")
  return rand_rhyme

print(gen_1st_order_rhyme(words, chain))

"""2nd order Markov Chain method"""

# First order rhyme generator
def gen_2nd_order_chain(words):
  chain = {}  
  n_words = len(words)  
  for i, key1 in enumerate(words):  
      if n_words > i + 2:
          key2 = words[i + 1]
          word = words[i + 2]
          if (key1, key2) not in chain:
              chain[(key1, key2)] = [word]
          else:
              chain[(key1, key2)].append(word)
  return chain

chain_2 = gen_2nd_order_chain(words)
print(f'Chain size: {len(chain_2)} distinct word pairs.')

"""Choosing a word pair that appears somewhere in the text and then examining the transitions in the chain for that pair of words (to ensure that the 2nd order chain is operating correctly)."""

# 'to your' appears in nusery_rhymes.txt multiple times
chain_2[("to", "your")]

"""2nd order Markov Chain rhyme method"""

def gen_2nd_order_rhyme(chain, words):
    rhyme_lst = []  
    rand_word = random.randint(0, len(words) - 1)
    rhyme_lst.append(rand_word)
    key = (words[rand_word], words[rand_word + 1])
    rhyme = key[0] + ' ' + key[1]
    for i in range(19):
        rand_word_2 = random.choice(chain[key])
        rhyme_lst.append(rand_word_2)
        rhyme += ' ' + rand_word_2
        key = (key[1], rand_word_2)
    return rhyme

# testing 2nd order method
for i in range(4): print(gen_2nd_order_rhyme(chain_2, words))

def gen_nusery_rhymes(n_lines=30, output_file="markov_rhymes.txt"):
  with open(output_file, "w") as out_file:
    for i in range(n_lines):
      curr_line = gen_2nd_order_rhyme(chain_2, words)
      out_file.write(curr_line + ".\n")

gen_nusery_rhymes()

"""Sources:
*   Medium article by John Wittenauer: https://medium.com/@jdwittenauer/markov-chains-from-scratch-33340ba6535b



---


"""