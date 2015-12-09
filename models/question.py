import random


class Question:
    '''
    Question represents an SAT critical reading question.
    Members:
        - question (string)
        - choices (dictionary)
          {
            'a': "",
            'b': "",
            'c': "",
            'd': "",
            'e': "",
           }
        - answer (invariant key to dictionary)
        - selection (the user selected answer)
    '''
    valid_answers = ['a', 'b', 'c', 'd', 'e']

    def __init__(self, question_number, question, choices):
        self.question_number = question_number
        self.question = question
        self.choices = choices
        self.answer = 'a'
        self.selection = random.choice(choices.keys())

    def set_answer(self, question_number, answer):
        assert answer in self.valid_answers
        assert self.question_number == question_number
        self.answer = answer

    def set_selection(self, selection):
        assert selection in self.valid_answers
        self.selection = selection

    def check_answer(self):
        '''
        Return whether a question is correctly solved.
        Returns False if the selection is unset.
        '''
        return self.selection == self.answer

    @classmethod
    def answer_dict(cls):
        return {
            'a': "",
            'b': "",
            'c': "",
            'd': "",
            'e': "",
        }


class SentenceCompletionQuestion(Question):
    '''
    SentenceCompletionQuestion extends Question and
    represents a sentence completion type question.
    '''
    def __init__(self, question, choices):
        Question.__init__(self,
                          question_number=question.split('. ')[0],
                          question=question.split('. ')[1],
                          choices=choices)


class PassageBasedReadingQuestion(Question):
    '''
    PassageBasedReadingQuestion extends Question and
    represents a sentence completion type question.
    Members:
        - passage (string)
    '''
    def __init__(self, passage, question, choices):
        self.passage = passage
        Question.__init__(self,
                          question_number=question.split('. ')[0],
                          question=". ".join(question.split('. ')[1:]),
                          choices=choices)
