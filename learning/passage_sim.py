import nltk
import random
import gensim
import operator
import sys
import numpy as np
import re


def prune_list(lis, model):
    new_lis = []
    for item in lis:
        if item in model:
            new_lis.append(item)
    return new_lis


def get_relevant_text(passage, question):
    reg = re.match(r"^[\s\S]*line ([0-9]{1,3})", question)
    if reg == None:
        reg = re.match(r"^[\s\S]*lines ([0-9]{1,2}-[0-9]{1,2})", question).group(1)
        reg = reg.split('-')[0]
    else:
        reg = reg.group(1)
    line_number = int(reg)
    pref = False
    if "PREFACE" in passage:
        pref = True
    p_split = passage.replace("PREFACE", "").replace("PASSAGE", "").strip('\n').strip().split('\n')
    if pref:
        for line in xrange(len(p_split)):
            if p_split[line].strip() == "":
                p_split = p_split[line+1:]
                break
    print line_number, p_split
    relevant_text = p_split[line_number-1]
    if '.' not in relevant_text:
        relevant_text += p_split[line_number]
    return relevant_text



def solve(passage, question, choices):
    model = gensim.models.Word2Vec.load("./learning/models/text8_model")
    relevant_text = get_relevant_text(passage, question)

    sent_split = relevant_text.strip('.').split(' ')
    pruned_sent = prune_list(sent_split, model)

    results = []
    for key, answer in choices.iteritems():
        answer = answer.split(' ')
        answer = prune_list(answer, model)
        results.append((key, 1-model.n_similarity(answer, pruned_sent)))
    results = sorted(results, key=lambda x: x[1])
    # Results shows "difference"
    return results
