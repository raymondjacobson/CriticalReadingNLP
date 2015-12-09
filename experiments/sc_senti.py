# -*- coding: utf-8 -*-
# from nltk.corpus import wordnet as wn
from unidecode import unidecode
import os
# from spacy.en import English, LOCAL_DATA_DIR

# def dependency_labels_to_root(token):
#     '''Walk up the syntactic tree, collecting the arc labels.'''
#     dep_labels = []
#     while token.head is not token:
#         dep_labels.append(token.dep)
#         token = token.head
#     return dep_labels


# data_dir = os.environ.get('SPACY_DATA', LOCAL_DATA_DIR)
# nlp = English(data_dir=data_dir)
# doc = nlp(unicode("Many private universities depend heavily on -------, the wealthy individuals who support them with gifts and bequests."))
# print doc

# token = doc[0]
# sentence = next(doc.sents)
# assert token is sentence[0]
# # assert sentence.text == 'Hello, world.'


# print dependency_labels_to_root(token)


# from sentiwordnet import SentiWordNetCorpusReader, SentiSynset
# swn_filename = 'SentiWordNet_3.0.0_20130122.txt'
# swn = SentiWordNetCorpusReader(swn_filename)

# sentence = """
# I know what your e-mail in-box looks like, and it
# isn’t pretty: a babble of come-ons and lies from hucksters
# and con artists. To find your real e-mail, you must wade
# through the torrent of fraud and obscenity known politely
# as “unsolicited bulk e-mail” and colloquially as “spam.”
# In a perverse tribute to the power of the online revolution,
# we are all suddenly getting the same mail: easy weight
# loss, get-rich-quick schemes, etc. The crush of these mes-
# sages is now numbered in billions per day. “It’s becoming
# a major systems and engineering and network problem,”
# says one e-mail expert. “Spammers are gaining control of
# the Internet.”
# """

# sentence = sentence.decode('utf-8')
# sentence = unidecode(sentence).strip().replace('\n', ' ')

# print swn.senti_synsets('slow')

# print swn.senti_synset('breakdown.n.03')

import sys
import numpy as np


def avg(lis):
    return float(sum(lis))/len(lis)


def split_line(line):
    cols = line.split("\t")
    return cols


def get_words(cols):
    words_ids = cols[4].split(" ")
    words = [w.split("#")[0] for w in words_ids]
    return words


def get_positive(cols):
    return cols[2]


def get_negative(cols):
    return cols[3]


def get_objective(cols):
    return 1 - (float(cols[2]) + float(cols[3]))


def get_gloss(cols):
    return cols[5]


def get_scores(f, word):
    p_score = 0.
    n_score = 0.
    o_score = 0.
    count = 0.

    for line in f:
        if not line.startswith("#"):
            cols = split_line(line)
            words = get_words(cols)

            if word in words:
                p_score += float(get_positive(cols))
                n_score += float(get_negative(cols))
                o_score += float(get_objective(cols))
                count += 1.
    f.seek(0, 0)
    if count != 0:
        return p_score/count, n_score/count, o_score/count
    return 0, 0, 0


def score_sentence(filename, sentence):
    sentence = sentence.strip('.').strip().strip('\n')
    words = sentence.split(' ')
    p_scores = []
    n_scores = []
    o_scores = []
    f = open(filename)
    for word in words:
        p_score, n_score, o_score = get_scores(f, word.lower())
        if (p_score + n_score + o_score != 0):
            p_scores.append(p_score)
            n_scores.append(n_score)
            o_scores.append(o_score)
    f.close()
    return avg(p_scores), avg(n_scores), avg(o_scores)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: {0} <path to SentiWordNet>".format(sys.argv[0]))
        exit(1)

    sentence = "Lucy Honeychurch has no faults, said Cecil, with grave sincerity."

    answer1 = "great conviction"
    answer2 = "studied neutrality"
    answer3 = "playful irony"
    answer4 = "genuine surprise"
    answer5 = "weary cynicism"
    score = score_sentence(sys.argv[1], sentence)
    score1 = score_sentence(sys.argv[1], answer1)
    score2 = score_sentence(sys.argv[1], answer2)
    score3 = score_sentence(sys.argv[1], answer3)
    score4 = score_sentence(sys.argv[1], answer4)
    score5 = score_sentence(sys.argv[1], answer5)

    print "truth", np.argmax(score), score[np.argmax(score)]
    print np.argmax(score1), score1[np.argmax(score1)]
    print np.argmax(score2), score2[np.argmax(score2)]
    print np.argmax(score3), score3[np.argmax(score3)]
    print np.argmax(score4), score4[np.argmax(score4)]
    print np.argmax(score5), score5[np.argmax(score5)]

    print "\n\n--"

    sentence = "I felt a rush of nostalgia for the perfumed sharpener shavings of my youth."

    answer1 = "unrestrained joy"
    answer2 = "sentimental reminiscence"
    answer3 = "bitter disappointment"
    answer4 = "cautious optimism"
    answer5 = "dark foreboding"
    score = score_sentence(sys.argv[1], sentence)
    score1 = score_sentence(sys.argv[1], answer1)
    score2 = score_sentence(sys.argv[1], answer2)
    score3 = score_sentence(sys.argv[1], answer3)
    score4 = score_sentence(sys.argv[1], answer4)
    score5 = score_sentence(sys.argv[1], answer5)

    print "truth", np.argmax(score), score[np.argmax(score)]
    print np.argmax(score1), score1[np.argmax(score1)]
    print np.argmax(score2), score2[np.argmax(score2)]
    print np.argmax(score3), score3[np.argmax(score3)]
    print np.argmax(score4), score4[np.argmax(score4)]
    print np.argmax(score5), score5[np.argmax(score5)]

    sentence = "Because rap and hip-hop offer such ------- commentary on contemporary issues, they are often said to be sharp-edged musical genres."
    print score_sentence(sys.argv[1], sentence)
    sentence = "Because rap and hip-hop offer such nebulous commentary on contemporary issues, they are often said to be sharp-edged musical genres."
    print score_sentence(sys.argv[1], sentence)
    sentence = "Because rap and hip-hop offer such trenchant commentary on contemporary issues, they are often said to be sharp-edged musical genres."
    print score_sentence(sys.argv[1], sentence)
    sentence = "Because rap and hip-hop offer such circumspect commentary on contemporary issues, they are often said to be sharp-edged musical genres."
    print score_sentence(sys.argv[1], sentence)
    sentence = "Because rap and hip-hop offer such prosaic commentary on contemporary issues, they are often said to be sharp-edged musical genres."
    print score_sentence(sys.argv[1], sentence)
    sentence = "Because rap and hip-hop offer such benign commentary on contemporary issues, they are often said to be sharp-edged musical genres."
    print score_sentence(sys.argv[1], sentence)

    print
    print

    sentence = "Many private universities depend heavily on -------, the wealthy individuals who support them with gifts and bequests."
    print score_sentence(sys.argv[1], sentence)
    sentence = "Many private universities depend heavily on instructors, the wealthy individuals who support them with gifts and bequests."
    print score_sentence(sys.argv[1], sentence)
    sentence = "Many private universities depend heavily on administrators, the wealthy individuals who support them with gifts and bequests."
    print score_sentence(sys.argv[1], sentence)
    sentence = "Many private universities depend heavily on monitors, the wealthy individuals who support them with gifts and bequests."
    print score_sentence(sys.argv[1], sentence)
    sentence = "Many private universities depend heavily on accountants, the wealthy individuals who support them with gifts and bequests."
    print score_sentence(sys.argv[1], sentence)
    sentence = "Many private universities depend heavily on benefactors, the wealthy individuals who support them with gifts and bequests."
    print score_sentence(sys.argv[1], sentence)
