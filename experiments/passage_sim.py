import nltk
import random
import gensim
import operator
import sys
import numpy as np


def prune_list(lis, model):
    new_lis = []
    for item in lis:
        if item in model:
            new_lis.append(item)
    return new_lis

model = gensim.models.Word2Vec.load("./text8_model")

# passage = ["I","know","what","your","e-mail","in-box","looks","like,","and","it","isn't","pretty:","a","babble","of","come-ons","and","lies","from","hucksters","and","con","artists.","To","find","your","real","e-mail,","you","must","wade","through","the","torrent","of","fraud","and","obscenity","known","politely","as","unsolicited","bulk","e-mail","and","colloquially","as","spam.","In","a","perverse","tribute","to","the","power","of","the","online","revolution,","we","are","all","suddenly","getting","the","same","mail:","easy","weight","loss,","get-rich-quick","schemes,","etc.","The","crush","of","these","messages","is","now","numbered","in","billions","per","day.","It's","becoming","a","major","systems","and","engineering","and","network","problem,","says","one","e-mail","expert.","Spammers","are","gaining","control","of","the","Internet."]
# answers = [
#     ["comparison"],
#     ["hypothesis"],
#     ["controversy"],
#     ["distinction"],
#     ["concern"],
# ]

# passage = ["Many", "people", "who", "hate", "spam", "assume", "that", "it", "is", "protected", "as", "free", "speech", "Not", "necessarily", "so", "The", "United", "States", "Supreme", "Court", "has", "previously", "ruled", "that", "individuals", "may", "preserve", "a", "threshold", "of", "privacy", "Nothing", "in", "the", "Constitution", "compels", "us", "to", "listen", "to", "or", "view", "any", "unwanted", "communication", "whatever", "its", "merit", "wrote", "Chief", "Justice", "Warren", "Burger", "in", "a", "1970", "decision", "We", "therefore", "categorically", "reject", "the", "argument", "that", "a", "vendor", "has", "a", "right", "to", "send", "unwanted", "material", "into", "the", "home", "of", "another", "With", "regard", "to", "a", "seemingly", "similar", "problem", "the", "Telephone", "Consumer", "Protection", "Act", "of", "1991", "made", "it", "illegal", "in", "the", "United", "States", "to", "send", "unsolicited", "faxes;", "why", "not", "extend", "the", "act", "to", "include", "unsolicited", "bulk", "e-mail"]

# passage = prune_list(passage, model)

# answers = [
#     ["confirm","a","widely","held","belief"],
#     ["discuss","the","inadequacies","of","a","ruling"],
#     ["defend","a","controversial","technology"],
#     ["analyze","a","widespread","social","problem"],
#     ["lay","the","foundation","for","a","course","of","action"]
# ]

# for answer in answers:
#     answer = prune_list(answer, model)
#     print answer
#     print model.n_similarity(answer, passage)

sent = "Lucy Honeychurch has no faults, said Cecil, with grave sincerity."
sent = "I felt a rush of nostalgia for the perfumed sharpener shavings of my youth."
sent_split = sent.strip('.').split(' ')

pruned_sent = prune_list(sent_split, model)

# print model.n_similarity(pruned_sent, ['great', 'conviction']), " ['great', 'conviction'])"
# print model.n_similarity(pruned_sent, ['studied', 'neutrality'],), "['studied', 'neutrality'])"
# print model.n_similarity(pruned_sent, ['playful', 'irony']), " ['playful', 'irony'])"
# print model.n_similarity(pruned_sent, ['genuine', 'surprise']), " ['genuine', 'surprise'])"
# print model.n_similarity(pruned_sent, ['weary', 'cynicism']), "] ['weary', 'cynicism '])"

answers = [
    ['unrestrained', 'joy'],
    ['sentimental', 'reminisce'],
    ['bitter', 'disappointment'],
    ['cautious', 'optimism'],
    ['dark', 'foreboding'],
]

for answer in answers:
    answer = prune_list(answer, model)
    print answer
    print model.n_similarity(answer, pruned_sent)