from alchemyapi import AlchemyAPI
import json
import re
import operator


def rank_choices_sentiment(passage_sentiment, choices_sentiment):
    choices = []
    for choice, choice_sent in choices_sentiment.iteritems():
        score = 0
        for keyword, keyword_sent in passage_sentiment.iteritems():
            score += (float(choice_sent['score']) - float(keyword_sent['score']))**2
        choices.append((choice, score))
    choices.sort(key=operator.itemgetter(1))
    return choices


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
    relevant_text = get_relevant_text(passage, question)

    alchemyapi = AlchemyAPI()
    passage_sentiment = {}
    response = alchemyapi.keywords('text', relevant_text, {'sentiment': 1})
    if response['status'] == 'OK':
        for keyword in response['keywords']:
            if 'sentiment' in keyword.keys() and 'score' in keyword['sentiment']:
                passage_sentiment[keyword["text"]] = keyword['sentiment']
 
    choices_sentiment = {}
    for choice in choices:
        response = alchemyapi.keywords('text', "the" + choices[choice], {'sentiment': 1})
        if response['status'] == 'OK':
            for keyword in response['keywords']:
                if 'sentiment' in keyword.keys() and 'score' in keyword['sentiment']:
                    choices_sentiment[choice] = keyword['sentiment']
 
    return rank_choices_sentiment(passage_sentiment, choices_sentiment)