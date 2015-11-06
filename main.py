import parser

if __name__ == "__main__":
    parser = parser.Parser()
    sample_test = parser.parse_test(
        'data/clean/official_SAT_practice_test_2012-13.txt')
    print sample_test
