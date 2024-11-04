from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title3', 'title4']
        self.assertEqual(search('dog', dummy_keyword_dict), expected_search_results)


    def test_keyboard_to_titles(self):
        metadata = [['Article 1', 'Author 1', 1181623340, 21023, ['dog', 'cat', 'rat', 'bat']],
        ['Article 2', 'Author 2', 1172208041, 5569, ['french', 'pop', 'dog']], 
        ['Article 3', 'Author 3', 1222607041, 4526, ['edogawa', 'the', 'rat', 'bat']]]
        output = {'dog': ['Article 1', 'Article 2'], 'cat': ['Article 1'], 
        'rat': ['Article 1', 'Article 3'], 'bat': ['Article 1', 'Article 3'], 
        'french': ['Article 2'], 'pop': ['Article 2'], 'edogawa': ['Article 3'], 'the': ['Article 3']}

        self.assertEqual(keyword_to_titles(metadata), output)
        self.assertEqual(keyword_to_titles([]), {})

        metadata2 =[['Article 1', 'Author 1', 1181623340, 21023, []]]
        output2 ={}
        self.assertEqual(keyword_to_titles(metadata2), output2)


    def test_title_to_info(self):
        metadata = metadata = [['Article 1', 'Author 1', 1181623340, 21023, ['dog', 'cat', 'rat', 'bat']],
        ['Article 2', 'Author 2', 1172208041, 5569, ['french', 'pop', 'dog']], 
        ['Article 3', 'Author 3', 1222607041, 4526, ['edogawa', 'the', 'rat', 'bat']]]
        output = {'Article 1': {'author': 'Author 1', 'timestamp': 1181623340, 'length': 21023}, 
        'Article 2': {'author': 'Author 2', 'timestamp': 1172208041, 'length': 5569}, 
        'Article 3': {'author': 'Author 3', 'timestamp': 1222607041, 'length': 4526}}
        
        self.assertEqual(title_to_info(metadata), output)
        self.assertEqual(title_to_info([]), {})

        metadata2 = [['Article 1', 'Author 1', 1181623340, 21023, ['dog', 'cat', 'rat', 'bat']]]
        output2 = {'Article 1': {'author': 'Author 1', 'timestamp': 1181623340, 'length': 21023}}
        self.assertEqual(title_to_info(metadata2), output2)

    def test_search(self):
        data1 = {'dog': ['Article 1', 'Article 2'], 'cat': ['Article 1'], 
        'rat': ['Article 1', 'Article 3'], 'bat': ['Article 1', 'Article 3'], 
        'french': ['Article 2'], 'pop': ['Article 2'], 'edogawa': ['Article 3'], 'the': ['Article 3']}
        output1 = ['Article 1', 'Article 2'] 

       

        self.assertEqual(search('dog', data1), ['Article 1', 'Article 2'] )
        self.assertEqual(search('tiger', data1),[])
        self.assertEqual(search('', data1),[])
        self.assertEqual(search('lion', {}),[])

    
    def test_article_length(self):
        data = {'Article 1': {'author': 'Author 1', 'timestamp': 1181623340, 'length': 21023}, 
        'Article 2': {'author': 'Author 2', 'timestamp': 1172208041, 'length': 5569}, 
        'Article 3': {'author': 'Author 3', 'timestamp': 1222607041, 'length': 4526}}

        self.assertEqual(article_length(6000, ['Article 1', 'Article 2', 'Article 3'], data), ['Article 2', 'Article 3'] )
        self.assertEqual(article_length(0, ['Article 1', 'Article 2', 'Article 3'], data), [])
        self.assertEqual(article_length(-7, ['Article 1', 'Article 2', 'Article 3'], data), [] )
        self.assertEqual(article_length(1000, ['Article 1', 'Article 2', 'Article 3'], data), [] )
        self.assertEqual(article_length(6000, [], data), [] )

    def test_key_by_author(self):
        data = {'Article 1': {'author': 'Author 1', 'timestamp': 1181623340, 'length': 21023}, 
        'Article 2': {'author': 'Author 2', 'timestamp': 1172208041, 'length': 5569}, 
        'Article 3': {'author': 'Author 3', 'timestamp': 1222607041, 'length': 4526},
        'Article 4': {'author': 'Author 1', 'timestamp': 1222607041, 'length': 4526}}

        self.assertEqual(key_by_author(['Article 1', 'Article 2', 'Article 3', 'Article 4'], data), {'Author 1': ['Article 1', 'Article 4'], 'Author 2': ['Article 2'], 'Author 3': ['Article 3']} )
        self.assertEqual(key_by_author([], data), {})
        self.assertEqual(key_by_author([], {}), {})
        self.assertEqual(key_by_author(['Article 1', 'Article 2'], data), {'Author 1': ['Article 1'], 'Author 2': ['Article 2']})
        

    def test_filter_to_author(self):
        data = {'Article 1': {'author': 'Author 1', 'timestamp': 1181623340, 'length': 21023}, 
        'Article 2': {'author': 'Author 2', 'timestamp': 1172208041, 'length': 5569}, 
        'Article 3': {'author': 'Author 3', 'timestamp': 1222607041, 'length': 4526},
        'Article 4': {'author': 'Author 1', 'timestamp': 1222607041, 'length': 4526}}

        self.assertEqual(filter_to_author('Author 1', ['Article 1', 'Article 2', 'Article 3', 'Article 4'], data),['Article 1', 'Article 4'])
        self.assertEqual(filter_to_author('Author 1', ['Article 1', 'Article 2'], data),['Article 1'])
        self.assertEqual(filter_to_author('', [], data),[])
        self.assertEqual(filter_to_author('Author 1', [], {}),[])

    def test_filter_out(self):
        data = {'dog': ['Article 1', 'Article 2'], 'cat': ['Article 1'], 
        'rat': ['Article 1', 'Article 3'], 'bat': ['Article 1', 'Article 3'], 
        'french': ['Article 2'], 'pop': ['Article 2'], 'edogawa': ['Article 3'], 'the': ['Article 3']}

        self.assertEqual(filter_out('dog',['Article 1', 'Article 2', 'Article 3'], data), ['Article 3']) 
        self.assertEqual(filter_out('apple',['Article 1', 'Article 2', 'Article 3'], data), ['Article 1', 'Article 2', 'Article 3']) 
        self.assertEqual(filter_out('',['Article 1', 'Article 2', 'Article 3'], data), ['Article 1', 'Article 2', 'Article 3']) 
        self.assertEqual(filter_out('dog',[], data), []) 

    def test_articles_from_year(self):
        data = {'Article 1': {'author': 'Author 1', 'timestamp': 1181623340, 'length': 21023}, 
        'Article 2': {'author': 'Author 2', 'timestamp': 1172208041, 'length': 5569}, 
        'Article 3': {'author': 'Author 3', 'timestamp': 1222607041, 'length': 4526}}
        

        self.assertEqual(articles_from_year(2007,['Article 1', 'Article 2', 'Article 3'], data), ['Article 1', 'Article 2',])
        self.assertEqual(articles_from_year(2000,['Article 1', 'Article 2', 'Article 3'], data), []) 
        self.assertEqual(articles_from_year(2007,[], data), []) 
        # self.assertEqual(articles_from_year(2000,['Article 1', 'Article 2', 'Article 3'], {}), []) 

    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 5
        advanced_response = 2009

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_advanced_option_1(self, input_mock):
        keyword = 'soccer'
        advanced_option = 1
        advanced_response = 3000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)

    
    @patch('builtins.input')
    def test_advanced_option_2(self, input_mock):
        keyword = 'soccer'
        advanced_option = 2

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + "\n\nHere are your articles: {'jack johnson': ['Spain national beach soccer team'], 'Burna Boy': ['Will Johnson (soccer)'], 'Mack Johnson': ['Steven Cohen (soccer)']}\n"

        self.assertEqual(output, expected)

    @patch('builtins.input') 
    def test_advanced_option_1(self, input_mock):
        keyword = 'dog'
        advanced_option = 3
        advanced_response = 'Mr Jake'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Dalmatian (dog)', 'Sun dog']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input') 
    def test_advanced_option_1(self, input_mock):
        keyword = 'soccer'
        advanced_option = 4
        advanced_response = 'beach'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Will Johnson (soccer)', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)

    # @patch('builtins.input')
    # def test_advanced_option_2(self, input_mock):
    #     keyword = 'soccer'
    #     advanced_option = 2

    #     output = get_print(input_mock, [keyword, advanced_option])
    #     expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + "\n\nNo articles found\n"

    #     self.assertEqual(output, expected)

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()