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
    a = len(alphabet)
    n = len(sequence)
    mappings = {char: i + 1 for i, char in enumerate(alphabet)}
    numbers = [mappings[char] for char in sequence]

    hash_value = 0
    # Compute of polynomial rolling hash.
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
        print("Hash Value of", sequence[i : i + k], hash_value)


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


test_get_hash()
