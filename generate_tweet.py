##############################################
'''
This code generates and returns a tweet based on files in output folder without
start and stop characters
'''
##############################################

import nltk
from os import listdir

def create_corpus(files):
    text = []
    in_file = open('output.txt', 'r')
    for line in in_file:
        line = line.strip()
        line =  '<s>' + ' ' +  line + ' ' + '</s>' + ' '
        line = line.split()
        text += line
    in_file.close()
    return text

def dist(text):
    freq_dist = nltk.ConditionalFreqDist(nltk.bigrams(text))
    return nltk.ConditionalProbDist(freq_dist, nltk.MLEProbDist)

def generate_sent(files, text, prob_dist):
    sent = '<s> '
    word = '<s>'
    while word != '</s>':
        word = prob_dist[word].generate()
        sent += ' ' + word
    return sent


def generate():
    files = [f for f in listdir('./output')]
    text = create_corpus(files)
    prob_dist = dist(text)

    sent = generate_sent(files, text, prob_dist)
    over140 = True
    while over140:
        if len(sent) < 141:
            over140 = False
        else:
            sent = generate_sent(files, text, prob_dist)
    return sent[4:len(sent)-5]

