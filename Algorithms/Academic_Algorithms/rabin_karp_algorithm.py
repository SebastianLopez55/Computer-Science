"""
This module implements the Rabin-Karp algorithm for substring search and sequence identification. 
The Rabin-Karp algorithm uses a 'rolling hash' to quickly filter out positions in the text that 
cannot match the pattern, and then checks for a match at the remaining positions. It is particularly 
efficient for multiple pattern search and finding repeated sequences within a string, utilizing 
polynomial hashing for efficient hash computation and comparison.

Functions:
- get_hash(string, alphabet, modulus): Computes the polynomial hash of a given string.
- find_repeated_sequences(sequence, k, alphabet): Finds all repeated sequences of a specified length within a string.
- test_get_hash(): Runs tests on the get_hash function.
- test_find_repeated_sequences(): Runs tests on the find_repeated_sequences function.
"""


def get_hash(string: str, alphabet=None, modulus=1000000007):
    """
    Computes the polynomial hash for a given string using a specified alphabet and modulus.
    The hash is calculated by mapping each character of the string to a unique integer,
    and then computing a polynomial accumulation of those integers modulated by a prime number.

    Parameters:
    - string (str): The string to hash.
    - alphabet (list[str]): The alphabet used to map characters to integers. If None, uses the order in the string.
    - modulus (int): The modulus to prevent integer overflow.

    Returns:
    - int: The polynomial hash value of the string.
    """
    k = len(string)
    a = len(alphabet)
    mappings = {char: i + 1 for i, char in enumerate(alphabet)}

    hash_value = 0
    for i in range(k):
        char_value = mappings.get(string[i])
        hash_value += (char_value * (a ** (k - i - 1))) % modulus
    return hash_value


def find_repeated_sequences(sequence, k, alphabet):
    """
    Identifies and returns all unique sequences of length 'k' that occur more than once
    in the given sequence using the Rabin-Karp algorithm. It uses polynomial hashing to efficiently
    search for repeated sequences.

    Parameters:
    - sequence (str): The sequence in which to search for repeated patterns.
    - k (int): The length of sequences to search for.
    - alphabet (list[str]): The alphabet from which the sequence is composed.

    Returns:
    - list[str]: A list of unique sequences that are repeated in the original sequence.
    """
    print_substrings = False  # Used for testing
    if print_substrings:
        print("\nInput Sequence: ", sequence)

    a = len(alphabet)
    n = len(sequence)
    mappings = {char: i + 1 for i, char in enumerate(alphabet)}
    numbers = [mappings[char] for char in sequence]
    visited, repeated = set(), set()

    # Compute of polynomial rolling hash.
    hash_value = 0
    for i in range(n - k + 1):
        if i == 0:
            # Computes polynomial stationary hash first.
            for j in range(k):
                char_value = mappings.get(sequence[j])
                hash_value += char_value * (a ** (k - j - 1))
        else:
            # Compute polynomial rolling hash.
            prev_hash = hash_value
            out_window_hash = numbers[i - 1] * (a ** (k - 1))
            in_window_hash = numbers[i + k - 1]
            hash_value = ((prev_hash - out_window_hash) * a) + in_window_hash

        if hash_value in visited:
            repeated.add(sequence[i : i + k])
        else:
            visited.add(hash_value)

        if print_substrings:
            print(
                "\tHash value of ",
                sequence[i : i + k],
                ":",
                hash_value,
                "\n\tVisited: ",
                visited,
                "\n\tRepeated: ",
                repeated,
                "\n",
            )

    return list(repeated)


# O(n) average time.
# O(n) space, thanks to numbers and visited set.


# TESTING
def test_get_hash():
    """
    Tests the get_hash function with predefined test cases to verify the accuracy of the hash computation.
    Covers basic cases, including simple strings, longer strings with repeated patterns, and edge cases like
    empty strings.
    """
    alphabet = ["A", "C", "G", "T"]  # Example alphabet for DNA sequences

    # Test case 1
    assert (
        get_hash("AGA", alphabet) == 29
    ), "Test case 1 failed: Hash values do not match."

    # Test case 2
    assert (
        get_hash("AGACCTAGAC", alphabet) == 486518
    ), "Test case 2 failed: Hash values do not match."

    # Test case 3: Repeated character
    assert (
        get_hash("AAAAACCCCCAAAAACCCCCC", alphabet, 1467445762730 + 1) == 1467445762730
    ), "Test case 3 failed"

    # Test case 4: Empty string
    assert (
        get_hash("", alphabet) == 0
    ), "Test case 4 failed: Hash value for an empty string should be 0."

    print("All test cases passed!")


def test_find_repeated_sequences():
    """
    Tests the find_repeated_sequences function with various sequences to ensure it accurately identifies and
    returns all unique sequences of a specified length that occur more than once. Test cases include sequences
    with no repeats, simple and complex repeats, and sequences composed of a single repeating character.
    """
    alphabet = ["A", "C", "G", "T"]  # Example alphabet for DNA sequences

    # Test case 1: No repeats
    assert (
        find_repeated_sequences("ACGT", 3, alphabet) == []
    ), "Test case 1 failed: Expected no repeated sequences."

    # Test case 2: Simple repeats
    sequence = "AGACCTAGAC"
    k = 3
    expected = ["AGA", "GAC"]  # Expected repeated sequences
    assert sorted(find_repeated_sequences(sequence, k, alphabet)) == sorted(
        expected
    ), "Test case 2 failed: Expected repeated sequences not found."

    # Test case 3: Longer repeats
    sequence = "AAAAACCCCCAAAAACCCCCC"
    k = 8
    expected = ["AAAAACCC", "AAACCCCC", "AAAACCCC"]  # Expected repeated sequences
    assert sorted(find_repeated_sequences(sequence, k, alphabet)) == sorted(
        expected
    ), "Test case 3 failed: Expected longer repeated sequences not found."

    # Test case 4: Repeats with a single character
    sequence = "GGGGGGGGGGGGGGGGGGGGGGGGG"
    k = 12
    expected = ["GGGGGGGGGGGG"]  # Expected repeated sequence
    assert sorted(find_repeated_sequences(sequence, k, alphabet)) == sorted(
        expected
    ), "Test case 4 failed: Expected repeated sequences of single character not found."

    print("All test cases passed!")


test_get_hash()
test_find_repeated_sequences()
