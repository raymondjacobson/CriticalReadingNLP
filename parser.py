import re
import models.sat
import models.question


def enum(**enums):
    return type('Enum', (), enums)

States = enum(START='START',
              SECTION='SECTION',
              QUESTION='QUESTION',
              ANSWER='ANSWER',
              PASSAGE='PASSAGE',
              END='END')


class Parser:
    '''
    This class is a parser for an SAT test (only critical reading sections)
    in .txt format.

    Parser implements a simple state machine to capture sections and questions
    from an SAT test.
    '''
    def __init__(self):
        self.state = States.START
        self.syntax_error = "SAT test is in invalid format"

        # Deliminators
        self.section_deliminator = r"SECTION"
        self.passage_deliminator = r"PASSAGE"
        self.question_deliminator = r"[0-9]{1,3}\. [a-zA-Z]+"
        self.answer_deliminator = r"\([a-zA-Z]\)"

    def match_line(self, line, deliminiator):
        return re.match(deliminiator, line)

    def get_section_number(self, line):
        return int(line.strip(self.section_deliminator).strip())

    def split_answer(self, line):
        '''
        (A) rebellious --> ('a', 'rebellious')
        '''
        line_split = line.split(')')
        key = line_split[0].strip().strip('(').lower()
        value = line_split[1].strip()
        return key, value

    def parse_test(self, file_name):
        # Initialize default containers
        sat_test = models.sat.SAT()
        sections = []
        section = models.sat.Section(-1)
        questions = []
        question_text = ""
        passage_text = ""
        answers = models.question.Question.answer_dict()
        answer_letter = 'a'
        start_passage_questions = False

        with open(file_name) as test_file:
            line = test_file.readline()
            while line:
                line = line.replace('\n', ' ')

                # Saw a section
                if self.match_line(line, self.section_deliminator):
                    if self.state == States.START:
                        self.state = States.SECTION
                        section_number = self.get_section_number(line)
                        section = models.sat.Section(section_number)
                    elif self.state == States.ANSWER:
                        # End of the section, add the questions to a section
                        questions.append(
                            models.question.PassageBasedReadingQuestion(
                                passage=passage_text,
                                question=question_text,
                                choices=answers))
                        question_text = ""

                        section.set_questions(questions)
                        sections.append(section)
                        questions = []
                        section_number = self.get_section_number(line)
                        section = models.sat.Section(section_number)
                        self.state = States.SECTION
                        start_passage_questions = False
                    else:
                        print self.state
                        raise SyntaxError(self.syntax_error)

                # Saw a question
                elif self.match_line(line, self.question_deliminator):
                    if self.state == States.SECTION:
                        self.state = States.QUESTION
                        question_text += line
                    elif self.state == States.ANSWER:
                        if not start_passage_questions:
                            questions.append(
                                models.question.SentenceCompletionQuestion(
                                    question=question_text,
                                    choices=answers))
                        else:
                            questions.append(
                                models.question.PassageBasedReadingQuestion(
                                    passage=passage_text,
                                    question=question_text,
                                    choices=answers))
                        question_text = ""
                        question_text += line
                        self.state = States.QUESTION
                    elif self.state == States.PASSAGE:
                        self.state = States.QUESTION
                        question_text += line

                # Saw an answer
                elif self.match_line(line, self.answer_deliminator):
                    if self.state == States.QUESTION:
                        answers = models.question.Question.answer_dict()
                        self.state = States.ANSWER
                    answer_letter, answer_text = self.split_answer(line)
                    answers[answer_letter] = answer_text

                # Saw a passage
                elif self.match_line(line, self.passage_deliminator):
                    passage_text = ""
                    if self.state == States.ANSWER:
                        if not start_passage_questions:
                            questions.append(
                                models.question.SentenceCompletionQuestion(
                                    question=question_text,
                                    choices=answers))
                        else:
                            questions.append(
                                models.question.PassageBasedReadingQuestion(
                                    passage=passage_text,
                                    question=question_text,
                                    choices=answers))
                        question_text = ""
                        self.state = States.PASSAGE
                        passage_text += line
                    elif self.state == States.QUESTION:
                        pass
                    start_passage_questions = True

                else:
                    if self.state == States.QUESTION:
                        question_text += line
                    elif self.state == States.PASSAGE:
                        passage_text += line
                    elif self.state == States.ANSWER:
                        answers[answer_letter] += line.strip()
                line = test_file.readline()

        questions.append(
            models.question.PassageBasedReadingQuestion(
                passage=passage_text,
                question=question_text,
                choices=answers))
        question_text = ""
        section.set_questions(questions)
        sections.append(section)

        self.state = States.END
        sat_test.set_sections(sections)

        self.__init__()

        return sat_test

    def parse_answer_key(self, sat_test, file_name):
        '''
        Load an answer key from file_name. Mandates that the format:
        1. A
        2. B
        4. E
        (question_number question_answer)
        '''
        with open(file_name) as answer_key:
            for section in sat_test.sections:
                for question in section.questions:
                    line = answer_key.readline()
                    split = line.split('. ')
                    question_number = split[0]
                    answer = split[1].strip().lower()
                    question.set_answer(question_number, answer)

    def parse_scoring_key(self, sat_test, file_name):
        '''
        Load a scoring key from file_name. Mandates that the format:
        67 800
        66 800
        65 780
        (raw_score actual_score)
        '''
        with open(file_name) as scoring_key:
            for line in scoring_key.readlines():
                split = line.split(' ')
                sat_test.scoring_key[int(split[0])] = int(split[1].strip('\n'))
