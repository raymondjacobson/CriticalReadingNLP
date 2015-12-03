'''Sentence completion word similarity'''

import nltk
import random
import gensim
import sys
import numpy as np


def solve(sentence, answers):
    model = gensim.models.Word2Vec.load('./text8_model')
    stopwords = nltk.corpus.stopwords.words('english')

    sentence_rm_stopwords = [i.strip('.').strip(',').strip().lower()
                             for i in sentence.split() if i not in stopwords]
    # print sentence_rm_stopwords
    keywords = [i for i in sentence_rm_stopwords if i in model]
    print keywords
    keyword_vectors = [model[keyword] for keyword in keywords]

    scores = []
    for answer in answers:
        dist = 0
        for keyword in keywords:
            dist += model.similarity(answer, keyword)
            # dist += np.linalg.norm(model[answer] - model[keyword])
        scores.append(dist/(len(keywords)))

    best_choice = answers[np.argmax(scores)]
    for i in xrange(len(scores)):
        print answers[i], scores[i]
    return best_choice
if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'train':
            model = gensim.models.Word2Vec(nltk.corpus.treebank.sents())
            model.save('./sc_wordsim_model')

    else:
        sentence = """
            Many private universities depend heavily on -------,
            the wealthy individuals who support them with gifts and bequests.
        """
        # sentence = """
        #     One of the characters in Milton Murayama's novel
        #     is considered ------- because he deliberately defies
        #     an oppressive hierarchical society.
        # """

        answers = ["instructors", "administrators",
                   "monitors", "accountants", "benefactors"]
        # answers = ["rebellious", "impulsive", "artistic", "industrious", "tyrannical"]

        print solve(sentence, answers)