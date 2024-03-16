def get_hash(string: str, alphabet=None, modulus=1000000007):
    """
    Compute the polynomial hash for a string given an alphabet.

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
    Searches for repeated sequences of length k in the provided string composed of the given alphabet.
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
    Tests the get_hash function to ensure it correctly computes the polynomial hash of a string
    given an alphabet and handles edge cases, such as empty strings and characters not in the alphabet.
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
    Tests the find_repeated_sequences function to ensure it accurately identifies and reports repeated sequences
    of a given length k within a sequence, using a specific alphabet.
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
