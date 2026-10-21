"""Sections 1–6."""


def register(add):
    add("topic-1-1", "Add every number", "array", ["nums", "total", "x"],
        "Return the sum of every integer in nums.",
        "An algorithm is a finite list of steps. Each step reads one number from memory and writes an updated total.",
        ["Store 0 in total.", "Add one number at a time.", "Return total. That return value is the output."],
        "Start total at 0 and add each value.",
        """
        def solve(nums):
            total = 0
            for x in nums:
                total = total + x
            return total
        """,
        ["solve([4, 1, 7])", "solve([])", "solve([5])"],
        expect=[12, 0, 5])

    add("topic-1-2", "Highest score", "array", ["scores", "best", "x"],
        "Scores live in a list, which is a data structure. Return the largest score.",
        "A data structure decides how values sit in memory. A list stores them in a row, so a scan can visit every slot.",
        ["Remember the first score as best.", "Replace best when a later score is larger.", "Return the best score stored."],
        "Track the largest value while scanning the list.",
        """
        def solve(scores):
            best = scores[0]
            for x in scores:
                if x > best:
                    best = x
            return best
        """,
        ["solve([3, 9, 4, 2])", "solve([8])", "solve([-2, -5, -1])"],
        expect=[9, 8, -1])

    add("topic-1-3", "Count the positives", "array", ["nums", "count", "x"],
        "Before coding, define the question: how many values are strictly greater than 0? Return that count.",
        "Problem solving starts by naming the output. Here the output is a count, so memory needs a counter and the current value.",
        ["Set the counter to 0.", "Add 1 only when the current value is positive.", "Return the counter."],
        "Increase count only when a value is greater than 0.",
        """
        def solve(nums):
            count = 0
            for x in nums:
                if x > 0:
                    count = count + 1
            return count
        """,
        ["solve([3, -1, 0, 4])", "solve([])", "solve([-2, -3])"],
        expect=[2, 0, 0])

    add("topic-1-4", "Pair sum, the slow way", "array", ["nums", "i", "j", "target"],
        "Return True if any two different positions add up to target. Use two nested loops, the brute-force scan.",
        "Brute force tries every candidate. Two loops store two indices and test every pair.",
        ["Fix index i.", "Try every later index j.", "Return True as soon as nums[i] + nums[j] equals target."],
        "Check every pair with two loops.",
        """
        def solve(nums, target):
            i = 0
            while i < len(nums):
                j = i + 1
                while j < len(nums):
                    if nums[i] + nums[j] == target:
                        return True
                    j = j + 1
                i = i + 1
            return False
        """,
        ["solve([1, 4, 3, 2], 6)", "solve([1, 2], 2)", "solve([5], 5)"],
        expect=[True, False, False])

    add("topic-1-5", "Pair sum, remembered", "hash", ["nums", "seen", "x", "need"],
        "Return True if two values add up to target. Store values you have already seen so each new value is one lookup.",
        "Optimization replaces a repeated scan with memory. A dictionary remembers values already visited.",
        ["For each value, the partner is target minus that value.", "If the partner is already stored, you are done.", "Otherwise store the value and continue."],
        "Save each number in a dictionary as you go.",
        """
        def solve(nums, target):
            seen = {}
            for x in nums:
                need = target - x
                if need in seen:
                    return True
                seen[x] = True
            return False
        """,
        ["solve([1, 4, 3, 2], 6)", "solve([1, 2], 2)", "solve([5, 5], 10)"],
        expect=[True, False, True])

    add("topic-1-6", "Turn the steps into code", "array", ["nums", "total", "i"],
        "Pseudocode: set total to 0, then for each index add the value, then return total. Implement those steps.",
        "Pseudocode is the flow written in plain steps. Code is those steps stored as instructions the machine follows.",
        ["Write the starting value.", "Translate each 'for each' into a loop.", "The last step is the return, which creates the output."],
        "Follow the three written steps exactly.",
        """
        def solve(nums):
            total = 0
            i = 0
            while i < len(nums):
                total = total + nums[i]
                i = i + 1
            return total
        """,
        ["solve([2, 2, 2])", "solve([])", "solve([10, -4])"],
        expect=[6, 0, 6])

    add("topic-1-7", "Repair the running total", "array", ["nums", "total", "x"],
        "A buggy sum forgot the first item and started from 0 only after skipping index 0. Return the real sum of every item, including the first.",
        "Debugging compares what memory holds with what you expected. Watch total after each write.",
        ["Start total at 0 before the loop.", "Add every item, including the first.", "Return total and compare it with the example."],
        "Do not skip the first value.",
        """
        def solve(nums):
            total = 0
            for x in nums:
                total = total + x
            return total
        """,
        ["solve([5, 1, 1])", "solve([0])", "solve([-1, 1])"],
        expect=[7, 0, 0])

    add("topic-1-8", "Second largest", "array", ["nums", "first", "second", "x"],
        "Return the second largest distinct value. If it does not exist, return None.",
        "Edge cases are inputs that break a happy-path story: one item, duplicates, or an empty idea of 'second'.",
        ["Track the largest and the second largest.", "Ignore a value equal to the current largest.", "If second was never set, return None."],
        "Keep two champions and skip duplicates of the largest.",
        """
        def solve(nums):
            first = None
            second = None
            for x in nums:
                if first is None or x > first:
                    second = first
                    first = x
                elif x != first and (second is None or x > second):
                    second = x
            return second
        """,
        ["solve([4, 1, 4, 3])", "solve([7, 7])", "solve([2])"],
        expect=[3, None, None])

    add("topic-1-9", "Split the sentence", "array", ["text", "words", "word", "count"],
        "Count how many words in a sentence contain the letter a. A word is text split on spaces.",
        "Decomposition gives each part a job: split into words, then test one word, then count.",
        ["Break the sentence into a list of words.", "Test each word.", "Return how many words passed the test."],
        "Split on spaces, then count words that contain a.",
        """
        def solve(text):
            words = text.split(" ")
            count = 0
            for word in words:
                if "a" in word:
                    count = count + 1
            return count
        """,
        ["solve('a cat and a dog')", "solve('dog')", "solve('')"],
        expect=[4, 0, 0])

    add("topic-1-10", "Same pattern, new data", "hash", ["nums", "freq", "x", "best"],
        "Many problems are 'count how often each value appears'. Return the value that appears most. If there is a tie, return the smaller value.",
        "Pattern recognition means you have seen this shape before: a frequency table, then a scan for the best key.",
        ["Store a count for every value.", "Scan the table.", "Keep the value with the higher count, or the smaller value on a tie."],
        "Build a frequency dictionary, then pick the winner.",
        """
        def solve(nums):
            freq = {}
            for x in nums:
                if x not in freq:
                    freq[x] = 0
                freq[x] = freq[x] + 1
            best = None
            for x in freq:
                if best is None or freq[x] > freq[best] or (freq[x] == freq[best] and x < best):
                    best = x
            return best
        """,
        ["solve([2, 2, 3, 3, 3, 1])", "solve([4, 4, 1, 1])", "solve([9])"],
        expect=[3, 1, 9])

    add("topic-1-11", "How many comparisons", "flow", ["n", "pairs"],
        "A Fermi estimate counts work without running the real system. If every person shakes hands with every other person, return how many handshakes happen for n people.",
        "Estimation turns a story into one formula. n people each pair with n - 1 others, and each handshake was counted twice.",
        ["Store n.", "Compute n * (n - 1) / 2.", "That integer is the estimated output."],
        "Each unordered pair is one handshake.",
        """
        def solve(n):
            pairs = n * (n - 1) // 2
            return pairs
        """,
        ["solve(5)", "solve(1)", "solve(10)"],
        expect=[10, 0, 45])

    add("topic-1-12", "The sum invariant", "flow", ["n", "guess", "total", "i"],
        "An invariant is a fact that stays true. For 1 + 2 + ... + n, the closed form n * (n + 1) / 2 must match the loop. Return True when they match.",
        "Check the invariant by storing both the formula and the running sum. They should be equal at the end.",
        ["Compute the formula into guess.", "Add 1 through n into total.", "Return whether guess and total are the same object value."],
        "Compare the formula with an actual loop.",
        """
        def solve(n):
            guess = n * (n + 1) // 2
            total = 0
            i = 1
            while i <= n:
                total = total + i
                i = i + 1
            return guess == total
        """,
        ["solve(5)", "solve(0)", "solve(1)"],
        expect=[True, True, True])

    add("topic-2-1", "Types in one row", "array", ["text", "count", "flag", "score"],
        "Build a list that stores a string, an int, a bool, and a float-free whole number: the word, its length, whether it is non-empty, and the length times 2. Return that list.",
        "Each Python value has a type. The list is one object whose slots point at values of different types.",
        ["Read the string.", "Derive an int, a bool, and another int.", "Return them together so you can see four types in one structure."],
        "Return [word, length, non-empty, length * 2].",
        """
        def solve(text):
            count = len(text)
            flag = count > 0
            score = count * 2
            return [text, count, flag, score]
        """,
        ["solve('ok')", "solve('')", "solve('dsa')"],
        expect=[["ok", 2, True, 4], ["", 0, False, 0], ["dsa", 3, True, 6]])

    add("topic-2-2", "Keep the evens", "array", ["nums", "out", "x"],
        "Return a new list of the even numbers, in the same order. Use a condition inside a loop.",
        "A condition chooses a branch. A loop repeats that decision once per stored item.",
        ["Look at one number.", "Append it only when it is divisible by 2.", "Return the new list."],
        "Append x when x % 2 == 0.",
        """
        def solve(nums):
            out = []
            for x in nums:
                if x % 2 == 0:
                    out.append(x)
            return out
        """,
        ["solve([1, 2, 3, 4])", "solve([1, 3])", "solve([])"],
        expect=[[2, 4], [], []])

    add("topic-2-3", "One job per function", "flow", ["nums", "total"],
        "Write solve so it returns the average of nums as an integer division (sum // length). Use a nested helper named total_of to compute the sum.",
        "A function is a reusable frame of memory. solve calls total_of, waits for its return, then computes the average.",
        ["Call the helper. A new frame appears.", "The helper returns the sum.", "solve divides that sum by the length."],
        "Nested def total_of(nums) should add the numbers.",
        """
        def solve(nums):
            def total_of(nums):
                total = 0
                for x in nums:
                    total = total + x
                return total
            total = total_of(nums)
            return total // len(nums)
        """,
        ["solve([2, 4, 6])", "solve([5])", "solve([1, 2])"],
        expect=[4, 5, 1])

    add("topic-2-4", "Countdown product", "recursion", ["n", "rest"],
        "Return n! (1 for 0). Use recursion: n! = n * (n - 1)!, and 0! = 1.",
        "Each recursive call stores its own n. The frames pile up until n is 0, then each return multiplies on the way back.",
        ["If n is 0, return 1.", "Otherwise call solve(n - 1).", "Multiply the returned value by n."],
        "Base case 0 returns 1. Otherwise return n * solve(n - 1).",
        """
        def solve(n):
            if n == 0:
                return 1
            rest = solve(n - 1)
            return n * rest
        """,
        ["solve(4)", "solve(0)", "solve(1)"],
        expect=[24, 1, 1])

    add("topic-2-5", "Reverse into a new list", "array", ["nums", "out", "i"],
        "Return a new list with the same values in reverse order. Do not use slicing.",
        "A list is a growable row. Reading from the end and appending builds the reverse in new memory.",
        ["Start an empty output list.", "Walk the input from the last index down to 0.", "Append each value, then return the new list."],
        "Walk the indices backward and append.",
        """
        def solve(nums):
            out = []
            i = len(nums) - 1
            while i >= 0:
                out.append(nums[i])
                i = i - 1
            return out
        """,
        ["solve([1, 2, 3])", "solve([])", "solve([7])"],
        expect=[[3, 2, 1], [], [7]])

    add("topic-2-6", "Fixed pair", "array", ["pair", "a", "b"],
        "A tuple cannot be rewritten in place. Return a new tuple that swaps the two items of pair.",
        "Tuples are a fixed record. Updating one means building a new tuple and storing that.",
        ["Read both items.", "Build a new tuple in the other order.", "Return that new object."],
        "Return (pair[1], pair[0]).",
        """
        def solve(pair):
            a = pair[0]
            b = pair[1]
            return (b, a)
        """,
        ["solve((1, 2))", "solve(('x', 'y'))", "solve((0, 0))"],
        expect=[(2, 1), ("y", "x"), (0, 0)])

    add("topic-2-7", "Shared hobbies", "hash", ["a", "b", "both"],
        "Return the sorted list of hobbies that appear in both input lists.",
        "A set stores each value once. Intersection asks which values live in both sets.",
        ["Turn each list into a set.", "Keep values that are in both.", "Return those values in sorted order so the output is stable."],
        "Use sets, then sort the common values.",
        """
        def solve(a, b):
            both = set(a) & set(b)
            return sorted(both)
        """,
        ["solve(['chess', 'run', 'run'], ['run', 'swim'])", "solve([1, 2], [3])", "solve(['a'], ['a', 'a'])"],
        expect=[["run"], [], ["a"]])

    add("topic-2-8", "Word counts", "hash", ["words", "freq", "word"],
        "Return a list of [word, count] pairs sorted by word for the words in the list.",
        "A dictionary maps a key to a value. Here the key is the word and the value is how many times it was stored.",
        ["Start an empty dictionary.", "Add 1 for each word.", "Turn the items into a sorted list."],
        "Count with a dict, then return sorted pairs.",
        """
        def solve(words):
            freq = {}
            for word in words:
                if word not in freq:
                    freq[word] = 0
                freq[word] = freq[word] + 1
            return sorted(freq.items())
        """,
        ["solve(['a', 'b', 'a'])", "solve([])", "solve(['z'])"],
        expect=[[("a", 2), ("b", 1)], [], [("z", 1)]])

    add("topic-2-9", "Clean the word", "string", ["text", "out", "ch"],
        "Return the lowercase letters of text only, as a new string. Drop spaces, digits, and punctuation.",
        "A string is a row of characters. Building a new string writes only the characters you decide to keep.",
        ["Look at one character.", "Keep it when it is a letter.", "Join the kept characters into the output."],
        "Keep characters for which ch.isalpha() is true, then lowercase them.",
        """
        def solve(text):
            out = []
            for ch in text:
                if ch.isalpha():
                    out.append(ch.lower())
            return "".join(out)
        """,
        ["solve('Hi, Py!')", "solve('123')", "solve('A')"],
        expect=["hipy", "", "a"])

    add("topic-2-10", "Squares of evens", "array", ["nums", "out", "x"],
        "Return the squares of the even numbers, in order. Write the loop yourself so each square is a visible store.",
        "A comprehension is a compact loop that builds a list. The same memory story is: test, compute, append.",
        ["Visit each number.", "If it is even, store its square.", "Return the new list."],
        "Append x * x when x is even.",
        """
        def solve(nums):
            out = []
            for x in nums:
                if x % 2 == 0:
                    out.append(x * x)
            return out
        """,
        ["solve([1, 2, 3, 4])", "solve([1])", "solve([0, -2])"],
        expect=[[4, 16], [], [0, 4]])

    add("topic-2-11", "Sort by last letter", "array", ["words"],
        "Return the words sorted by their last character. Use a lambda as the sort key.",
        "A lambda is a tiny function object stored in memory and handed to sort. Sort calls it once per word.",
        ["Give sorted a key function.", "The key reads the last character.", "sorted returns a new list."],
        "sorted(words, key=lambda word: word[-1])",
        """
        def solve(words):
            return sorted(words, key=lambda word: word[-1])
        """,
        ["solve(['cat', 'bed', 'car'])", "solve(['b'])", "solve(['za', 'yb'])"],
        expect=[["bed", "car", "cat"], ["b"], ["za", "yb"]])

    add("topic-2-12", "Sort by abs, then value", "array", ["nums"],
        "Return nums sorted by absolute value, and by the number itself when absolute values tie. Use sorted.",
        "Python's sort is stable and can take a tuple key. The tuple is compared left to right.",
        ["Build a key (abs(x), x).", "Ask sorted to use it.", "Return the new list."],
        "key=lambda x: (abs(x), x)",
        """
        def solve(nums):
            return sorted(nums, key=lambda x: (abs(x), x))
        """,
        ["solve([3, -1, 1, -2])", "solve([0])", "solve([-2, 2])"],
        expect=[[-1, 1, -2, 3], [0], [-2, 2]])

    add("topic-2-13", "Cost of the tool", "flow", ["n", "loops", "lookups"],
        "A list append is treated as 1 step here, and a dict lookup as 1 step. Return [list_appends, dict_lookups] after doing n appends and n successful lookups.",
        "Built-in cost is about how many memory writes or hash jumps happen. This counter makes those costs visible.",
        ["Append n times onto a list.", "Store n keys, then look each up.", "Return both counters."],
        "Count appends and lookups separately.",
        """
        def solve(n):
            row = []
            loops = 0
            i = 0
            while i < n:
                row.append(i)
                loops = loops + 1
                i = i + 1
            table = {}
            i = 0
            while i < n:
                table[i] = i
                i = i + 1
            lookups = 0
            i = 0
            while i < n:
                lookups = lookups + (1 if i in table else 0)
                i = i + 1
            return [loops, lookups]
        """,
        ["solve(3)", "solve(0)", "solve(1)"],
        expect=[[3, 3], [0, 0], [1, 1]])

    add("topic-2-14", "First unique", "hash", ["nums", "freq", "order", "x"],
        "Return the first value that appears once. If every value repeats, return None. Use a count map.",
        "collections.Counter is a dictionary made for counts. The same picture is a dict plus a scan that keeps order.",
        ["Count every value.", "Scan again in original order.", "Return the first value whose count is 1."],
        "Count, then scan from left to right.",
        """
        def solve(nums):
            freq = {}
            for x in nums:
                if x not in freq:
                    freq[x] = 0
                freq[x] = freq[x] + 1
            for x in nums:
                if freq[x] == 1:
                    return x
            return None
        """,
        ["solve([2, 3, 2, 4, 3])", "solve([1, 1])", "solve([5])"],
        expect=[4, None, 5])

    add("topic-2-15", "K smallest with a heap", "array", ["nums", "heap", "x"],
        "Return the k smallest values in increasing order. Build that result with heapq.",
        "A heap keeps the smallest item at the front of its list. nsmallest reads that order for you.",
        ["Hand the list to the heap tool.", "Ask for k smallest.", "The returned list is sorted."],
        "import heapq and return heapq.nsmallest(k, nums).",
        """
        def solve(nums, k):
            import heapq
            heap = list(nums)
            heapq.heapify(heap)
            out = []
            while len(out) < k and heap:
                out.append(heapq.heappop(heap))
            return out
        """,
        ["solve([5, 1, 4, 2], 2)", "solve([3], 1)", "solve([2, 2, 1], 3)"],
        expect=[[1, 2], [3], [1, 2, 2]])

    add("topic-2-16", "Insertion index", "array", ["nums", "target", "lo", "hi", "mid"],
        "nums is sorted. Return the index where target should be inserted so the list stays sorted. Use binary search.",
        "bisect walks the middle of the remaining range. lo and hi shrink until they meet at the insertion slot.",
        ["Set lo to 0 and hi to the length.", "Move lo or hi from the middle.", "When they meet, lo is the index."],
        "Classic lower-bound binary search.",
        """
        def solve(nums, target):
            lo = 0
            hi = len(nums)
            while lo < hi:
                mid = (lo + hi) // 2
                if nums[mid] < target:
                    lo = mid + 1
                else:
                    hi = mid
            return lo
        """,
        ["solve([1, 3, 3, 5], 3)", "solve([1, 3, 5], 4)", "solve([], 1)"],
        expect=[1, 2, 0])

    add("topic-2-17", "Running totals from pairs", "array", ["pairs", "total", "out"],
        "pairs is a list of [value, times]. Return the list made by repeating each value that many times.",
        "itertools.repeat and chain expand data. The memory picture is the same if you append in two loops.",
        ["Read a value and a repeat count.", "Append the value that many times.", "Return the expanded list."],
        "For each pair, append the value `times` times.",
        """
        def solve(pairs):
            out = []
            for pair in pairs:
                value = pair[0]
                times = pair[1]
                i = 0
                while i < times:
                    out.append(value)
                    i = i + 1
            return out
        """,
        ["solve([[2, 3], [7, 1]])", "solve([[1, 0]])", "solve([])"],
        expect=[[2, 2, 2, 7], [], []])

    add("topic-2-18", "Fold with a start", "array", ["nums", "acc", "x"],
        "Return the sum of nums starting from the given start value. This is what functools.reduce does.",
        "A fold keeps one accumulator in memory and feeds it every item. The accumulator is the whole history compressed.",
        ["Store start in acc.", "Replace acc with acc + x for each item.", "Return acc."],
        "Start from start and add every number.",
        """
        def solve(nums, start):
            acc = start
            for x in nums:
                acc = acc + x
            return acc
        """,
        ["solve([1, 2, 3], 10)", "solve([], 4)", "solve([5], 0)"],
        expect=[16, 4, 5])

    add("topic-2-19", "Two names, one list", "array", ["shared", "alias", "i"],
        "Append the numbers 0, 1, ... n-1 onto a list, but also keep a second name for that same list. Return the length seen through the second name.",
        "Assignment stores a reference, not a copy. Both names point at one list object, so a write through one name is visible through the other.",
        ["Create one list.", "Point alias at that same object.", "Append through shared and read the length through alias."],
        "alias = shared, then append on shared.",
        """
        def solve(n):
            shared = []
            alias = shared
            i = 0
            while i < n:
                shared.append(i)
                i = i + 1
            return len(alias)
        """,
        ["solve(3)", "solve(0)", "solve(1)"],
        expect=[3, 0, 1])

    add("topic-2-20", "Growth of a list", "array", ["row", "caps", "i"],
        "Python lists grow by reserving extra slots. Simulate a capacity that starts at 0 and doubles when an append does not fit, beginning at 1. Return the list of capacities after each of n appends.",
        "Amortized growth means most appends are cheap, and sometimes one append copies into a bigger block. The capacity variable is that block size.",
        ["If the next item does not fit, double the capacity (or set it to 1).", "Record the capacity.", "Do this n times."],
        "When size would pass capacity, set capacity to max(1, capacity * 2).",
        """
        def solve(n):
            size = 0
            cap = 0
            caps = []
            i = 0
            while i < n:
                if size + 1 > cap:
                    if cap == 0:
                        cap = 1
                    else:
                        cap = cap * 2
                size = size + 1
                caps.append(cap)
                i = i + 1
            return caps
        """,
        ["solve(5)", "solve(1)", "solve(0)"],
        expect=[[1, 2, 4, 4, 8], [1], []])

    add("topic-2-21", "Equal is not identical", "flow", ["a", "b", "c"],
        "Build two different empty lists a and b, and a third name c that refers to a. Return [a == b, a is b, a is c].",
        "== compares values. is compares identity: whether two names point at the same object in memory.",
        ["Create two separate empty lists.", "Alias the first one.", "Compare value and identity."],
        "Return [a == b, a is b, a is c].",
        """
        def solve(flag):
            a = []
            b = []
            c = a
            if flag:
                a.append(1)
                b.append(1)
            return [a == b, a is b, a is c]
        """,
        ["solve(False)", "solve(True)"],
        expect=[[True, False, True], [True, False, True]])

    add("topic-2-22", "One runner at a time", "flow", ["turn", "log", "a", "b"],
        "Two tasks each need to count to n, but only one task runs a single step at a time, like the GIL running one Python thread. Return the log of who ran: 'a', 'b', 'a', 'b', ...",
        "The GIL story in one picture: a turn variable decides which task may write. The other task waits in memory.",
        ["Let a take one step and flip the turn.", "Let b take one step and flip the turn.", "Stop when both have reached n."],
        "Alternate one increment of a and one of b.",
        """
        def solve(n):
            turn = "a"
            log = []
            a = 0
            b = 0
            while a < n or b < n:
                if turn == "a" and a < n:
                    a = a + 1
                    log.append("a")
                    turn = "b"
                elif b < n:
                    b = b + 1
                    log.append("b")
                    turn = "a"
                else:
                    turn = "a"
            return log
        """,
        ["solve(2)", "solve(0)", "solve(1)"],
        expect=[["a", "b", "a", "b"], [], ["a", "b"]])

    add("topic-3-1", "Count the nested steps", "flow", ["n", "steps", "i", "j"],
        "A double loop runs i from 0 to n-1 and, for each i, j from 0 to n-1. Return how many inner-body steps run. That count is the concrete meaning of O(n^2) for this loop.",
        "Big-O names how the step count grows. Here you can watch the counter itself climb by n * n.",
        ["Reset a step counter.", "Add 1 in the inner body.", "Return the counter and compare it with n * n."],
        "Count inner-loop body executions.",
        """
        def solve(n):
            steps = 0
            i = 0
            while i < n:
                j = 0
                while j < n:
                    steps = steps + 1
                    j = j + 1
                i = i + 1
            return steps
        """,
        ["solve(3)", "solve(0)", "solve(1)"],
        expect=[9, 0, 1])

    add("topic-3-2", "Best and upper labels", "flow", ["n", "lower", "upper"],
        "For a loop that always runs n times, Theta(n) means the tight bound is n. Return [n, n]: a lower bound and an upper bound that match.",
        "O is an upper bound, Omega a lower bound, Theta means they meet. When the loop always does n steps, both bounds are n.",
        ["Store n.", "Set both bounds to n.", "Return the pair."],
        "Return [n, n].",
        """
        def solve(n):
            lower = n
            upper = n
            return [lower, upper]
        """,
        ["solve(4)", "solve(0)", "solve(7)"],
        expect=[[4, 4], [0, 0], [7, 7]])

    add("topic-3-3", "Find in a sorted row", "array", ["nums", "target", "lo", "hi", "mid", "steps"],
        "nums is sorted and contains target. Return [index, steps]. steps is how many middle checks you used. The same algorithm does fewer checks when the target is the middle.",
        "Best, worst, and average describe the same flow on different data. Binary search's step count depends on where the target sits.",
        ["Check the middle.", "Keep the half that can still hold the target.", "Return the index and the number of checks."],
        "Binary search, counting middle probes.",
        """
        def solve(nums, target):
            lo = 0
            hi = len(nums) - 1
            steps = 0
            while lo <= hi:
                steps = steps + 1
                mid = (lo + hi) // 2
                if nums[mid] == target:
                    return [mid, steps]
                if nums[mid] < target:
                    lo = mid + 1
                else:
                    hi = mid - 1
            return [-1, steps]
        """,
        ["solve([1, 3, 5, 7, 9], 5)", "solve([1, 3, 5, 7, 9], 1)", "solve([1], 1)"],
        expect=[[2, 1], [0, 2], [0, 1]])

    add("topic-3-4", "Triangle of work", "flow", ["n", "steps", "i", "j"],
        "The inner loop runs j from i to n-1. Return how many times the body runs. That is 1 + 2 + ... + n = n * (n + 1) / 2, still O(n^2).",
        "Not every nested loop is n * n. The changing inner bound still draws a triangle of steps.",
        ["For each i, run j from i upward.", "Count the body.", "Return the count."],
        "Count iterations of for i in range(n) for j in range(i, n).",
        """
        def solve(n):
            steps = 0
            i = 0
            while i < n:
                j = i
                while j < n:
                    steps = steps + 1
                    j = j + 1
                i = i + 1
            return steps
        """,
        ["solve(4)", "solve(1)", "solve(0)"],
        expect=[10, 1, 0])

    add("topic-3-5", "Recursion tree size", "recursion", ["n", "left", "right"],
        "A recursion tree for T(n) = 2T(n/2) + 1, with T(1) = 1, has one unit of work at every call. Return the number of calls, which is 2n - 1 when n is a power of two.",
        "The recursion tree draws one frame per call. Leaves are the n/2 base calls, and internal nodes fill the levels above.",
        ["If n is 1, count 1 call.", "Otherwise count this call plus the left half and the right half.", "The returned number is the size of the tree."],
        "Return 1 at n == 1, else 1 + solve(n//2) + solve(n//2).",
        """
        def solve(n):
            if n <= 1:
                return 1
            left = solve(n // 2)
            right = solve(n // 2)
            return 1 + left + right
        """,
        ["solve(4)", "solve(1)", "solve(8)"],
        expect=[7, 1, 15])

    add("topic-3-6", "Which Master case", "flow", ["a", "b", "k", "power"],
        "T(n) = a T(n/b) + n^k. Return 1 when a > b^k (root dominates), 2 when a == b^k (extra log), and 3 when a < b^k (leaves/work dominate).",
        "The Master Theorem compares the branching a with the work exponent through b^k. One integer, the case, names the closed form.",
        ["Compute b to the power k.", "Compare it with a.", "Return 1, 2, or 3."],
        "Compare a with b ** k.",
        """
        def solve(a, b, k):
            power = b ** k
            if a > power:
                return 1
            if a == power:
                return 2
            return 3
        """,
        ["solve(2, 2, 1)", "solve(1, 2, 0)", "solve(4, 2, 1)"],
        expect=[2, 2, 1])

    add("topic-3-7", "Extra memory", "array", ["nums", "copy", "i"],
        "Return a reversed copy of nums, and also return how many extra slots the copy used: [reversed, len(nums)]. The input itself is not extra space.",
        "Space complexity counts extra memory. A new list of n slots is O(n) extra space, even though the answer is just a rearrangement.",
        ["Allocate a new list.", "Fill it from the back.", "Return the copy and its length."],
        "Build a new list while walking backward.",
        """
        def solve(nums):
            copy = []
            i = len(nums) - 1
            while i >= 0:
                copy.append(nums[i])
                i = i - 1
            return [copy, len(copy)]
        """,
        ["solve([1, 2, 3])", "solve([])", "solve([8])"],
        expect=[[[3, 2, 1], 3], [[], 0], [[8], 1]])

    add("topic-3-8", "Cheap appends, rare copies", "array", ["n", "copies", "cap"],
        "Simulate a dynamic array: capacity doubles when full, and a growth copies every current item. Start capacity at 1. Return how many item-copies happen across n appends.",
        "Amortized analysis averages the rare expensive growth over the many cheap appends. The copy counter jumps only when capacity doubles.",
        ["Append into the current capacity for free.", "When it is full, add the current size to the copy counter and double capacity.", "Return the copy counter."],
        "On growth, copies += size, then capacity *= 2.",
        """
        def solve(n):
            size = 0
            cap = 1
            copies = 0
            i = 0
            while i < n:
                if size == cap:
                    copies = copies + size
                    cap = cap * 2
                size = size + 1
                i = i + 1
            return copies
        """,
        ["solve(8)", "solve(1)", "solve(0)"],
        expect=[7, 0, 0])

    add("topic-3-9", "Unwind a recurrence", "recursion", ["n", "rest"],
        "T(n) = T(n - 1) + n, and T(0) = 0. Return T(n). This is the same recurrence as the triangular numbers.",
        "A recurrence is a flow that calls a smaller version of itself and then adds local work. The stack shows n, n-1, ... down to 0.",
        ["Stop at 0.", "Ask for T(n - 1).", "Add n after that call returns."],
        "Return 0 at n == 0, else solve(n - 1) + n.",
        """
        def solve(n):
            if n == 0:
                return 0
            rest = solve(n - 1)
            return rest + n
        """,
        ["solve(4)", "solve(0)", "solve(1)"],
        expect=[10, 0, 1])

    add("topic-3-10", "Check the formula", "flow", ["n", "formula", "total", "i"],
        "Induction claim: the sum of the first n positives equals n * (n + 1) / 2. Return True if a loop agrees with the formula.",
        "A proof by induction has a base and a step. Here the loop is the expanded step, and the formula is the claim you store beside it.",
        ["Compute the formula.", "Add 1..n.", "Return whether they match."],
        "Compare n * (n + 1) // 2 with the loop sum.",
        """
        def solve(n):
            formula = n * (n + 1) // 2
            total = 0
            i = 1
            while i <= n:
                total = total + i
                i = i + 1
            return formula == total
        """,
        ["solve(6)", "solve(0)", "solve(2)"],
        expect=[True, True, True])
