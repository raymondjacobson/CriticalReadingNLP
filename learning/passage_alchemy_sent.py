from alchemyapi import AlchemyAPI
import json
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


def get_alchemy_sentiment_rank(passage, question, choices):
    line_number = int(re.match(r"^[\s\S]*line ([0-9]{1,3})", question).group(1))
    p_split = passage.replace("PREFACE", "").replace("PASSAGE", "").strip('\n').strip().split('\n')
    for line in xrange(len(p_split)):
        if p_split[line].strip() == "":
            p_split = p_split[line+1:]
            break
    relevant_text = p_split[line_number-1]
    if '.' not in relevant_text:
        relevant_text += p_split[line_number]

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