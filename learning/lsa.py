'''Sentence completion solver based on word similarity'''

import nltk
import random
import gensim
import operator
import sys
import numpy as np


def solve(sentence, answers):
    model = gensim.models.Word2Vec.load('learning/models/text8_model')
    stopwords = nltk.corpus.stopwords.words('english')

    sentence = [i.strip('.').strip(',').strip().lower()
                for i in sentence.split()]
    keywords = [i for i in sentence if i in model]
    keyword_vectors = [model[keyword] for keyword in keywords]

    scores = {}
    for answer_key, answer in answers.iteritems():
        print answer
        dist = 0
        scoring = []
        for keyword in keywords:
            b = False
            answer_split = answer.split('. .')
            strip_answer_split = []
            for a in answer_split:
                a = a.strip()
                strip_answer_split.append(a)
                if a not in model:
                    b = True
            if b:
                break
            scoring.append(model.n_similarity(strip_answer_split, [keyword]))
        scoring.sort()
        top_n = len(scoring)
        # print scoring[-top_n:-1]
        scores[answer_key] = (sum(scoring[-top_n:-1])/(top_n-1))
        # print "\n"
    print scores

    best_choice = max(scores.iteritems(), key=operator.itemgetter(1))[0]
    # for i in answers.keys():
    #     print answers[i], scores[i]
    return best_choice
