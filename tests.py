# Imports to test the functions
import unittest
from unittest.mock import patch
import io

from main import word_intro, check_game, ask_user

# word_intro function inputs to Tests.
## First test have to end in a correct input (e.g:[..., "aaaaa"]) and contain only alpha
test_len_word_intro_inputs = ["a", "aa", "aaa", "aaaa", "aaaaaa", "aaaaa"]
## Second test have to end in a correct input (e.g:[..., "aaaaa"]) and contain only strings with no alpha of length 5
test_chars_word_intro_inputs = ["^^^^^", "aaa/n", ";;;;;", "555aa", "aaaaa"]
## In third test words are capitalized and contain only correct strings of length 5
test_caps_word_intro_inputs = ["aaaAa", "PEPDP", "PepPe", "YYUUY"]
## In last test all words are correct entries
test_correct_word_intro_inputs = ["pepdp", "aaaaa", "yyyyy"]

# ask_user function inputs to Tests.
## First test have to end in [..., "y"] in order to stop the function
incorrect_ask_user_inputs = ["yesz", "not", "match", "nothing", "y"]
correct_yes_ask_user_inputs = ["y", "Y", "yes", "YES"]
correct_no_ask_user_inputs = ["n", "N", "no", "NO"]

# check_game function inputs to Tests. format [guess, secret, {word: char_char_char_char_char, solved: int}]
# guess = word to guess
# secret = solution for worlde
# word = 5 letters formatted
# solved = integer with the number of guessed letters
params_test_game = [
    ["aaaaa", "aaaaa", {"word": f"\033[1m\033[42m\033[30m{'A'}\033[0m"
                                f"\033[1m\033[42m\033[30m{'A'}\033[0m"
                                f"\033[1m\033[42m\033[30m{'A'}\033[0m"
                                f"\033[1m\033[42m\033[30m{'A'}\033[0m"
                                f"\033[1m\033[42m\033[30m{'A'}\033[0m",
                        "solved": 5}],
    ["aabaa", "aabaa", {"word": f"\033[1m\033[42m\033[30m{'A'}\033[0m"
                                f"\033[1m\033[42m\033[30m{'A'}\033[0m"
                                f"\033[1m\033[42m\033[30m{'B'}\033[0m"
                                f"\033[1m\033[42m\033[30m{'A'}\033[0m"
                                f"\033[1m\033[42m\033[30m{'A'}\033[0m",
                        "solved": 5}],
    ["badia", "abaco", {"word": f"\033[1m\033[43m\033[30m{'B'}\033[0m"
                                f"\033[1m\033[43m\033[30m{'A'}\033[0m"
                                f"\033[1m\033[47m\033[30m{'D'}\033[0m"
                                f"\033[1m\033[47m\033[30m{'I'}\033[0m"
                                f"\033[1m\033[43m\033[30m{'A'}\033[0m",
                        "solved": 0}],
    ["badia", "badal", {"word": f"\033[1m\033[42m\033[30m{'B'}\033[0m"
                                f"\033[1m\033[42m\033[30m{'A'}\033[0m"
                                f"\033[1m\033[42m\033[30m{'D'}\033[0m"
                                f"\033[1m\033[47m\033[30m{'I'}\033[0m"
                                f"\033[1m\033[43m\033[30m{'A'}\033[0m",
                        "solved": 3}]
]


# Testing the function word_intro
class Test_word_intro(unittest.TestCase):
    # Test 1: Let's try if we got an error message when type a too short or too long word. As the function needs to
    # end the last input is correct, but we only take care of the first two inputs
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=test_len_word_intro_inputs)
    def test_len(self, mock_input, mock_output):
        word_intro()
        output = mock_output.getvalue().strip().splitlines()
        for line in output:
            self.assertEqual(line, "Your word hasn't the correct length, it have to be 5 letters long")

    # Test 2: Let's try if we got an error message when type a not alpha value. As the function needs to
    # end the last input is correct, but we only take care of the first two inputs
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=test_chars_word_intro_inputs)
    def test_chars(self, mock_input, mock_output):
        word_intro()
        output = mock_output.getvalue().strip().splitlines()
        for line in output:
            print(line)
            self.assertEqual(line, "Your input isn't a word, only words are allowed")

    # Test 3: Let's try if we get a return if we place a correct word but with caps. We try two times
    @patch('builtins.input', side_effect=test_caps_word_intro_inputs)
    def test_caps(self, mock_input):
        words = test_caps_word_intro_inputs
        for w in words:
            self.assertEqual(word_intro(), w.lower())

    # Test 4: Let's try if we get a return if we place a correct word in the function. We try two times
    @patch('builtins.input', side_effect=test_correct_word_intro_inputs)
    def test_correct(self, mock_input):
        words = test_correct_word_intro_inputs
        for w in words:
            self.assertEqual(word_intro(), w)


# Testing the function ask_user
class Test_ask_user(unittest.TestCase):
    # Test 1: Let's try if the function ask for new input when we input a string that isn't "y" or "n"
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=incorrect_ask_user_inputs)
    def test_bad_input(self, mock_input, mock_output):
        ask_user("Question")
        output = mock_output.getvalue().strip().splitlines()
        for line in output:
            self.assertEqual(line, "Please enter a valid input")

    # Test 2: Let's try if we got True if we input "y"
    @patch('builtins.input', side_effect=correct_yes_ask_user_inputs)
    def test_chars(self, mock_input):
        words = correct_yes_ask_user_inputs
        for w in words:
            self.assertEqual(ask_user("Question"), True)

    # Test 3: Let's try if we get False if we input "n"
    @patch('builtins.input', side_effect=correct_no_ask_user_inputs)
    def test_correct_word(self, mock_input):
        words = correct_no_ask_user_inputs
        for w in words:
            self.assertEqual(ask_user("Question"), False)


# Testing the function check_game
class Test_check_game(unittest.TestCase):
    # Testing the game
    def test_game(self):
        for w in params_test_game:
            self.assertEqual(check_game(w[0], w[1]), w[2])


if __name__ == '__main__':
    unittest.main()
