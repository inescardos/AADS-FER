class TrieNode:
    def __init__(self):
        self.children = {}      # Child nodes (dictionary of characters)
        self.is_end = False     # Marks the end of a word
        self.indices = []       # Store the indices of word occurrences
        self.depth = 0          # Depth of the node (length of the substring it represents)

class PrefixTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, index=None):
        """
        Reverses the word, insertis, and then inserts all its suffixes into the trie.
        :param word: The word to insert (string).
        :param index: Optional, index of the word occurrence (int).
        :return: None

        Time Complexity: O(n^2), where n is the length of the word.
        Space Complexity: O(n^2), for the additional nodes created in the trie.
        """
        word = word[::-1]  # Reverse the word before inserting
        for i in range(len(word)):
            suffix = word[i:]
            node = self.root
            for char in suffix:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                if index is not None:
                    node.indices.append(index)
            node.is_end = True
        print(f"Inserted all suffixes (inverted): '{word[::-1]}'")

    def find_pattern(self, pattern):
        """
        Checks if a pattern exists in the trie as a substring.
        - Reverses the pattern and searches for it recursively in the trie.
        - Traverses the trie to find matching paths.
        :param pattern: Pattern to check (string).
        :return: True if pattern exists, False otherwise.

        Time Complexity: O(n * m), where n is the length of the pattern and m is the total number of nodes in the trie.
        Space Complexity: O(n), for the recursion stack during the pattern match.
        """
        pattern = pattern[::-1]

        def _search_from_node(node, pattern, depth=0):
            if depth == len(pattern):
                return True

            char = pattern[depth]
            if char not in node.children:
                return False

            return _search_from_node(node.children[char], pattern, depth + 1)

        def _traverse_and_match(node, pattern):
            if _search_from_node(node, pattern):
                return True

            for child in node.children.values():
                if _traverse_and_match(child, pattern):
                    return True

            return False

        if _traverse_and_match(self.root, pattern):
            print(f"Pattern '{pattern[::-1]}' exists as a substring.")
            return True
        else:
            print(f"Pattern '{pattern[::-1]}' does not exist as a substring.")
            return False

    def find_longest_common_substring(self, word):
        """
        Finds the longest common substring between the trie and the given word.
        Compares the suffixes of the reversed word against the trie.
        :param word: Word to compare with the trie (string).
        :return: Longest common substring (string).

        Time Complexity: O(n*m), where n is the length of the word and m is the maximum depth of the trie (length of the longest substring stored)
        Space Complexity: O(m), for storing the current substring during traversal.
        """
        word = word[::-1]  # Reverse the word to match the trie structure
        longest_common_substring = ""
        current_substring = []

        def search(node, index):
            nonlocal longest_common_substring
            if index == len(word):
                return

            char = word[index]
            if char in node.children:
                current_substring.append(char)
                search(node.children[char], index + 1)

                if len(current_substring) > len(longest_common_substring):
                    longest_common_substring = "".join(current_substring)

                current_substring.pop()

        for i in range(len(word)):
            search(self.root, i)

        return longest_common_substring[::-1]
    
    def count_substring_occurrences(self, pattern):
        """
        Counts the number of occurrences of a pattern in the string.
        :param pattern: Pattern to count (string).
        :return: Number of occurrences (int).

        Time Complexity: O(n*m), where n is the length of the original word, and m the length of the pattern.
        Space Complexity: O(m), for the recursion stack during the DFS.
        """
        pattern = pattern[::-1]  # Reverse the pattern to match the trie structure
        total_count = 0
        node = self.root

        for depth, char in enumerate(pattern):
            if char in node.children:
                node = node.children[char]
            else:
                # Pattern does not exist in the trie
                return 0

        # Count occurrences from this node
        def count_end_nodes(current_node):
            """
            Counts all end nodes (representing full occurrences) starting from the current node.
            """
            nonlocal total_count
            if current_node.is_end:
                total_count += 1
            for child in current_node.children.values():
                count_end_nodes(child)

        # Start counting from the node where the pattern ends
        count_end_nodes(node)
        #print(f"Pattern '{pattern[::-1]}' occurs {total_count} time(s).")
        return total_count
    

def lz_compress(trie, input_string):
    """
    Compresses the input string using the LZ algorithm with the provided trie structure.

    :param trie: An instance of PrefixTrie.
    :param input_string: The string to compress.
    :return: List of tuples (index, char).
    """
    compressed_data = [] 
    node = trie.root 
    trie.next_index = 1 
    prefix_index = 0 

    print("Starting compression...")
    for char in input_string:
        print(f"Processing character: {char}")
        if char in node.children:
            node = node.children[char] 
            prefix_index = node.depth
            print(f"Found existing prefix: (index={prefix_index})")
        else:
            print(f"New substring detected. Outputting ({prefix_index}, {char})")
            compressed_data.append((prefix_index, char))

            # Add a new node to the trie for the new substring (prefix + char)
            new_node = TrieNode() 
            node.children[char] = new_node  # Add it as a child of the current node
            new_node.depth = trie.next_index  # Assign the next available index to the new node
            print(f"Adding new node for substring '{char}' with index {trie.next_index}")
            trie.next_index += 1  # Increment the next index counter

            # Reset for the next iteration:
            node = trie.root
            prefix_index = 0 

    if prefix_index > 0:
        print(f"Remaining prefix detected. Outputting ({prefix_index}, '')")
        compressed_data.append((prefix_index, "")) 

    print("Compression complete.")
    print("Compressed data:", compressed_data)
    return compressed_data


def lz_decompress(compressed_data):
    dictionary = {0: ""}
    decompressed_string = []

    for index, char in compressed_data:
        prefix = dictionary[index]
        substring = prefix + char
        decompressed_string.append(substring)
        dictionary[len(dictionary)] = substring

    return "".join(decompressed_string)


def main():
    trie = PrefixTrie()

    # Example strings to test
    test_string = "banana"
    test_pattern1 = "ana"
    test_pattern2 = "na"
    test_pattern3 = "a"
    test_pattern4 = "xyz"
    common_string1 = "canada"
    common_string2 = "ananas"

    # Test the `insert` method
    print("\n=== Testing insert ===")
    trie.insert(test_string)
    print("Inserted string:", test_string)

    # Test the `find_pattern` method
    print("\n=== Testing find_pattern ===")
    exists = trie.find_pattern(test_pattern1)
    print(f"Does pattern '{test_pattern1}' exist in '{test_string}'?", exists)
    exists = trie.find_pattern(test_pattern4)
    print(f"Does pattern '{test_pattern4}' exist in '{test_string}'?", exists)

    # Test the `find_longest_common_substring` method
    print("\n=== Testing find_longest_common_substring ===")
    longest_common = trie.find_longest_common_substring(common_string1)
    print(f"Longest common substring between '{test_string}' and '{common_string1}':", longest_common)
    longest_common = trie.find_longest_common_substring(common_string2)
    print(f"Longest common substring between '{test_string}' and '{common_string2}':", longest_common)

    # Test the `count_substring_occurrences` method
    print("\n=== Testing count_substring_occurrences ===")
    count = trie.count_substring_occurrences(test_pattern1)
    print(f"Count of pattern '{test_pattern1}' in '{test_string}':", count)
    count = trie.count_substring_occurrences(test_pattern2)
    print(f"Count of pattern '{test_pattern2}' in '{test_string}':", count)
    count = trie.count_substring_occurrences(test_pattern3)
    print(f"Count of pattern '{test_pattern3}' in '{test_string}':", count)
    count = trie.count_substring_occurrences(test_pattern4)
    print(f"Count of pattern '{test_pattern4}' in '{test_string}':", count)

    # Test LZ compression
    print("\n=== Testing LZ compression ===")
    trie = PrefixTrie()

    # Input string to compress
    input_string = "abracadabraabracadabra"
    print("Input String", input_string )

    # Compress using the trie
    compressed = lz_compress(trie, input_string)
    print("Compressed:", compressed)

    # Decompress using the trie
    decompressed = lz_decompress(compressed)
    print("Decompressed:", decompressed)

if __name__ == "__main__":
    main()
