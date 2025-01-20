import numpy as np
from bisect import bisect_left, bisect_right

class SuffixArray:
    def __init__(self, text):
        self.original_text = text
        self.text = text
        self.suffix_array = self.build_suffix_array(self.text)
        self.lcp_array = self.build_lcp_array()

    def build_suffix_array(self, s):
        """
        Constructs the suffix array using a radix sort-based approach.
        :param s: Input string.
        :return: Suffix array (numpy array of integers).

        Time Complexity: O(n log n), where n is the length of the input string.
        Space Complexity: O(n), as additional arrays are used for sorting and ranking.
        """
        n = len(s)
        m = 256  # Number of possible characters (ASCII range)

        sa = np.zeros(n, dtype=np.int32)       # Suffix array
        rk = np.zeros(n, dtype=np.int32)      # Current rankings
        tmp_rk = np.zeros(n, dtype=np.int32)  # Temporary rankings
        cnt = np.zeros(max(m, n), dtype=np.int32)  # Counting array

        # Initial ranking based on the first character
        for i in range(n):
            rk[i] = ord(s[i])
            cnt[rk[i]] += 1
        for i in range(1, m):
            cnt[i] += cnt[i - 1]
        for i in range(n - 1, -1, -1):
            sa[cnt[rk[i]] - 1] = i
            cnt[rk[i]] -= 1

        # Doubling phase
        d = 1
        while d < n:
            # Sort based on the second key
            rank = 0
            tmp_sa = np.zeros(n, dtype=np.int32)
            for i in range(n - d, n):
                tmp_sa[rank] = i
                rank += 1
            for i in range(n):
                if sa[i] >= d:
                    tmp_sa[rank] = sa[i] - d
                    rank += 1

            # Counting sort based on the first key
            cnt.fill(0)
            for i in range(n):
                cnt[rk[i]] += 1
            for i in range(1, max(m, n)):
                cnt[i] += cnt[i - 1]
            for i in range(n - 1, -1, -1):
                sa[cnt[rk[tmp_sa[i]]] - 1] = tmp_sa[i]
                cnt[rk[tmp_sa[i]]] -= 1

            # Update rankings
            tmp_rk[sa[0]] = 0
            rank = 0
            for i in range(1, n):
                a, b = sa[i], sa[i - 1]
                if rk[a] == rk[b] and (a + d < n and b + d < n and rk[a + d] == rk[b + d]):
                    tmp_rk[sa[i]] = rank
                else:
                    rank += 1
                    tmp_rk[sa[i]] = rank
            rk[:] = tmp_rk

            if rank == n - 1:
                break
            d *= 2

        return sa

    def build_lcp_array(self):
        """
        Constructs the LCP (Longest Common Prefix) array using the Kasai algorithm.
        :return: LCP array (numpy array of integers).

        Time Complexity: O(n), where n is the length of the input string.
        Space Complexity: O(n), as additional arrays are used for rank and LCP storage.
        """
        n = len(self.text)
        lcp = np.zeros(n, dtype=np.int32)
        rank = np.zeros(n, dtype=np.int32)
        for i, suffix in enumerate(self.suffix_array):
            rank[suffix] = i

        h = 0
        for i in range(n):
            if rank[i] > 0:
                j = self.suffix_array[rank[i] - 1]
                while i + h < n and j + h < n and self.text[i + h] == self.text[j + h]:
                    h += 1
                lcp[rank[i]] = h
                if h > 0:
                    h -= 1

        return lcp

    def get_suffixes(self):
        return [self.text[i:] for i in self.suffix_array]

    def pattern_search(self, pattern):
        """
        Searches for all occurrences of a pattern in the text using binary search on the suffix array.
        :param pattern: The pattern string to search for.
        :return: A tuple (exists, result), where:
            - exists (bool): True if the pattern exists in the text, False otherwise.
            - result (list): A list of starting indices where the pattern occurs in the text.

        Time Complexity: O(m log n), where m is the pattern length and n is the text length.
        Space Complexity: O(1).
        """
        sa = self.suffix_array
        n = len(self.text)
        m = len(pattern)

        def compare_suffix(index):
            """Helper function to compare the suffix with the pattern."""
            suffix = self.text[index:index + m]
            if suffix < pattern:
                return -1
            elif suffix > pattern:
                return 1
            return 0

        # Binary search for the leftmost match
        left = bisect_left(sa, pattern, key=lambda x: self.text[x:x + m])

        # Binary search for the rightmost match
        right = bisect_right(sa, pattern, key=lambda x: self.text[x:x + m])

        # Collect starting indices of matching suffixes
        result = [sa[i] for i in range(left, right)]

        # Determine if the pattern exists
        exists = len(result) > 0

        return exists, result

    def suffices_pattern_search(self, pattern):
        sa = self.suffix_array
        n = len(self.text)
        results = []

        for start in sa:
            suffix = self.text[start:]
            if pattern in suffix:
                results.append(suffix)

        return results

    def count_substring_occurrences(self, pattern):
        """
        Counts the occurrences of a pattern in the text using binary search on the suffix array.
        :param pattern: The pattern string to count.
        :return: Number of occurrences (integer).

        Time Complexity: O(m log n), where m is the pattern length and n is the text length.
        Space Complexity: O(m).
        """
        sa = self.suffix_array
        n = len(self.text)
        m = len(pattern)

        def compare_suffix(index):
            return self.text[index:index + m]

        left = bisect_left(sa, pattern, key=lambda x: compare_suffix(x))
        right = bisect_right(sa, pattern, key=lambda x: compare_suffix(x))

        return right - left

    def insert(self, new_text):
        self.text += new_text
        self.suffix_array = self.build_suffix_array(self.text)
        print(f"Inserted '{new_text}'. Rebuilt Suffix Array.")

    def delete(self, substring):
        index = self.text.find(substring)
        if index != -1:
            self.text = self.text[:index] + self.text[index + len(substring):]
            self.suffix_array = self.build_suffix_array(self.text)
            print(f"Deleted '{substring}'. Rebuilt Suffix Array.")
        else:
            print(f"Substring '{substring}' not found in text.")

    def lz_compress(self):
        """
        Compresses the text using the LZ77 compression algorithm, leveraging the suffix and LCP arrays.
        :return: A list of tuples representing the compressed data (offset, length, next character).
        
        Time Complexity: O(n log n), where n is the length of the text.
        Space Complexity: O(n), as the suffix array and LCP array are used.
        """
        n = len(self.text)
        result = []
        i = 0

        print("Starting LZ77 compression with suffix array...")
        while i < n:
            best_offset = 0
            best_length = 0

            print(f"\nProcessing position {i}: current substring '{self.text[i:]}'")
            
            # Binary search to narrow down candidate suffixes
            left, right = 0, len(self.suffix_array) - 1
            print(f"Performing binary search for suffix match...")
            while left <= right:
                mid = (left + right) // 2
                suffix_start = self.suffix_array[mid]
                suffix = self.text[suffix_start:suffix_start + (n - i)]
                current = self.text[i:]

                print(f"  Comparing suffix '{suffix}' (start: {suffix_start}) with '{current}'")

                if suffix < current:
                    left = mid + 1
                else:
                    right = mid - 1

            print(f"Binary search narrowed down to range [{max(0, left - 1)}, {min(len(self.suffix_array), left + 2) - 1}]")

            # Find the longest match among candidates
            for j in range(max(0, left - 1), min(len(self.suffix_array), left + 2)):
                suffix_start = self.suffix_array[j]
                if suffix_start >= i:
                    print(f"  Skipping suffix at index {suffix_start} (future suffix).")
                    continue  # Ignore future suffixes

                # Compute match length
                length = 0
                while i + length < n and suffix_start + length < n and self.text[suffix_start + length] == self.text[i + length]:
                    length += 1

                print(f"  Found match of length {length} at suffix index {suffix_start}.")

                if length > best_length:
                    best_length = length
                    best_offset = i - suffix_start
                    print(f"  New best match: offset={best_offset}, length={best_length}.")

            # Add match
            if best_length > 0:
                next_char = self.text[i + best_length] if i + best_length < n else None
                print(f"Adding match: offset={best_offset}, length={best_length}, next_char={next_char}.")
                result.append((best_offset, best_length, next_char))
                i += best_length + 1
            else:
                print(f"No match found. Adding literal: char='{self.text[i]}'.")
                result.append((0, 0, self.text[i]))
                i += 1

        print("\nCompression complete.")
        print("Compressed data:", result)
        return result


def find_longest_common_substring(str1, str2):
    """
    Finds the longest common substring between two strings using a combined suffix array and LCP array.
    :param str1: First input string.
    :param str2: Second input string.
    :return: The longest common substring (string).

    Time Complexity: O(n log n), where n is the combined length of the two strings.
    Space Complexity: O(n), due to suffix array and LCP array storage.
    """
    separator = '#'
    if separator in str1 or separator in str2:
        raise ValueError("Strings must not contain the separator character '#'.")

    concatenated = str1 + separator + str2

    suffix_array_obj = SuffixArray(concatenated)

    sa = suffix_array_obj.suffix_array
    lcp = suffix_array_obj.lcp_array
    text = suffix_array_obj.text

    n1 = len(str1)
    max_length = 0
    lcs_start = 0

    for i in range(1, len(lcp)):
        suffix1 = sa[i]
        suffix2 = sa[i - 1]

        if (suffix1 < n1 and suffix2 > n1) or (suffix2 < n1 and suffix1 > n1):
            if lcp[i] > max_length:
                max_length = lcp[i]
                lcs_start = suffix1 if suffix1 < n1 else suffix2

    return text[lcs_start:lcs_start + max_length]


def lz_decompress(compressed_data):
    """
    Decompresses a string that was compressed using the LZ77 algorithm.
    :param compressed_data: List of tuples (offset, length, next character) representing the compressed data.
    :return: The decompressed string.

    Time Complexity: O(n), where n is the length of the decompressed data.
    Space Complexity: O(n), as the decompressed string is constructed.
    """
    decompressed_text = []

    for offset, length, next_char in compressed_data:
        if offset > 0 and length > 0:
            start = len(decompressed_text) - offset
            for _ in range(length):
                decompressed_text.append(decompressed_text[start])
                start += 1

        if next_char is not None:
            decompressed_text.append(next_char)

    return ''.join(decompressed_text)


def main():
    test_string = "banana"
    suffix_array_obj = SuffixArray(test_string)

    print("\n=== Suffix Array ===")
    print(suffix_array_obj.suffix_array)

    print("\n=== Pattern Search ===")
    pattern = "ana"
    results, exists = suffix_array_obj.pattern_search(pattern)
    print(f"Pattern '{pattern}' exists: {exists}")
    print("Matching suffixes:", results)

    print("\n=== Count Substring Occurrences ===")
    count = suffix_array_obj.count_substring_occurrences(pattern)
    print(f"Count of pattern '{pattern}' in '{test_string}': {count}")

    print("\n=== Longest Common Substring ===")
    str1 = "canada"
    str2 = "ananas"
    longest_common = find_longest_common_substring(str1, str2)
    print(f"Longest common substring between '{str1}' and '{str2}': '{longest_common}'")

    print("\n=== LZ Compression ===")
    compressed = suffix_array_obj.lz_compress()
    print("Compressed:", compressed)

    print("\n=== LZ Decompression ===")
    decompressed = lz_decompress(compressed)
    print("Decompressed:", decompressed)

if __name__ == "__main__":
    main()
