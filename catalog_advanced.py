"""Sections 15–24."""


def register(add):
    add("topic-15-1", "Remembered Fibonacci", "recursion", ["n", "memo", "ans"],
        "Return the nth Fibonacci number. F(0)=0, F(1)=1. Store each answer in memo so a call is not repeated.",
        "Memoization stores a return value the first time a state is solved. The next call reads that memory instead of rebuilding the tree.",
        ["If n is in memo, return it.", "Otherwise compute F(n-1)+F(n-2).", "Write the answer into memo before returning."],
        "Top-down Fibonacci with a dictionary.",
        """
        def solve(n):
            memo = {0: 0, 1: 1}

            def fib(k):
                if k in memo:
                    return memo[k]
                ans = fib(k - 1) + fib(k - 2)
                memo[k] = ans
                return ans

            return fib(n)
        """,
        ["solve(7)", "solve(0)", "solve(1)"],
        expect=[13, 0, 1])

    add("topic-15-2", "Table of Fibonacci", "dp", ["n", "dp", "i"],
        "Return F(n) by filling a table from the left. F(0)=0, F(1)=1.",
        "Tabulation writes small answers first. dp[i] is stored before any larger index tries to read it.",
        ["dp[0] and dp[1] are the base cells.", "dp[i] = dp[i-1] + dp[i-2].", "The last cell is the output."],
        "Fill dp left to right.",
        """
        def solve(n):
            if n == 0:
                return 0
            dp = [0, 1]
            i = 2
            while i <= n:
                dp.append(dp[i - 1] + dp[i - 2])
                i = i + 1
            return dp[n]
        """,
        ["solve(7)", "solve(0)", "solve(2)"],
        expect=[13, 0, 1])

    add("topic-15-3", "Rob the row", "dp", ["nums", "dp", "i"],
        "You cannot rob two adjacent houses. Return the maximum amount. The state is the house index.",
        "A state is the subproblem you store: the best loot using the first i houses. The choice is rob house i-1 or skip it.",
        ["dp[i] is the best for the first i houses.", "It is the max of skipping the last house or robbing it.", "Return dp at the end."],
        "House robber. dp[i] = max(dp[i-1], dp[i-2] + nums[i-1]).",
        """
        def solve(nums):
            if not nums:
                return 0
            if len(nums) == 1:
                return nums[0]
            dp = [nums[0], nums[0]]
            if nums[1] > dp[1]:
                dp[1] = nums[1]
            i = 2
            while i < len(nums):
                take = dp[i - 2] + nums[i]
                skip = dp[i - 1]
                if take > skip:
                    dp.append(take)
                else:
                    dp.append(skip)
                i = i + 1
            return dp[-1]
        """,
        ["solve([2, 7, 9, 3, 1])", "solve([5])", "solve([])"],
        expect=[12, 5, 0])

    add("topic-15-4", "Climb the stairs", "dp", ["n", "dp", "i"],
        "You climb 1 or 2 stairs. Return how many ways to climb n stairs. Order matters.",
        "The transition is the rule that fills a cell from older cells. Here ways(i) = ways(i-1) + ways(i-2).",
        ["One stair has 1 way. Two stairs have 2 ways.", "Each later stair adds the two previous answers.", "Return the nth cell."],
        "dp[i] = dp[i-1] + dp[i-2].",
        """
        def solve(n):
            if n <= 2:
                return n
            dp = [0, 1, 2]
            i = 3
            while i <= n:
                dp.append(dp[i - 1] + dp[i - 2])
                i = i + 1
            return dp[n]
        """,
        ["solve(4)", "solve(1)", "solve(2)"],
        expect=[5, 1, 2])

    add("topic-15-5", "Fibonacci again", "dp", ["n", "a", "b"],
        "Return F(n) with two variables instead of a whole table. F(0)=0, F(1)=1.",
        "The table only needs the last two cells. a and b are those two pieces of memory, shifted forward each step.",
        ["a is F(i), b is F(i+1).", "Replace them with b and a+b.", "After n steps, a is F(n)."],
        "Two rolling variables.",
        """
        def solve(n):
            a = 0
            b = 1
            i = 0
            while i < n:
                nxt = a + b
                a = b
                b = nxt
                i = i + 1
            return a
        """,
        ["solve(7)", "solve(0)", "solve(1)"],
        expect=[13, 0, 1])

    add("topic-15-6", "Zero-one knapsack", "dp", ["weights", "values", "cap", "dp"],
        "Each item may be taken once. Return the maximum value with weight at most cap.",
        "dp[w] stores the best value using capacity w. Items are considered one at a time, and the capacity loop runs backward so an item is not reused.",
        ["Start dp at zeros.", "For each item, update capacities from the right.", "dp[cap] is the output."],
        "0/1 knapsack, backward capacity loop.",
        """
        def solve(weights, values, cap):
            dp = []
            w = 0
            while w <= cap:
                dp.append(0)
                w = w + 1
            i = 0
            while i < len(weights):
                w = cap
                while w >= weights[i]:
                    take = dp[w - weights[i]] + values[i]
                    if take > dp[w]:
                        dp[w] = take
                    w = w - 1
                i = i + 1
            return dp[cap]
        """,
        ["solve([1, 3, 4, 5], [1, 4, 5, 7], 7)", "solve([4], [10], 3)", "solve([], [], 5)"],
        expect=[9, 0, 0])

    add("topic-15-7", "Longest common subsequence", "dp", ["a", "b", "dp", "i", "j"],
        "Return the length of the longest common subsequence of a and b.",
        "dp[i][j] stores the answer for the first i characters of a and the first j of b. Equal characters extend the diagonal. Different characters take the better neighbor.",
        ["A zero row and column are the empty prefixes.", "If characters match, add 1 to the diagonal.", "Otherwise take the max of the cell above or to the left."],
        "Classic LCS length.",
        """
        def solve(a, b):
            dp = []
            i = 0
            while i <= len(a):
                row = []
                j = 0
                while j <= len(b):
                    row.append(0)
                    j = j + 1
                dp.append(row)
                i = i + 1
            i = 1
            while i <= len(a):
                j = 1
                while j <= len(b):
                    if a[i - 1] == b[j - 1]:
                        dp[i][j] = dp[i - 1][j - 1] + 1
                    elif dp[i - 1][j] > dp[i][j - 1]:
                        dp[i][j] = dp[i - 1][j]
                    else:
                        dp[i][j] = dp[i][j - 1]
                    j = j + 1
                i = i + 1
            return dp[len(a)][len(b)]
        """,
        ["solve('abcde', 'ace')", "solve('abc', 'def')", "solve('', 'a')"],
        expect=[3, 0, 0])

    add("topic-15-8", "Longest increasing subsequence", "dp", ["nums", "best", "i", "j"],
        "Return the length of the longest strictly increasing subsequence.",
        "best[i] stores the longest increasing subsequence that ends at i. It is 1 plus the best earlier smaller value.",
        ["Every position starts at length 1.", "Extend it from each earlier smaller value.", "Return the maximum stored length."],
        "O(n^2) LIS.",
        """
        def solve(nums):
            best = []
            i = 0
            while i < len(nums):
                best.append(1)
                i = i + 1
            i = 0
            while i < len(nums):
                j = 0
                while j < i:
                    if nums[j] < nums[i] and best[j] + 1 > best[i]:
                        best[i] = best[j] + 1
                    j = j + 1
                i = i + 1
            ans = 0
            for x in best:
                if x > ans:
                    ans = x
            return ans
        """,
        ["solve([10, 9, 2, 5, 3, 7, 101, 18])", "solve([1])", "solve([])"],
        expect=[4, 1, 0])

    add("topic-15-9", "Fewest coins", "dp", ["coins", "amount", "dp"],
        "Return the fewest coins that sum to amount, or -1 if it is impossible. You may reuse coins.",
        "dp[a] stores the fewest coins that make amount a. The transition tries every coin that fits and keeps the minimum.",
        ["dp[0] is 0.", "For each amount, try each coin.", "If amount stays at the sentinel, return -1."],
        "Unbounded coin change.",
        """
        def solve(coins, amount):
            inf = amount + 1
            dp = [0]
            a = 1
            while a <= amount:
                dp.append(inf)
                a = a + 1
            a = 1
            while a <= amount:
                for coin in coins:
                    if coin <= a and dp[a - coin] + 1 < dp[a]:
                        dp[a] = dp[a - coin] + 1
                a = a + 1
            if dp[amount] > amount:
                return -1
            return dp[amount]
        """,
        ["solve([1, 2, 5], 11)", "solve([2], 3)", "solve([1], 0)"],
        expect=[3, -1, 0])

    add("topic-15-10", "Matrix chain", "dp", ["dims", "dp", "i", "j", "k"],
        "dims[i] is the row count of matrix i, and dims[i+1] its columns. Return the minimum multiplication cost.",
        "dp[i][j] stores the cheapest way to multiply matrices i through j. The transition tries every split k.",
        ["A single matrix costs 0.", "Try every split between i and j.", "Add the cost of multiplying the two resulting matrices."],
        "Matrix-chain order.",
        """
        def solve(dims):
            n = len(dims) - 1
            dp = []
            i = 0
            while i < n:
                row = []
                j = 0
                while j < n:
                    row.append(0)
                    j = j + 1
                dp.append(row)
                i = i + 1
            length = 2
            while length <= n:
                i = 0
                while i + length - 1 < n:
                    j = i + length - 1
                    dp[i][j] = 10 ** 9
                    k = i
                    while k < j:
                        cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                        if cost < dp[i][j]:
                            dp[i][j] = cost
                        k = k + 1
                    i = i + 1
                length = length + 1
            if n == 0:
                return 0
            return dp[0][n - 1]
        """,
        ["solve([1, 2, 3, 4])", "solve([10, 20])", "solve([2, 3, 4])"],
        expect=[18, 0, 24])

    add("topic-15-11", "Equal partition", "dp", ["nums", "target", "dp"],
        "Return True when the numbers can be split into two groups with the same sum.",
        "Partition DP here is a boolean table: dp[s] means some subset sums to s. The target is half the total.",
        ["If the total is odd, it is impossible.", "Mark sums you can build.", "Return whether half the total is marked."],
        "Subset-sum to half the total.",
        """
        def solve(nums):
            total = 0
            for x in nums:
                total = total + x
            if total % 2 == 1:
                return False
            target = total // 2
            dp = []
            i = 0
            while i <= target:
                dp.append(False)
                i = i + 1
            dp[0] = True
            for x in nums:
                s = target
                while s >= x:
                    if dp[s - x]:
                        dp[s] = True
                    s = s - 1
            return dp[target]
        """,
        ["solve([1, 5, 11, 5])", "solve([1, 2, 3, 5])", "solve([1])"],
        expect=[True, False, False])

    add("topic-15-12", "Rob the tree", "tree", ["root"],
        "You cannot rob a node and its child. Return the maximum sum. spec is [value, left, right] or None.",
        "Each node returns two stored answers: the best if this node is taken, and the best if it is skipped. The parent reads those two numbers.",
        ["A taken node adds its value to the skipped answers of the children.", "A skipped node takes the better answer from each child.", "The root returns the larger of the two."],
        "Tree house robber.",
        """
        def solve(spec):
            def build(spec):
                if spec is None:
                    return None
                return {"val": spec[0], "left": build(spec[1]), "right": build(spec[2])}

            def walk(node):
                if node is None:
                    return [0, 0]
                left = walk(node["left"])
                right = walk(node["right"])
                take = node["val"] + left[1] + right[1]
                skip_left = left[0]
                if left[1] > skip_left:
                    skip_left = left[1]
                skip_right = right[0]
                if right[1] > skip_right:
                    skip_right = right[1]
                return [take, skip_left + skip_right]

            pair = walk(build(spec))
            if pair[0] > pair[1]:
                return pair[0]
            return pair[1]
        """,
        ["solve([3, [2, None, None], [3, None, None]])", "solve([3, [4, None, None], None])", "solve(None)"],
        expect=[5, 4, 0])

    add("topic-15-13", "DAG distances", "graph", ["dist", "edges", "u"],
        "edges are directed [u, v, w] and every edge goes from a smaller id to a larger id. Return distances from 0.",
        "On a DAG the nodes are already a topological order. dp[v] is the best distance stored so far, relaxed only from earlier nodes.",
        ["dist[0] = 0.", "Relax each edge from left to right.", "Return the distance list."],
        "One pass over forward edges.",
        """
        def solve(n, edges):
            dist = []
            i = 0
            while i < n:
                dist.append(10 ** 9)
                i = i + 1
            dist[0] = 0
            ordered = sorted(edges, key=lambda e: e[0])
            for e in ordered:
                if dist[e[0]] < 10 ** 9 and dist[e[0]] + e[2] < dist[e[1]]:
                    dist[e[1]] = dist[e[0]] + e[2]
            return dist
        """,
        ["solve(4, [[0, 1, 1], [0, 2, 4], [1, 2, 1], [1, 3, 5], [2, 3, 1]])", "solve(1, [])", "solve(2, [[0, 1, 3]])"],
        expect=[[0, 1, 2, 3], [0], [0, 3]],
        extra={"nodes": [0, 1, 2, 3], "edges": [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3]]})

    add("topic-15-14", "Tiny tour", "dp", ["dist", "dp", "mask", "u"],
        "dist is a 3x3 matrix. Return the cheapest tour that starts at 0, visits every city once, and returns to 0.",
        "The state is a bitmask of visited cities plus the city you are standing in. dp[mask][u] stores the cheapest way to reach that state.",
        ["Start at city 0 with only bit 0 set.", "Try flying to a city not in the mask.", "When all bits are set, add the flight home."],
        "Bitmask DP for 3 cities.",
        """
        def solve(dist):
            n = 3
            inf = 10 ** 9
            dp = []
            mask = 0
            while mask < (1 << n):
                row = []
                u = 0
                while u < n:
                    row.append(inf)
                    u = u + 1
                dp.append(row)
                mask = mask + 1
            dp[1][0] = 0
            mask = 0
            while mask < (1 << n):
                u = 0
                while u < n:
                    if dp[mask][u] < inf:
                        v = 0
                        while v < n:
                            if (mask & (1 << v)) == 0:
                                nxt = mask | (1 << v)
                                cost = dp[mask][u] + dist[u][v]
                                if cost < dp[nxt][v]:
                                    dp[nxt][v] = cost
                            v = v + 1
                    u = u + 1
                mask = mask + 1
            full = (1 << n) - 1
            best = inf
            u = 0
            while u < n:
                cost = dp[full][u] + dist[u][0]
                if cost < best:
                    best = cost
                u = u + 1
            return best
        """,
        ["solve([[0, 1, 5], [1, 0, 2], [5, 2, 0]])", "solve([[0, 4, 1], [4, 0, 2], [1, 2, 0]])"],
        expect=[8, 7])

    add("topic-15-15", "Digit sum count", "recursion", ["n", "target", "memo"],
        "Return how many integers from 0 through n have digits that sum to target. Leading zeros are part of the digit walk.",
        "Digit DP walks one digit at a time. The state stores the position, whether the prefix is still tight to n, and the digit sum so far.",
        ["If the sum already passed the target, return 0.", "At the end, return 1 only for an exact sum.", "Try each legal next digit and memoize."],
        "Count numbers <= n with digit sum == target.",
        """
        def solve(n, target):
            digs = str(n)
            memo = {}

            def walk(i, tight, total):
                if total > target:
                    return 0
                if i == len(digs):
                    if total == target:
                        return 1
                    return 0
                key = (i, tight, total)
                if key in memo:
                    return memo[key]
                limit = 9
                if tight:
                    limit = int(digs[i])
                ans = 0
                d = 0
                while d <= limit:
                    ans = ans + walk(i + 1, tight and d == limit, total + d)
                    d = d + 1
                memo[key] = ans
                return ans

            return walk(0, True, 0)
        """,
        ["solve(10, 1)", "solve(5, 0)", "solve(10, 2)"],
        expect=[2, 1, 1])

    add("topic-15-16", "Monotone splits", "dp", ["n", "dp", "j"],
        "Cover 1..n with contiguous segments. A segment from j+1 through i costs (i-j)*(i-j). Return the minimum cost. This is the kind of recurrence divide-and-conquer DP speeds up; here n is small so every split is tried.",
        "dp[i] is the best cost to cover the first i items. The transition tries the start of the last segment.",
        ["dp[0] is 0.", "For each end i, try each previous j.", "Store the minimum."],
        "dp[i] = min over j < i of dp[j] + (i-j)^2.",
        """
        def solve(n):
            dp = [0]
            i = 1
            while i <= n:
                best = 10 ** 9
                j = 0
                while j < i:
                    cost = dp[j] + (i - j) * (i - j)
                    if cost < best:
                        best = cost
                    j = j + 1
                dp.append(best)
                i = i + 1
            return dp[n]
        """,
        ["solve(3)", "solve(1)", "solve(0)"],
        expect=[3, 1, 0])

    add("topic-15-17", "Optimal BST shape", "dp", ["freq", "dp", "i", "j", "k"],
        "freq[i] is the number of searches for key i. Return the minimum search cost of a BST on these keys, where a key's cost is freq times its depth (root depth 1).",
        "Knuth optimization speeds this exact table. dp[i][j] is the best cost for keys i through j. Every key in the range is a candidate root.",
        ["A single key costs its own frequency.", "Try each root.", "Add the frequencies of the range, because every key gets one level deeper."],
        "Optimal BST, root depth starts at 1.",
        """
        def solve(freq):
            n = len(freq)
            dp = []
            i = 0
            while i < n:
                row = []
                j = 0
                while j < n:
                    row.append(0)
                    j = j + 1
                dp.append(row)
                i = i + 1
            i = 0
            while i < n:
                dp[i][i] = freq[i]
                i = i + 1
            length = 2
            while length <= n:
                i = 0
                while i + length - 1 < n:
                    j = i + length - 1
                    total = 0
                    t = i
                    while t <= j:
                        total = total + freq[t]
                        t = t + 1
                    dp[i][j] = 10 ** 9
                    k = i
                    while k <= j:
                        left = 0
                        if k > i:
                            left = dp[i][k - 1]
                        right = 0
                        if k < j:
                            right = dp[k + 1][j]
                        cost = left + right + total
                        if cost < dp[i][j]:
                            dp[i][j] = cost
                        k = k + 1
                    i = i + 1
                length = length + 1
            if n == 0:
                return 0
            return dp[0][n - 1]
        """,
        ["solve([1, 2, 1])", "solve([5])", "solve([])"],
        expect=[6, 5, 0])

    add("topic-15-18", "Lowest line", "flow", ["lines", "x", "best", "y"],
        "lines are [slope, intercept]. Return the minimum y at the given x. A convex hull trick keeps only lines that win for some x; this small set compares every stored line.",
        "Each line is a pair in memory. y = slope * x + intercept. best remembers the smallest y seen.",
        ["Evaluate the first line.", "Replace best when a line is lower.", "Return best."],
        "Min over y = m*x + b.",
        """
        def solve(lines, x):
            best = None
            for line in lines:
                y = line[0] * x + line[1]
                if best is None or y < best:
                    best = y
            return best
        """,
        ["solve([[2, 0], [0, 5], [-1, 8]], 0)", "solve([[2, 0], [0, 5], [-1, 8]], 3)", "solve([[2, 0], [0, 5], [-1, 8]], 10)"],
        expect=[0, 5, -2])

    add("topic-15-19", "Tile a 2 by n", "dp", ["n", "dp", "i"],
        "Return how many ways to tile a 2xn board with 1x2 and 2x1 dominoes. This is the profile a column-by-column DP would count; the closed recurrence is the same as Fibonacci.",
        "A profile remembers how the previous column was filled. For plain dominoes the stored counts satisfy dp[i] = dp[i-1] + dp[i-2].",
        ["A width of 1 has one vertical domino.", "A width of 2 has two layouts.", "Later widths add those two histories."],
        "dp[n] = dp[n-1] + dp[n-2], dp[0]=1.",
        """
        def solve(n):
            dp = [1, 1]
            i = 2
            while i <= n:
                dp.append(dp[i - 1] + dp[i - 2])
                i = i + 1
            return dp[n]
        """,
        ["solve(3)", "solve(1)", "solve(0)"],
        expect=[3, 1, 1])

    add("topic-15-20", "Subset sums", "dp", ["arr", "sos", "bit", "mask"],
        "arr[mask] is a value on that bitmask. Return sos where sos[mask] is the sum of arr[sub] over every submask of mask.",
        "SOS DP stores subset sums. For each bit it adds the sum of the mask with that bit turned off into the mask that has the bit on.",
        ["Copy arr into sos.", "For each bit, walk every mask.", "If the bit is on, add the mask with that bit off."],
        "Sum over subsets.",
        """
        def solve(arr):
            sos = []
            for x in arr:
                sos.append(x)
            nbits = 0
            size = len(arr)
            p = 1
            while p < size:
                p = p * 2
                nbits = nbits + 1
            bit = 0
            while bit < nbits:
                mask = 0
                while mask < size:
                    if (mask & (1 << bit)) != 0:
                        sos[mask] = sos[mask] + sos[mask ^ (1 << bit)]
                    mask = mask + 1
                bit = bit + 1
            return sos
        """,
        ["solve([1, 2, 3, 4])", "solve([5])", "solve([1, 7])"],
        expect=[[1, 3, 4, 10], [5], [1, 8]])

    from catalog_elite import register as more
    more(add)
