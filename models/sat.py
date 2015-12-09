import re
from question import SentenceCompletionQuestion, PassageBasedReadingQuestion
from learning import sc_wordsim, passage_sentiwordnet, passage_sim, passage_alchemy_sent


class Section:
    '''
    Section represents a critical reading section of an SAT test
    Members:
        - questions (list of Question)
    '''
    def __init__(self, number):
        self.questions = []
        self.number = number

    def set_questions(self, questions):
        self.questions = questions


class SAT:
    '''
    SAT represents an SAT test.
    '''
    def __init__(self):
        self.sections = []
        self.scoring_key = {}

    def set_sections(self, sections):
        self.sections = sections

    def score(self):
        raw_score = 0.
        correct = 0
        incorrect = 0
        for section in self.sections:
            for question in section.questions:
                if question.check_answer():
                    correct += 1
                else:
                    incorrect += 1
        raw_score = round(correct - incorrect * 0.25)
        score = self.scoring_key.get(raw_score, self.scoring_key[-2])
        return raw_score, score

    def solve(self):
        correct = 0.
        total = 0.
        for section in self.sections:
            for question in section.questions:
                # Check the type of question we are trying to solve
                """if isinstance(question, SentenceCompletionQuestion):
                    # print question.question
                    # print question.choices
                    guess = sc_wordsim.solve(question.question,
                                             question.choices)
                    question.selection = guess
                    print "answer", question.choices[question.answer]
                    print "guess", question.choices[question.selection]
                    print "answer", question.answer, "guess", question.selection, \
                        question.answer == question.selection
                    print
                    if question.answer == question.selection:
                        correct += 1
                    total += 1"""
                if isinstance(question, PassageBasedReadingQuestion):
                    if 'tone' in question.question or 'mood' in question.question:
                        guess = passage_sentiwordnet.solve(question.passage,
                                                           question.question,
                                                           question.choices)
                        print guess
                        guess2 = passage_sim.solve(question.passage,
                                                   question.question,
                                                   question.choices)
                        print guess2
                        guess3 = passage_alchemy_sent.solve(question.passage,
                                                            question.question,
                                                            question.choices)
                        print guess3
        print correct/total


    def __repr__(self):
        output = ""
        for section in self.sections:
            output += "SECTION" + str(section.number) + "\n\n"
            for question in section.questions:
                output += "Question: " + question.question + "\n"
                output += "Choices: " + str(question.choices) + "\n"
                output += "Answer: " + question.answer + "\n"
                output += "Selection: " + question.selection + "\n"
                output += "\n"
        return output
