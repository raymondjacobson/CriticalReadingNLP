'''Sentence completion solver based on word similarity'''

import nltk
import random
import gensim
import operator
import sys
import numpy as np
from nltk.corpus import wordnet


def prune_list(lis, model):
    new_lis = []
    for item in lis:
        if item in model:
            new_lis.append(item)
    return new_lis


def get_syn(lis, model):
    output_lemmas = set([])
    for l in lis:
        for synset in wordnet.synsets(l):
            for lemma in synset.lemmas():
                output_lemmas.add(lemma.name())
    output_lemmas = prune_list(output_lemmas, model)
    return output_lemmas


def solve(sentence, answers):
    model = gensim.models.Word2Vec.load('learning/models/text8_model')
    stopwords = nltk.corpus.stopwords.words('english')

    sentence_rm_stopwords = [i.strip('.').strip(',').strip().lower()
                             for i in sentence.split() if i not in stopwords]
    # print sentence_rm_stopwords
    # idx = sentence_rm_stopwords.index('-------')
    # amplitude = 2
    # min_bound = (idx - amplitude) if idx > amplitude else 0
    # max_bound = (idx - len(sentence_rm_stopwords)) if \
    #     (idx < len(sentence_rm_stopwords)) else \
    #     (len(sentence_rm_stopwords))
    # print sentence_rm_stopwords
    # sentence_rm_stopwords = sentence_rm_stopwords[min_bound: max_bound]
    keywords = [i for i in sentence_rm_stopwords if i in model]
    
    keyword_lemmas = get_syn(keywords, model)

    keyword_vectors = [model[keyword] for keyword in keyword_lemmas]

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
                a_split = a.split(' ')
                for a_i in a_split:
                    if a_i != 'a' and a_i != 'an':
                        strip_answer_split.append(a_i)
            print "strip ans split", strip_answer_split
                # if a not in model:
                #     b = True
            # if b:
            #     break
            answer_lemmas = get_syn(strip_answer_split, model)
            print answer_lemmas
            if len(answer_lemmas) == 0:
                break 
            scoring.append(model.n_similarity(answer_lemmas, keyword_lemmas))
        print scoring
        scoring.sort()
        top_n = 5
        # print scoring[-top_n:-1]
        scores[answer_key] = (sum(scoring[-top_n:-1])/(top_n-1))
        # print "\n"
    print scores

    best_choice = max(scores.iteritems(), key=operator.itemgetter(1))[0]
    # for i in answers.keys():
    #     print answers[i], scores[i]
    return best_choice
