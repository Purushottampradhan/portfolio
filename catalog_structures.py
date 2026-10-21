"""Sections 7–12."""


def register(add):
    add("topic-7-1", "Reverse the characters", "string", ["s", "out", "i"],
        "Return s reversed, built one character at a time.",
        "A string is a row of characters. Reversing reads from the last index and writes a new row.",
        ["Start an empty list of characters.", "Append from the end of s toward the start.", "Join the characters into the output string."],
        "Walk backward and join.",
        """
        def solve(s):
            out = []
            i = len(s) - 1
            while i >= 0:
                out.append(s[i])
                i = i - 1
            return "".join(out)
        """,
        ["solve('dsa')", "solve('')", "solve('a')"],
        expect=["asd", "", "a"])

    add("topic-7-2", "Letter counts", "hash", ["s", "freq", "ch"],
        "Return the sorted list of [character, count] for every character in s.",
        "Frequency counting stores a tally for each character. The dictionary is that table.",
        ["Add 1 for each character.", "Read the table.", "Return the pairs in sorted order."],
        "Count characters, then sort the pairs.",
        """
        def solve(s):
            freq = {}
            for ch in s:
                if ch not in freq:
                    freq[ch] = 0
                freq[ch] = freq[ch] + 1
            return sorted(freq.items())
        """,
        ["solve('aba')", "solve('')", "solve('ccc')"],
        expect=[[("a", 2), ("b", 1)], [], [("c", 3)]])

    add("topic-7-3", "Are they anagrams", "hash", ["a", "b", "freq", "ch"],
        "Return True when a and b use the same characters the same number of times.",
        "An anagram is two strings with the same frequency table. Build the table for one, then undo it with the other.",
        ["Count characters in a.", "Subtract characters in b.", "True only if every count returns to 0."],
        "Compare frequency tables.",
        """
        def solve(a, b):
            if len(a) != len(b):
                return False
            freq = {}
            for ch in a:
                if ch not in freq:
                    freq[ch] = 0
                freq[ch] = freq[ch] + 1
            for ch in b:
                if ch not in freq or freq[ch] == 0:
                    return False
                freq[ch] = freq[ch] - 1
            return True
        """,
        ["solve('listen', 'silent')", "solve('ab', 'aa')", "solve('', '')"],
        expect=[True, False, True])

    add("topic-7-4", "Longest palindrome slice", "string", ["s", "best", "i", "l", "r"],
        "Return the longest palindromic substring. If there are two of the same length, keep the one found first.",
        "A palindrome reads the same from both ends. Expand around a center and store the best slice.",
        ["Try each index as a center.", "Grow while the two sides match.", "Keep the longer slice."],
        "Expand around odd and even centers.",
        """
        def solve(s):
            best = ""
            i = 0
            while i < len(s):
                l = i
                r = i
                while l >= 0 and r < len(s) and s[l] == s[r]:
                    if r - l + 1 > len(best):
                        best = s[l:r + 1]
                    l = l - 1
                    r = r + 1
                l = i
                r = i + 1
                while l >= 0 and r < len(s) and s[l] == s[r]:
                    if r - l + 1 > len(best):
                        best = s[l:r + 1]
                    l = l - 1
                    r = r + 1
                i = i + 1
            return best
        """,
        ["solve('babad')", "solve('cbbd')", "solve('a')"],
        expect=["bab", "bb", "a"])

    add("topic-7-5", "Find the pattern", "string", ["text", "pat", "i", "j"],
        "Return the first index where pat occurs in text, or -1. Compare characters directly.",
        "Naive matching stores a start index i and a pattern index j. j resets when a character disagrees.",
        ["Line pat up at i.", "Walk j while characters match.", "Return i when j reaches the end of pat."],
        "Check every alignment.",
        """
        def solve(text, pat):
            if pat == "":
                return 0
            i = 0
            while i + len(pat) <= len(text):
                j = 0
                while j < len(pat) and text[i + j] == pat[j]:
                    j = j + 1
                if j == len(pat):
                    return i
                i = i + 1
            return -1
        """,
        ["solve('hello', 'll')", "solve('abc', 'd')", "solve('abc', '')"],
        expect=[2, -1, 0])

    add("topic-7-6", "Polynomial hash", "flow", ["s", "mod", "base", "h", "ch"],
        "Return the polynomial hash of s using base 31 and the given mod. An empty string hashes to 0.",
        "A string hash folds every character into one integer. Each step multiplies the stored hash by the base and adds the next character.",
        ["Start h at 0.", "h = (h * base + character code) % mod.", "Return h."],
        "Rolling polynomial hash.",
        """
        def solve(s, mod):
            base = 31
            h = 0
            for ch in s:
                h = (h * base + ord(ch)) % mod
            return h
        """,
        ["solve('ab', 97)", "solve('', 97)", "solve('a', 10)"],
        expect=[(ord("a") * 31 + ord("b")) % 97, 0, ord("a") % 10])

    add("topic-7-7", "Same window hash", "string", ["s", "k", "base", "mod", "h", "i"],
        "Return True when any two windows of length k in s have the same polynomial hash (base 31, mod 101). Overlapping windows count.",
        "A rolling hash updates the window in constant memory: drop the character that leaves and add the one that enters.",
        ["Hash the first window.", "Slide it, storing hashes you have seen.", "Return True on a repeated hash."],
        "Roll a window of length k.",
        """
        def solve(s, k):
            if k == 0 or k > len(s):
                return False
            base = 31
            mod = 101
            h = 0
            power = 1
            i = 0
            while i < k:
                h = (h * base + ord(s[i])) % mod
                if i < k - 1:
                    power = (power * base) % mod
                i = i + 1
            seen = {h: True}
            while i < len(s):
                leave = ord(s[i - k]) * power
                h = (h - leave) % mod
                h = (h * base + ord(s[i])) % mod
                if h in seen:
                    return True
                seen[h] = True
                i = i + 1
            return False
        """,
        ["solve('abcabc', 3)", "solve('abcd', 2)", "solve('aaa', 2)"],
        expect=[True, False, True])
    from catalog_trees import register as more
    more(add)

    add("topic-7-8", "Rabin-Karp index", "string", ["text", "pat", "h", "need", "i"],
        "Return the first index of pat in text using rolling hashes, or -1. Confirm a hash hit by comparing the slice, so a collision cannot fool you.",
        "Rabin-Karp hashes the pattern once, then rolls the same-sized window across the text. A matching hash is checked character by character.",
        ["Hash the pattern.", "Roll the text window.", "When hashes match, compare the actual characters."],
        "Rolling hash plus a direct check.",
        """
        def solve(text, pat):
            if pat == "":
                return 0
            if len(pat) > len(text):
                return -1
            base = 31
            mod = 101
            need = 0
            power = 1
            i = 0
            while i < len(pat):
                need = (need * base + ord(pat[i])) % mod
                if i < len(pat) - 1:
                    power = (power * base) % mod
                i = i + 1
            h = 0
            i = 0
            while i < len(pat):
                h = (h * base + ord(text[i])) % mod
                i = i + 1
            start = 0
            while True:
                if h == need and text[start:start + len(pat)] == pat:
                    return start
                if start + len(pat) >= len(text):
                    return -1
                leave = ord(text[start]) * power
                h = (h - leave) % mod
                h = (h * base + ord(text[start + len(pat)])) % mod
                start = start + 1
        """,
        ["solve('hello', 'll')", "solve('abc', 'd')", "solve('abc', '')"],
        expect=[2, -1, 0])

    add("topic-7-9", "KMP search", "string", ["text", "pat", "lps", "i", "j"],
        "Return the first index of pat in text using the KMP failure function, or -1.",
        "KMP stores, for each pattern prefix, how far you can fall back without re-reading the text. That table is lps.",
        ["Build lps so lps[i] is the longest proper prefix that is also a suffix.", "Scan the text with j pointing into the pattern.", "On a mismatch, set j = lps[j - 1] instead of restarting at 0."],
        "Build the LPS table, then scan.",
        """
        def solve(text, pat):
            if pat == "":
                return 0
            lps = []
            i = 0
            while i < len(pat):
                lps.append(0)
                i = i + 1
            length = 0
            i = 1
            while i < len(pat):
                if pat[i] == pat[length]:
                    length = length + 1
                    lps[i] = length
                    i = i + 1
                elif length > 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i = i + 1
            i = 0
            j = 0
            while i < len(text):
                if text[i] == pat[j]:
                    i = i + 1
                    j = j + 1
                    if j == len(pat):
                        return i - j
                elif j > 0:
                    j = lps[j - 1]
                else:
                    i = i + 1
            return -1
        """,
        ["solve('AABAACAADAABAABA', 'AABA')", "solve('aaaa', 'b')", "solve('abc', '')"],
        expect=[0, -1, 0])

    add("topic-7-10", "Z array", "string", ["s", "z", "i", "l", "r"],
        "Return the Z-array of s. z[0] is 0. z[i] is the longest substring starting at i that matches the prefix.",
        "The Z-array stores how far the prefix repeats at each index. The window [l, r] is a match already stored, so later indexes can copy from it.",
        ["Grow a match by comparing with the prefix.", "Remember the window that matched.", "Inside a window, copy a previous Z value and then extend."],
        "Classic Z-algorithm.",
        """
        def solve(s):
            n = len(s)
            z = []
            i = 0
            while i < n:
                z.append(0)
                i = i + 1
            l = 0
            r = 0
            i = 1
            while i < n:
                if i <= r:
                    if z[i - l] < r - i + 1:
                        z[i] = z[i - l]
                    else:
                        z[i] = r - i + 1
                while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                    z[i] = z[i] + 1
                if i + z[i] - 1 > r:
                    l = i
                    r = i + z[i] - 1
                i = i + 1
            return z
        """,
        ["solve('aabaac')", "solve('aaaa')", "solve('a')"],
        expect=[[0, 1, 0, 2, 1, 0], [0, 3, 2, 1], [0]])

    add("topic-7-11", "Expand the palindrome", "string", ["s", "best", "c", "l", "r"],
        "Return the longest palindromic substring by expanding around centers. Keep the earliest slice when lengths tie.",
        "Manacher's idea starts here: every palindrome has a center. Odd and even centers are both tried, and the best radius is stored.",
        ["Pick a center.", "Expand while both sides match.", "Store the best substring."],
        "Expand around every center.",
        """
        def solve(s):
            best = ""
            c = 0
            while c < len(s):
                radius = 0
                while radius < 2:
                    l = c
                    r = c + radius
                    while l >= 0 and r < len(s) and s[l] == s[r]:
                        if r - l + 1 > len(best):
                            best = s[l:r + 1]
                        l = l - 1
                        r = r + 1
                    radius = radius + 1
                c = c + 1
            return best
        """,
        ["solve('babad')", "solve('cbbd')", "solve('')"],
        expect=["bab", "bb", ""])

    add("topic-7-12", "Suffix order", "array", ["s", "pairs", "i"],
        "Return the suffix array of s: the starting indexes of the suffixes in lexicographic order.",
        "A suffix array stores starting indexes, not the strings themselves. Sorting those indexes orders the suffixes.",
        ["Pair each start index with its suffix.", "Sort the pairs by the suffix.", "Return only the indexes."],
        "Sort (suffix, index) pairs.",
        """
        def solve(s):
            pairs = []
            i = 0
            while i < len(s):
                pairs.append([s[i:], i])
                i = i + 1
            pairs.sort()
            out = []
            for pair in pairs:
                out.append(pair[1])
            return out
        """,
        ["solve('banana')", "solve('a')", "solve('')"],
        expect=[[5, 3, 1, 0, 4, 2], [0], []])

    add("topic-7-13", "Suffix trie size", "hash", ["s", "root", "node", "ch"],
        "Insert every suffix of s into a trie of nested dictionaries. Return how many nodes were created, not counting the root.",
        "A suffix tree compresses this picture. The trie stores each character of each suffix as a dictionary link.",
        ["For each start index, walk from the root.", "Create a dictionary when the character is missing.", "Count every created node."],
        "Insert every suffix and count new nodes.",
        """
        def solve(s):
            root = {}
            made = 0
            i = 0
            while i < len(s):
                node = root
                for ch in s[i:]:
                    if ch not in node:
                        node[ch] = {}
                        made = made + 1
                    node = node[ch]
                i = i + 1
            return made
        """,
        ["solve('aba')", "solve('a')", "solve('')"],
        expect=[5, 1, 0])

    add("topic-7-14", "Patterns in the text", "hash", ["text", "root", "node", "found"],
        "Patterns are he, she, and his. Return the patterns that occur in text, in the order a left-to-right trie scan discovers them.",
        "Aho-Corasick starts with a trie of every pattern. This scan walks from each text index and reports a pattern when the trie marks a word end.",
        ["Insert the three patterns into a trie.", "From each text index, walk while the next character exists.", "Record a pattern when you reach its end marker."],
        "Trie scan of he, she, and his.",
        """
        def solve(text):
            patterns = ["he", "she", "his"]
            root = {}
            for pat in patterns:
                node = root
                for ch in pat:
                    if ch not in node:
                        node[ch] = {}
                    node = node[ch]
                node["$"] = pat
            found = []
            i = 0
            while i < len(text):
                node = root
                j = i
                while j < len(text) and text[j] in node:
                    node = node[text[j]]
                    if "$" in node:
                        found.append(node["$"])
                    j = j + 1
                i = i + 1
            return found
        """,
        ["solve('she')", "solve('his')", "solve('abc')"],
        expect=[["she", "he"], ["his"], []])

    add("topic-7-15", "Repeating piece", "string", ["s", "best", "i", "j", "k"],
        "Return the longest substring that occurs at least twice, possibly overlapping. If none exists, return an empty string. On a tie, keep the one found first.",
        "Two start indexes i and j walk forward together while characters match. The matched slice is a repeat, and best stores the longest one.",
        ["Choose two different starts.", "Count the matching run.", "Keep the run if it is longer than best."],
        "Compare every pair of start indexes.",
        """
        def solve(s):
            best = ""
            i = 0
            while i < len(s):
                j = i + 1
                while j < len(s):
                    k = 0
                    while i + k < len(s) and j + k < len(s) and s[i + k] == s[j + k]:
                        k = k + 1
                    if k > len(best):
                        best = s[i:i + k]
                    j = j + 1
                i = i + 1
            return best
        """,
        ["solve('banana')", "solve('abcd')", "solve('aaa')"],
        expect=["ana", "", "aa"])
    from catalog_linear import register as more
    more(add)
