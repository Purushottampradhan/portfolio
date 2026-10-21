"""Sections 16–24."""


def register(add):
    add("topic-16-1", "Count the set bits", "bits", ["n", "count"],
        "Return how many bits are 1 in the non-negative integer n.",
        "Each step looks at the last bit with n & 1, then shifts n right so the next bit falls into that place.",
        ["Add the current last bit to count.", "Shift n one place right.", "Stop when n becomes 0."],
        "Popcount by shifting.",
        """
        def solve(n):
            count = 0
            while n:
                count = count + (n & 1)
                n = n >> 1
            return count
        """,
        ["solve(13)", "solve(0)", "solve(7)"],
        expect=[3, 0, 3])

    add("topic-16-2", "XOR cancels itself", "bits", ["a", "b", "mixed"],
        "Return [a XOR b, (a XOR b) XOR b, (a XOR b) XOR a]. The last two values recover a and b.",
        "XOR stores the bits where two numbers differ. XORing the same number again erases it, because x XOR x is 0 and x XOR 0 is x.",
        ["Mix a and b.", "XOR b back out to recover a.", "XOR a back out to recover b."],
        "Show that x XOR y XOR y returns x.",
        """
        def solve(a, b):
            mixed = a ^ b
            return [mixed, mixed ^ b, mixed ^ a]
        """,
        ["solve(5, 3)", "solve(0, 0)", "solve(7, 1)"],
        expect=[[6, 5, 3], [0, 0, 0], [6, 7, 1]])

    add("topic-16-3", "The number left over", "bits", ["nums", "ans", "x"],
        "Every value appears twice except one. Return the single value.",
        "Pairs cancel under XOR. The memory cell ans keeps the running mix, and the unpaired number is what remains.",
        ["Start ans at 0.", "XOR every value into ans.", "Return ans."],
        "XOR the whole list.",
        """
        def solve(nums):
            ans = 0
            for x in nums:
                ans = ans ^ x
            return ans
        """,
        ["solve([2, 2, 1])", "solve([4, 1, 2, 1, 2])", "solve([7])"],
        expect=[1, 4, 7])

    add("topic-16-4", "Subsets from bits", "bits", ["nums", "mask", "subset", "i"],
        "Return every subset of nums. Mask bit i means nums[i] is included.",
        "A mask is a small integer whose bits choose the subset. Walking masks from 0 through 2^n - 1 visits every choice once.",
        ["Start at mask 0, the empty subset.", "Read each bit to build the subset.", "Move to the next mask."],
        "Bitmask subset enumeration.",
        """
        def solve(nums):
            n = len(nums)
            out = []
            mask = 0
            while mask < (1 << n):
                subset = []
                i = 0
                while i < n:
                    if (mask & (1 << i)) != 0:
                        subset.append(nums[i])
                    i = i + 1
                out.append(subset)
                mask = mask + 1
            return out
        """,
        ["solve([1, 2])", "solve([1])", "solve([])"],
        expect=[[[], [1], [2], [1, 2]], [[], [1]], [[]]])

    add("topic-16-5", "Gray code", "array", ["n", "codes", "i"],
        "Return n-bit Gray codes in order. Consecutive codes differ by one bit. Use i XOR (i >> 1).",
        "The binary counter i changes many bits. Folding it with i >> 1 makes only one bit change between neighbors.",
        ["i runs from 0 to 2^n - 1.", "Each code is i XOR (i shifted right).", "Return the list."],
        "Binary-reflected Gray code.",
        """
        def solve(n):
            codes = []
            i = 0
            while i < (1 << n):
                codes.append(i ^ (i >> 1))
                i = i + 1
            return codes
        """,
        ["solve(2)", "solve(1)", "solve(0)"],
        expect=[[0, 1, 3, 2], [0, 1], [0]])

    add("topic-16-6", "Count with a mask", "bits", ["nums", "mask", "total", "count"],
        "Return how many subsets of nums sum to target, including the empty subset when target is 0.",
        "Bit DP on a tiny set uses the mask as the state. Each mask is one subset, and total is the sum stored for that mask.",
        ["Walk every mask.", "Add nums[i] when bit i is on.", "Count the masks whose sum equals target."],
        "Subset sums by bitmask.",
        """
        def solve(nums, target):
            n = len(nums)
            count = 0
            mask = 0
            while mask < (1 << n):
                total = 0
                i = 0
                while i < n:
                    if (mask & (1 << i)) != 0:
                        total = total + nums[i]
                    i = i + 1
                if total == target:
                    count = count + 1
                mask = mask + 1
            return count
        """,
        ["solve([1, 2, 3], 3)", "solve([1], 0)", "solve([], 0)"],
        expect=[2, 1, 1])

    add("topic-17-1", "Activity selection", "array", ["acts", "end", "count"],
        "acts are [start, end]. Return how many you can keep when no two overlap. A start equal to the previous end is allowed.",
        "Sorting by finish time puts the activity that frees the room soonest first. end remembers when the room next opens.",
        ["Sort by ending time.", "Take an activity when it starts at or after end.", "Move end to that activity's finish."],
        "Earliest-finish greedy.",
        """
        def solve(acts):
            ordered = sorted(acts, key=lambda act: act[1])
            count = 0
            end = -10 ** 9
            for act in ordered:
                if act[0] >= end:
                    count = count + 1
                    end = act[1]
            return count
        """,
        ["solve([[1, 3], [2, 4], [3, 5]])", "solve([[1, 2]])", "solve([])"],
        expect=[2, 1, 0])

    add("topic-17-2", "Fractional knapsack", "bars", ["items", "cap", "total"],
        "items are [value, weight]. You may take a fraction of an item. Return the maximum value that fits in cap.",
        "The score of an item is value / weight. The greedy choice fills the bag with the highest score first, then a fraction of the next item.",
        ["Sort by value per weight.", "Take as much as the remaining capacity allows.", "Add value * taken / weight."],
        "Value-per-weight greedy.",
        """
        def solve(items, cap):
            ordered = sorted(items, key=lambda it: it[0] / it[1], reverse=True)
            total = 0.0
            for it in ordered:
                if cap == 0:
                    break
                take = it[1]
                if take > cap:
                    take = cap
                total = total + it[0] * take / it[1]
                cap = cap - take
            return total
        """,
        ["solve([[60, 10], [100, 20], [120, 30]], 50)", "solve([[10, 5]], 2)", "solve([], 5)"],
        expect=[240.0, 4.0, 0.0])

    add("topic-17-3", "Huffman cost", "bars", ["freq", "nodes", "cost"],
        "freq holds symbol weights. Return the total cost of a Huffman tree: each time two nodes merge, add their weight sum to the cost.",
        "The two lightest nodes are combined into a parent whose weight is their sum. That parent goes back into the list. The cost is the sum of every parent weight.",
        ["While two or more nodes remain, sort them.", "Remove the two lightest and add their sum to the cost.", "Put the parent weight back."],
        "Huffman merge cost.",
        """
        def solve(freq):
            nodes = []
            for weight in freq:
                nodes.append(weight)
            cost = 0
            while len(nodes) > 1:
                nodes.sort()
                a = nodes.pop(0)
                b = nodes.pop(0)
                cost = cost + a + b
                nodes.append(a + b)
            return cost
        """,
        ["solve([1, 2, 3])", "solve([5])", "solve([1, 1])"],
        expect=[9, 0, 2])

    add("topic-17-4", "Job sequencing", "array", ["jobs", "slot", "profit"],
        "jobs are [deadline, profit]. Each job takes one time slot and must finish by its deadline. Return the maximum profit.",
        "Taking the highest profit first is the greedy choice. slot[t] remembers whether time t is already used. A job slides into the latest free slot at or before its deadline.",
        ["Sort jobs by profit, high to low.", "Give each job the latest free slot it can use.", "Add its profit when a slot is found."],
        "One slot per job, latest feasible slot.",
        """
        def solve(jobs):
            ordered = sorted(jobs, key=lambda job: -job[1])
            max_d = 0
            for job in jobs:
                if job[0] > max_d:
                    max_d = job[0]
            slot = []
            t = 0
            while t <= max_d:
                slot.append(False)
                t = t + 1
            profit = 0
            for job in ordered:
                d = job[0]
                while d > 0 and slot[d]:
                    d = d - 1
                if d > 0:
                    slot[d] = True
                    profit = profit + job[1]
            return profit
        """,
        ["solve([[1, 20], [2, 15], [2, 30]])", "solve([[1, 10]])", "solve([])"],
        expect=[50, 10, 0])

    add("topic-17-5", "Merge intervals", "array", ["intervals", "out", "i"],
        "intervals are [start, end]. Merge any that touch or overlap and return the merged list.",
        "After sorting by start, the current merged interval sits at the end of out. The next interval either extends that end or starts a new one.",
        ["Sort by start.", "Extend the last end when the next start is inside it.", "Otherwise append a new interval."],
        "Sort, then one left-to-right merge.",
        """
        def solve(intervals):
            if not intervals:
                return []
            ordered = sorted(intervals, key=lambda it: it[0])
            out = [[ordered[0][0], ordered[0][1]]]
            i = 1
            while i < len(ordered):
                if ordered[i][0] <= out[-1][1]:
                    if ordered[i][1] > out[-1][1]:
                        out[-1][1] = ordered[i][1]
                else:
                    out.append([ordered[i][0], ordered[i][1]])
                i = i + 1
            return out
        """,
        ["solve([[1, 3], [2, 6], [8, 10]])", "solve([[1, 4], [4, 5]])", "solve([])"],
        expect=[[[1, 6], [8, 10]], [[1, 5]], []])

    add("topic-17-6", "Gas station circuit", "array", ["gas", "cost", "tank", "start"],
        "gas[i] is the fuel at station i and cost[i] is the fuel to reach the next station. Return the starting index of a full clockwise circuit, or -1.",
        "tank is the fuel since the current start. If it goes negative, every index in that stretch fails, so start moves to the next station and tank resets. The total says whether any circuit exists.",
        ["Add gas[i] - cost[i] to tank and to the total.", "If tank is negative, start at i + 1 and clear tank.", "If the total is negative, return -1."],
        "One-pass circular gas station.",
        """
        def solve(gas, cost):
            total = 0
            tank = 0
            start = 0
            i = 0
            while i < len(gas):
                total = total + gas[i] - cost[i]
                tank = tank + gas[i] - cost[i]
                if tank < 0:
                    start = i + 1
                    tank = 0
                i = i + 1
            if total < 0:
                return -1
            return start
        """,
        ["solve([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])", "solve([1], [2])", "solve([2, 2], [3, 1])"],
        expect=[3, -1, 1])

    add("topic-18-1", "Dot product", "flow", ["a", "b"],
        "a and b are 2D vectors [x, y]. Return their dot product.",
        "The dot product multiplies matching coordinates and adds those products. It is one number stored from the two vectors.",
        ["Multiply the x coordinates.", "Multiply the y coordinates.", "Add the two products."],
        "a.x * b.x + a.y * b.y.",
        """
        def solve(a, b):
            return a[0] * b[0] + a[1] * b[1]
        """,
        ["solve([1, 0], [0, 1])", "solve([2, 3], [4, 5])", "solve([1, 1], [1, 1])"],
        expect=[0, 23, 2])

    add("topic-18-2", "Cross product", "flow", ["a", "b"],
        "a and b are 2D vectors. Return the z-component of their cross product.",
        "The 2D cross product is one signed number. Positive means b sits to the left of a. Negative means b sits to the right. Zero means they are parallel.",
        ["Multiply a.x by b.y.", "Multiply a.y by b.x.", "Subtract the second from the first."],
        "a.x * b.y - a.y * b.x.",
        """
        def solve(a, b):
            return a[0] * b[1] - a[1] * b[0]
        """,
        ["solve([1, 0], [0, 1])", "solve([1, 0], [1, 0])", "solve([0, 1], [1, 0])"],
        expect=[1, 0, -1])

    add("topic-18-3", "Left or right turn", "flow", ["a", "b", "c"],
        "Return 1 for a left turn from a to b to c, -1 for a right turn, and 0 when the points are collinear.",
        "The turn is the cross product of vector b-a with vector c-a. The sign of that one number is the orientation.",
        ["Build the two edge vectors from a.", "Compute their cross product.", "Return the sign."],
        "Orientation by cross product.",
        """
        def solve(a, b, c):
            cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            if cross > 0:
                return 1
            if cross < 0:
                return -1
            return 0
        """,
        ["solve([0, 0], [1, 0], [1, 1])", "solve([0, 0], [1, 0], [1, -1])", "solve([0, 0], [1, 0], [2, 0])"],
        expect=[1, -1, 0])

    add("topic-18-4", "Do the segments cross?", "flow", ["a", "b", "c", "d"],
        "Return True when segment ab intersects segment cd, including a touch at an endpoint.",
        "Each endpoint is tested against the other segment. The segments cross when the endpoints of each one lie on opposite sides of the other line, or when a collinear endpoint lies on the segment.",
        ["Find the orientation of each endpoint against the other segment.", "Opposite orientations mean a proper crossing.", "A zero orientation still counts when the point lies on the segment."],
        "Orientation-based segment intersection.",
        """
        def solve(a, b, c, d):
            def orient(p, q, r):
                value = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
                if value > 0:
                    return 1
                if value < 0:
                    return -1
                return 0

            def on_segment(p, q, r):
                return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])

            o1 = orient(a, b, c)
            o2 = orient(a, b, d)
            o3 = orient(c, d, a)
            o4 = orient(c, d, b)
            if o1 != o2 and o3 != o4:
                return True
            if o1 == 0 and on_segment(a, c, b):
                return True
            if o2 == 0 and on_segment(a, d, b):
                return True
            if o3 == 0 and on_segment(c, a, d):
                return True
            if o4 == 0 and on_segment(c, b, d):
                return True
            return False
        """,
        ["solve([0, 0], [2, 2], [0, 2], [2, 0])", "solve([0, 0], [1, 0], [2, 0], [3, 0])", "solve([0, 0], [2, 0], [1, 0], [1, 1])"],
        expect=[True, False, True])

    add("topic-18-5", "Polygon area", "flow", ["points", "total", "i"],
        "points go around a polygon in order. Return its area as an integer. The sample polygons have even shoelace sums.",
        "The shoelace formula adds x*next_y - next_x*y around the boundary. Half the absolute value is the area. Memory only needs the running total.",
        ["Walk each edge to the next point, wrapping to the first.", "Add the cross product of the two endpoints.", "Return half the absolute total."],
        "Shoelace formula.",
        """
        def solve(points):
            n = len(points)
            if n < 3:
                return 0
            total = 0
            i = 0
            while i < n:
                j = (i + 1) % n
                total = total + points[i][0] * points[j][1] - points[j][0] * points[i][1]
                i = i + 1
            if total < 0:
                total = -total
            return total // 2
        """,
        ["solve([[0, 0], [2, 0], [2, 2], [0, 2]])", "solve([[0, 0], [4, 0], [0, 3]])", "solve([[1, 1]])"],
        expect=[4, 6, 0])

    add("topic-18-6", "Convex hull", "array", ["points", "lower", "upper"],
        "Return the convex hull of the points in counter-clockwise order, starting from the leftmost point. Drop points inside an edge.",
        "Andrew's monotone chain sorts the points, builds the lower chain left to right, then the upper chain right to left. A non-left turn is popped, so the stored chain only bends left.",
        ["Sort the points and remove duplicates.", "Build the lower chain, popping right turns.", "Build the upper chain the same way and join them."],
        "Monotone-chain convex hull.",
        """
        def solve(points):
            uniq = []
            for point in sorted(points):
                if not uniq or uniq[-1] != point:
                    uniq.append(point)
            if len(uniq) <= 1:
                return uniq

            def cross(o, a, b):
                return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

            lower = []
            for point in uniq:
                while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
                    lower.pop()
                lower.append(point)
            upper = []
            for point in reversed(uniq):
                while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
                    upper.pop()
                upper.append(point)
            return lower[:-1] + upper[:-1]
        """,
        ["solve([[0, 0], [2, 0], [2, 2], [0, 2], [1, 1]])", "solve([[1, 1]])", "solve([[0, 0], [1, 1]])"],
        expect=[[[0, 0], [2, 0], [2, 2], [0, 2]], [[1, 1]], [[0, 0], [1, 1]]])

    add("topic-18-7", "Maximum overlap", "array", ["intervals", "events", "cur", "best"],
        "intervals are half-open [start, end). Return how many overlap at the busiest moment. Touching at an endpoint does not overlap.",
        "A sweep stores +1 at each start and -1 at each end. Sorting by time, with ends before starts at the same time, lets cur count the intervals currently open.",
        ["Turn each interval into a start event and an end event.", "Sort by time, and process ends before starts.", "Track the highest running count."],
        "Sweep line over interval events.",
        """
        def solve(intervals):
            events = []
            for it in intervals:
                events.append([it[0], 1])
                events.append([it[1], -1])
            events.sort()
            cur = 0
            best = 0
            for event in events:
                cur = cur + event[1]
                if cur > best:
                    best = cur
            return best
        """,
        ["solve([[1, 4], [2, 5], [6, 7]])", "solve([[1, 2], [2, 3]])", "solve([])"],
        expect=[2, 1, 0])

    add("topic-19-1", "Ordered map", "array", ["items", "out"],
        "ops are [\"put\", key, value] or [\"get\", key]. Keep keys sorted. Return [list of get results, list of keys]. A missing get is None.",
        "The map is a list of [key, value] pairs kept in key order. A put walks the list until it finds the key or the first larger key, then overwrites or inserts.",
        ["On put, replace a matching key or insert before the first larger key.", "On get, scan for the key.", "Also return the keys in their stored order."],
        "Sorted list as an ordered map.",
        """
        def solve(ops):
            items = []
            out = []
            for op in ops:
                if op[0] == "put":
                    i = 0
                    placed = False
                    while i < len(items):
                        if items[i][0] == op[1]:
                            items[i][1] = op[2]
                            placed = True
                            break
                        if items[i][0] > op[1]:
                            items.insert(i, [op[1], op[2]])
                            placed = True
                            break
                        i = i + 1
                    if not placed:
                        items.append([op[1], op[2]])
                else:
                    val = None
                    for pair in items:
                        if pair[0] == op[1]:
                            val = pair[1]
                    out.append(val)
            keys = []
            for pair in items:
                keys.append(pair[0])
            return [out, keys]
        """,
        ["solve([['put', 'b', 2], ['put', 'a', 1], ['get', 'a'], ['get', 'c']])", "solve([['put', 'a', 1], ['put', 'a', 4], ['get', 'a']])", "solve([['put', 'z', 1]])"],
        expect=[[[1, None], ["a", "b"]], [[4], ["a"]], [[], ["z"]]])

    add("topic-19-2", "Treap inorder", "tree", ["root", "pairs"],
        "pairs are [key, priority]. Higher priority stays closer to the root. Return [inorder keys, root key]. An empty treap has root key None.",
        "A treap is a binary tree. Keys obey search-tree order. Priorities obey heap order, restored by a rotation when a child outranks its parent.",
        ["Insert the key as in a binary search tree.", "Rotate while the child priority is higher.", "Read the keys inorder and report the root key."],
        "BST by key, max-heap by priority.",
        """
        def solve(pairs):
            root = None

            def rotate_right(n):
                left = n["left"]
                n["left"] = left["right"]
                left["right"] = n
                return left

            def rotate_left(n):
                right = n["right"]
                n["right"] = right["left"]
                right["left"] = n
                return right

            def insert(n, key, pri):
                if n is None:
                    return {"val": key, "p": pri, "left": None, "right": None}
                if key < n["val"]:
                    n["left"] = insert(n["left"], key, pri)
                    if n["left"]["p"] > n["p"]:
                        n = rotate_right(n)
                else:
                    n["right"] = insert(n["right"], key, pri)
                    if n["right"]["p"] > n["p"]:
                        n = rotate_left(n)
                return n

            def walk(n, out):
                if n is None:
                    return
                walk(n["left"], out)
                out.append(n["val"])
                walk(n["right"], out)

            for pair in pairs:
                root = insert(root, pair[0], pair[1])
            out = []
            walk(root, out)
            top = None
            if root is not None:
                top = root["val"]
            return [out, top]
        """,
        ["solve([[2, 1], [1, 5], [3, 2]])", "solve([[4, 1]])", "solve([])"],
        expect=[[[1, 2, 3], 1], [[4], 4], [[], None]])

    add("topic-19-3", "Two-level skip search", "array", ["values", "express", "path", "j"],
        "values is sorted. The express lane holds every even index. Return [found, path] while searching for target. The path lists express values, then the bottom values after the drop, including the target when it is present.",
        "A skip list stores a sparse top lane and a dense bottom lane. Search walks the top lane while the next stop is still <= target, then drops and scans forward one value at a time.",
        ["Build the express lane from even indexes.", "Advance while the next express value is <= target.", "Scan the bottom lane from that drop until you pass the target."],
        "Express lane plus a short bottom scan.",
        """
        def solve(values, target):
            express = []
            i = 0
            while i < len(values):
                express.append([i, values[i]])
                i = i + 2
            path = []
            e = 0
            while e + 1 < len(express) and express[e + 1][1] <= target:
                path.append(express[e][1])
                e = e + 1
            if express:
                path.append(express[e][1])
                j = express[e][0]
            else:
                j = 0
            while j < len(values) and values[j] < target:
                if not path or path[-1] != values[j]:
                    path.append(values[j])
                j = j + 1
            found = j < len(values) and values[j] == target
            if found and (not path or path[-1] != values[j]):
                path.append(values[j])
            return [found, path]
        """,
        ["solve([1, 3, 5, 7, 9], 7)", "solve([1, 3, 5, 7, 9], 4)", "solve([1], 1)"],
        expect=[[True, [1, 5, 7]], [False, [1, 3]], [True, [1]]])

    add("topic-19-4", "Tiny B-tree split", "flow", ["root", "keys"],
        "Insert keys into a B-tree that holds at most 2 keys per node. Return [root keys, children], and each child has that same shape. A leaf has an empty child list.",
        "A leaf that grows to 3 keys splits. The middle key moves up, and the left and right keys become two children. The root is replaced when the split reaches it.",
        ["Insert into the correct leaf and keep its keys sorted.", "If a node has 3 keys, send the middle key upward.", "Make a new root when the old root splits."],
        "B-tree of order 3, max 2 keys.",
        """
        def solve(keys):
            root = {"keys": [], "kids": []}

            def insert(node, key):
                if not node["kids"]:
                    node["keys"].append(key)
                    node["keys"].sort()
                    if len(node["keys"]) <= 2:
                        return None
                    mid = node["keys"][1]
                    left = {"keys": [node["keys"][0]], "kids": []}
                    right = {"keys": [node["keys"][2]], "kids": []}
                    return [mid, left, right]
                i = 0
                while i < len(node["keys"]) and key > node["keys"][i]:
                    i = i + 1
                split = insert(node["kids"][i], key)
                if split is None:
                    return None
                node["keys"].insert(i, split[0])
                node["kids"][i] = split[1]
                node["kids"].insert(i + 1, split[2])
                if len(node["keys"]) <= 2:
                    return None
                mid = node["keys"][1]
                left = {"keys": [node["keys"][0]], "kids": node["kids"][:2]}
                right = {"keys": [node["keys"][2]], "kids": node["kids"][2:]}
                return [mid, left, right]

            for key in keys:
                split = insert(root, key)
                if split is not None:
                    root = {"keys": [split[0]], "kids": [split[1], split[2]]}

            def flat(node):
                kids = []
                for kid in node["kids"]:
                    kids.append(flat(kid))
                return [node["keys"], kids]

            return flat(root)
        """,
        ["solve([1, 2, 3])", "solve([1])", "solve([1, 2])"],
        expect=[[[2], [[[1], []], [[3], []]]], [[1], []], [[1, 2], []]])

    add("topic-19-5", "Nearest point", "array", ["points", "target", "best", "dist"],
        "points are [x, y]. Return the point closest to target. Distance is compared by squared length, so no square root is needed. Ties keep the earlier point.",
        "A kd-tree would prune far half-planes. On a handful of points the same query checks every stored point and keeps the smallest squared distance.",
        ["Start with no best point.", "Compute (dx*dx + dy*dy) for each point.", "Replace best when the distance is smaller."],
        "Nearest neighbor by squared distance.",
        """
        def solve(points, target):
            best = None
            best_d = None
            for point in points:
                dist = (point[0] - target[0]) * (point[0] - target[0]) + (point[1] - target[1]) * (point[1] - target[1])
                if best is None or dist < best_d:
                    best = point
                    best_d = dist
            return best
        """,
        ["solve([[0, 0], [5, 5], [1, 2]], [1, 1])", "solve([[0, 0], [5, 5]], [0, 0])", "solve([[4, 4]], [0, 0])"],
        expect=[[1, 2], [0, 0], [4, 4]])

    add("topic-19-6", "Persistent copies", "array", ["versions", "nxt", "sums"],
        "Start from base. Each update is [index, value] and creates a new version without changing the old one. Return the sum of every version, including the original.",
        "A persistent array keeps old versions. This small one copies the previous list, writes the new value into the copy, and appends that copy. The old list object stays intact.",
        ["Store the base as version 0.", "Copy the latest version before each write.", "Sum every stored version."],
        "Copy-on-write versions.",
        """
        def solve(base, updates):
            versions = []
            first = []
            for value in base:
                first.append(value)
            versions.append(first)
            for update in updates:
                nxt = []
                for value in versions[-1]:
                    nxt.append(value)
                nxt[update[0]] = update[1]
                versions.append(nxt)
            sums = []
            for version in versions:
                total = 0
                for value in version:
                    total = total + value
                sums.append(total)
            return sums
        """,
        ["solve([1, 2, 3], [[0, 5], [2, 0]])", "solve([4], [])", "solve([], [])"],
        expect=[[6, 10, 7], [4], [0]])

    add("topic-19-7", "Rope slice", "tree", ["root", "left", "right"],
        "Concatenate left and right, then return the slice that starts at start and has the given length.",
        "A rope is a binary tree. Each leaf stores a string. An internal node stores the weight of its left subtree, which tells a search whether the slice is in the left child or the right child.",
        ["Build a root whose children are the two strings.", "If the start is in the left weight, read there first.", "Continue into the right child for any leftover characters."],
        "Concatenate, then substring by left weight.",
        """
        def solve(left, right, start, length):
            root = {
                "val": len(left),
                "w": len(left) + len(right),
                "left": {"val": left, "w": len(left), "left": None, "right": None},
                "right": {"val": right, "w": len(right), "left": None, "right": None},
            }

            def substr(node, s, n, out):
                if node is None or n == 0:
                    return
                if node["left"] is None and node["right"] is None:
                    out.append(node["val"][s:s + n])
                    return
                left_w = node["left"]["w"]
                if s < left_w:
                    take = n
                    if s + take > left_w:
                        take = left_w - s
                    substr(node["left"], s, take, out)
                    substr(node["right"], 0, n - take, out)
                else:
                    substr(node["right"], s - left_w, n, out)

            out = []
            substr(root, start, length, out)
            text = ""
            for part in out:
                text = text + part
            return text
        """,
        ["solve('hello', 'world', 3, 5)", "solve('ab', 'cd', 0, 4)", "solve('ab', 'cd', 4, 0)"],
        expect=["lowor", "abcd", ""])

    add("topic-20-1", "Meet in the middle", "array", ["nums", "left", "right", "need"],
        "Return True when some subset of nums sums to target. nums has at most 4 values. The empty subset sums to 0.",
        "Split the list in half. Store every subset sum of the left half, sort every subset sum of the right half, and binary-search for target - left_sum.",
        ["Build both half-sum lists.", "Sort the right sums.", "Search for the complement of each left sum."],
        "Two halves, then binary search.",
        """
        def solve(nums, target):
            mid = len(nums) // 2

            def sums(arr):
                out = [0]
                for value in arr:
                    nxt = []
                    for total in out:
                        nxt.append(total)
                        nxt.append(total + value)
                    out = nxt
                return out

            left = sums(nums[:mid])
            right = sorted(sums(nums[mid:]))
            for total in left:
                need = target - total
                lo = 0
                hi = len(right) - 1
                while lo <= hi:
                    m = (lo + hi) // 2
                    if right[m] == need:
                        return True
                    if right[m] < need:
                        lo = m + 1
                    else:
                        hi = m - 1
            return False
        """,
        ["solve([1, 2, 3, 4], 10)", "solve([1, 2, 3, 4], 11)", "solve([1, 2, 3, 4], 0)"],
        expect=[True, False, True])

    add("topic-20-2", "Block-sorted range sums", "array", ["arr", "queries", "cur", "ans"],
        "queries are inclusive [left, right]. Return the sum of each range. Sort the queries by block of the left index, then by the right index, and move the window from the previous query.",
        "Mo's method stores the current window sum. Sorting nearby queries means the window only slides a short distance. add grows the window and remove shrinks it.",
        ["Order queries by (left // 2, right).", "Move the right edge, then the left edge.", "Write each sum back into the original query order."],
        "Range sums with a sliding window.",
        """
        def solve(arr, queries):
            order = []
            i = 0
            while i < len(queries):
                order.append(i)
                i = i + 1
            order.sort(key=lambda idx: (queries[idx][0] // 2, queries[idx][1]))
            cur_l = 0
            cur_r = -1
            cur = 0
            ans = []
            i = 0
            while i < len(queries):
                ans.append(0)
                i = i + 1
            for idx in order:
                left = queries[idx][0]
                right = queries[idx][1]
                while cur_r < right:
                    cur_r = cur_r + 1
                    cur = cur + arr[cur_r]
                while cur_r > right:
                    cur = cur - arr[cur_r]
                    cur_r = cur_r - 1
                while cur_l < left:
                    cur = cur - arr[cur_l]
                    cur_l = cur_l + 1
                while cur_l > left:
                    cur_l = cur_l - 1
                    cur = cur + arr[cur_l]
                ans[idx] = cur
            return ans
        """,
        ["solve([1, 2, 3, 4], [[0, 2], [1, 3], [0, 0]])", "solve([5], [[0, 0]])", "solve([1, 2], [])"],
        expect=[[6, 9, 1], [5], []])

    add("topic-20-3", "Block range sums", "array", ["arr", "blocks", "queries", "total"],
        "queries are inclusive [left, right]. Return each range sum using square-root blocks.",
        "blocks[b] stores the sum of one chunk. A query adds whole chunks in the middle and single cells on the two edges.",
        ["Build a sum for every chunk.", "Inside a query, jump a whole chunk when it fits.", "Otherwise add one cell."],
        "Square-root decomposition range sum.",
        """
        def solve(arr, queries):
            b = int(len(arr) ** 0.5)
            if b < 1:
                b = 1
            blocks = []
            i = 0
            while i < len(arr):
                total = 0
                j = i
                while j < len(arr) and j < i + b:
                    total = total + arr[j]
                    j = j + 1
                blocks.append(total)
                i = i + b
            out = []
            for query in queries:
                left = query[0]
                right = query[1]
                total = 0
                i = left
                while i <= right:
                    if i % b == 0 and i + b - 1 <= right:
                        total = total + blocks[i // b]
                        i = i + b
                    else:
                        total = total + arr[i]
                        i = i + 1
                out.append(total)
            return out
        """,
        ["solve([1, 2, 3, 4], [[0, 2], [1, 3], [0, 0]])", "solve([5], [[0, 0]])", "solve([1, 2], [])"],
        expect=[[6, 9, 1], [5], []])

    add("topic-20-4", "Majority vote", "array", ["nums", "cand", "count"],
        "Return the value that appears more than half the time, or None when there is no majority. The scan is deterministic.",
        "Boyer-Moore keeps one candidate and a count. A match increments the count. A mismatch decrements it. A second pass checks that the candidate really is a majority.",
        ["Replace the candidate when the count hits 0.", "Increment on a match and decrement on a mismatch.", "Count the candidate again and accept it only if it is more than half."],
        "Boyer-Moore majority.",
        """
        def solve(nums):
            cand = None
            count = 0
            for value in nums:
                if count == 0:
                    cand = value
                    count = 1
                elif value == cand:
                    count = count + 1
                else:
                    count = count - 1
            count = 0
            for value in nums:
                if value == cand:
                    count = count + 1
            if count * 2 > len(nums):
                return cand
            return None
        """,
        ["solve([2, 2, 1, 2, 3])", "solve([1, 2])", "solve([5])"],
        expect=[2, None, 5])

    add("topic-20-5", "Pair sum by sorting", "two-pointer", ["nums", "target", "i", "j"],
        "Return one pair of values that sums to target, as [smaller, larger], or None. Each value is used once.",
        "Sorting reduces an unsorted pair search to two pointers. i starts at the left and j at the right. Their sum says which pointer moves.",
        ["Sort a copy.", "Move i right when the sum is too small.", "Move j left when the sum is too large."],
        "Sort, then two pointers.",
        """
        def solve(nums, target):
            arr = sorted(nums)
            i = 0
            j = len(arr) - 1
            while i < j:
                total = arr[i] + arr[j]
                if total == target:
                    return [arr[i], arr[j]]
                if total < target:
                    i = i + 1
                else:
                    j = j - 1
            return None
        """,
        ["solve([3, 1, 4, 2], 6)", "solve([1, 2, 3], 10)", "solve([5, 5], 10)"],
        expect=[[2, 4], None, [5, 5]])

    add("topic-20-6", "Subset-sum decision", "dp", ["nums", "target", "dp"],
        "Return True when a subset sums to target. The empty subset sums to 0.",
        "dp[s] stores whether a subset sums to s. Each number updates the table from the right so it is used at most once. This decision version is the heart of the knapsack family of NP-complete problems.",
        ["Mark dp[0] True.", "For each number, walk sums downward.", "Return dp[target]."],
        "Boolean subset sum.",
        """
        def solve(nums, target):
            dp = []
            s = 0
            while s <= target:
                dp.append(False)
                s = s + 1
            dp[0] = True
            for value in nums:
                s = target
                while s >= value:
                    if dp[s - value]:
                        dp[s] = True
                    s = s - 1
            return dp[target]
        """,
        ["solve([1, 5, 3], 8)", "solve([1, 5, 3], 7)", "solve([1, 5, 3], 0)"],
        expect=[True, False, True])

    add("topic-20-7", "Two growth rates", "flow", ["n"],
        "Return [2^n, n]. 2^n is how many subsets a brute-force check would list. n is how many values a single pass would read.",
        "P and NP are about how fast a problem grows. This function does not solve an NP-complete problem. It puts the two sizes next to each other so the gap is visible.",
        ["Compute 2 to the power n.", "Keep n beside it.", "Return both numbers."],
        "Compare an exponential count with a linear count.",
        """
        def solve(n):
            return [2 ** n, n]
        """,
        ["solve(3)", "solve(0)", "solve(4)"],
        expect=[[8, 3], [1, 0], [16, 4]])

    add("topic-20-8", "Climb to a local peak", "bars", ["nums", "i", "best"],
        "nums is a line of heights. Start at index start. Move to a higher neighbor until both neighbors are lower or equal. Return the height where you stop.",
        "Hill climbing only accepts a better neighbor, so it can stop on a local peak and miss a taller hill farther away. Simulated annealing would sometimes step downhill to escape. This climb does not.",
        ["Look at the left and right neighbors.", "Move to the higher one when it beats the current height.", "Stop when neither neighbor is higher."],
        "Uphill walk on a line.",
        """
        def solve(nums, start):
            i = start
            steps = 0
            while steps < len(nums):
                best = i
                if i > 0 and nums[i - 1] > nums[best]:
                    best = i - 1
                if i + 1 < len(nums) and nums[i + 1] > nums[best]:
                    best = i + 1
                if best == i:
                    return nums[i]
                i = best
                steps = steps + 1
            return nums[i]
        """,
        ["solve([1, 3, 2, 5], 0)", "solve([1, 2, 3], 0)", "solve([4], 0)"],
        expect=[3, 3, 4])

    add("topic-21-1", "LRU cache", "hash", ["table", "order", "out"],
        "cap is the capacity. ops are [\"put\", key, value] or [\"get\", key]. Return every get result. A missing get is -1. The least recently used key is evicted when the cache is full.",
        "table stores the values. order stores keys from oldest to newest. A get or an update removes the key and appends it, which marks it as just used.",
        ["On put of a new key, drop the oldest key when full.", "Move a used key to the end of order.", "Read the value from table."],
        "Capacity-limited least-recently-used cache.",
        """
        def solve(cap, ops):
            table = {}
            order = []
            out = []
            for op in ops:
                if op[0] == "put":
                    if op[1] in table:
                        order.remove(op[1])
                    elif cap > 0 and len(order) == cap:
                        old = order.pop(0)
                        del table[old]
                    if cap > 0:
                        table[op[1]] = op[2]
                        order.append(op[1])
                else:
                    if op[1] not in table:
                        out.append(-1)
                    else:
                        order.remove(op[1])
                        order.append(op[1])
                        out.append(table[op[1]])
            return out
        """,
        ["solve(2, [['put', 1, 1], ['put', 2, 2], ['get', 1], ['put', 3, 3], ['get', 2], ['get', 1]])", "solve(1, [['get', 1]])", "solve(1, [['put', 1, 1], ['put', 1, 2], ['get', 1]])"],
        expect=[[1, -1, 1], [-1], [2]])

    add("topic-21-2", "LFU cache", "hash", ["items", "out"],
        "cap is the capacity. ops are [\"put\", key, value] or [\"get\", key]. Return every get result, or -1 when missing. Evict the lowest frequency, and the oldest key on a tie.",
        "Each stored record is [key, value, frequency]. A get increments frequency. A new put into a full cache removes the lowest frequency. Equal frequencies keep the earlier record, so the oldest index is the victim.",
        ["Update the value and frequency when the key is already stored.", "Otherwise evict the lowest frequency if the cache is full.", "Append the new key with frequency 1."],
        "Least-frequently-used cache.",
        """
        def solve(cap, ops):
            items = []
            out = []

            def find(key):
                i = 0
                while i < len(items):
                    if items[i][0] == key:
                        return i
                    i = i + 1
                return -1

            for op in ops:
                if op[0] == "put":
                    i = find(op[1])
                    if i >= 0:
                        items[i][1] = op[2]
                        items[i][2] = items[i][2] + 1
                    else:
                        if cap > 0 and len(items) == cap:
                            victim = 0
                            j = 1
                            while j < len(items):
                                if items[j][2] < items[victim][2]:
                                    victim = j
                                j = j + 1
                            items.pop(victim)
                        if cap > 0:
                            items.append([op[1], op[2], 1])
                else:
                    i = find(op[1])
                    if i < 0:
                        out.append(-1)
                    else:
                        items[i][2] = items[i][2] + 1
                        out.append(items[i][1])
            return out
        """,
        ["solve(2, [['put', 1, 1], ['put', 2, 2], ['get', 1], ['put', 3, 3], ['get', 2], ['get', 3], ['get', 1]])", "solve(0, [['put', 1, 1], ['get', 1]])", "solve(1, [['put', 5, 9], ['get', 5]])"],
        expect=[[1, -1, 3, 1], [-1], [9]])

    add("topic-21-3", "Tiny feed", "array", ["tweets", "follows", "out"],
        "ops are [\"post\", user, tweetId], [\"follow\", user, followee], or [\"feed\", user]. A feed returns up to 2 tweet ids, newest first, from the user and the people they follow.",
        "tweets is a list of [time, user, id] in post order. follows is a list of [user, followee]. A feed scans that memory, keeps matching tweets, and sorts them by time descending.",
        ["Append a post with the next time.", "Record a follow as a pair.", "On a feed, collect matches and keep the two newest ids."],
        "Posts, follows, and a 2-tweet feed.",
        """
        def solve(ops):
            tweets = []
            follows = []
            out = []
            time = 0
            for op in ops:
                if op[0] == "post":
                    tweets.append([time, op[1], op[2]])
                    time = time + 1
                elif op[0] == "follow":
                    follows.append([op[1], op[2]])
                else:
                    user = op[1]
                    feed = []
                    for tweet in tweets:
                        if tweet[1] == user:
                            feed.append(tweet)
                        else:
                            for pair in follows:
                                if pair[0] == user and pair[1] == tweet[1]:
                                    feed.append(tweet)
                                    break
                    feed.sort(key=lambda tweet: -tweet[0])
                    ids = []
                    i = 0
                    while i < len(feed) and i < 2:
                        ids.append(feed[i][2])
                        i = i + 1
                    out.append(ids)
            return out
        """,
        ["solve([['post', 1, 10], ['post', 2, 20], ['follow', 1, 2], ['feed', 1], ['post', 1, 30], ['feed', 1]])", "solve([['feed', 1]])", "solve([['post', 1, 5], ['feed', 1]])"],
        expect=[[[20, 10], [30, 20]], [[]], [[5]]])

    add("topic-21-4", "Min stack", "stack", ["stack", "mins", "out"],
        "ops are [\"push\", value], [\"pop\"], [\"top\"], or [\"getMin\"]. Return the results of top and getMin, in order.",
        "stack stores the values. mins stores the minimum at every height. Pushing writes both. Popping removes both. getMin reads the end of mins, which is the minimum of the current stack.",
        ["On push, append the value and the min of that value and the old minimum.", "On pop, remove one item from each list.", "top reads stack, getMin reads mins."],
        "A stack with a parallel minimum.",
        """
        def solve(ops):
            stack = []
            mins = []
            out = []
            for op in ops:
                if op[0] == "push":
                    stack.append(op[1])
                    low = op[1]
                    if mins and mins[-1] < low:
                        low = mins[-1]
                    mins.append(low)
                elif op[0] == "pop":
                    stack.pop()
                    mins.pop()
                elif op[0] == "top":
                    out.append(stack[-1])
                else:
                    out.append(mins[-1])
            return out
        """,
        ["solve([['push', 2], ['push', 1], ['push', 3], ['getMin'], ['pop'], ['top'], ['getMin']])", "solve([['push', 5], ['push', 1], ['pop'], ['getMin']])", "solve([['push', 4], ['top']])"],
        expect=[[1, 1, 1], [5], [4]])

    add("topic-21-5", "Hash map", "hash", ["table", "out"],
        "ops are [\"put\", key, value], [\"get\", key], or [\"remove\", key]. Return every get result. A missing get is -1.",
        "table is a dictionary. put writes key to value, get reads it, and remove deletes it. The picture shows the pairs currently stored.",
        ["put stores the pair.", "get appends the stored value or -1.", "remove deletes the key when it is present."],
        "Put, get, and remove.",
        """
        def solve(ops):
            table = {}
            out = []
            for op in ops:
                if op[0] == "put":
                    table[op[1]] = op[2]
                elif op[0] == "get":
                    if op[1] in table:
                        out.append(table[op[1]])
                    else:
                        out.append(-1)
                else:
                    if op[1] in table:
                        del table[op[1]]
            return out
        """,
        ["solve([['put', 1, 10], ['put', 4, 40], ['get', 1], ['get', 4], ['remove', 1], ['get', 1]])", "solve([['get', 3]])", "solve([['put', 2, 7], ['remove', 2], ['get', 2]])"],
        expect=[[10, 40, -1], [-1], [-1]])

    add("topic-21-6", "Rate limiter", "array", ["log", "times", "out"],
        "Allow at most limit events in a window. An event at time t counts earlier events with age strictly less than window. Return True or False for each time in order.",
        "log stores the times that were allowed and are still inside the window. Before a decision, times that have fallen out of the window are dropped.",
        ["Drop times older than the window.", "Allow the event when the log is shorter than limit.", "Leave the log unchanged when the event is denied."],
        "Sliding-window counter.",
        """
        def solve(limit, window, times):
            log = []
            out = []
            for t in times:
                kept = []
                for old in log:
                    if t - old < window:
                        kept.append(old)
                log = kept
                if len(log) < limit:
                    log.append(t)
                    out.append(True)
                else:
                    out.append(False)
            return out
        """,
        ["solve(2, 10, [1, 2, 3, 12])", "solve(1, 5, [0])", "solve(1, 5, [0, 1])"],
        expect=[[True, True, False, True], [True], [True, False]])

    add("topic-21-7", "Vending change", "array", ["price", "paid", "change", "out"],
        "Return the coins that make paid - price, using denominations 25, 10, 5, and 1, largest first. Return None when paid is less than price. Exact payment returns an empty list.",
        "change starts as the amount owed. Each denomination is taken as many times as it fits, and those coins are appended to out. The remainder stays in change.",
        ["Reject a payment that is too small.", "Try 25, then 10, then 5, then 1.", "Append a coin every time it fits."],
        "Greedy change.",
        """
        def solve(price, paid):
            if paid < price:
                return None
            change = paid - price
            out = []
            for coin in [25, 10, 5, 1]:
                while change >= coin:
                    out.append(coin)
                    change = change - coin
            return out
        """,
        ["solve(30, 50)", "solve(40, 40)", "solve(50, 40)"],
        expect=[[10, 10], [], None])

    add("topic-21-8", "Short code", "flow", ["n", "alphabet", "out"],
        "Turn a non-negative integer into a base-62 short code. The digits are 0-9, then a-z, then A-Z.",
        "Repeatedly store n % 62 as the next digit and replace n with n // 62. The digits come out backward, so they are reversed before the string is returned.",
        ["Special-case 0.", "Append the digit for n % 62.", "Reverse the digits."],
        "Base-62 encoding.",
        """
        def solve(n):
            alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if n == 0:
                return "0"
            out = []
            while n:
                out.append(alphabet[n % 62])
                n = n // 62
            out.reverse()
            text = ""
            for ch in out:
                text = text + ch
            return text
        """,
        ["solve(0)", "solve(1)", "solve(62)"],
        expect=["0", "1", "10"])

    add("topic-21-9", "Filter the log", "array", ["logs", "start", "end", "out"],
        "logs are [timestamp, message]. Return the messages whose timestamp is between start and end, inclusive, in their original order.",
        "The log is a list of pairs. The scan keeps a message only when its timestamp sits inside the closed range. out is the filtered list.",
        ["Read each pair.", "Keep the message when the timestamp is inside the range.", "Return the kept messages."],
        "Inclusive timestamp filter.",
        """
        def solve(logs, start, end):
            out = []
            for row in logs:
                if start <= row[0] <= end:
                    out.append(row[1])
            return out
        """,
        ["solve([[1, 'a'], [5, 'b'], [8, 'c']], 4, 8)", "solve([[1, 'a']], 2, 3)", "solve([], 0, 1)"],
        expect=[["b", "c"], [], []])

    add("topic-22-1", "Name the pattern", "flow", ["clues"],
        "clues is a list of words. Return two pointers, prefix sums, intervals, bfs, or brute force.",
        "Pattern recognition checks a few stored clues before any code is written. The first matching rule picks the family.",
        ["Look for a sorted pair.", "Then look for a prefix, an overlap, or a shortest-path clue.", "Otherwise the family is brute force."],
        "Classify clues into a pattern family.",
        """
        def solve(clues):
            if "sorted" in clues and "pair" in clues:
                return "two pointers"
            if "prefix" in clues:
                return "prefix sums"
            if "overlap" in clues:
                return "intervals"
            if "shortest" in clues or "grid" in clues:
                return "bfs"
            return "brute force"
        """,
        ["solve(['sorted', 'pair'])", "solve(['prefix'])", "solve(['notes'])"],
        expect=["two pointers", "prefix sums", "brute force"])

    add("topic-22-2", "Difficulty from n", "flow", ["n"],
        "Return easy when n is at most 100, medium when n is at most 10000, and hard after that.",
        "The ladder uses the input size as its state. One comparison picks the label a study plan would attach to that size.",
        ["Compare n with 100.", "Then compare n with 10000.", "Return the matching label."],
        "Size buckets.",
        """
        def solve(n):
            if n <= 100:
                return "easy"
            if n <= 10000:
                return "medium"
            return "hard"
        """,
        ["solve(50)", "solve(5000)", "solve(100000)"],
        expect=["easy", "medium", "hard"])

    add("topic-22-3", "Missing whiteboard steps", "array", ["done", "missing"],
        "done lists the steps already covered. The full order is restate, examples, approach, code, test. Return the missing steps in that order.",
        "The checklist is a fixed list in memory. Each step is copied to missing when it is absent from done.",
        ["Walk the five steps in order.", "Skip a step that is already in done.", "Return the ones that remain."],
        "Whiteboard checklist.",
        """
        def solve(done):
            steps = ["restate", "examples", "approach", "code", "test"]
            missing = []
            for step in steps:
                if step not in done:
                    missing.append(step)
            return missing
        """,
        ["solve(['restate', 'code'])", "solve(['restate', 'examples', 'approach', 'code', 'test'])", "solve([])"],
        expect=[["examples", "approach", "test"], [], ["restate", "examples", "approach", "code", "test"]])

    add("topic-22-4", "What was said", "flow", ["said", "score"],
        "said lists the parts that were explained. Score one point each for goal, plan, and tradeoff. Return the score.",
        "Communication here is a count over a fixed list. Each required word that appears in said increments the stored score.",
        ["Start the score at 0.", "Add 1 for each required word that was said.", "Return the score."],
        "Count goal, plan, and tradeoff.",
        """
        def solve(said):
            needed = ["goal", "plan", "tradeoff"]
            score = 0
            for word in needed:
                if word in said:
                    score = score + 1
            return score
        """,
        ["solve(['goal', 'plan'])", "solve([])", "solve(['goal', 'plan', 'tradeoff'])"],
        expect=[2, 0, 3])

    add("topic-22-5", "Time budget", "flow", ["minutes"],
        "A problem slot is 15 minutes. Return [how many full slots fit, how many minutes are left].",
        "Integer division stores the number of complete slots. The remainder stores the unused minutes.",
        ["Divide minutes by 15.", "Keep the remainder.", "Return both."],
        "Slots and leftover minutes.",
        """
        def solve(minutes):
            return [minutes // 15, minutes % 15]
        """,
        ["solve(45)", "solve(50)", "solve(10)"],
        expect=[[3, 0], [3, 5], [0, 10]])

    add("topic-22-6", "Sum a line of numbers", "array", ["line", "total", "part"],
        "line is a string of integers separated by spaces. Return their sum. An empty line sums to 0.",
        "Fast input at this scale is a split into tokens, then a running total. Each token is parsed and added.",
        ["Split the line on spaces.", "Turn each token into an integer.", "Add it to total."],
        "Parse and sum.",
        """
        def solve(line):
            total = 0
            for part in line.split():
                total = total + int(part)
            return total
        """,
        ["solve('1 2 3')", "solve('')", "solve('-4 10')"],
        expect=[6, 0, 6])

    add("topic-22-7", "Positive remainder", "flow", ["a", "m"],
        "Return a mod m in the range 0 through m - 1, even when a is negative.",
        "Python's remainder already has the sign of the divisor, but a second mod makes the habit explicit: ((a % m) + m) % m lands in 0 .. m-1 for a positive m.",
        ["Take a % m.", "Add m so a negative remainder becomes positive.", "Mod by m again."],
        "Non-negative modulo.",
        """
        def solve(a, m):
            return ((a % m) + m) % m
        """,
        ["solve(-3, 5)", "solve(5, 5)", "solve(7, 5)"],
        expect=[2, 0, 2])

    add("topic-22-8", "Contest score", "array", ["problems", "score", "count"],
        "problems are [points, solved]. solved is True or False. Return [total points of solved problems, how many were solved].",
        "The scoreboard walks the list once. A solved flag adds the points and increments the count. An unsolved problem changes neither.",
        ["Start score and count at 0.", "Add points only when the flag is True.", "Return both numbers."],
        "Sum the solved problems.",
        """
        def solve(problems):
            score = 0
            count = 0
            for problem in problems:
                if problem[1]:
                    score = score + problem[0]
                    count = count + 1
            return [score, count]
        """,
        ["solve([[100, True], [200, False], [300, True]])", "solve([])", "solve([[50, False]])"],
        expect=[[400, 2], [0, 0], [0, 0]])

    add("topic-22-9", "Mock score", "array", ["scores", "total"],
        "scores holds four small marks. Return [total, True] when the total is at least 6, otherwise [total, False].",
        "The rubric adds the marks into one total. The pass bit is that total compared with 6.",
        ["Add every mark.", "Compare the total with 6.", "Return the total and the pass bit."],
        "Sum and a pass line.",
        """
        def solve(scores):
            total = 0
            for mark in scores:
                total = total + mark
            return [total, total >= 6]
        """,
        ["solve([2, 2, 2, 1])", "solve([1, 1, 1, 1])", "solve([])"],
        expect=[[7, True], [4, False], [0, False]])

    add("topic-22-10", "Next review gap", "flow", ["interval", "quality"],
        "quality is 0 through 5. If quality is below 3, return 1. Otherwise return interval * 2, or 1 when interval is below 1.",
        "A revision schedule stores the current gap. A weak recall resets it. A good recall doubles it so the next review sits farther out.",
        ["Reset to 1 when quality is below 3.", "Reset to 1 when the old interval is below 1.", "Otherwise double the interval."],
        "Double the gap after a good recall.",
        """
        def solve(interval, quality):
            if quality < 3:
                return 1
            if interval < 1:
                return 1
            return interval * 2
        """,
        ["solve(2, 4)", "solve(2, 2)", "solve(0, 5)"],
        expect=[4, 1, 1])

    add("topic-23-1", "One job: the ledger", "array", ["ops", "balance", "log"],
        "ops is a list of amounts to add, which may be negative. Return the balance after each amount. This function only updates the ledger.",
        "Single responsibility means this memory does one job. balance is the current total and log stores the balance after every change. Nothing here formats or prints.",
        ["Start the balance at 0.", "Add each amount.", "Append the new balance to the log."],
        "Running balance.",
        """
        def solve(ops):
            balance = 0
            log = []
            for amount in ops:
                balance = balance + amount
                log.append(balance)
            return log
        """,
        ["solve([10, -3, 5])", "solve([])", "solve([-2])"],
        expect=[[10, 7, 12], [], [-2]])

    add("topic-23-2", "One shared box", "flow", ["names", "shared", "out"],
        "names is the list of callers. The first caller becomes the owner. Later callers see that same owner and a hit count that keeps growing. Return [owner, hits] after each call.",
        "A singleton is one shared object. shared lives outside the loop, so every caller reads and writes the same dictionary instead of creating a new one.",
        ["Create one dictionary before the loop.", "Set the owner only when it is still empty.", "Increment hits for every caller."],
        "Shared owner and hit count.",
        """
        def solve(names):
            shared = {"owner": None, "hits": 0}
            out = []
            for name in names:
                if shared["owner"] is None:
                    shared["owner"] = name
                shared["hits"] = shared["hits"] + 1
                out.append([shared["owner"], shared["hits"]])
            return out
        """,
        ["solve(['a', 'b'])", "solve(['solo'])", "solve([])"],
        expect=[[["a", 1], ["a", 2]], [["solo", 1]], []])

    add("topic-23-3", "Pick a container", "flow", ["kind"],
        "Return [\"stack\", []] for stack, [\"queue\", []] for queue, and [\"list\", []] for anything else.",
        "A factory chooses which object to build from a tag. The tag is the input. The new empty container is the output. The caller does not construct the branches itself.",
        ["Compare kind with stack.", "Then compare it with queue.", "Otherwise build a list."],
        "Build the container named by kind.",
        """
        def solve(kind):
            if kind == "stack":
                return ["stack", []]
            if kind == "queue":
                return ["queue", []]
            return ["list", []]
        """,
        ["solve('stack')", "solve('queue')", "solve('map')"],
        expect=[["stack", []], ["queue", []], ["list", []]])

    add("topic-23-4", "Celsius adapter", "flow", ["celsius"],
        "A legacy reading is in Celsius. Return the Fahrenheit value.",
        "An adapter wraps a value the caller does not want to handle directly. The formula stores the converted number: celsius * 9 / 5 + 32.",
        ["Multiply by 9.", "Divide by 5.", "Add 32."],
        "Convert Celsius to Fahrenheit.",
        """
        def solve(celsius):
            return celsius * 9 / 5 + 32
        """,
        ["solve(0)", "solve(100)", "solve(-40)"],
        expect=[32.0, 212.0, -40.0])

    add("topic-23-5", "Wrap the text", "flow", ["text"],
        "Uppercase the text, then surround it with ***. Return that string.",
        "A decorator wraps a function instead of rewriting it. shout uppercases. banner calls shout and adds the stars around the result.",
        ["Uppercase the text.", "Add *** on both sides.", "Return the wrapped string."],
        "banner(shout(text)).",
        """
        def solve(text):
            def shout(value):
                return value.upper()

            def banner(fn, value):
                return "***" + fn(value) + "***"

            return banner(shout, text)
        """,
        ["solve('hi')", "solve('A')", "solve('')"],
        expect=["***HI***", "***A***", "******"])

    add("topic-23-6", "One greeting call", "flow", ["name"],
        "Trim spaces, title-case the name, and return Hello plus that name.",
        "A facade is one call in front of several small steps. trim, title, and greet stay separate. The caller only sees the final greeting.",
        ["Strip the outer spaces.", "Title-case the result.", "Prefix it with Hello and a space."],
        "trim, then title, then greet.",
        """
        def solve(name):
            def trim(value):
                return value.strip()

            def title(value):
                return value.title()

            def greet(value):
                return "Hello " + value

            return greet(title(trim(name)))
        """,
        ["solve('  ada ')", "solve('ada lovelace')", "solve('  ' )"],
        expect=["Hello Ada", "Hello Ada Lovelace", "Hello "])

    add("topic-23-7", "Notify the watchers", "array", ["watchers", "event", "notes"],
        "watchers is a list of names. Return name:event for each watcher, in order.",
        "An observer list stores who wants the event. The notify loop does not special-case a watcher. It appends one note per stored name.",
        ["Start an empty note list.", "Append each watcher, a colon, and the event.", "Return the notes."],
        "Fan a message out to every watcher.",
        """
        def solve(watchers, event):
            notes = []
            for name in watchers:
                notes.append(name + ":" + event)
            return notes
        """,
        ["solve(['ui', 'log'], 'save')", "solve([], 'save')", "solve(['ui'], 'open')"],
        expect=[["ui:save", "log:save"], [], ["ui:open"]])

    add("topic-23-8", "Pick the operation", "array", ["kind", "nums"],
        "kind is sum, max, or min. Return that result for nums. max and min are only called with a non-empty list.",
        "A strategy is a swappable rule behind one function. kind selects the rule. The numbers stay the same.",
        ["Sum by walking every value.", "For max, keep a value only when it is larger.", "For min, keep a value only when it is smaller."],
        "sum, max, or min.",
        """
        def solve(kind, nums):
            if kind == "sum":
                total = 0
                for value in nums:
                    total = total + value
                return total
            best = nums[0]
            i = 1
            while i < len(nums):
                if kind == "max" and nums[i] > best:
                    best = nums[i]
                if kind == "min" and nums[i] < best:
                    best = nums[i]
                i = i + 1
            return best
        """,
        ["solve('sum', [1, 2, 3])", "solve('max', [1, 2, 3])", "solve('min', [1, 2, 3])"],
        expect=[6, 3, 1])

    add("topic-23-9", "Vending states", "flow", ["events", "state", "log"],
        "Start at idle. coin moves idle to ready. select moves ready to dispense. take moves dispense to idle. Any other event leaves the state unchanged. Return the state before the events and after each event.",
        "The state pattern stores the current mode in one variable. Each event is legal only from one mode, so the same word does nothing in the wrong mode.",
        ["Record the starting state.", "Apply an event only when the current state allows it.", "Append the state after every event."],
        "idle, ready, dispense.",
        """
        def solve(events):
            state = "idle"
            log = [state]
            for event in events:
                if state == "idle" and event == "coin":
                    state = "ready"
                elif state == "ready" and event == "select":
                    state = "dispense"
                elif state == "dispense" and event == "take":
                    state = "idle"
                log.append(state)
            return log
        """,
        ["solve(['coin', 'select', 'take'])", "solve(['select'])", "solve([])"],
        expect=[["idle", "ready", "dispense", "idle"], ["idle", "idle"], ["idle"]])

    add("topic-24-1", "Weighted score", "array", ["weights", "scores", "total"],
        "weights and scores are parallel lists of integers. Return the weighted average, rounded down. An empty weight list returns 0.",
        "The rubric multiplies each score by its weight, adds those products, and divides by the total weight. Integer division rounds down.",
        ["Add weight * score for every index.", "Add the weights.", "Divide the products by the total weight."],
        "Floor of the weighted average.",
        """
        def solve(weights, scores):
            total_w = 0
            total = 0
            i = 0
            while i < len(weights):
                total_w = total_w + weights[i]
                total = total + weights[i] * scores[i]
                i = i + 1
            if total_w == 0:
                return 0
            return total // total_w
        """,
        ["solve([1, 1, 2], [10, 0, 5])", "solve([1, 1], [10, 8])", "solve([], [])"],
        expect=[5, 9, 0])

    add("topic-24-2", "Week focus", "flow", ["week"],
        "Weeks 1 through 8 focus on arrays, search, linked, trees, graphs, dp, design, then mock. Any other week returns rest.",
        "The roadmap is a list of eight labels. The week number is an index into that list. A week outside 1..8 does not read the list.",
        ["Reject a week outside 1..8.", "Subtract 1 to get the index.", "Return that label."],
        "Eight-week focus list.",
        """
        def solve(week):
            plan = ["arrays", "search", "linked", "trees", "graphs", "dp", "design", "mock"]
            if week < 1 or week > 8:
                return "rest"
            return plan[week - 1]
        """,
        ["solve(1)", "solve(6)", "solve(9)"],
        expect=["arrays", "dp", "rest"])

    add("topic-24-3", "Checklist count", "array", ["flags", "count"],
        "flags is a list of True or False. Return [how many are True, True] when every flag is True. An empty list counts as complete.",
        "The checklist stores one boolean per case. count walks the list. The second result compares that count with the length.",
        ["Count the True flags.", "Compare the count with the length.", "Return both."],
        "Passed cases and a complete bit.",
        """
        def solve(flags):
            count = 0
            for flag in flags:
                if flag:
                    count = count + 1
            return [count, count == len(flags)]
        """,
        ["solve([True, False, True])", "solve([True, True])", "solve([])"],
        expect=[[2, False], [2, True], [0, True]])

    add("topic-24-4", "Minute marks", "array", ["phases", "marks", "t"],
        "phases are [name, minutes]. Return [name, start minute] for each phase, then [\"end\", total minutes]. The first phase starts at minute 0.",
        "t is the clock. Each phase records the current t, then adds its length. The end mark stores the clock after the last phase.",
        ["Start the clock at 0.", "Record the name and the clock, then add the length.", "Append the end mark."],
        "Cumulative phase clock.",
        """
        def solve(phases):
            marks = []
            t = 0
            for phase in phases:
                marks.append([phase[0], t])
                t = t + phase[1]
            marks.append(["end", t])
            return marks
        """,
        ["solve([['intro', 5], ['solve', 25]])", "solve([])", "solve([['feedback', 5]])"],
        expect=[[["intro", 0], ["solve", 5], ["end", 30]], [["end", 0]], [["feedback", 0], ["end", 5]]])

    add("topic-24-5", "Day label", "flow", ["day"],
        "Days 1, 3, and 5 are contest days. Days 2 and 4 are interview days. Every other day is review.",
        "The routine is a label chosen from the day number. Two small membership checks pick contest or interview. Everything else is review.",
        ["Return contest for days 1, 3, and 5.", "Return interview for days 2 and 4.", "Return review otherwise."],
        "Contest, interview, or review.",
        """
        def solve(day):
            if day == 1 or day == 3 or day == 5:
                return "contest"
            if day == 2 or day == 4:
                return "interview"
            return "review"
        """,
        ["solve(1)", "solve(2)", "solve(7)"],
        expect=["contest", "interview", "review"])

    add("topic-24-6", "Proof-pack count", "array", ["have", "count"],
        "have lists the artifacts you already have. The pack is readme, tests, trace, and writeup. Return how many of those four are present.",
        "needed is the fixed pack. count increments when a required name is in have. Extra names do not count.",
        ["Walk the four required names.", "Add 1 when the name is present.", "Return the count."],
        "Count the four proof artifacts.",
        """
        def solve(have):
            needed = ["readme", "tests", "trace", "writeup"]
            count = 0
            for name in needed:
                if name in have:
                    count = count + 1
            return count
        """,
        ["solve(['readme', 'trace'])", "solve([])", "solve(['readme', 'tests', 'trace', 'writeup', 'extra'])"],
        expect=[2, 0, 4])

    add("topic-24-7", "Readiness gate", "array", ["criteria"],
        "criteria is a list of True or False. Return True only when there are at least 4 criteria and every one is True.",
        "The gate reads the whole list. A short list fails. Any False fails. Otherwise the candidate passes.",
        ["Fail when the list has fewer than 4 items.", "Fail when any item is False.", "Return True when both checks pass."],
        "At least four passing criteria.",
        """
        def solve(criteria):
            if len(criteria) < 4:
                return False
            for item in criteria:
                if not item:
                    return False
            return True
        """,
        ["solve([True, True, True, True])", "solve([True, True, False, True])", "solve([True, True, True])"],
        expect=[True, False, False])
