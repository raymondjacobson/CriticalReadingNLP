import parser

if __name__ == "__main__":
    parser = parser.Parser()
    sample_test = parser.parse_test(
        'data/clean/official_SAT_practice_test_2012-13.txt')
    parser.parse_answer_key(
        sample_test,
        'data/clean/official_SAT_practice_test_2012-13_answer.txt')
    parser.parse_scoring_key(
        sample_test,
        'data/clean/official_SAT_practice_test_2012-13_scoring.txt')
    print sample_test

    print sample_test.score()
