##############################################
'''
This code generates and returns a tweet based on output.txt

generate() is called in tweet.py and returns a generated tweet
'''
##############################################

import nltk

# Returns list of words as a corpus
def create_corpus():
    text = []
    in_file = open('output.txt', 'r')
    for line in in_file:
        line = line.strip()
        # Add stop and start characters
        line =  '<s>' + ' ' +  line + ' ' + '</s>' + ' '
        line = line.split()
        text += line
    in_file.close()
    return text

# Create frequency distribution
def dist(text):
    freq_dist = nltk.ConditionalFreqDist(nltk.bigrams(text))
    return nltk.ConditionalProbDist(freq_dist, nltk.MLEProbDist)

# Generates a sentence
def generate_sent(text, prob_dist):
    sent = '<s> '
    word = '<s>'
    while word != '</s>':
        word = prob_dist[word].generate()
        sent += ' ' + word
    return sent

# Calls generate_sent and recalls until sentence is under 140 characters
# Returns sentence
def generate():
    text = create_corpus()
    prob_dist = dist(text)

    sent = generate_sent(text, prob_dist)
    over140 = True
    while over140:
        if len(sent) < 141:
            over140 = False
        else:
            sent = generate_sent(files, text, prob_dist)
    return sent[4:len(sent)-5]

