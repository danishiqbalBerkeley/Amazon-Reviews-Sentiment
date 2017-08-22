import pprint
import json
from pyspark import SparkConf
from pyspark import SparkContext
import argparse
import urllib
#import matplotlib.pyplot as plt
#import matplotlib.dates as md
import nltk
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from time import time
#from collections import namedtuple
import csv, io

class LightData:

    def __init__(self, asin, reviewerID, reviewText, overall, neg, neu, pos, compound):
        self.asin = asin
        self.reviewerID = reviewerID
        self.reviewText = reviewText
        self.overall = overall
        self.neg = neg
        self.neu = neu
        self.pos = pos
        self.compound = compound

sia = SentimentIntensityAnalyzer()


############################################################################
# function definitions

def jsonMapReviewTime(x):
    obj =json.loads(x)
    return (obj['unixReviewTime'])

def jsonMap(x):
    obj =json.loads(x)
    return (sia.polarity_scores(obj['reviewText']), obj)
#    return json.loads(x)

# This second map only returns tuple of some fields(asin, reviewerId, reviewText). 
# It can be used later
def jsonMap2(x):
    obj =json.loads(x)
    score = sia.polarity_scores(obj['reviewText'])
    #print(result, obj['reviewText'])
#    obj2 = LightData(obj['asin'], obj['reviewerID'], obj['reviewText'], obj['overall'], score['neg'],score['neu'],score['pos'],score['compound'])
#    return ( obj['asin'], obj['reviewerID'], obj['reviewText'], obj['overall'], score['neg'],score['neu'],score['pos'],score['compound'])
#    return (obj['overall'], score['neg'],score['neu'],score['pos'],score['compound'])
    return(obj['overall']-5*score['compound'], obj['overall'], score['compound'], obj['asin'], obj['reviewText'])

# Given a url of a gz file, download it as save as a locale file with pathname local_file.
# Then parse the json objects in the file and return them as rdd
def parse_data(url, local_file):
    print("Downloading " + url)
    content = urllib.urlretrieve(url, local_file)
    print("Done with " + url)
    dataset = sc.textFile("file://" + local_file)
    # filter on overall - 5*compound > 8 or < -3
    objects = dataset.map(jsonMap2).filter(lambda x: x[0] > 8 or x[0] < -3)
    return(objects)

def list_to_csv_str(x):
    """Given a list of strings, returns a properly-csv-formatted string."""
    output = io.StringIO(None)
    csv.writer(output).writerow(x)
    return output.getvalue().strip() # remove extra newline


#################################################################################
# Main code 

conf = SparkConf().setAppName("appName")
sc = SparkContext(conf=conf)

parser = argparse.ArgumentParser(description='parse a json data file')
parser.add_argument('input_url', help='input url in gz format')
args = parser.parse_args()
rdd = parse_data(args.input_url, "/home/w205/json.gz")

pp = pprint.PrettyPrinter(indent=2)
print('First few records: ')
pp.pprint(rdd.take(1000))



# ... do stuff with your rdd ...
#rdd = rdd.map(list_to_csv_str)
#rdd.saveAsTextFile("file:///home/w205/output")



#print(rdd.first()['reviewerID','reviewText'])
#print('Record count',  objects.count())

# Sampling 1% of data
#print("Now sampling 1% of this set...")
#sample=rdd.map(lambda x: x['asin']).sample(False,0.01,12345)

#sample=rdd.map(lambda x: (x[1],x[2],x[3])).sample(False,0.01,12345)
#sample=objects.takeSample(False,1000,12345)
#print(sample.count())
#pp.pprint(sample.collection())

# Plot sample of reviews per month
#sample.values().histogram(50)

#ax=plt.gca()
#xfmt = md.DateFormatter('%Y-%m')
#ax.xaxis.set_major_formatter(xfmt)
#plt.title("Reviews by Month Histogram")
#plt.xlabel("Month")
#plt.ylabel("Number of Reviews")
#plt.hist(sample.collect())

#plt.show()
