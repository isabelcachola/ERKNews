##############################################
'''
This code generates and returns a tweet based on output.txt

generate() is called in tweet.py and returns a generated tweet
'''
##############################################

import nltk
from nltk.util import ngrams
import language_check
from collections import Counter
import math
import operator


class GenerateTweet:
    def __init__(self, data_file='output.txt'):
        self.data_file = data_file

        self.text = self.create_corpus()
        self.prob_dist = self.dist()

    # Returns list of words as a corpus
    def create_corpus(self):
        text = []
        in_file = open(self.data_file, 'r')
        for line in in_file:
            line = line.strip()
            # Add stop and start characters
            line =  '<s>' + ' ' +  line + ' ' + '</s>' + ' '
            line = line.split()
            text += line
        in_file.close()
        return text

    # Create frequency distribution
    def dist(self):
        freq_dist = nltk.ConditionalFreqDist(nltk.bigrams(self.text))
        return nltk.ConditionalProbDist(freq_dist, nltk.MLEProbDist)

    # Generates a sentence
    def generate_sent(self):
        sent = '<s> '
        word = '<s>'
        while word != '</s>':
            word = self.prob_dist[word].generate()
            sent += ' ' + word
        return sent

    # Calls generate_sent and recalls until sentence is under 140 characters
    # Returns sentence
    def generate(self):
        sent =self.generate_sent()
        over140 = True
        while over140:
            if len(sent) < 141:
                over140 = False
            else:
                sent = self.generate_sent()
        return sent[4:len(sent)-5]

    def language_model(self, generated_sents, n=2):
        data = []
        for sent in self.text:
            token = nltk.word_tokenize(sent)
            data += token
        bigrams = ngrams(data, n)
        bigram_dist = Counter(bigrams)

        total = sum(bigram_dist.values(), 0.0)
        for gram in bigram_dist:
            bigram_dist[gram] /= total
            bigram_dist[gram] += 1.1
            bigram_dist[gram] = math.log(bigram_dist[gram])

        sent_probs = {}
        keys = bigram_dist.keys()
        #print(keys)
        #print(bigram_dist)
        for sent in generated_sents:
            if len(sent.split()) < 6:
                pass
            else:
                sent_bigram = list(ngrams(nltk.word_tokenize(sent), n))
                prob = 1
                for gram in sent_bigram:
                    if gram in keys:
                        prob *= bigram_dist[gram]
                sent_probs[sent] = prob
        return max(sent_probs.items(), key=operator.itemgetter(1))[0]

    def check_grammar(self, text):
        tool = language_check.LanguageTool('en-US')
        matches = tool.check(text)
        correct_sent = language_check.correct(text, matches)
        return correct_sent

