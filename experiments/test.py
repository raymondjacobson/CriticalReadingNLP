import nltk
import random
import gensim
import sys
import numpy as np
from nltk.corpus import wordnet


model = gensim.models.Word2Vec.load('./text8_model')

answers = ["rebellious", "impulsive", "artistic", "industrious", "tyrannical"]
answers = ["instructors", "administrators", "monitors", "accountants", "benefactors"]
# keywords = ['one', 'characters', 'milton', 'novel', 'considered', 'deliberately', 'defies', 'oppressive', 'hierarchical', 'society']
# keywords = ['deliberately', 'defies', 'oppressive', 'hierarchical', 'society']
keywords = ['many', 'private', 'universities', 'depend', 'heavily', 'wealthy', 'individuals', 'support', 'gifts', 'bequests']

keyword_lemmas = set([])
for keyword in keywords:
    for synset in wordnet.synsets(keyword):
        for lemma in synset.lemmas():
            keyword_lemmas.add(lemma.name())
print keyword_lemmas

for answer in answers:
    print answer
    answer_lemmas = set([])
    for synset in wordnet.synsets(answer):
        for lemma in synset.lemmas():
            answer_lemmas.add(lemma.name())

    dist = 0.
    count = 0.
    for lemma in answer_lemmas:
        for keyword in keyword_lemmas:
            if lemma in model and keyword in model:
                sim = model.similarity(lemma, keyword)
                # print lemma, keyword, sim
                count += 1
                dist += sim
    print dist/count