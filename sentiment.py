#!/usr/bin/python
from sys import argv
import nltk
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from time import time

print("runing sentiment analysis")

# Initialize analyzer
sid = SentimentIntensityAnalyzer()

# Open test file
with open(argv[1], 'r') as fh:
    sentence = fh.readlines()

start = time()

# Turn review into string
sentence = "\n".join(sentence)

ss = sid.polarity_scores(sentence)

end = time() - start
print(sentence)
for key, value in ss.iteritems():
    print("%s: %f" % (key, value))

print(end)
