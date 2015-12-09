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


def solve(passage, question, choices):
    print passage

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("USAGE: {0} <path to SentiWordNet>".format(sys.argv[0]))
#         exit(1)

#     sentence = "Lucy Honeychurch has no faults, said Cecil, with grave sincerity."

#     answer1 = "great conviction"
#     answer2 = "studied neutrality"
#     answer3 = "playful irony"
#     answer4 = "genuine surprise"
#     answer5 = "weary cynicism"
#     score = score_sentence(sys.argv[1], sentence)
#     score1 = score_sentence(sys.argv[1], answer1)
#     score2 = score_sentence(sys.argv[1], answer2)
#     score3 = score_sentence(sys.argv[1], answer3)
#     score4 = score_sentence(sys.argv[1], answer4)
#     score5 = score_sentence(sys.argv[1], answer5)

#     print "truth", np.argmax(score), score[np.argmax(score)]
#     print np.argmax(score1), score1[np.argmax(score1)]
#     print np.argmax(score2), score2[np.argmax(score2)]
#     print np.argmax(score3), score3[np.argmax(score3)]
#     print np.argmax(score4), score4[np.argmax(score4)]
#     print np.argmax(score5), score5[np.argmax(score5)]

#     print "\n\n--"

#     sentence = "I felt a rush of nostalgia for the perfumed sharpener shavings of my youth."

#     answer1 = "unrestrained joy"
#     answer2 = "sentimental reminiscence"
#     answer3 = "bitter disappointment"
#     answer4 = "cautious optimism"
#     answer5 = "dark foreboding"
#     score = score_sentence(sys.argv[1], sentence)
#     score1 = score_sentence(sys.argv[1], answer1)
#     score2 = score_sentence(sys.argv[1], answer2)
#     score3 = score_sentence(sys.argv[1], answer3)
#     score4 = score_sentence(sys.argv[1], answer4)
#     score5 = score_sentence(sys.argv[1], answer5)

#     print "truth", np.argmax(score), score[np.argmax(score)]
#     print np.argmax(score1), score1[np.argmax(score1)]
#     print np.argmax(score2), score2[np.argmax(score2)]
#     print np.argmax(score3), score3[np.argmax(score3)]
#     print np.argmax(score4), score4[np.argmax(score4)]
#     print np.argmax(score5), score5[np.argmax(score5)]
