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


# Example usage with a specific alphabet
alphabet = ["A", "C", "G", "T"]  # Example for a DNA sequence
string = "AGA"

print(get_hash(string, alphabet))
