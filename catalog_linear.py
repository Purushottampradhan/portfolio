"""Sections 8–12. Linked lists, stacks, hashing, trees, heaps."""


def register(add):
    add("topic-8-1", "Insert at the head", "linked", ["head", "cur", "v"],
        "Insert each value at the head of a singly linked list. Return the values from the head.",
        "A node is a small object: a value and a link called next. Inserting at the head points the new node at the old head.",
        ["Create a node for the next value.", "Point its next at the current head.", "Move head to the new node."],
        "head = {val, next: head} for each value.",
        """
        def solve(values):
            head = None
            for v in values:
                head = {"val": v, "next": head}
            out = []
            cur = head
            while cur is not None:
                out.append(cur["val"])
                cur = cur["next"]
            return out
        """,
        ["solve([1, 2, 3])", "solve([])", "solve([8])"],
        expect=[[3, 2, 1], [], [8]])

    add("topic-8-2", "Doubly linked tail", "linked", ["head", "tail", "node", "cur"],
        "Insert each value at the tail of a doubly linked list (each node has prev and next). Return the values from the head.",
        "A doubly linked node stores two links. tail.prev is the previous node, and the previous node's next is the new tail.",
        ["Create a node whose prev is the current tail.", "Link the old tail forward.", "Move tail to the new node."],
        "Append at the tail using prev and next.",
        """
        def solve(values):
            head = None
            tail = None
            for v in values:
                node = {"val": v, "next": None, "prev": tail}
                if tail is None:
                    head = node
                else:
                    tail["next"] = node
                tail = node
            out = []
            cur = head
            while cur is not None:
                out.append(cur["val"])
                cur = cur["next"]
            return out
        """,
        ["solve([1, 2, 3])", "solve([])", "solve([4])"],
        expect=[[1, 2, 3], [], [4]])

    add("topic-8-3", "Close the circle", "linked", ["head", "tail", "cur"],
        "Build a circular list and walk exactly len(values) steps. Return [values in that walk, True if you are back at the head].",
        "A circular list stores the tail's next as the head. After one full walk, the cursor is the same object as the head.",
        ["Link the nodes in order.", "Point the tail at the head.", "Walk n steps and check the cursor."],
        "tail next is head. Walk n steps.",
        """
        def solve(values):
            if not values:
                return [[], False]
            head = None
            tail = None
            for v in values:
                node = {"val": v, "next": None}
                if head is None:
                    head = node
                else:
                    tail["next"] = node
                tail = node
            tail["next"] = head
            out = []
            cur = head
            i = 0
            while i < len(values):
                out.append(cur["val"])
                cur = cur["next"]
                i = i + 1
            return [out, cur is head]
        """,
        ["solve([1, 2, 3])", "solve([7])", "solve([])"],
        expect=[[[1, 2, 3], True], [[7], True], [[], False]])

    add("topic-8-4", "Reverse the links", "linked", ["head", "prev", "cur", "nxt"],
        "Build a list in the given order, reverse the links, and return the values from the new head.",
        "Reversal keeps the nodes and rewrites next. prev, cur, and nxt are three fingers walking the chain.",
        ["Save cur.next in nxt.", "Point cur.next at prev.", "Step prev and cur forward."],
        "Classic three-pointer reversal.",
        """
        def solve(values):
            head = None
            tail = None
            for v in values:
                node = {"val": v, "next": None}
                if head is None:
                    head = node
                else:
                    tail["next"] = node
                tail = node
            prev = None
            cur = head
            while cur is not None:
                nxt = cur["next"]
                cur["next"] = prev
                prev = cur
                cur = nxt
            out = []
            node = prev
            while node is not None:
                out.append(node["val"])
                node = node["next"]
            return out
        """,
        ["solve([1, 2, 3, 4])", "solve([])", "solve([9])"],
        expect=[[4, 3, 2, 1], [], [9]])

    add("topic-8-5", "Cycle or not", "linked", ["slow", "fast", "nodes"],
        "values become a linked list. If join is >= 0, the last node points at that index. Return True when Floyd's two pointers meet.",
        "slow moves one node, fast moves two. On a cycle they land on the same object. On a straight list fast falls off the end.",
        ["Build the nodes and the optional back edge.", "Move slow once and fast twice.", "Return True if they become the same node."],
        "Floyd's tortoise and hare.",
        """
        def solve(values, join):
            nodes = []
            for v in values:
                nodes.append({"val": v, "next": None})
            i = 0
            while i < len(nodes) - 1:
                nodes[i]["next"] = nodes[i + 1]
                i = i + 1
            if nodes and join >= 0:
                nodes[-1]["next"] = nodes[join]
            if not nodes:
                return False
            slow = nodes[0]
            fast = nodes[0]
            while fast is not None and fast["next"] is not None:
                slow = slow["next"]
                fast = fast["next"]["next"]
                if slow is fast:
                    return True
            return False
        """,
        ["solve([1, 2, 3, 4], 1)", "solve([1, 2, 3], -1)", "solve([], -1)"],
        expect=[True, False, False])

    add("topic-8-6", "Merge two sorted lists", "linked", ["left", "right", "tail"],
        "a and b are sorted. Merge them into one sorted linked list and return the values.",
        "Two heads move forward. The smaller value is linked onto the result, and that list's cursor advances.",
        ["Compare the two current values.", "Link the smaller node.", "Append whichever list remains."],
        "Merge by always taking the smaller head.",
        """
        def solve(a, b):
            def build(values):
                head = None
                tail = None
                for v in values:
                    node = {"val": v, "next": None}
                    if head is None:
                        head = node
                    else:
                        tail["next"] = node
                    tail = node
                return head
            left = build(a)
            right = build(b)
            dummy = {"val": 0, "next": None}
            tail = dummy
            while left is not None and right is not None:
                if left["val"] <= right["val"]:
                    tail["next"] = left
                    left = left["next"]
                else:
                    tail["next"] = right
                    right = right["next"]
                tail = tail["next"]
            if left is not None:
                tail["next"] = left
            else:
                tail["next"] = right
            out = []
            cur = dummy["next"]
            while cur is not None:
                out.append(cur["val"])
                cur = cur["next"]
            return out
        """,
        ["solve([1, 3], [2, 4])", "solve([], [1])", "solve([], [])"],
        expect=[[1, 2, 3, 4], [1], []])

    add("topic-8-7", "Shared tail", "linked", ["a", "b"],
        "Build two lists that share the nodes of shared after their own fronts. Return the value of the first shared node, or None.",
        "Intersection is one node object with two incoming links. Equal length tails meet on that object when both cursors step together.",
        ["Build the shared tail once.", "Attach each front to that same tail.", "Skip the length difference, then walk in lockstep."],
        "Two pointers after equalizing length.",
        """
        def solve(a_vals, b_vals, shared):
            shared_head = None
            prev = None
            for v in shared:
                node = {"val": v, "next": None}
                if shared_head is None:
                    shared_head = node
                else:
                    prev["next"] = node
                prev = node

            def chain(values, tail):
                first = None
                prev_node = None
                for v in values:
                    node = {"val": v, "next": None}
                    if first is None:
                        first = node
                    else:
                        prev_node["next"] = node
                    prev_node = node
                if prev_node is None:
                    return tail
                prev_node["next"] = tail
                return first

            a = chain(a_vals, shared_head)
            b = chain(b_vals, shared_head)

            def length(node):
                n = 0
                while node is not None:
                    n = n + 1
                    node = node["next"]
                return n

            la = length(a)
            lb = length(b)
            while la > lb:
                a = a["next"]
                la = la - 1
            while lb > la:
                b = b["next"]
                lb = lb - 1
            while a is not None and a is not b:
                a = a["next"]
                b = b["next"]
            if a is None:
                return None
            return a["val"]
        """,
        ["solve([1, 2], [3], [8, 9])", "solve([1], [2], [])", "solve([1], [], [7])"],
        expect=[8, None, 7])

    add("topic-8-8", "Remove the nth last node", "linked", ["dummy", "slow", "fast"],
        "Remove the nth node from the end (n starts at 1) and return the remaining values.",
        "A fast cursor is n steps ahead of slow. When fast reaches the end, slow is just before the node to unlink.",
        ["Move fast n steps.", "Move both until fast is on the last node.", "Skip slow.next."],
        "One-pass two pointers from a dummy head.",
        """
        def solve(values, n):
            head = None
            tail = None
            for v in values:
                node = {"val": v, "next": None}
                if head is None:
                    head = node
                else:
                    tail["next"] = node
                tail = node
            dummy = {"val": 0, "next": head}
            fast = dummy
            i = 0
            while i < n:
                fast = fast["next"]
                i = i + 1
            slow = dummy
            while fast["next"] is not None:
                fast = fast["next"]
                slow = slow["next"]
            slow["next"] = slow["next"]["next"]
            out = []
            cur = dummy["next"]
            while cur is not None:
                out.append(cur["val"])
                cur = cur["next"]
            return out
        """,
        ["solve([1, 2, 3, 4], 2)", "solve([1], 1)", "solve([1, 2], 2)"],
        expect=[[1, 2, 4], [], [2]])

    add("topic-8-9", "Tiny LRU", "hash", ["cache", "order", "op", "out"],
        "Capacity is 2. ops are ['put', key, value] or ['get', key]. Return the list of get results. A missing key returns -1. Getting or updating a key makes it the newest.",
        "An LRU cache stores values in a map and order in a list. The front of the order is the least recently used key, the one evicted when the cache is full.",
        ["On put of a new key at capacity, drop the oldest key.", "Move the touched key to the newest end.", "On get, return the stored value or -1."],
        "Dictionary plus an order list of capacity 2.",
        """
        def solve(ops):
            cap = 2
            cache = {}
            order = []
            out = []
            for op in ops:
                if op[0] == "put":
                    key = op[1]
                    val = op[2]
                    if key in order:
                        order.remove(key)
                    elif len(order) == cap:
                        old = order.pop(0)
                        del cache[old]
                    cache[key] = val
                    order.append(key)
                else:
                    key = op[1]
                    if key in order:
                        order.remove(key)
                        order.append(key)
                        out.append(cache[key])
                    else:
                        out.append(-1)
            return out
        """,
        ["solve([['put', 1, 1], ['put', 2, 2], ['get', 1], ['put', 3, 3], ['get', 2], ['get', 3]])", "solve([['get', 1]])", "solve([['put', 1, 5], ['get', 1]])"],
        expect=[[1, -1, 3], [-1], [5]])

    add("topic-9-1", "Stack log", "stack", ["stack", "op", "out"],
        "ops are ['push', x], ['pop'], or ['peek']. Return the values produced by pop and peek. Pop or peek on an empty stack produces None.",
        "A stack stores items in a list. The last item is the top. Push appends. Pop and peek read that end.",
        ["Push appends.", "Pop removes and records the last item.", "Peek records the last item without removing it."],
        "Use a list as a stack.",
        """
        def solve(ops):
            stack = []
            out = []
            for op in ops:
                if op[0] == "push":
                    stack.append(op[1])
                elif op[0] == "pop":
                    if stack:
                        out.append(stack.pop())
                    else:
                        out.append(None)
                else:
                    if stack:
                        out.append(stack[-1])
                    else:
                        out.append(None)
            return out
        """,
        ["solve([['push', 1], ['push', 2], ['peek'], ['pop'], ['pop'], ['pop']])", "solve([['peek']])", "solve([])"],
        expect=[[2, 2, 1, None], [None], []])

    add("topic-9-2", "Next smaller on the right", "stack", ["nums", "stack", "ans", "i"],
        "For each index, return the next strictly smaller value on its right, or -1.",
        "A monotonic stack stores indexes whose values are still waiting for a smaller item. When a smaller value arrives, it answers those indexes.",
        ["Scan from the left.", "Pop indexes that are larger than the current value and write the answer.", "Push the current index."],
        "Monotonic increasing stack of indexes.",
        """
        def solve(nums):
            ans = []
            i = 0
            while i < len(nums):
                ans.append(-1)
                i = i + 1
            stack = []
            i = 0
            while i < len(nums):
                while stack and nums[stack[-1]] > nums[i]:
                    ans[stack.pop()] = nums[i]
                stack.append(i)
                i = i + 1
            return ans
        """,
        ["solve([4, 2, 5, 1])", "solve([1, 2])", "solve([])"],
        expect=[[2, 1, 1, -1], [-1, -1], []])

    add("topic-9-3", "Next greater on the right", "stack", ["nums", "stack", "ans", "i"],
        "For each index, return the next strictly greater value on its right, or -1.",
        "The stack stays decreasing. A bigger value resolves every smaller index waiting on top.",
        ["Pop indexes smaller than the current value.", "Store the current value as their answer.", "Push this index."],
        "Monotonic decreasing stack.",
        """
        def solve(nums):
            ans = []
            i = 0
            while i < len(nums):
                ans.append(-1)
                i = i + 1
            stack = []
            i = 0
            while i < len(nums):
                while stack and nums[stack[-1]] < nums[i]:
                    ans[stack.pop()] = nums[i]
                stack.append(i)
                i = i + 1
            return ans
        """,
        ["solve([2, 1, 3])", "solve([3, 2, 1])", "solve([1])"],
        expect=[[3, 3, -1], [-1, -1, -1], [-1]])

    add("topic-9-4", "Postfix evaluation", "stack", ["tokens", "stack", "b", "a"],
        "tokens are integers or '+', '-', '*'. Evaluate the postfix expression.",
        "Postfix keeps operands on a stack. An operator pops two values, computes, and pushes one result back.",
        ["Push numbers.", "On an operator, pop the right operand then the left.", "Push the result. The last value is the output."],
        "Stack-based postfix eval.",
        """
        def solve(tokens):
            stack = []
            for tok in tokens:
                if tok == "+" or tok == "-" or tok == "*":
                    b = stack.pop()
                    a = stack.pop()
                    if tok == "+":
                        stack.append(a + b)
                    elif tok == "-":
                        stack.append(a - b)
                    else:
                        stack.append(a * b)
                else:
                    stack.append(tok)
            return stack[-1]
        """,
        ["solve([2, 1, '+', 3, '*'])", "solve([5])", "solve([8, 3, '-'])"],
        expect=[9, 5, 5])

    add("topic-9-5", "Queue log", "queue", ["q", "op", "out"],
        "ops are ['push', x], ['pop'], or ['peek']. The queue pops from the front. Return pop and peek results. Empty produces None.",
        "A queue stores items in arrival order. Index 0 is the front. Push goes to the back. Pop leaves from the front.",
        ["Push appends.", "Pop removes index 0.", "Peek reads index 0."],
        "Use a list. pop(0) is the front.",
        """
        def solve(ops):
            q = []
            out = []
            for op in ops:
                if op[0] == "push":
                    q.append(op[1])
                elif op[0] == "pop":
                    if q:
                        out.append(q.pop(0))
                    else:
                        out.append(None)
                else:
                    if q:
                        out.append(q[0])
                    else:
                        out.append(None)
            return out
        """,
        ["solve([['push', 1], ['push', 2], ['peek'], ['pop'], ['pop']])", "solve([['pop']])", "solve([])"],
        expect=[[1, 1, 2], [None], []])

    add("topic-9-6", "Circular buffer", "queue", ["buf", "head", "size", "op"],
        "Capacity is 3. ops are ['push', x] or ['pop']. Push into a full buffer is ignored. Pop from empty returns None and is recorded. Return the list of popped values.",
        "A circular queue reuses a fixed list. head is the front slot. size is how many items are stored. The next free slot is (head + size) modulo capacity.",
        ["Push writes at (head + size) % 3 when size < 3.", "Pop reads buf[head] and moves head.", "Record every pop."],
        "Fixed buffer of length 3.",
        """
        def solve(ops):
            cap = 3
            buf = [None, None, None]
            head = 0
            size = 0
            out = []
            for op in ops:
                if op[0] == "push":
                    if size < cap:
                        buf[(head + size) % cap] = op[1]
                        size = size + 1
                else:
                    if size == 0:
                        out.append(None)
                    else:
                        out.append(buf[head])
                        head = (head + 1) % cap
                        size = size - 1
            return out
        """,
        ["solve([['push', 1], ['push', 2], ['push', 3], ['push', 4], ['pop'], ['pop'], ['push', 5], ['pop'], ['pop']])", "solve([['pop']])", "solve([])"],
        expect=[[1, 2, 3, 5], [None], []])

    add("topic-9-7", "Deque log", "queue", ["dq", "op", "out"],
        "ops are pushL, pushR, popL, popR, each as [name] or [name, x]. Return values from the pops. Empty pops return None.",
        "A deque can grow or shrink at either end. The list's two ends are the two doors.",
        ["pushL inserts at index 0. pushR appends.", "popL removes index 0. popR removes the last item.", "Record pops."],
        "List used at both ends.",
        """
        def solve(ops):
            dq = []
            out = []
            for op in ops:
                if op[0] == "pushL":
                    dq.insert(0, op[1])
                elif op[0] == "pushR":
                    dq.append(op[1])
                elif op[0] == "popL":
                    if dq:
                        out.append(dq.pop(0))
                    else:
                        out.append(None)
                else:
                    if dq:
                        out.append(dq.pop())
                    else:
                        out.append(None)
            return out
        """,
        ["solve([['pushR', 1], ['pushL', 2], ['popR'], ['popL'], ['popL']])", "solve([['popR']])", "solve([])"],
        expect=[[1, 2, None], [None], []])

    add("topic-9-8", "Highest first", "array", ["heap", "x", "out"],
        "Push every value, then pop k times. Return the popped values. The largest value leaves first.",
        "A priority queue stores items so the extreme value is at the front. Python's heap is a min-heap, so storing negatives makes the largest value come out first.",
        ["Push -value onto a min-heap.", "Pop k times.", "Negate again to restore the original values."],
        "heapq with negated values.",
        """
        def solve(nums, k):
            import heapq
            heap = []
            for x in nums:
                heapq.heappush(heap, -x)
            out = []
            while len(out) < k and heap:
                out.append(-heapq.heappop(heap))
            return out
        """,
        ["solve([3, 1, 4], 2)", "solve([5], 1)", "solve([1, 2], 0)"],
        expect=[[4, 3], [5], []])

    add("topic-9-9", "Window maximum", "queue", ["nums", "k", "dq", "i", "out"],
        "Return the maximum of every contiguous window of length k.",
        "A monotonic deque stores indexes in decreasing value order. The front is the maximum of the current window. Indexes that fall out of the window are dropped.",
        ["Pop indexes that left the window.", "Pop indexes whose values are smaller than the new value.", "The front index holds the window maximum."],
        "Decreasing deque of indexes.",
        """
        def solve(nums, k):
            dq = []
            out = []
            i = 0
            while i < len(nums):
                while dq and dq[0] <= i - k:
                    dq.pop(0)
                while dq and nums[dq[-1]] <= nums[i]:
                    dq.pop()
                dq.append(i)
                if i >= k - 1:
                    out.append(nums[dq[0]])
                i = i + 1
            return out
        """,
        ["solve([1, 3, -1, -3, 5], 3)", "solve([4], 1)", "solve([1, 2], 2)"],
        expect=[[3, 3, 5], [4], [2]])
