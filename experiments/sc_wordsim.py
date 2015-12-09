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
        print answer
        dist = 0
        scoring = []
        for keyword in keywords:
            b = False
            for a in answer:
                if a not in model:
                    b = True
            if b:
                break
            scoring.append(model.n_similarity(answer, [keyword]))
            # dist += model.similarity(answer, keyword)
            # dist += np.linalg.norm(model[answer] - model[keyword])
        scoring.sort()
        top_n = 5
        print scoring[-top_n:-1]
        scores.append(sum(scoring[-top_n:-1])/(top_n-1))
        print "\n"

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
        sentence = """
            One of the characters in Milton Murayama's novel
            is considered ------- because he deliberately defies
            an oppressive hierarchical society.
        """

        sentence = """
            The range of colors that homeowners could use on the
            exterior of their houses was ------- by the community's
            stringent rules regarding upkeep of property.
        """

        sentence = """Canadian Lynn Johnston was named Cartoonist of
            the Year in 1985, the first woman to be so -------.
            """

        sentence = """Folk painter Grandma Moses has become such
            an enduring icon that many consider her ------ of America.
            """

        sentence = """
            Nightjars possess a camouflage perhaps unparalleled
            in the bird world: by day they roost hidden in shady
            woods, so ------- with their surroundings that they are
            nearly impossible to -------.
        """

        sentence = """
            Many economists believe that since resources are
            scarce and since human desires cannot all be -------,
            a method of ------- is needed.
        """

        sentence = """
            Years of ------- lifting of heavy furniture had left him
            too ------- to be able to stand erect for long periods of
            time.
        """

        answers = ["instructors", "administrators","monitors", "accountants", "benefactors"]
        answers = ["rebellious", "impulsive", "artistic", "industrious", "tyrannical"]
        answers = ["circumscribed", "bolstered", "embellished", "insinuated", "cultivated"]
        answers = ["inspired", "entrusted", "honored", "employed", "refined"]
        answers = ["innovator","emblem","successor","detractor","lobbyist"]

        answers = [['vexed', 'dislodge'], ['blended', 'discern'], ['harmonized', 'interrupt'], ['impatient', 'distinguish'], ['integrated', 'classify']]
        answers = [["indulged", "apportionment"], ["verified", "distribution"], ["usurped", "expropriation"], ["expressed", "reparation"], ["anticipated", "advertising"]]
        answers = [["profitable", "dumbfounded"],["generous", "distracted"],["onerous", "hesitant"],["strenuous", "debilitated"],["unstinting", "eminent"]]

        print solve(sentence, answers)




