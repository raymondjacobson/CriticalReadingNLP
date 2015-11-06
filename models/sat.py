import re
from question import Question


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
        self.section_deliminator = "SECTION"

    def set_sections(self, sections):
        self.sections = sections

    def __repr__(self):
        output = ""
        for section in self.sections:
            output += "SECTION" + str(section.number) + "\n\n"
            for question in section.questions:
                output += "Question: " + question.question + "\n"
                output += "Choices: " + str(question.choices) + "\n"
                output += "\n"
        return output
