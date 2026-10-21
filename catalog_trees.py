"""Sections 10–12."""


def register(add):
    add("topic-10-1", "Chained table", "hash", ["buckets", "key", "out"],
        "Insert [key, value] pairs into 3 buckets using key % 3. Each bucket is a list of pairs. Then answer the queries. Return the query values, or None when missing.",
        "A hash table picks a bucket from the key, then scans only that short chain. Two keys can share a bucket.",
        ["Append the pair to buckets[key % 3].", "For a query, scan that same bucket.", "Return the stored value or None."],
        "Three chains. Hash is key % 3.",
        """
        def solve(pairs, queries):
            buckets = [[], [], []]
            for pair in pairs:
                buckets[pair[0] % 3].append(pair)
            out = []
            for key in queries:
                found = None
                for pair in buckets[key % 3]:
                    if pair[0] == key:
                        found = pair[1]
                out.append(found)
            return out
        """,
        ["solve([[1, 'a'], [4, 'b'], [2, 'c']], [4, 3])", "solve([], [1])", "solve([[3, 9]], [3])"],
        expect=[["b", None], [None], [9]])

    add("topic-10-2", "Who collided", "hash", ["buckets", "key"],
        "Insert the keys into 3 buckets with key % 3, chaining in insert order. Return the three buckets.",
        "A collision is two keys landing in the same bucket. The chain remembers both, in the order they arrived.",
        ["Start three empty lists.", "Append each key to key % 3.", "Return the buckets."],
        "Return the chains.",
        """
        def solve(keys):
            buckets = [[], [], []]
            for key in keys:
                buckets[key % 3].append(key)
            return buckets
        """,
        ["solve([1, 4, 2, 7])", "solve([])", "solve([3])"],
        expect=[[[], [1, 4, 7], [2]], [[], [], []], [[3], [], []]])

    add("topic-10-3", "Key to value", "hash", ["table", "key", "out"],
        "pairs are [key, value]. Return the value for each query key, or None if the key was never stored.",
        "A dictionary stores the value beside the key. Lookup jumps to that slot instead of scanning every pair again.",
        ["Write each pair into the table.", "Read each query.", "Return the stored values."],
        "Build a dict, then look up.",
        """
        def solve(pairs, queries):
            table = {}
            for pair in pairs:
                table[pair[0]] = pair[1]
            out = []
            for key in queries:
                if key in table:
                    out.append(table[key])
                else:
                    out.append(None)
            return out
        """,
        ["solve([['a', 1], ['b', 2]], ['b', 'c'])", "solve([], ['a'])", "solve([['a', 1], ['a', 9]], ['a'])"],
        expect=[[2, None], [None], [9]])

    add("topic-10-4", "Most frequent", "hash", ["nums", "freq", "best", "x"],
        "Return the value that appears most often. On a tie, return the smaller value.",
        "A frequency map stores the count of each value. A second pass remembers the winning key.",
        ["Count every value.", "Keep the key with the larger count.", "If counts tie, keep the smaller key."],
        "Frequency dictionary, then choose.",
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
        ["solve([2, 2, 1, 1, 1])", "solve([4, 4, 3, 3])", "solve([8])"],
        expect=[1, 3, 8])

    add("topic-10-5", "Two sum indexes", "hash", ["nums", "target", "seen", "i", "need"],
        "Return the two indexes that add up to target, earlier index first. Exactly one answer exists.",
        "The map stores value -> index for numbers already seen. need = target - current is one lookup.",
        ["If need is already stored, return both indexes.", "Otherwise store this value's index.", "Move to the next index."],
        "One pass with a dictionary.",
        """
        def solve(nums, target):
            seen = {}
            i = 0
            while i < len(nums):
                need = target - nums[i]
                if need in seen:
                    return [seen[need], i]
                seen[nums[i]] = i
                i = i + 1
            return [-1, -1]
        """,
        ["solve([2, 7, 11, 15], 9)", "solve([3, 3], 6)", "solve([1, 2], 3)"],
        expect=[[0, 1], [0, 1], [0, 1]])

    add("topic-10-6", "Subarrays equaling k", "hash", ["nums", "k", "seen", "run", "count"],
        "Return how many contiguous subarrays sum to k.",
        "A prefix sum plus a map of how often each prefix occurred turns the scan into a lookup. count grows when run - k was seen.",
        ["Store prefix 0 once before the loop.", "Add the current value to run.", "Add seen[run - k] to count, then record run."],
        "Prefix map.",
        """
        def solve(nums, k):
            seen = {0: 1}
            run = 0
            count = 0
            for x in nums:
                run = run + x
                need = run - k
                if need in seen:
                    count = count + seen[need]
                if run not in seen:
                    seen[run] = 0
                seen[run] = seen[run] + 1
            return count
        """,
        ["solve([1, 1, 1], 2)", "solve([1, 2, 3], 3)", "solve([], 0)"],
        expect=[2, 2, 0])

    add("topic-10-7", "Hash the letters", "hash", ["words", "buckets"],
        "Place each word into one of 3 buckets. The hash is the sum of character codes modulo 3. Return the three buckets, each sorted.",
        "A custom hash is a function you write from the data to a bucket index. Equal words land together because the function is deterministic.",
        ["Sum the character codes.", "Append the word to that bucket.", "Sort each bucket and return them."],
        "Bucket by sum(ord) % 3.",
        """
        def solve(words):
            buckets = [[], [], []]
            for word in words:
                total = 0
                for ch in word:
                    total = total + ord(ch)
                buckets[total % 3].append(word)
            for bucket in buckets:
                bucket.sort()
            return buckets
        """,
        ["solve(['a', 'b', 'ab'])", "solve([])", "solve(['a', 'a'])"])

    add("topic-11-1", "Height and size", "tree", ["root", "node"],
        "spec is [value, left, right] or None. Height of an empty tree is 0 and a leaf is 1. Return [height, node count].",
        "Tree words are stored on the nodes themselves. Height is the longest chain of nodes. Size is how many node objects exist.",
        ["An empty spec is height 0 and size 0.", "A node is 1 plus the larger child height.", "Size is 1 plus both children."],
        "Recurse on the nested spec.",
        """
        def solve(spec):
            def walk(node):
                if node is None:
                    return [0, 0]
                left = walk(node["left"])
                right = walk(node["right"])
                height = 1
                if left[0] > right[0]:
                    height = height + left[0]
                else:
                    height = height + right[0]
                return [height, 1 + left[1] + right[1]]

            def build(spec):
                if spec is None:
                    return None
                return {"val": spec[0], "left": build(spec[1]), "right": build(spec[2])}

            return walk(build(spec))
        """,
        ["solve([1, [2, None, None], [3, None, None]])", "solve(None)", "solve([4, None, None])"],
        expect=[[2, 3], [0, 0], [1, 1]])

    add("topic-11-2", "Three walks", "tree", ["root", "pre", "ino", "post"],
        "Return [preorder, inorder, postorder] of the values.",
        "The same nodes, three orders. Preorder writes the value before the children, inorder between them, postorder after them.",
        ["Build the tree.", "Visit left and right in each order.", "Return the three lists."],
        "Recursive preorder, inorder, and postorder.",
        """
        def solve(spec):
            def build(spec):
                if spec is None:
                    return None
                return {"val": spec[0], "left": build(spec[1]), "right": build(spec[2])}

            def pre(node, out):
                if node is None:
                    return
                out.append(node["val"])
                pre(node["left"], out)
                pre(node["right"], out)

            def ino(node, out):
                if node is None:
                    return
                ino(node["left"], out)
                out.append(node["val"])
                ino(node["right"], out)

            def post(node, out):
                if node is None:
                    return
                post(node["left"], out)
                post(node["right"], out)
                out.append(node["val"])

            root = build(spec)
            pre_out = []
            in_out = []
            post_out = []
            pre(root, pre_out)
            ino(root, in_out)
            post(root, post_out)
            return [pre_out, in_out, post_out]
        """,
        ["solve([1, [2, None, None], [3, None, None]])", "solve(None)", "solve([4, None, [5, None, None]])"],
        expect=[[[1, 2, 3], [2, 1, 3], [2, 3, 1]], [[], [], []], [[4, 5], [4, 5], [5, 4]]])

    add("topic-11-3", "Inorder with a stack", "stack", ["stack", "cur", "out"],
        "Return the inorder values using an explicit stack, not a recursive call.",
        "The stack stores the nodes still waiting to be visited. Go left first, then pop, then go right. That is inorder.",
        ["Push the left spine.", "Pop a node and record it.", "Step to its right child."],
        "Iterative inorder.",
        """
        def solve(spec):
            def build(spec):
                if spec is None:
                    return None
                return {"val": spec[0], "left": build(spec[1]), "right": build(spec[2])}

            cur = build(spec)
            stack = []
            out = []
            while cur is not None or stack:
                while cur is not None:
                    stack.append(cur)
                    cur = cur["left"]
                cur = stack.pop()
                out.append(cur["val"])
                cur = cur["right"]
            return out
        """,
        ["solve([1, [2, None, None], [3, None, None]])", "solve(None)", "solve([1, None, [2, None, None]])"],
        expect=[[2, 1, 3], [], [1, 2]])

    add("topic-11-4", "Height and diameter", "tree", ["root"],
        "Return [height, diameter] measured in nodes. A leaf has height 1. Diameter is the longest path's node count.",
        "At each node the diameter candidate is left height plus right height plus this node. The answer is the best candidate stored on the way down.",
        ["Get both children's heights.", "Update the best diameter.", "Return this node's height upward."],
        "One recursion returns height and updates best.",
        """
        def solve(spec):
            def build(spec):
                if spec is None:
                    return None
                return {"val": spec[0], "left": build(spec[1]), "right": build(spec[2])}

            best = [0]

            def height(node):
                if node is None:
                    return 0
                left = height(node["left"])
                right = height(node["right"])
                path = left + right + 1
                if path > best[0]:
                    best[0] = path
                if left > right:
                    return left + 1
                return right + 1

            root = build(spec)
            h = height(root)
            return [h, best[0]]
        """,
        ["solve([1, [2, [3, None, None], None], [4, None, None]])", "solve(None)", "solve([1, None, None])"],
        expect=[[3, 4], [0, 0], [1, 1]])

    add("topic-11-5", "Is it balanced", "tree", ["root"],
        "Return True when every node has subtree heights differing by at most 1. Empty is balanced. Height of empty is 0.",
        "Balance is a local rule checked at every node. The recursion returns the height, or -1 when a subtree is already unbalanced.",
        ["Ask both children for their heights.", "If either is -1 or they differ by more than 1, return -1.", "Otherwise return 1 plus the taller child."],
        "Return True when the walk does not report -1.",
        """
        def solve(spec):
            def build(spec):
                if spec is None:
                    return None
                return {"val": spec[0], "left": build(spec[1]), "right": build(spec[2])}

            def check(node):
                if node is None:
                    return 0
                left = check(node["left"])
                right = check(node["right"])
                if left < 0 or right < 0:
                    return -1
                diff = left - right
                if diff < 0:
                    diff = -diff
                if diff > 1:
                    return -1
                if left > right:
                    return left + 1
                return right + 1

            return check(build(spec)) >= 0
        """,
        ["solve([1, [2, None, None], [3, None, None]])", "solve([1, [2, [3, None, None], None], None])", "solve(None)"],
        expect=[True, False, True])

    add("topic-11-6", "Lowest common ancestor", "tree", ["root", "p", "q"],
        "p and q are values in the tree. Return the value of their lowest common ancestor.",
        "If a node finds p in one subtree and q in the other, that node is the split point. That split is the lowest ancestor stored on both paths.",
        ["If this node is p or q, return it.", "Search both children.", "If both sides return a node, this node is the ancestor."],
        "Recursive LCA.",
        """
        def solve(spec, p, q):
            def build(spec):
                if spec is None:
                    return None
                return {"val": spec[0], "left": build(spec[1]), "right": build(spec[2])}

            def lca(node):
                if node is None or node["val"] == p or node["val"] == q:
                    return node
                left = lca(node["left"])
                right = lca(node["right"])
                if left is not None and right is not None:
                    return node
                if left is not None:
                    return left
                return right

            return lca(build(spec))["val"]
        """,
        ["solve([1, [2, [4, None, None], None], [3, None, None]], 4, 3)", "solve([1, [2, [4, None, None], None], [3, None, None]], 4, 2)", "solve([1, None, None], 1, 1)"],
        expect=[1, 2, 1])

    add("topic-11-7", "Path equals target", "tree", ["root", "target", "left"],
        "Return True when some root-to-leaf path sums to target.",
        "Each call stores the remaining sum. A leaf succeeds when the remaining sum equals its value.",
        ["Subtract the node value from the target.", "A leaf checks whether the remainder is 0.", "Otherwise try the left path or the right path."],
        "Remaining-sum recursion.",
        """
        def solve(spec, target):
            def build(spec):
                if spec is None:
                    return None
                return {"val": spec[0], "left": build(spec[1]), "right": build(spec[2])}

            def walk(node, need):
                if node is None:
                    return False
                left_need = need - node["val"]
                if node["left"] is None and node["right"] is None:
                    return left_need == 0
                return walk(node["left"], left_need) or walk(node["right"], left_need)

            return walk(build(spec), target)
        """,
        ["solve([5, [4, [11, None, None], None], [8, None, None]], 20)", "solve([5, [4, None, None], None], 5)", "solve(None, 0)"],
        expect=[True, False, False])

    add("topic-11-8", "Flatten the shape", "tree", ["root", "out"],
        "Return the preorder list of the tree, using None wherever a child is missing.",
        "Serialization stores the shape, not only the values. None marks a missing child so the list can be rebuilt later.",
        ["Write the value.", "Serialize the left child, even if it is None.", "Serialize the right child."],
        "Preorder with None markers.",
        """
        def solve(spec):
            def build(spec):
                if spec is None:
                    return None
                return {"val": spec[0], "left": build(spec[1]), "right": build(spec[2])}

            out = []

            def walk(node):
                if node is None:
                    out.append(None)
                    return
                out.append(node["val"])
                walk(node["left"])
                walk(node["right"])

            walk(build(spec))
            return out
        """,
        ["solve([1, [2, None, None], None])", "solve(None)", "solve([1, None, None])"],
        expect=[[1, 2, None, None, None], [None], [1, None, None]])

    add("topic-11-9", "BST in order", "tree", ["root", "v"],
        "Insert the values into an empty binary search tree in the given order. Return the inorder values.",
        "A BST stores smaller values on the left and larger values on the right. Inorder then reads them sorted.",
        ["Walk left or right by comparing with the node.", "Create a leaf when you fall off.", "Read the tree inorder."],
        "BST insert, then inorder.",
        """
        def solve(values):
            root = None

            def insert(node, v):
                if node is None:
                    return {"val": v, "left": None, "right": None}
                if v < node["val"]:
                    node["left"] = insert(node["left"], v)
                else:
                    node["right"] = insert(node["right"], v)
                return node

            for v in values:
                root = insert(root, v)

            out = []

            def inorder(node):
                if node is None:
                    return
                inorder(node["left"])
                out.append(node["val"])
                inorder(node["right"])

            inorder(root)
            return out
        """,
        ["solve([2, 1, 3])", "solve([])", "solve([1, 1])"],
        expect=[[1, 2, 3], [], [1, 1]])

    add("topic-11-10", "AVL insert", "tree", ["root", "v"],
        "Insert the values into an AVL tree. Return [root value, inorder values].",
        "An AVL node stores a height. After each insert, a balance check may rotate so the stored heights differ by at most 1.",
        ["Insert like a BST.", "Update the height.", "Rotate when the balance is 2 or -2."],
        "AVL insert with single and double rotations.",
        """
        def solve(values):
            root = None

            def height(node):
                if node is None:
                    return 0
                return node["h"]

            def fix(node):
                left_h = height(node["left"])
                right_h = height(node["right"])
                if left_h > right_h:
                    node["h"] = left_h + 1
                else:
                    node["h"] = right_h + 1
                return node

            def bal(node):
                return height(node["left"]) - height(node["right"])

            def rot_right(y):
                x = y["left"]
                y["left"] = x["right"]
                x["right"] = y
                fix(y)
                fix(x)
                return x

            def rot_left(x):
                y = x["right"]
                x["right"] = y["left"]
                y["left"] = x
                fix(x)
                fix(y)
                return y

            def insert(node, v):
                if node is None:
                    return {"val": v, "left": None, "right": None, "h": 1}
                if v < node["val"]:
                    node["left"] = insert(node["left"], v)
                else:
                    node["right"] = insert(node["right"], v)
                fix(node)
                b = bal(node)
                if b > 1 and v < node["left"]["val"]:
                    return rot_right(node)
                if b < -1 and node["right"] is not None and v > node["right"]["val"]:
                    return rot_left(node)
                if b > 1 and node["left"] is not None and v > node["left"]["val"]:
                    node["left"] = rot_left(node["left"])
                    return rot_right(node)
                if b < -1 and node["right"] is not None and v < node["right"]["val"]:
                    node["right"] = rot_right(node["right"])
                    return rot_left(node)
                return node

            for v in values:
                root = insert(root, v)
            out = []

            def inorder(node):
                if node is None:
                    return
                inorder(node["left"])
                out.append(node["val"])
                inorder(node["right"])

            inorder(root)
            return [root["val"], out]
        """,
        ["solve([3, 2, 1])", "solve([1, 2, 3])", "solve([2])"],
        expect=[[2, [1, 2, 3]], [2, [1, 2, 3]], [2, [2]]])

    add("topic-11-11", "Paint the colors", "tree", ["root", "color"],
        "Color the root black (0) and each child the opposite of its parent. Return [value, color] in preorder. This is the red-black color rule on a tiny tree: the root is black, and a red node's parent is not red.",
        "A color is data stored beside the value. The root writes 0. Each child writes 1 minus the parent color.",
        ["Write the root as black.", "Pass the opposite color to each child.", "Collect value and color in preorder."],
        "Root color 0, child color 1 - parent.",
        """
        def solve(spec):
            def build(spec):
                if spec is None:
                    return None
                return {"val": spec[0], "left": build(spec[1]), "right": build(spec[2])}

            out = []

            def walk(node, color):
                if node is None:
                    return
                out.append([node["val"], color])
                walk(node["left"], 1 - color)
                walk(node["right"], 1 - color)

            walk(build(spec), 0)
            return out
        """,
        ["solve([2, [1, None, None], [3, None, None]])", "solve(None)", "solve([1, None, [2, None, None]])"],
        expect=[[[2, 0], [1, 1], [3, 1]], [], [[1, 0], [2, 1]]])

    add("topic-11-12", "Trie yes or no", "hash", ["root", "node", "word"],
        "Insert words, then return a boolean for each query: True when that word was inserted.",
        "A trie is a tree of characters stored as nested dictionaries. A word ends only when its last node is marked.",
        ["Walk or create a node per character.", "Mark the end of the word.", "A query must follow existing links and see the mark."],
        "Nested dict trie.",
        """
        def solve(words, queries):
            root = {}
            for word in words:
                node = root
                for ch in word:
                    if ch not in node:
                        node[ch] = {}
                    node = node[ch]
                node["$"] = True
            out = []
            for word in queries:
                node = root
                ok = True
                for ch in word:
                    if ch not in node:
                        ok = False
                        break
                    node = node[ch]
                if ok and "$" in node:
                    out.append(True)
                else:
                    out.append(False)
            return out
        """,
        ["solve(['he', 'she'], ['he', 'her', 'she'])", "solve([], [''])", "solve(['a'], ['a', 'b'])"],
        expect=[[True, False, True], [False], [True, False]])

    add("topic-11-13", "Range sum tree", "array", ["tree", "arr", "left", "right"],
        "Build a segment tree for sum and return the inclusive range sum from left to right.",
        "Each segment-tree slot stores the sum of a range. A query reads O(log n) of those stored ranges instead of every item.",
        ["A leaf stores arr[i].", "A parent stores the sum of its children.", "Add the nodes that sit fully inside the query."],
        "Segment tree range sum.",
        """
        def solve(arr, left, right):
            n = len(arr)
            tree = []
            i = 0
            while i < 4 * n:
                tree.append(0)
                i = i + 1

            def build(node, l, r):
                if l == r:
                    tree[node] = arr[l]
                    return
                mid = (l + r) // 2
                build(node * 2, l, mid)
                build(node * 2 + 1, mid + 1, r)
                tree[node] = tree[node * 2] + tree[node * 2 + 1]

            def query(node, l, r, ql, qr):
                if qr < l or r < ql:
                    return 0
                if ql <= l and r <= qr:
                    return tree[node]
                mid = (l + r) // 2
                return query(node * 2, l, mid, ql, qr) + query(node * 2 + 1, mid + 1, r, ql, qr)

            build(1, 0, n - 1)
            return query(1, 0, n - 1, left, right)
        """,
        ["solve([1, 3, 5], 0, 2)", "solve([1, 3, 5], 1, 2)", "solve([4], 0, 0)"],
        expect=[9, 8, 4])

    add("topic-11-14", "Fenwick prefixes", "array", ["bit", "arr", "i"],
        "Build a Fenwick tree (binary indexed tree) from arr and return the prefix sums: index i is the sum of arr[0] through arr[i].",
        "A Fenwick tree stores partial sums on ranges whose length is a power of two. Prefix queries add those blocks.",
        ["Add each arr[i] into the tree.", "The update jumps by the lowest set bit.", "Read each prefix the same way."],
        "Point updates, then prefix queries.",
        """
        def solve(arr):
            n = len(arr)
            bit = []
            i = 0
            while i <= n:
                bit.append(0)
                i = i + 1

            def add(i, value):
                i = i + 1
                while i <= n:
                    bit[i] = bit[i] + value
                    i = i + (i & -i)

            def pref(i):
                i = i + 1
                total = 0
                while i > 0:
                    total = total + bit[i]
                    i = i - (i & -i)
                return total

            i = 0
            while i < n:
                add(i, arr[i])
                i = i + 1
            out = []
            i = 0
            while i < n:
                out.append(pref(i))
                i = i + 1
            return out
        """,
        ["solve([1, 2, 3])", "solve([4])", "solve([])"],
        expect=[[1, 3, 6], [4], []])

    add("topic-11-15", "Range minimum", "array", ["arr", "left", "right", "i"],
        "Return the minimum of arr[left..right] inclusive. Build the answer by comparing stored block minimums of doubling length. For this small array, fill a sparse table and read the one block that covers the query.",
        "A sparse table stores the minimum of every range whose length is a power of two. A query overlaps two such blocks.",
        ["st[k][i] is the min of 2^k items starting at i.", "Build longer blocks from shorter ones.", "Cover the query with two blocks."],
        "Sparse table range minimum.",
        """
        def solve(arr, left, right):
            n = len(arr)
            log = [0]
            i = 1
            while i <= n:
                log.append(log[i // 2] + (0 if i == 1 else 1))
                i = i + 1
            # log[1] should be 0
            log[1] = 0
            st = []
            row = []
            i = 0
            while i < n:
                row.append(arr[i])
                i = i + 1
            st.append(row)
            length = 1
            while length * 2 <= n:
                prev = st[-1]
                row = []
                i = 0
                while i + length * 2 <= n:
                    a = prev[i]
                    b = prev[i + length]
                    if a < b:
                        row.append(a)
                    else:
                        row.append(b)
                    i = i + 1
                st.append(row)
                length = length * 2
            span = right - left + 1
            k = 0
            size = 1
            while size * 2 <= span:
                size = size * 2
                k = k + 1
            a = st[k][left]
            b = st[k][right - size + 1]
            if a < b:
                return a
            return b
        """,
        ["solve([4, 1, 7, 3], 1, 3)", "solve([4, 1, 7, 3], 0, 0)", "solve([2, 2], 0, 1)"],
        expect=[1, 4, 2])

    add("topic-11-16", "Kth ancestor", "array", ["parent", "node", "k", "up"],
        "parent[i] is the parent of i, or -1 for the root. Return the kth ancestor of node, or -1 if it does not exist. Use binary lifting.",
        "Binary lifting stores the 1st, 2nd, 4th, ... ancestor. The bits of k choose which of those jumps to follow.",
        ["Fill the 2^b ancestor table.", "Walk the bits of k from small to large.", "If a jump leaves the tree, return -1."],
        "Binary lifting with 4 levels.",
        """
        def solve(parent, node, k):
            log = 4
            n = len(parent)
            up = []
            i = 0
            while i < n:
                row = []
                b = 0
                while b < log:
                    row.append(-1)
                    b = b + 1
                row[0] = parent[i]
                up.append(row)
                i = i + 1
            b = 1
            while b < log:
                i = 0
                while i < n:
                    prev = up[i][b - 1]
                    if prev == -1:
                        up[i][b] = -1
                    else:
                        up[i][b] = up[prev][b - 1]
                    i = i + 1
                b = b + 1
            b = 0
            while b < log:
                if (k & (1 << b)) != 0:
                    if node == -1:
                        return -1
                    node = up[node][b]
                b = b + 1
            return node
        """,
        ["solve([-1, 0, 0, 1, 1], 4, 2)", "solve([-1, 0, 0, 1, 1], 4, 1)", "solve([-1, 0, 0, 1, 1], 4, 5)"],
        expect=[0, 1, -1])

    add("topic-11-17", "Enter times", "tree", ["g", "tin", "time", "node"],
        "edges are undirected pairs of a tree rooted at 0. Return tin, the time each node is first entered on a DFS. Children are visited in increasing node id.",
        "An Euler tour writes the time when DFS enters a node. tin[node] is that clock value, stored before the children are visited.",
        ["Sort each adjacency list.", "Record tin when you enter.", "Increase the clock, then visit children."],
        "DFS enter times from root 0.",
        """
        def solve(n, edges):
            g = []
            i = 0
            while i < n:
                g.append([])
                i = i + 1
            for e in edges:
                g[e[0]].append(e[1])
                g[e[1]].append(e[0])
            for row in g:
                row.sort()
            tin = []
            i = 0
            while i < n:
                tin.append(0)
                i = i + 1
            clock = [0]

            def dfs(node, parent):
                tin[node] = clock[0]
                clock[0] = clock[0] + 1
                for nxt in g[node]:
                    if nxt != parent:
                        dfs(nxt, node)

            dfs(0, -1)
            return tin
        """,
        ["solve(6, [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]])", "solve(1, [])", "solve(2, [[0, 1]])"],
        expect=[[0, 1, 4, 2, 3, 5], [0], [0, 1]])

    add("topic-11-18", "Heavy child", "tree", ["g", "size", "heavy"],
        "The same tree shape as an undirected edge list rooted at 0. Return heavy[node], the child with the largest subtree, or -1 for a leaf. Ties keep the smaller child id.",
        "Heavy-light decomposition starts by storing subtree sizes. The heavy child is the one whose subtree is strictly larger than the others.",
        ["Compute subtree sizes bottom-up.", "Pick the child with the greatest size.", "Store -1 when there is no child."],
        "Subtree sizes, then the heavy child.",
        """
        def solve(n, edges):
            g = []
            i = 0
            while i < n:
                g.append([])
                i = i + 1
            for e in edges:
                g[e[0]].append(e[1])
                g[e[1]].append(e[0])
            for row in g:
                row.sort()
            size = []
            heavy = []
            i = 0
            while i < n:
                size.append(0)
                heavy.append(-1)
                i = i + 1

            def dfs(node, parent):
                size[node] = 1
                best = -1
                for nxt in g[node]:
                    if nxt == parent:
                        continue
                    dfs(nxt, node)
                    size[node] = size[node] + size[nxt]
                    if best == -1 or size[nxt] > size[best]:
                        best = nxt
                heavy[node] = best

            dfs(0, -1)
            return heavy
        """,
        ["solve(6, [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]])", "solve(1, [])", "solve(2, [[0, 1]])"],
        expect=[[1, 3, 5, -1, -1, -1], [-1], [1, -1]])

    add("topic-11-19", "One centroid", "tree", ["g", "size", "n"],
        "Return one centroid of the undirected tree rooted conceptually at 0: a node whose removal leaves every piece of size at most n/2.",
        "A centroid is found from subtree sizes. Walk toward the child whose subtree is bigger than n/2. The node where you stop is a centroid.",
        ["Compute subtree sizes.", "From 0, move to a child with size > n/2 if one exists.", "Return the node where every child is at most n/2."],
        "Walk to the centroid.",
        """
        def solve(n, edges):
            g = []
            i = 0
            while i < n:
                g.append([])
                i = i + 1
            for e in edges:
                g[e[0]].append(e[1])
                g[e[1]].append(e[0])
            size = []
            i = 0
            while i < n:
                size.append(0)
                i = i + 1

            def dfs(node, parent):
                size[node] = 1
                for nxt in g[node]:
                    if nxt != parent:
                        dfs(nxt, node)
                        size[node] = size[node] + size[nxt]

            dfs(0, -1)
            node = 0
            parent = -1
            while True:
                moved = False
                for nxt in g[node]:
                    if nxt != parent and size[nxt] > n // 2:
                        parent = node
                        node = nxt
                        moved = True
                        break
                if not moved:
                    return node
        """,
        ["solve(6, [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]])", "solve(1, [])", "solve(2, [[0, 1]])"],
        expect=[0, 0, 0])

    add("topic-12-1", "Min-heap pops", "array", ["heap", "x"],
        "Push every value into a min-heap, then pop all of them. Return the popped values.",
        "A min-heap stores the smallest value at index 0. Pop removes it and sifts the last item down so the shape stays a heap.",
        ["Push each value.", "Pop until the heap is empty.", "The output is sorted ascending."],
        "heapq push and pop.",
        """
        def solve(nums):
            import heapq
            heap = []
            for x in nums:
                heapq.heappush(heap, x)
            out = []
            while heap:
                out.append(heapq.heappop(heap))
            return out
        """,
        ["solve([3, 1, 2])", "solve([])", "solve([4])"],
        expect=[[1, 2, 3], [], [4]])

    add("topic-12-2", "Max-heap pops", "array", ["heap", "x"],
        "Push every value so the largest comes out first. Return the popped values.",
        "Python's heap is a min-heap. Storing the negation flips the order, so the most negative entry is the largest original value.",
        ["Push -value.", "Pop and negate.", "The output is sorted descending."],
        "Negated min-heap.",
        """
        def solve(nums):
            import heapq
            heap = []
            for x in nums:
                heapq.heappush(heap, -x)
            out = []
            while heap:
                out.append(-heapq.heappop(heap))
            return out
        """,
        ["solve([3, 1, 2])", "solve([])", "solve([4])"],
        expect=[[3, 2, 1], [], [4]])

    add("topic-12-3", "Heapify the row", "array", ["a", "i"],
        "Turn the list into a min-heap in place and return it.",
        "Heapify sifts nodes from the middle backward. After it, index 0 holds the smallest value and every parent is <= its children.",
        ["Start at the last parent.", "Sift that index down.", "Return the list."],
        "heapq.heapify.",
        """
        def solve(a):
            import heapq
            a = list(a)
            heapq.heapify(a)
            return a
        """,
        ["solve([3, 1, 2])", "solve([4])", "solve([])"],
        expect=[[1, 3, 2], [4], []])

    add("topic-12-4", "Three largest", "array", ["heap", "x"],
        "Return the 3 largest values in descending order. If there are fewer than 3, return all of them in that order.",
        "A size-limited heap can keep the best values seen so far. Here the whole list is small, so a max-heap pop does the same memory story.",
        ["Push negated values.", "Pop up to 3 times.", "Negate them back."],
        "Pop at most 3 from a max-heap.",
        """
        def solve(nums):
            import heapq
            heap = []
            for x in nums:
                heapq.heappush(heap, -x)
            out = []
            while heap and len(out) < 3:
                out.append(-heapq.heappop(heap))
            return out
        """,
        ["solve([5, 1, 4, 2, 3])", "solve([9])", "solve([])"],
        expect=[[5, 4, 3], [9], []])

    add("topic-12-5", "Merge sorted rows", "array", ["heap", "lists", "i"],
        "lists is a list of sorted lists. Merge them into one sorted list using a heap of the current heads.",
        "The heap stores one head from each list: (value, which list, index). Popping the smallest writes the next output and pushes that list's next item.",
        ["Push the first item of every list.", "Pop the smallest and append it.", "Push the next item from that same list."],
        "Heap of list heads.",
        """
        def solve(lists):
            import heapq
            heap = []
            i = 0
            while i < len(lists):
                if lists[i]:
                    heapq.heappush(heap, (lists[i][0], i, 0))
                i = i + 1
            out = []
            while heap:
                value, li, idx = heapq.heappop(heap)
                out.append(value)
                if idx + 1 < len(lists[li]):
                    heapq.heappush(heap, (lists[li][idx + 1], li, idx + 1))
            return out
        """,
        ["solve([[1, 4], [2, 3], [0]])", "solve([[], [1]])", "solve([])"],
        expect=[[0, 1, 2, 3, 4], [1], []])

    add("topic-12-6", "Lower medians", "array", ["lo", "hi", "x"],
        "After each inserted value, record the lower median: the middle after sorting, or the lower of the two middles when the count is even. Return that list.",
        "Two heaps split the stream. The max-heap holds the lower half, so its top is the lower median. The min-heap holds the rest.",
        ["Push into the lower half, then move its top to the upper half.", "If the upper half is taller, move one back.", "Record the top of the lower half."],
        "Two heaps. Return lower medians.",
        """
        def solve(nums):
            import heapq
            lo = []
            hi = []
            out = []
            for x in nums:
                heapq.heappush(lo, -x)
                heapq.heappush(hi, -heapq.heappop(lo))
                if len(hi) > len(lo):
                    heapq.heappush(lo, -heapq.heappop(hi))
                out.append(-lo[0])
            return out
        """,
        ["solve([1, 2, 3])", "solve([5])", "solve([])"],
        expect=[[1, 1, 2], [5], []])

