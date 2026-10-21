"""Sections 5.10–6.15."""


def register(add):
    add("topic-5-10", "Both diagonals", "matrix", ["grid", "main", "anti", "i"],
        "grid is square. Return [main diagonal, anti-diagonal], each as a list from the top row downward.",
        "A 2D array is a list of rows. The main diagonal is the cells where row and column indexes match.",
        ["Read grid[i][i] into the main diagonal.", "Read grid[i][n - 1 - i] into the anti-diagonal.", "Return both lists."],
        "Walk i from 0 to n - 1.",
        """
        def solve(grid):
            main = []
            anti = []
            i = 0
            n = len(grid)
            while i < n:
                main.append(grid[i][i])
                anti.append(grid[i][n - 1 - i])
                i = i + 1
            return [main, anti]
        """,
        ["solve([[1, 2], [3, 4]])", "solve([[5]])", "solve([[1, 2, 3], [4, 5, 6], [7, 8, 9]])"],
        expect=[[[1, 4], [2, 3]], [[5], [5]], [[1, 5, 9], [3, 5, 7]]])

    add("topic-5-11", "Column by column", "matrix", ["grid", "out", "c", "r"],
        "Return the matrix values in column-major order: finish a column before the next.",
        "Traversal is the order of reads. Column-major holds the column index still and walks the rows.",
        ["Start at column 0.", "Walk every row in that column.", "Move to the next column."],
        "For each column, for each row, append grid[r][c].",
        """
        def solve(grid):
            out = []
            if not grid or not grid[0]:
                return out
            c = 0
            while c < len(grid[0]):
                r = 0
                while r < len(grid):
                    out.append(grid[r][c])
                    r = r + 1
                c = c + 1
            return out
        """,
        ["solve([[1, 2, 3], [4, 5, 6]])", "solve([[7]])", "solve([[]])"],
        expect=[[1, 4, 2, 5, 3, 6], [7], []])

    add("topic-5-12", "Spiral order", "matrix", ["grid", "out", "top", "bottom", "left", "right"],
        "Return the matrix values in clockwise spiral order.",
        "Four edges of a shrinking rectangle are stored as top, bottom, left, and right. Each pass peels one layer.",
        ["Read the top row left to right.", "Read the right column, then the bottom row, then the left column.", "Shrink the bounds and repeat."],
        "Peel the rectangle one side at a time.",
        """
        def solve(grid):
            out = []
            if not grid or not grid[0]:
                return out
            top = 0
            bottom = len(grid) - 1
            left = 0
            right = len(grid[0]) - 1
            while top <= bottom and left <= right:
                c = left
                while c <= right:
                    out.append(grid[top][c])
                    c = c + 1
                top = top + 1
                r = top
                while r <= bottom and top <= bottom + 1 and left <= right:
                    out.append(grid[r][right])
                    r = r + 1
                right = right - 1
                if top <= bottom:
                    c = right
                    while c >= left:
                        out.append(grid[bottom][c])
                        c = c - 1
                    bottom = bottom - 1
                if left <= right:
                    r = bottom
                    while r >= top:
                        out.append(grid[r][left])
                        r = r - 1
                    left = left + 1
            return out
        """,
        ["solve([[1, 2, 3], [4, 5, 6], [7, 8, 9]])", "solve([[1, 2], [3, 4]])", "solve([[8]])"],
        expect=[[1, 2, 3, 6, 9, 8, 7, 4, 5], [1, 2, 4, 3], [8]])

    add("topic-5-13", "Subarrays with sum", "array", ["nums", "target", "i", "j", "total", "count"],
        "Return how many contiguous subarrays add up to target.",
        "A subarray is a contiguous slice. Two indices i and j mark its ends, and total is the sum stored for that slice.",
        ["Choose the start i.", "Extend j and add nums[j].", "Count the slice when total equals target."],
        "Check every i..j slice.",
        """
        def solve(nums, target):
            count = 0
            i = 0
            while i < len(nums):
                total = 0
                j = i
                while j < len(nums):
                    total = total + nums[j]
                    if total == target:
                        count = count + 1
                    j = j + 1
                i = i + 1
            return count
        """,
        ["solve([1, 2, 3], 3)", "solve([1, 1, 1], 2)", "solve([], 0)"],
        expect=[2, 2, 0])

    add("topic-5-14", "All non-empty subsequences", "recursion", ["nums", "path", "out"],
        "Return every non-empty subsequence. A subsequence keeps relative order but may skip items. Include an item before you try skipping it.",
        "A subsequence choice is a branch in the call stack: take the item, or skip it. path is the subsequence stored so far.",
        ["At the end of the list, save a copy of path if it is not empty.", "First try including nums[i].", "Then try skipping it."],
        "Backtrack through include and skip.",
        """
        def solve(nums):
            out = []
            path = []

            def walk(i):
                if i == len(nums):
                    if path:
                        out.append(path[:])
                    return
                path.append(nums[i])
                walk(i + 1)
                path.pop()
                walk(i + 1)

            walk(0)
            return out
        """,
        ["solve([1, 2])", "solve([7])", "solve([])"],
        expect=[[[1, 2], [1], [2]], [[7]], []])

    add("topic-6-1", "Linear search", "array", ["nums", "target", "i"],
        "Return the index of the first target, or -1.",
        "Linear search reads one slot at a time, from index 0 upward, until the value matches or the row ends.",
        ["Compare nums[i] with target.", "Move i forward on a miss.", "Return i or -1."],
        "Scan from the left.",
        """
        def solve(nums, target):
            i = 0
            while i < len(nums):
                if nums[i] == target:
                    return i
                i = i + 1
            return -1
        """,
        ["solve([4, 1, 7, 1], 1)", "solve([4, 1, 7], 9)", "solve([], 0)"],
        expect=[1, -1, -1])

    add("topic-6-2", "Binary search", "array", ["nums", "target", "lo", "hi", "mid"],
        "nums is sorted ascending. Return the index of target, or -1.",
        "Binary search throws away half the row. lo and hi are the edges of the part still stored as possible.",
        ["Look at the middle.", "If it is too small, move lo to mid + 1.", "If it is too large, move hi to mid - 1."],
        "Standard binary search.",
        """
        def solve(nums, target):
            lo = 0
            hi = len(nums) - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if nums[mid] == target:
                    return mid
                if nums[mid] < target:
                    lo = mid + 1
                else:
                    hi = mid - 1
            return -1
        """,
        ["solve([1, 3, 5, 7, 9], 7)", "solve([1, 3, 5], 4)", "solve([], 1)"],
        expect=[3, -1, -1])

    add("topic-6-3", "Ternary peak", "array", ["nums", "lo", "hi", "m1", "m2"],
        "nums rises and then falls (it may be strictly increasing or strictly decreasing). Return the index of the maximum value.",
        "Ternary search compares two interior points and drops the third that cannot hold the peak.",
        ["Place m1 and m2 one third and two thirds along the range.", "Keep the side with the larger value.", "When the range is tiny, return the higher end."],
        "Shrink lo and hi using two mid points.",
        """
        def solve(nums):
            lo = 0
            hi = len(nums) - 1
            while lo < hi:
                m1 = lo + (hi - lo) // 3
                m2 = hi - (hi - lo) // 3
                if nums[m1] < nums[m2]:
                    lo = m1 + 1
                else:
                    hi = m2 - 1
            return lo
        """,
        ["solve([1, 3, 8, 4, 2])", "solve([1, 2, 3])", "solve([5])"],
        expect=[2, 2, 0])

    add("topic-6-4", "Exponential search", "array", ["nums", "target", "bound", "lo", "hi", "mid"],
        "nums is sorted. Find target by doubling an index until you pass it, then binary search that window. Return the index or -1.",
        "Exponential search stores a growing bound. Once the bound passes the target, only that window is searched.",
        ["Double bound while nums[bound] is still below the target.", "Binary search from bound/2 through bound.", "Return the index or -1."],
        "Grow the bound, then binary search.",
        """
        def solve(nums, target):
            if not nums:
                return -1
            if nums[0] == target:
                return 0
            bound = 1
            while bound < len(nums) and nums[bound] < target:
                bound = bound * 2
            lo = bound // 2
            if bound < len(nums):
                hi = bound
            else:
                hi = len(nums) - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if nums[mid] == target:
                    return mid
                if nums[mid] < target:
                    lo = mid + 1
                else:
                    hi = mid - 1
            return -1
        """,
        ["solve([1, 3, 5, 7, 9], 7)", "solve([1, 3, 5, 7, 9], 1)", "solve([1, 3, 5], 4)"],
        expect=[3, 0, -1])

    add("topic-6-5", "Bubble sort", "bars", ["a", "i", "j"],
        "Return the list sorted ascending. Swap neighbors that are out of order.",
        "Bubble sort walks adjacent memory slots. A swap writes each value into the other's slot.",
        ["Compare a[j] and a[j + 1].", "Swap them when the left one is larger.", "Repeat until the largest values have bubbled to the end."],
        "Swap neighbors while scanning.",
        """
        def solve(a):
            a = list(a)
            i = 0
            while i < len(a):
                j = 0
                while j < len(a) - 1 - i:
                    if a[j] > a[j + 1]:
                        tmp = a[j]
                        a[j] = a[j + 1]
                        a[j + 1] = tmp
                    j = j + 1
                i = i + 1
            return a
        """,
        ["solve([3, 1, 2])", "solve([1])", "solve([])"],
        expect=[[1, 2, 3], [1], []])

    add("topic-6-6", "Selection sort", "bars", ["a", "i", "j", "min_idx"],
        "Return the list sorted ascending by repeatedly selecting the minimum of the unsorted suffix.",
        "Selection sort stores the index of the smallest remaining value, then swaps it into the next output slot.",
        ["Find min_idx from i to the end.", "Swap it with i.", "Move i forward."],
        "Select the minimum of the unsorted part.",
        """
        def solve(a):
            a = list(a)
            i = 0
            while i < len(a):
                min_idx = i
                j = i + 1
                while j < len(a):
                    if a[j] < a[min_idx]:
                        min_idx = j
                    j = j + 1
                tmp = a[i]
                a[i] = a[min_idx]
                a[min_idx] = tmp
                i = i + 1
            return a
        """,
        ["solve([4, 1, 3, 2])", "solve([2, 1])", "solve([])"],
        expect=[[1, 2, 3, 4], [1, 2], []])

    add("topic-6-7", "Insertion sort", "bars", ["a", "i", "j", "key"],
        "Return the list sorted ascending. Insert each next value into the sorted prefix.",
        "Insertion sort keeps a sorted prefix in memory. key is the value being slid left until it reaches its slot.",
        ["Pick the next key.", "Shift larger prefix items one slot right.", "Write key into the opened slot."],
        "Slide key left through the sorted prefix.",
        """
        def solve(a):
            a = list(a)
            i = 1
            while i < len(a):
                key = a[i]
                j = i - 1
                while j >= 0 and a[j] > key:
                    a[j + 1] = a[j]
                    j = j - 1
                a[j + 1] = key
                i = i + 1
            return a
        """,
        ["solve([3, 1, 4, 2])", "solve([1, 2])", "solve([])"],
        expect=[[1, 2, 3, 4], [1, 2], []])

    add("topic-6-8", "Merge sort", "bars", ["a", "mid", "i", "j"],
        "Return the list sorted ascending using merge sort.",
        "Merge sort splits the row, sorts each half in its own calls, then merges by always taking the smaller front item.",
        ["Split into left and right.", "Sort each half.", "Merge into a new row by taking the smaller head."],
        "Recursive split and merge.",
        """
        def solve(a):
            a = list(a)
            if len(a) <= 1:
                return a
            mid = len(a) // 2
            left = solve(a[:mid])
            right = solve(a[mid:])
            i = 0
            j = 0
            out = []
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    out.append(left[i])
                    i = i + 1
                else:
                    out.append(right[j])
                    j = j + 1
            while i < len(left):
                out.append(left[i])
                i = i + 1
            while j < len(right):
                out.append(right[j])
                j = j + 1
            return out
        """,
        ["solve([5, 1, 4, 2])", "solve([1])", "solve([])"],
        expect=[[1, 2, 4, 5], [1], []])

    add("topic-6-9", "Quick sort", "bars", ["a", "pivot", "i", "j"],
        "Return the list sorted ascending using quick sort. Pivot is the last item.",
        "Quick sort partitions memory around a pivot. Items smaller than the pivot move to its left.",
        ["Choose the last item as the pivot.", "Swap smaller items toward the front.", "Sort the two sides."],
        "Lomuto partition around the last item.",
        """
        def solve(a):
            a = list(a)

            def sort(lo, hi):
                if lo >= hi:
                    return
                pivot = a[hi]
                i = lo
                j = lo
                while j < hi:
                    if a[j] < pivot:
                        tmp = a[i]
                        a[i] = a[j]
                        a[j] = tmp
                        i = i + 1
                    j = j + 1
                tmp = a[i]
                a[i] = a[hi]
                a[hi] = tmp
                sort(lo, i - 1)
                sort(i + 1, hi)

            sort(0, len(a) - 1)
            return a
        """,
        ["solve([3, 1, 4, 2])", "solve([1])", "solve([])"],
        expect=[[1, 2, 3, 4], [1], []])

    add("topic-6-10", "Heap sort", "bars", ["a", "i", "largest"],
        "Return the list sorted ascending using heap sort.",
        "A heap stores the largest item at index 0. Heap sort swaps that item to the end, then repairs the heap.",
        ["Build a max heap.", "Swap the root to the end of the unsorted prefix.", "Sift the new root down."],
        "Max-heap then extract.",
        """
        def solve(a):
            a = list(a)

            def sift(n, i):
                while True:
                    largest = i
                    left = 2 * i + 1
                    right = 2 * i + 2
                    if left < n and a[left] > a[largest]:
                        largest = left
                    if right < n and a[right] > a[largest]:
                        largest = right
                    if largest == i:
                        return
                    tmp = a[i]
                    a[i] = a[largest]
                    a[largest] = tmp
                    i = largest

            n = len(a)
            i = n // 2 - 1
            while i >= 0:
                sift(n, i)
                i = i - 1
            end = n - 1
            while end > 0:
                tmp = a[0]
                a[0] = a[end]
                a[end] = tmp
                sift(end, 0)
                end = end - 1
            return a
        """,
        ["solve([4, 1, 3, 2])", "solve([2, 1])", "solve([])"],
        expect=[[1, 2, 3, 4], [1, 2], []])

    add("topic-6-11", "Counting sort", "array", ["a", "count", "out", "x"],
        "Values are integers from 0 to 9. Return them sorted ascending using counting sort.",
        "Counting sort stores a tally per value, not a comparison. The tally list is the memory of how many times each value appeared.",
        ["Add 1 in count[value].", "Walk the counts from 0 to 9.", "Append that value once per tally."],
        "Count, then write values in order.",
        """
        def solve(a):
            count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for x in a:
                count[x] = count[x] + 1
            out = []
            x = 0
            while x <= 9:
                k = 0
                while k < count[x]:
                    out.append(x)
                    k = k + 1
                x = x + 1
            return out
        """,
        ["solve([3, 1, 3, 0])", "solve([])", "solve([9, 1])"],
        expect=[[0, 1, 3, 3], [], [1, 9]])

    add("topic-6-12", "Radix sort", "array", ["a", "exp", "buckets", "out"],
        "Non-negative integers. Return them sorted with LSD radix sort, one decimal digit at a time.",
        "Radix sort buckets numbers by one digit, then by the next. Each bucket is a list in memory. Stable collection keeps earlier digits in order.",
        ["Bucket by the current digit.", "Collect the buckets from 0 to 9.", "Move to the next digit."],
        "LSD radix sort in base 10.",
        """
        def solve(a):
            a = list(a)
            if not a:
                return a
            exp = 1
            max_v = a[0]
            for x in a:
                if x > max_v:
                    max_v = x
            while max_v // exp > 0:
                buckets = [[], [], [], [], [], [], [], [], [], []]
                for x in a:
                    digit = (x // exp) % 10
                    buckets[digit].append(x)
                out = []
                for bucket in buckets:
                    for x in bucket:
                        out.append(x)
                a = out
                exp = exp * 10
            return a
        """,
        ["solve([170, 45, 75, 90, 2])", "solve([3])", "solve([])"],
        expect=[[2, 45, 75, 90, 170], [3], []])

    add("topic-6-13", "Bucket sort", "bars", ["a", "buckets", "b", "x"],
        "Values are integers from 0 through 9. Scatter them into 10 buckets, sort each bucket, and concatenate.",
        "Bucket sort chooses a bucket from the value, so nearby values share a list. Concatenating the buckets is the output.",
        ["Append each value to buckets[value].", "Insertion-sort each bucket.", "Join the buckets."],
        "One bucket per digit 0..9.",
        """
        def solve(a):
            buckets = []
            b = 0
            while b < 10:
                buckets.append([])
                b = b + 1
            for x in a:
                buckets[x].append(x)
            out = []
            for bucket in buckets:
                i = 1
                while i < len(bucket):
                    key = bucket[i]
                    j = i - 1
                    while j >= 0 and bucket[j] > key:
                        bucket[j + 1] = bucket[j]
                        j = j - 1
                    bucket[j + 1] = key
                    i = i + 1
                for x in bucket:
                    out.append(x)
            return out
        """,
        ["solve([4, 1, 4, 2])", "solve([0])", "solve([])"],
        expect=[[1, 2, 4, 4], [0], []])

    add("topic-6-14", "Stable by key", "array", ["a", "i", "j", "key"],
        "pairs are [number, label]. Sort them by number ascending, and keep the original order when numbers tie. Return the sorted pairs.",
        "A stable sort does not reorder equal keys. Insertion sort only shifts a strictly greater key, so equal keys stay in the order they were stored.",
        ["Take the next pair as key.", "Shift pairs with a larger number.", "Write key back. Equal numbers are not moved past it."],
        "Stable insertion sort on pair[0].",
        """
        def solve(pairs):
            a = []
            for pair in pairs:
                a.append(pair[:])
            i = 1
            while i < len(a):
                key = a[i]
                j = i - 1
                while j >= 0 and a[j][0] > key[0]:
                    a[j + 1] = a[j]
                    j = j - 1
                a[j + 1] = key
                i = i + 1
            return a
        """,
        ["solve([[2, 'a'], [1, 'b'], [2, 'c']])", "solve([[1, 'z']])", "solve([])"],
        expect=[[[1, "b"], [2, "a"], [2, "c"]], [[1, "z"]], []])

    add("topic-6-15", "Count inversions", "array", ["arr", "inv", "i", "j"],
        "Return how many pairs i < j have arr[i] > arr[j]. Count them while merging sorted halves.",
        "An inversion is a pair stored out of order. During a merge, when the right half is taken first, every remaining left item forms an inversion with it.",
        ["Sort the two halves.", "When you take from the right, add the number of items still on the left.", "Return the total."],
        "Merge-sort inversion count.",
        """
        def solve(nums):
            arr = list(nums)

            def sort_count(left, right):
                if right - left <= 1:
                    return 0
                mid = (left + right) // 2
                inv = sort_count(left, mid) + sort_count(mid, right)
                merged = []
                i = left
                j = mid
                while i < mid and j < right:
                    if arr[i] <= arr[j]:
                        merged.append(arr[i])
                        i = i + 1
                    else:
                        merged.append(arr[j])
                        inv = inv + (mid - i)
                        j = j + 1
                while i < mid:
                    merged.append(arr[i])
                    i = i + 1
                while j < right:
                    merged.append(arr[j])
                    j = j + 1
                k = 0
                while k < len(merged):
                    arr[left + k] = merged[k]
                    k = k + 1
                return inv

            return sort_count(0, len(arr))
        """,
        ["solve([2, 4, 1, 3, 5])", "solve([1, 2, 3])", "solve([3, 2, 1])"],
        expect=[3, 0, 3])
