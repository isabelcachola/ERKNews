import nltk
import pprint
import random as r

# Creates bigram dictionary
def bigram_probs(corpus):
    count = {}

    words = corpus.split()

    # Creates dictionary that maps each word to a dictionary that maps a
    # second word to count
    for word1, word2 in nltk.bigrams(words):
        if word1 not in count:
            count[word1] = {}
        if word2 not in count[word1]:
            count[word1][word2] = 1
        else:
            count[word1][word2] += 1

    prob = {}

    # Creates a dictionary that maps each word to P(word2|word1)
    for word1 in count:
        for word2 in count[word1]:
            tot = sum(count[word1].values())
            if word1 not in prob:
                prob[word1] = {}
            prob[word1][word2] = (count[word1][word2] / tot)

    return prob

#########
# Problem 5a:

# Helper function that creates probability partion
def make_partition(word1):
    tot = 0
    words = list(word1.keys())
    partition = []
    for word in word1:
        tot += word1[word]
        partition.append(tot)
    return words, partition

# Generates a sentence 50 words long, including start and stop words
def generate_words(prob):
    sent = ['<s>']  # Initializes sentence with start character

    # Generates first word
    first_r = r.random()
    idx = 0
    first_words, first_partition = make_partition(prob['<s>'])
    for value in first_partition:
        if first_r < value:
            sent.append(first_words[idx])
            break
        else:
            idx +=1

    count = 0
    # Generates next 48 words
    prev_word = sent[-1]
    while count < 8:
        next_prob = r.random()
        idx = 0
        next_words, next_partition = make_partition(prob[prev_word])
        for value in next_partition:
            if next_prob < value:
                sent.append(next_words[idx])
                prev_word = next_words[idx]
                count += 1
                break
            else:
                idx += 1

    return ' '.join(sent)



def main():

    from os import listdir
    from os.path import isfile, join
    import csv

    files = [f for f in listdir('./output')]
    st = ''
    test_file = files[0]
    test_file = open('./output/' + test_file, 'r')
    reader = csv.reader(test_file)
    for row in reader:
        #print(row)
        st += '<s>' + ' ' +  row[0] + ' ' + '<\s>' + ' '
    #print(st)
    test_probs = bigram_probs(st)
    test_sent = generate_words(test_probs)
    print(test_sent)

    '''
    for f in files:
        in_file = open(f, 'r')
        for row in
        in_file.close()

    
    alice = open('alicecorpus.txt', 'r')
    alice_probs =  bigram_probs(alice.read())
    alice_sent = generate_words(alice_probs)

    print('Problem 5b:')
    print(alice_sent)
    print()
    '''
main()

