import sys
import numpy as np
import re
from unidecode import unidecode


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
    # print passage
    p_split = passage.replace("PREFACE", "").replace("PASSAGE", "").strip('\n').strip().split('\n')
    if pref:
        for line in xrange(len(p_split)):
            if p_split[line].strip() == "":
                p_split = p_split[line+1:]
                break
    relevant_text = p_split[line_number-1]
    if '.' not in relevant_text:
        relevant_text += p_split[line_number]
    return relevant_text


def solve(passage, question, choices):
    f_name = 'learning/models/SentiWordNet_3.0.0_20130122.txt'
    # print question
    relevant_text = get_relevant_text(passage, question)

    base_score = score_sentence(f_name, relevant_text)
    base_score_dimension = base_score[np.argmax(base_score)]
    results = []
    for key, answer in choices.iteritems():
        score = score_sentence(f_name, answer)
        # print answer, np.argmax(score), score[np.argmax(score)]
        sentiment = np.argmax(score)
        if sentiment == np.argmax(base_score):
            results.append((key, abs(base_score_dimension - score[np.argmax(score)])))
        else:
            results.append((key, 0))
    results = sorted(results, key=lambda x: x[1])
    return results
