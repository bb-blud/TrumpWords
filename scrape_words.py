import os
from time import time
import string
import collections
import math
import random
import numpy as np
import tensorflow as tf
from sklearn.manifold import TSNE
from matplotlib import pylab
from six.moves import cPickle as pickle

speaking_solo = [
    "aipac032116.txt",
    "blackhist020117.txt",
    "detroit0808.txt",
    "inaguration.txt",
    "law_order081616.txt",
    "miamispeech021617.txt",
    "national_security061316.txt",
    "national_security090716.txt",
    "onHilary.txt",
    "victory_speach_e.txt"]

speaking_not_solo = [
    "abc_interview012617_multi.txt",
    "clintonVtrump11016_multi.txt",
    "cpac022417_multi.txt",
    "gop_debate_all.txt",
    "immigration110116_multi.txt",
    "press_con021617_multi.txt",
    "townhall032916_multi.txt",
    "wp_interview032116_multi.txt"]
    

def getSoloWords(filename):
    with open("./solo/"+filename, 'rb') as f:
        words = f.read().split()
    return [w.translate(string.maketrans("","") , string.punctuation).lower() for w in words]

def getNonSolo(filename):
    with open("./non_solo/"+filename, 'rb') as f:
        words = f.read().split()
        
    trump_speaking = False
    trump_words = []
    for word in words:
        # Colon indicates speaker will speak
        if word[-1] == ':':
            if "TRUMP" in word: # If Trump is speaker
                trump_speaking = True
            else:
                trump_speaking = False
            continue
        # Strip punctuation
        word = word.translate(string.maketrans("","") , string.punctuation).lower()
            
        # take just spoken words, ignore transcipt descriptions (which are in parenthesis)
        if trump_speaking and word != "" and word[0] != '(' and word[-1] != ')':
            trump_words.append(word)
    return trump_words

def build_dataset(words):
  count = []
  count.extend(collections.Counter(words).most_common())
  dictionary = dict()
  for word, _ in count:
    dictionary[word] = len(dictionary)
  data = list()
  for word in words:
    if word in dictionary:
      index = dictionary[word]
    data.append(index)
  reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
  return data, count, dictionary, reverse_dictionary

#############################################################

word_corpus = []

for doc in speaking_solo:
    word_corpus += getSoloWords(doc)
for doc in speaking_not_solo:
    word_corpus += getNonSolo(doc)

s = time()
data, count, dictionary, reverse_dictionary = build_dataset(word_corpus)
print('Most common words', count[:5])
print('Sample data', data[:10])
print(time()-s)
print len(dictionary)


def findSkipGrams(r, corpus):
    window = r+1+r # window size extends r words away from target left & right
    target = None
    words_neighbors = []
    for i in xrange(len(corpus)-window+1):
        neighbors = []
        for j in xrange(window):
            if j == r: # target at center of window
                target = corpus[i+j]
            else:
                neighbors.append(corpus[i+j])
        words_neighbors.append( (target, neighbors) )
        
    return words_neighbors

print word_corpus[:10]
print findSkipGrams(3, word_corpus)[0]
# w_n = findSkipGrams(3, word_corpus)[0]
# in_nums = (dictionary[w_n[0]], [dictionary[w] for w in w_n[1]])
# in_ws = (reverse_dictionary[in_nums[0]], [reverse_dictionary[n] for n in in_nums[1]])

# print w_n
# print in_nums
# print in_ws

vocabulary_size = len(dictionary) # small corpus, not that many words
window_radius = 7 # How many words to consider left and right.

# get skipgrams as indices 
skipgrams = [ (dictionary[sg[0]], [dictionary[w] for w in sg[1] ]) for sg in findSkipGrams(window_radius, word_corpus) ]

print skipgrams[0]
