#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip3 install tensorflow')
get_ipython().system('pip3 install keras')


# In[2]:


# Tarek El-Hajjaoui
import numpy as np
import tensorflow as tf
import random
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding


# In[3]:


import string

def remove_punc(word, punc_set = string.punctuation):
  return ''.join(ch for ch in word if ch not in punc_set)


# In[4]:


# get the text from the file
def gen_corpus_from_file(in_file="/content/nursery_rhymes.txt", 
                         out_file="/content/parsed_txt.txt"):
  headers_lst = []
  rhymes_lst = []
  skip_ln = lambda ln : True if (ln == "") else False
  is_header = lambda ln : True if (ln[-1].isupper()) else False
  with open(in_file) as file:
    for line in file:
      strip_line = line.replace('\r', ' ').replace('\n', ' ').strip()
      if skip_ln(strip_line): continue
      if is_header(strip_line):
        headers_lst.append(strip_line)
      else:
        rhyme = remove_punc(strip_line.lower())
        rhymes_lst.append(rhyme)
  rhymes = ' '.join(rhymes_lst)
  del headers_lst
  del rhymes_lst
  with open(out_file, "w") as out_f:
    out_f.write(rhymes)
  return rhymes


# In[5]:


corpus = gen_corpus_from_file()


# In[20]:


# LSTM Model
class LSTM_Text_Generator():
  def __init__(self, corpus, step_back, epochs):
    # member variables
    self.corpus = corpus
    self.vocab_size = None
    self.max_length = None
    self.step_back = step_back
    self.tokenizer = Tokenizer()
    self.encoded = None
    self.sequences = None
    self.X = None
    self.y = None
    self.tokenize_words()
    self.epochs = epochs
    # Sequential is the base of the model
    self.model = Sequential()
  # integer encode sequences of words
  def tokenize_words(self):
    self.tokenizer.fit_on_texts([self.corpus])
    self.encoded = self.tokenizer.texts_to_sequences([self.corpus])[0]
    self.vocab_size = len(self.tokenizer.word_index) + 1
    print(f'Vocabulary Size: {self.vocab_size}')
  # encode step_back (2) words -> 1 word
  def gen_sequences(self):
    self.sequences = []
    for i in range(self.step_back, len(self.encoded)):
      sequence = self.encoded[i - self.step_back : i + 1]
      self.sequences.append(sequence)
    print(f'Total Sequences: {len(self.sequences)}')
    # pad sequences
    self.max_length = max([len(seq) for seq in self.sequences])
    self.sequences = pad_sequences(self.sequences, maxlen=self.max_length, padding='pre')
    print(f'Max Sequence Length: {self.max_length}')
  def dist_data_X_y(self):
    self.sequences = np.array(self.sequences)
    # split into input and output elements
    self.X, self.y = self.sequences[:,:-1], self.sequences[:,-1]
    self.y = to_categorical(self.y, num_classes=self.vocab_size)
  def pre_process(self):
    self.gen_sequences()
    self.dist_data_X_y()
  # compile network
  def compile(self):
    self.pre_process()
    self.model.add(Embedding(self.vocab_size, 10, input_length=self.max_length-1))
    self.model.add(LSTM(50))
    self.model.add(Dense(self.vocab_size, activation='softmax'))
    self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  # fit network
  def train(self):
    self.model.fit(self.X, self.y, epochs=self.epochs, verbose=2)
  def predict(self):
    return self.model.predict(self.encoded, verbose=0)
  def summary(self):
    return self.model.summary()
  def get_rand_word(self):
    return self.corpus.split(' ')[random.randint(0, len(self.corpus.split(' ')) - 1)]
  # generate a sequence from a language model
  def generate_seq(self, n_words=20):
    rand_seq = self.get_rand_word() + self.get_rand_word()
    in_text = rand_seq
    # generate a fixed number of words
    for _ in range(n_words-2):
      # encode the text as integer
      encoded = self.tokenizer.texts_to_sequences([in_text])[0]
      # pre-pad sequences to a fixed length
      encoded = pad_sequences([encoded], maxlen=self.max_length-1, padding='pre')
      # predict probabilities for each word
      predict = self.model.predict(encoded, verbose=0)
      yhat=np.argmax(predict,axis=1)
      # map predicted word index to word
      out_word = ''
      for word, index in self.tokenizer.word_index.items():
        if index == yhat:
          out_word = word
          break
      # append to input
      in_text += ' ' + out_word
    return in_text


# In[11]:


LSTM_Model = LSTM_Text_Generator(corpus, 2, 500)


# In[12]:


LSTM_Model.compile()


# In[19]:


LSTM_Model.model.summary()


# In[13]:


LSTM_Model.train()


# In[14]:


def gen_nusery_rhymes(trained_model, n_lines=30, output_file="lstm_rhymes.txt"):
  with open(output_file, "w") as out_file:
    for i in range(n_lines):
      curr_line = trained_model.generate_seq()
      out_file.write(curr_line + ".\n")


# In[15]:


gen_nusery_rhymes(LSTM_Model)


# In[33]:


LSTM_Model_2 = LSTM_Text_Generator(corpus, 2, 50)


# In[34]:


LSTM_Model_2.compile()


# In[ ]:


LSTM_Model_2.train()


# In[36]:


LSTM_Model_2.summary()


# In[37]:


gen_nusery_rhymes(LSTM_Model_2, 30, "lst_rhymes_2.txt")


# Sources
# - Jason Brownlee article: https://machinelearningmastery.com/develop-word-based-neural-language-models-python-keras/
# - https://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/
