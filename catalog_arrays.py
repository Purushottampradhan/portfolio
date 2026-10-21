"""Sections 4–6."""


def register(add):
    add("topic-4-1", "To binary", "bits", ["n", "bits"],
        "Return the binary digits of n, most significant bit first, without a leading zero. 0 returns [0].",
        "A number system is the same value written with a different base. Each remainder when dividing by 2 is one bit stored in memory.",
        ["Divide by 2 and store the remainder.", "Repeat until the value is 0.", "Reverse the remainders so the highest bit comes first."],
        "Collect n % 2, then n //= 2, then reverse.",
        """
        def solve(n):
            if n == 0:
                return [0]
            bits = []
            while n > 0:
                bits.append(n % 2)
                n = n // 2
            bits.reverse()
            return bits
        """,
        ["solve(13)", "solve(0)", "solve(1)"],
        expect=[[1, 1, 0, 1], [0], [1]])

    add("topic-4-2", "Is it prime", "flow", ["n", "d"],
        "Return True when n is prime. 0 and 1 are not prime.",
        "A prime has no divisor other than 1 and itself. The loop stores the candidate divisor d and stops at the square root.",
        ["Reject n below 2.", "Test divisors from 2 while d * d <= n.", "If none divide n, it is prime."],
        "Check divisors up to the square root.",
        """
        def solve(n):
            if n < 2:
                return False
            d = 2
            while d * d <= n:
                if n % d == 0:
                    return False
                d = d + 1
            return True
        """,
        ["solve(17)", "solve(1)", "solve(9)"],
        expect=[True, False, False])

    add("topic-4-3", "Sieve", "array", ["n", "prime", "i", "j"],
        "Return every prime from 2 through n, in order. Cross out multiples.",
        "The sieve stores a boolean per number. A True slot is still a candidate. Marking a multiple writes False into that slot.",
        ["Mark 0 and 1 as not prime.", "For each prime, mark its multiples.", "Collect the indexes that stayed True."],
        "Boolean array, then collect primes.",
        """
        def solve(n):
            prime = []
            i = 0
            while i <= n:
                prime.append(True)
                i = i + 1
            if n >= 0:
                prime[0] = False
            if n >= 1:
                prime[1] = False
            i = 2
            while i * i <= n:
                if prime[i]:
                    j = i * i
                    while j <= n:
                        prime[j] = False
                        j = j + i
                i = i + 1
            out = []
            i = 2
            while i <= n:
                if prime[i]:
                    out.append(i)
                i = i + 1
            return out
        """,
        ["solve(10)", "solve(2)", "solve(1)"],
        expect=[[2, 3, 5, 7], [2], []])

    add("topic-4-4", "GCD and LCM", "flow", ["a", "b", "x", "y", "g"],
        "Return [gcd, lcm] of two non-negative integers. lcm(a, b) = a * b / gcd when both are positive, else 0.",
        "Euclid's algorithm replaces the larger number with the remainder. The last non-zero remainder is the greatest shared divisor.",
        ["Replace a, b with b, a % b until b is 0.", "The remaining a is the gcd.", "Build the lcm from the product."],
        "Euclid for gcd, then a // g * b for lcm.",
        """
        def solve(a, b):
            x = a
            y = b
            while y != 0:
                r = x % y
                x = y
                y = r
            g = x
            if a == 0 or b == 0:
                return [g, 0]
            return [g, a // g * b]
        """,
        ["solve(12, 18)", "solve(7, 1)", "solve(0, 5)"],
        expect=[[6, 36], [1, 7], [5, 0]])

    add("topic-4-5", "Bezout pair", "flow", ["a", "b", "s", "t"],
        "Return [gcd, s, t] such that s * a + t * b = gcd. This is the extended Euclidean algorithm.",
        "Besides the remainder, the algorithm stores how the current remainder is built from a and b. Those coefficients are s and t.",
        ["Keep coefficients beside the remainders.", "Update them with the same quotient.", "When the remainder is 0, the previous coefficients are the answer."],
        "Extended Euclid. Return [gcd, s, t].",
        """
        def solve(a, b):
            old_r = a
            r = b
            old_s = 1
            s = 0
            old_t = 0
            t = 1
            while r != 0:
                q = old_r // r
                next_r = old_r - q * r
                next_s = old_s - q * s
                next_t = old_t - q * t
                old_r = r
                r = next_r
                old_s = s
                s = next_s
                old_t = t
                t = next_t
            return [old_r, old_s, old_t]
        """,
        ["solve(35, 15)", "solve(7, 3)", "solve(5, 0)"],
        expect=[[5, 1, -2], [1, 1, -2], [5, 1, 0]])

    add("topic-4-6", "Fast power", "flow", ["base", "exp", "mod", "result"],
        "Return (base ** exp) % mod. Use squaring, not a loop of exp multiplications.",
        "Fast exponentiation stores a result and a running square. Each bit of the exponent either multiplies the result or only squares the base.",
        ["If the exponent is odd, multiply result by base.", "Square the base and halve the exponent.", "Return result modulo mod."],
        "Binary exponentiation.",
        """
        def solve(base, exp, mod):
            result = 1
            base = base % mod
            while exp > 0:
                if exp % 2 == 1:
                    result = (result * base) % mod
                base = (base * base) % mod
                exp = exp // 2
            return result
        """,
        ["solve(2, 10, 1000)", "solve(3, 0, 7)", "solve(5, 3, 13)"],
        expect=[24, 1, 8])

    add("topic-4-7", "Clock arithmetic", "flow", ["a", "b", "mod", "sum_mod", "prod_mod"],
        "Return [(a + b) % mod, (a * b) % mod]. Both answers must stay inside 0 .. mod-1.",
        "Modular arithmetic wraps a number line into a circle of mod slots. The stored value is the remainder, not the full sum.",
        ["Add, then take the remainder.", "Multiply, then take the remainder.", "Return both remainders."],
        "Return [(a + b) % mod, (a * b) % mod].",
        """
        def solve(a, b, mod):
            sum_mod = (a + b) % mod
            prod_mod = (a * b) % mod
            return [sum_mod, prod_mod]
        """,
        ["solve(8, 5, 6)", "solve(0, 0, 3)", "solve(4, 4, 5)"],
        expect=[[1, 4], [0, 0], [3, 1]])

    add("topic-4-8", "Modular inverse", "flow", ["a", "mod", "i"],
        "Return the inverse of a modulo mod: a number x with (a * x) % mod == 1. If none exists, return -1. mod is prime in the tests.",
        "An inverse is the number that multiplies back to 1 on the clock. Fermat says a^(mod-2) works when mod is prime, and a scan also finds it.",
        ["Try x from 0 to mod - 1.", "Stop when the product remainder is 1.", "If the loop ends, return -1."],
        "Search x where (a * x) % mod == 1.",
        """
        def solve(a, mod):
            i = 0
            while i < mod:
                if (a * i) % mod == 1:
                    return i
                i = i + 1
            return -1
        """,
        ["solve(3, 7)", "solve(2, 5)", "solve(2, 4)"],
        expect=[5, 3, -1])

    add("topic-4-9", "Count the ways", "flow", ["n", "k", "ways", "i"],
        "Return C(n, k), the number of ways to choose k items from n. Use the multiplicative formula so the values stay small.",
        "Combinatorics counts without listing. The memory holds one running product: multiply (n - i) and divide by (i + 1).",
        ["Start ways at 1.", "For i in 0..k-1, update ways.", "Return ways."],
        "ways = ways * (n - i) // (i + 1) for i in 0..k-1.",
        """
        def solve(n, k):
            if k < 0 or k > n:
                return 0
            if k > n - k:
                k = n - k
            ways = 1
            i = 0
            while i < k:
                ways = ways * (n - i) // (i + 1)
                i = i + 1
            return ways
        """,
        ["solve(5, 2)", "solve(4, 0)", "solve(3, 5)"],
        expect=[10, 1, 0])

    add("topic-4-10", "Permute three", "recursion", ["items", "path", "used", "out"],
        "Return every permutation of items, in lexicographic order of the build. items has at most 3 values.",
        "A permutation is an ordering. The call stack stores the path built so far and which items are already used.",
        ["Choose an unused item and append it.", "Recurse.", "Remove it and try the next choice."],
        "Backtrack over unused items and collect full paths.",
        """
        def solve(items):
            out = []
            path = []
            used = []
            i = 0
            while i < len(items):
                used.append(False)
                i = i + 1

            def walk():
                if len(path) == len(items):
                    out.append(path[:])
                    return
                j = 0
                while j < len(items):
                    if not used[j]:
                        used[j] = True
                        path.append(items[j])
                        walk()
                        path.pop()
                        used[j] = False
                    j = j + 1

            walk()
            return out
        """,
        ["solve([1, 2])", "solve([1])", "solve([])"],
        expect=[[[1, 2], [2, 1]], [[1]], [[]]])

    add("topic-4-11", "Dice total", "dp", ["ways", "total", "face"],
        "One fair die has faces 1..6. Return how many ways to roll a total of exactly n with 2 dice. Order matters: 1 then 2 is different from 2 then 1.",
        "Probability here is a count of equally likely outcomes over 36. The table stores how many ways reach each partial total.",
        ["A first die writes 1 way into totals 1..6.", "A second die spreads those ways forward.", "Read the slot for n."],
        "Count ordered outcomes of two dice.",
        """
        def solve(n):
            ways = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            first = 1
            while first <= 6:
                second = 1
                while second <= 6:
                    ways[first + second] = ways[first + second] + 1
                    second = second + 1
                first = first + 1
            if n < 0 or n >= len(ways):
                return 0
            return ways[n]
        """,
        ["solve(7)", "solve(2)", "solve(1)"],
        expect=[6, 1, 0])

    add("topic-4-12", "Matrix sum", "matrix", ["grid", "total", "r", "c"],
        "Return the sum of every value in a matrix, row by row.",
        "A matrix is memory in rows and columns. Two indices, r and c, name the cell being read.",
        ["Start total at 0.", "Visit each row, then each column.", "Add the cell into total and return it."],
        "Add every grid[r][c].",
        """
        def solve(grid):
            total = 0
            r = 0
            while r < len(grid):
                c = 0
                while c < len(grid[r]):
                    total = total + grid[r][c]
                    c = c + 1
                r = r + 1
            return total
        """,
        ["solve([[1, 2], [3, 4]])", "solve([[5]])", "solve([[]])"],
        expect=[10, 5, 0])

    add("topic-4-13", "Totient", "flow", ["n", "result", "p"],
        "Return Euler's totient of n: how many integers from 1 to n are coprime to n.",
        "Totient factors n. For each prime factor p, multiply the result by (1 - 1/p), which the integer form writes as result - result / p.",
        ["Copy n into result and into the factor loop.", "For each prime factor, apply result -= result // p.", "Return result."],
        "Classic product formula for phi.",
        """
        def solve(n):
            result = n
            p = 2
            x = n
            while p * p <= x:
                if x % p == 0:
                    while x % p == 0:
                        x = x // p
                    result = result - result // p
                p = p + 1
            if x > 1:
                result = result - result // x
            return result
        """,
        ["solve(10)", "solve(1)", "solve(7)"],
        expect=[4, 1, 6])

    add("topic-4-14", "Two remainders", "flow", ["a1", "m1", "a2", "m2", "x"],
        "Find the smallest non-negative x with x % m1 == a1 and x % m2 == a2. m1 and m2 are coprime in the tests. This is a tiny Chinese Remainder case.",
        "CRT says one residue class matches both clocks when the moduli are coprime. A scan stores x and tests both remainders.",
        ["Try x from 0 upward.", "Check both remainders.", "Return the first x that satisfies both."],
        "Scan x until both congruences hold.",
        """
        def solve(a1, m1, a2, m2):
            x = 0
            while x < m1 * m2:
                if x % m1 == a1 and x % m2 == a2:
                    return x
                x = x + 1
            return -1
        """,
        ["solve(2, 3, 3, 5)", "solve(0, 3, 0, 5)", "solve(1, 4, 2, 3)"],
        expect=[8, 0, 5])

    add("topic-4-15", "Lucas digit product", "flow", ["n", "k", "mod", "result"],
        "mod is prime. Return C(n, k) % mod using Lucas: write n and k in base mod and multiply the small binomial coefficients.",
        "Lucas breaks a huge combination into one small combination per digit. Memory holds n, k, and a running product of those small answers.",
        ["While n or k remains, take both base-mod digits.", "If a k digit is larger, the answer is 0.", "Multiply the small combination into result."],
        "Lucas theorem for a prime modulus.",
        """
        def solve(n, k, mod):
            def small(a, b):
                if b < 0 or b > a:
                    return 0
                res = 1
                i = 0
                while i < b:
                    res = res * (a - i) // (i + 1)
                    i = i + 1
                return res % mod

            result = 1
            while n > 0 or k > 0:
                nd = n % mod
                kd = k % mod
                result = (result * small(nd, kd)) % mod
                n = n // mod
                k = k // mod
            return result
        """,
        ["solve(10, 3, 7)", "solve(5, 2, 3)", "solve(6, 0, 5)"],
        expect=[1, 1, 1])

    add("topic-4-16", "Divisible by 2 or 3", "flow", ["n", "by2", "by3", "by6"],
        "Return how many integers from 1 to n are divisible by 2 or by 3. Use inclusion-exclusion, not a scan of every integer.",
        "Inclusion-exclusion adds the two groups and subtracts the double-counted multiples of 6. Three integers in memory replace a long loop.",
        ["Count multiples of 2.", "Count multiples of 3.", "Subtract multiples of 6."],
        "n//2 + n//3 - n//6.",
        """
        def solve(n):
            by2 = n // 2
            by3 = n // 3
            by6 = n // 6
            return by2 + by3 - by6
        """,
        ["solve(10)", "solve(1)", "solve(6)"],
        expect=[7, 0, 4])

    add("topic-4-17", "Fibonacci by matrix power", "matrix", ["a", "b", "n", "steps"],
        "Return the nth Fibonacci number, with F(0)=0 and F(1)=1, by squaring the transformation (a, b) = (b, a + b). Count the transformation applications in the returned pair [F(n), steps] where steps is how many times you apply the pair update. Use fast doubling style: just apply the step n times so the flow is visible. Return only F(n).",
        "The vector [F(n), F(n+1)] is a matrix times the previous vector. Applying the step writes the next pair into a and b.",
        ["Start a=0, b=1, which is F(0), F(1).", "Replace them with b, a+b, n times.", "a is F(n)."],
        "Apply the Fibonacci step n times.",
        """
        def solve(n):
            a = 0
            b = 1
            steps = 0
            while steps < n:
                nxt = a + b
                a = b
                b = nxt
                steps = steps + 1
            return a
        """,
        ["solve(7)", "solve(0)", "solve(1)"],
        expect=[13, 0, 1])

    add("topic-5-1", "Rotate right by one", "array", ["nums", "last", "i"],
        "Return a new list rotated right by one position. The last value moves to the front. An empty list stays empty.",
        "An array stores values in index order. A rotation rewrites those slots: every item moves one index, and the last wraps around.",
        ["Remember the last value.", "Shift items toward the end.", "Write the saved value at index 0."],
        "Build a new list: last item, then everything except the last.",
        """
        def solve(nums):
            if not nums:
                return []
            out = [nums[-1]]
            i = 0
            while i < len(nums) - 1:
                out.append(nums[i])
                i = i + 1
            return out
        """,
        ["solve([1, 2, 3, 4])", "solve([])", "solve([8])"],
        expect=[[4, 1, 2, 3], [], [8]])

    add("topic-5-2", "Linear scan", "array", ["nums", "target", "i"],
        "Return the index of target, or -1. Scan from the left.",
        "Searching walks an index until the stored value matches. The index is the address you are reading.",
        ["Start i at 0.", "Compare nums[i] with target.", "Return i on a match, or -1 after the last slot."],
        "Return the first matching index.",
        """
        def solve(nums, target):
            i = 0
            while i < len(nums):
                if nums[i] == target:
                    return i
                i = i + 1
            return -1
        """,
        ["solve([4, 1, 7], 7)", "solve([4, 1, 7], 5)", "solve([], 1)"],
        expect=[2, -1, -1])

    add("topic-5-3", "Delete at index", "array", ["nums", "index", "out", "i"],
        "Return a new list with the value at index removed. Other values keep their order.",
        "Deletion from an array shifts later items into the hole. A new list makes each kept write visible.",
        ["Copy items before the index.", "Skip the index.", "Copy the rest."],
        "Append every item whose position is not index.",
        """
        def solve(nums, index):
            out = []
            i = 0
            while i < len(nums):
                if i != index:
                    out.append(nums[i])
                i = i + 1
            return out
        """,
        ["solve([8, 5, 2], 1)", "solve([1], 0)", "solve([1, 2], 0)"],
        expect=[[8, 2], [], [2]])

    add("topic-5-4", "Sorted pair", "two-pointer", ["nums", "target", "left", "right"],
        "nums is sorted. Return [left, right], the indices of two different positions that add up to target. If none exist, return [-1, -1].",
        "Two pointers store the ends of the remaining range. Their sum tells you which end is wrong.",
        ["If the sum is too small, move left rightward.", "If the sum is too large, move right leftward.", "If it matches, return both indices."],
        "Move the pointer on the side that fixes the sum.",
        """
        def solve(nums, target):
            left = 0
            right = len(nums) - 1
            while left < right:
                total = nums[left] + nums[right]
                if total == target:
                    return [left, right]
                if total < target:
                    left = left + 1
                else:
                    right = right - 1
            return [-1, -1]
        """,
        ["solve([1, 2, 4, 7], 6)", "solve([1, 2, 3], 10)", "solve([1, 1], 2)"],
        expect=[[1, 2], [-1, -1], [0, 1]])

    add("topic-5-5", "Best window of k", "window", ["nums", "k", "left", "total", "best"],
        "Return the maximum sum of any contiguous subarray of length k. k is at least 1 and not longer than nums.",
        "A sliding window remembers a running sum. When the window moves, subtract the value that leaves and add the value that enters.",
        ["Sum the first k items.", "Slide one step: drop nums[left], add the new right item.", "Keep the best sum."],
        "Maintain a sum of length k.",
        """
        def solve(nums, k):
            total = 0
            i = 0
            while i < k:
                total = total + nums[i]
                i = i + 1
            best = total
            left = 0
            while i < len(nums):
                total = total - nums[left] + nums[i]
                if total > best:
                    best = total
                left = left + 1
                i = i + 1
            return best
        """,
        ["solve([2, 1, 5, 1, 3], 3)", "solve([4], 1)", "solve([-1, -2, -3], 2)"],
        expect=[9, 4, -3])

    add("topic-5-6", "Range sum", "array", ["nums", "left", "right", "prefix", "i"],
        "Build a prefix array where prefix[i] is the sum of nums[0:i]. Return the sum of the inclusive range left..right using that prefix.",
        "A prefix stores every sum from the start. A range sum is then one subtraction of two stored totals.",
        ["Fill prefix so prefix[0] is 0.", "prefix[i + 1] = prefix[i] + nums[i].", "Return prefix[right + 1] - prefix[left]."],
        "Return prefix[right + 1] - prefix[left].",
        """
        def solve(nums, left, right):
            prefix = [0]
            i = 0
            while i < len(nums):
                prefix.append(prefix[i] + nums[i])
                i = i + 1
            return prefix[right + 1] - prefix[left]
        """,
        ["solve([2, 4, 1, 3], 1, 3)", "solve([5], 0, 0)", "solve([1, 2, 3], 0, 1)"],
        expect=[8, 5, 3])

    add("topic-5-7", "Range adds", "array", ["diff", "updates", "i"],
        "Start from a zero array of length n. updates is a list of [left, right, value] inclusive adds. Return the final array. Use a difference array.",
        "A difference array stores changes, not the values. A +v at left and -v just after right becomes the real array after one prefix sweep.",
        ["Add value at left and subtract it at right + 1.", "Sweep the difference into a running total.", "That running total is the final array."],
        "Difference array, then prefix sweep.",
        """
        def solve(n, updates):
            diff = []
            i = 0
            while i <= n:
                diff.append(0)
                i = i + 1
            for upd in updates:
                left = upd[0]
                right = upd[1]
                value = upd[2]
                diff[left] = diff[left] + value
                diff[right + 1] = diff[right + 1] - value
            out = []
            run = 0
            i = 0
            while i < n:
                run = run + diff[i]
                out.append(run)
                i = i + 1
            return out
        """,
        ["solve(5, [[1, 3, 2], [2, 4, 1]])", "solve(1, [[0, 0, 4]])", "solve(3, [])"],
        expect=[[0, 2, 3, 3, 1], [4], [0, 0, 0]])

    add("topic-5-8", "Best subarray sum", "array", ["nums", "run", "best", "x"],
        "Return the maximum sum of any non-empty contiguous subarray.",
        "Kadane stores the best sum that ends at the current index. Extending is run + x. Starting fresh is just x. best remembers the champion.",
        ["At each value, either extend the running sum or start over.", "Update best.", "Return best."],
        "run = max(x, run + x); best = max(best, run).",
        """
        def solve(nums):
            run = nums[0]
            best = nums[0]
            i = 1
            while i < len(nums):
                x = nums[i]
                if run + x > x:
                    run = run + x
                else:
                    run = x
                if run > best:
                    best = run
                i = i + 1
            return best
        """,
        ["solve([-2, 1, -3, 4, -1, 2, 1, -5, 4])", "solve([1])", "solve([-3, -1])"],
        expect=[6, 1, -1])

    add("topic-5-9", "Smallest enough capacity", "array", ["weights", "days", "lo", "hi", "mid"],
        "weights must be shipped in order. Return the smallest ship capacity that finishes in at most days days.",
        "Binary search on the answer stores a candidate capacity. A check walks the weights and counts how many days that capacity needs.",
        ["The low guess is the heaviest package. The high guess is the sum.", "Test the middle capacity.", "Keep the half that can still be the smallest working capacity."],
        "Binary search the capacity.",
        """
        def solve(weights, days):
            lo = weights[0]
            hi = 0
            for w in weights:
                hi = hi + w
                if w > lo:
                    lo = w
            while lo < hi:
                mid = (lo + hi) // 2
                need = 1
                load = 0
                for w in weights:
                    if load + w > mid:
                        need = need + 1
                        load = w
                    else:
                        load = load + w
                if need <= days:
                    hi = mid
                else:
                    lo = mid + 1
            return lo
        """,
        ["solve([1, 2, 3, 4, 5], 2)", "solve([3, 2, 2], 2)", "solve([1], 1)"],
        expect=[9, 4, 1])
