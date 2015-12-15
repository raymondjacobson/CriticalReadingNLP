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
    sample_test.solve()

    # sample_test2 = parser.parse_test(
    #     'data/clean/official_SAT_practice_test_2013-14.txt')
    # parser.parse_answer_key(
    #     sample_test2,
    #     'data/clean/official_SAT_practice_test_2013-14_answer.txt')
    # parser.parse_scoring_key(
    #     sample_test2,
    #     'data/clean/official_SAT_practice_test_2013-14_scoring.txt')
    # print sample_test2
    # sample_test2.solve()

    # print sample_test

    print sample_test.score()
    # print sample_test2.score()
