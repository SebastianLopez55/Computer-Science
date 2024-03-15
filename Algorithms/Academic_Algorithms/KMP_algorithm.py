"""
This module implements the Knuth-Morris-Pratt (KMP) algorithm for substring search. The KMP algorithm 
offers efficient string matching by precomputing the longest prefix that is also a suffix for all 
prefixes of the pattern, allowing the search to skip ahead based on this information. This results in 
a linear time search in the worst case, significantly improving over naive search methods, especially 
for patterns with repeating substrings. 

Note: KMP is especially efficient when you are searching for a single pattern in a text, as its
preprocessing step optimizes subsequent searches for that pattern.

Functions:
- longest_prefix_suffix(s): Computes the longest prefix-suffix table for a given pattern.
- occurrence_in_string(text, word): Searches for a word within a text using the KMP algorithm.
- test_longest_prefix_suffix(): Runs tests on the longest_prefix_suffix function.
- test_occurrence_in_string(): Runs tests on the occurrence_in_string function.
"""


def longest_prefix_suffix(s: str) -> list:
    """
    Computes the longest proper prefix which is also a suffix (LPS) array for a given string.
    This array is essential for the KMP algorithm to determine where to resume the search
    after a mismatch.

    Parameters:
    - s (str): The pattern string for which to compute the LPS array.

    Returns:
    - list: An array of integers representing the longest proper prefix which is also a suffix
            for each prefix of the string.
    """
    if s == "":
        return []
    n = len(s)
    lps_table = [0] * n
    prev_lps, curr_char_idx = 0, 1

    while curr_char_idx < n:
        if s[prev_lps] == s[curr_char_idx]:
            prev_lps += 1
            lps_table[curr_char_idx] = prev_lps
            curr_char_idx += 1
        elif prev_lps == 0:
            lps_table[curr_char_idx] = 0
            curr_char_idx += 1
        else:
            prev_lps = lps_table[prev_lps - 1]
    return lps_table

    # O(n) time
    # O(n) space


# KMP Algorithm
def occurrence_in_string(text: str, word: str):
    """
    Searches for the first occurrence of a word within a text using the Knuth-Morris-Pratt (KMP) algorithm.

    Parameters:
    - text (str): The text in which to search for the word.
    - word (str): The word to search for within the text.

    Returns:
    - int: The index of the first character of the first occurrence of the word in the text,
           or -1 if the word is not found.
    """
    if not text or not word:
        return -1

    word_lps_table = longest_prefix_suffix(word)
    i, j = 0, 0
    while i < len(text):
        if text[i] == word[j]:
            i, j = i + 1, j + 1
        elif j == 0:
            i += 1
        else:
            j = word_lps_table[j - 1]

        if j == len(word):
            return i - len(word)
    return -1

    # O(n + m) time
    # O(m) space


# TESTING
def test_longest_prefix_suffix():
    """
    Tests the longest_prefix_suffix function with various cases, including general patterns, empty strings,
    no repeating pattern, all characters being the same, and single character strings.
    """
    # Test case 1: General case with a repeating pattern
    assert longest_prefix_suffix("btab") == [0, 0, 0, 1], "Test case 1 failed: 'abtab'"

    # Test case 2: Empty string
    assert longest_prefix_suffix("") == [], "Test case 2 failed: Empty string"

    # Test case 3: No repeating pattern
    assert longest_prefix_suffix("abcd") == [0, 0, 0, 0], "Test case 3 failed: 'abcd'"

    # Test case 4: All characters are the same
    assert longest_prefix_suffix("aaaa") == [0, 1, 2, 3], "Test case 4 failed: 'aaaa'"

    # Test case 5: Single character string
    assert longest_prefix_suffix("a") == [0], "Test case 5 failed: 'a'"

    print("All test cases passed!")


def test_occurrence_in_string():
    """
    Tests the occurrence_in_string function to ensure it correctly identifies the position of a word within
    a text, handles cases of words not found, and deals with special characters, empty strings, and edge cases.
    """
    # Test case 1: Word found at the beginning
    assert (
        occurrence_in_string("hello world", "hello") == 0
    ), "Test case 1 failed: Word 'hello' not found at the beginning."

    # Test case 2: Word found in the middle
    assert (
        occurrence_in_string("the quick brown fox", "quick") == 4
    ), "Test case 2 failed: Word 'quick' not found in the middle."

    # Test case 3: Word found at the end
    assert (
        occurrence_in_string("subscribe to pewdiepie", "pie") == 19
    ), "Test case 3 failed: Word 'pie' not found at the end."

    # Test case 4: Word not found
    assert (
        occurrence_in_string("hello world", "bye") == -1
    ), "Test case 4 failed: Word 'bye' incorrectly found."

    # Test case 5: Empty text string
    assert (
        occurrence_in_string("", "hello") == -1
    ), "Test case 5 failed: Non-empty word found in empty text."

    # Test case 6: Empty word string (depending on your definition, might always return 0 or -1)
    assert (
        occurrence_in_string("hello world", "") == -1
    ), "Test case 6 failed: Empty word should return -1."

    # Test case 7: Word is longer than text
    assert (
        occurrence_in_string("hi", "hello") == -1
    ), "Test case 7 failed: Longer word found in shorter text."

    # Test case 8: Exact match
    assert (
        occurrence_in_string("hello", "hello") == 0
    ), "Test case 8 failed: Exact word not matched exactly."

    # Test case 9: Repeated patterns
    assert (
        occurrence_in_string("abababab", "abab") == 0
    ), "Test case 9 failed: Repeated pattern 'abab' not found at start."

    # Test case 10: Special characters
    assert (
        occurrence_in_string("fun&!!fun&!!", "&!!") == 3
    ), "Test case 10 failed: Special characters '&!!' not found."

    print("All test cases passed!")


test_longest_prefix_suffix()
test_occurrence_in_string()
