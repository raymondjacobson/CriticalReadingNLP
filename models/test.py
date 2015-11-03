from question import (
    Question,
    SentenceCompletionQuestion,
    PassageBasedReadingQuestion
)


class Section():
    '''
    Section represents a critical reading section of an SAT test
    It holds
        - questions (list of Question)
    '''
    def __init__():
        self.questions = []

    def parse_section(section_string, question_deliminator):
        for line in section_string:
            if question_deliminator in line[:5]:
                self.questions.append(line)


class Test():
    '''
    Test represents an SAT test.
    '''
    def __init__(section_deliminiator):
        self.sections = []
        self.section_deliminator = "x"
        self.question_deliminator = "f"

    def parse_test(filename):
        with open(filename) as test_file:
            line = test_file.readline()
            section_text = ""
            while line != self.section_deliminator:
                section_test += line
                line = test_file.readline()
            section = Section()
            section.parse_section(section, question_deliminator)
