/* Visual Lab for the DSA Master Course.
   Roadmap + one problem per topic.
   Your run and the solution run side by side: flow, memory, and output.
*/
(function () {
  "use strict";

  if (typeof module !== "undefined" && module.exports && typeof document === "undefined") {
    module.exports = { changedPairs, narration, sourceLine, nextFact, whyLine, errorHint, stdoutAt, clampIndex, layoutKind, stepStats, deriveEvents, describeEvents, trackListIds, motionMs, loopRoles, itemCursor, subscripts, walkFor, indexSpan };
    return;
  }

  const STORE_KEY = "dsa-visual-lab-v1";
  const REVEAL_KEY = "dsa-visual-lab-reveal";
  const UI_KEY = "dsa-visual-lab-ui";
  const PYODIDE_BASE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
  const RATES = { 0.5: 1040, 1: 520, 1.5: 340, 2: 260 };

  const VIZ_INTRO = {
    array: "Each cell is one memory slot. The number above it is the index. Arrows are variables that remember a position.",
    "two-pointer": "Two index variables walk the same array. Watch which end moves, and why the sum or the window changes.",
    window: "A window is a slice of the array remembered by a start and an end index. It grows or shrinks one step at a time.",
    bars: "Bar height is the value stored at that index. A swap is two bars exchanging the values in those memory slots.",
    string: "A string is a row of characters. An index variable points at the character the step is reading.",
    hash: "A hash table stores key → value. A lookup jumps to the slot for that key instead of scanning every item.",
    stack: "A stack stores items vertically. Push adds on top. Pop removes the top item. Only the top is touched.",
    queue: "A queue stores items in a line. New items join the back. The front item leaves first.",
    linked: "Each node is a small object in memory: a value, and a link to the next node. Arrows are those links.",
    tree: "Each node stores a value plus links to its left and right child. The call walks those links.",
    graph: "Circles are nodes. Lines are edges. Highlighted nodes are the ones the algorithm has already stored as seen.",
    dp: "The table stores answers to smaller questions. A later cell is filled from cells that were already stored.",
    matrix: "A matrix is memory in rows and columns. The highlighted cell is the one this step reads or writes.",
    bits: "Each number is a row of bits. 1 means that bit is on. Bitwise steps flip, shift, or combine those bits.",
    recursion: "Every call gets its own memory frame. The frames stack up, then collapse as each call returns.",
    flow: "Follow the order of steps. Memory on the right of each step is what the function has stored so far.",
  };

  const POINTER_NAMES = new Set([
    "i", "j", "k", "ii", "jj", "left", "right", "mid", "lo", "hi", "low", "high",
    "start", "end", "slow", "fast", "idx", "index", "p", "u", "v", "row", "col",
    "write", "read", "l", "r", "pos", "min_idx", "max_idx", "best", "gap",
  ]);

  const TRACER = `
import sys, io, json

def _finite_float(v):
    if v != v:
        return "nan"
    if v == float("inf") or v == float("-inf"):
        return str(v)
    return v

def _freeze(v, depth, ids):
    if v is None:
        return {"t": "none", "v": None}
    if isinstance(v, bool):
        return {"t": "bool", "v": True if v else False}
    if isinstance(v, int) and not isinstance(v, bool):
        if abs(v) > 10 ** 12:
            return {"t": "int", "v": str(v)}
        return {"t": "int", "v": int(v)}
    if isinstance(v, float):
        fv = _finite_float(v)
        if isinstance(fv, float):
            return {"t": "float", "v": fv}
        return {"t": "float", "v": fv}
    if isinstance(v, str):
        return {"t": "str", "v": v[:180]}
    if isinstance(v, (list, tuple, dict, set)):
        if id(v) in ids:
            return {"t": "alias", "id": ids[id(v)]}
        if depth > 5:
            return {"t": "obj", "v": "..."}
        ids[id(v)] = len(ids) + 1
        my = ids[id(v)]
        if isinstance(v, list):
            return {"t": "list", "id": my, "v": [_freeze(x, depth + 1, ids) for x in v[:40]]}
        if isinstance(v, tuple):
            return {"t": "tuple", "id": my, "v": [_freeze(x, depth + 1, ids) for x in v[:40]]}
        if isinstance(v, set):
            try:
                items = sorted(list(v), key=lambda x: repr(x))[:24]
            except Exception:
                items = list(v)[:24]
            return {"t": "set", "id": my, "v": [_freeze(x, depth + 1, ids) for x in items]}
        items = list(v.items())[:24]
        return {"t": "dict", "id": my, "v": [[_freeze(k, depth + 1, ids), _freeze(val, depth + 1, ids)] for k, val in items]}
    if type(v).__name__ == "deque":
        if id(v) in ids:
            return {"t": "alias", "id": ids[id(v)]}
        if depth > 5:
            return {"t": "obj", "v": "..."}
        ids[id(v)] = len(ids) + 1
        my = ids[id(v)]
        return {"t": "list", "id": my, "v": [_freeze(x, depth + 1, ids) for x in list(v)[:40]]}
    raw = getattr(v, "__dict__", None)
    if isinstance(raw, dict) and "value" in raw and ("next" in raw or "left" in raw or "right" in raw):
        if id(v) in ids:
            return {"t": "alias", "id": ids[id(v)]}
        if depth > 5:
            return {"t": "obj", "v": "..."}
        ids[id(v)] = len(ids) + 1
        my = ids[id(v)]
        pairs = [[{"t": "str", "v": "val"}, _freeze(raw.get("value"), depth + 1, ids)]]
        if "left" in raw or "right" in raw:
            pairs.append([{"t": "str", "v": "left"}, _freeze(raw.get("left"), depth + 1, ids)])
            pairs.append([{"t": "str", "v": "right"}, _freeze(raw.get("right"), depth + 1, ids)])
        else:
            pairs.append([{"t": "str", "v": "next"}, _freeze(raw.get("next"), depth + 1, ids)])
        return {"t": "dict", "id": my, "v": pairs}
    return {"t": "obj", "v": repr(v)[:100]}

def _locals_of(frame, ids):
    import types
    out = {}
    for k, v in frame.f_locals.items():
        if k.startswith("__"):
            continue
        if isinstance(v, (types.FunctionType, types.ModuleType, type)):
            continue
        try:
            out[k] = _freeze(v, 0, ids)
        except Exception:
            out[k] = {"t": "obj", "v": "?"}
    return out

def _stack(frame):
    frames = []
    f = frame
    while f is not None:
        if f.f_code.co_filename == "<student>":
            frames.append(f)
        f = f.f_back
    frames.reverse()
    return frames

def _line_no(frame):
    return frame.f_lineno or frame.f_code.co_firstlineno

def _snapshot(frame, event, arg, buf):
    ids = {}
    stack = []
    for f in _stack(frame):
        stack.append({
            "fn": f.f_code.co_name,
            "line": _line_no(f),
            "locals": _locals_of(f, ids),
        })
    ret = None
    if event == "return":
        try:
            ret = _freeze(arg, 0, ids)
        except Exception:
            ret = {"t": "obj", "v": "?"}
    top = stack[-1]["fn"] if stack else ""
    final = event == "return" and len(stack) == 1 and top in ("solve", "<module>")
    return {
        "e": event,
        "fn": frame.f_code.co_name,
        "line": _line_no(frame),
        "ret": ret,
        "final": final,
        "out_n": len(buf.getvalue()),
        "stack": stack,
    }

def run_plain(source, call_expr):
    try:
        ns = {}
        exec(compile(source, "<student>", "exec"), ns, ns)
        if "solve" not in ns or not callable(ns.get("solve")):
            return json.dumps({"error": "Define a function named solve. The lab calls solve(...) for you.", "result_repr": None, "stdout": ""})
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            result = eval(compile(call_expr, "<student-call>", "eval"), ns, ns)
            return json.dumps({"error": None, "result_repr": repr(result), "stdout": buf.getvalue()[:2000]})
        finally:
            sys.stdout = old
    except Exception as ex:
        return json.dumps({"error": type(ex).__name__ + ": " + str(ex), "result_repr": None, "stdout": ""})

def run_traced(source, call_expr):
    frames_out = []
    buf = io.StringIO()
    try:
        code = compile(source, "<student>", "exec")
    except SyntaxError as ex:
        return json.dumps({"error": "SyntaxError: " + str(ex), "frames": [], "result_repr": None, "stdout": "", "error_line": ex.lineno or 0})
    ns = {}
    try:
        exec(code, ns, ns)
    except Exception as ex:
        return json.dumps({"error": type(ex).__name__ + ": " + str(ex), "frames": [], "result_repr": None, "stdout": ""})
    if "solve" not in ns or not callable(ns.get("solve")):
        return json.dumps({"error": "Define a function named solve. The lab calls solve(...) for you.", "frames": [], "result_repr": None, "stdout": ""})

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<student>":
            return None
        if event not in ("line", "call", "return"):
            return tracer
        if len(frames_out) >= 650:
            raise RuntimeError("Stopped after 650 steps. This usually means an infinite loop, or the input is too big for a step-by-step picture.")
        frames_out.append(_snapshot(frame, event, arg, buf))
        return tracer

    old = sys.stdout
    sys.stdout = buf
    err = None
    result_repr = None
    try:
        sys.settrace(tracer)
        result = eval(compile(call_expr, "<student-call>", "eval"), ns, ns)
        result_repr = repr(result)
    except Exception as ex:
        err = type(ex).__name__ + ": " + str(ex)
    finally:
        sys.settrace(None)
        sys.stdout = old
    stdout = buf.getvalue()
    if len(stdout) > 4000:
        stdout = stdout[:4000] + "\\n… output truncated"
    return json.dumps({
        "error": err,
        "frames": frames_out,
        "result_repr": result_repr,
        "stdout": stdout,
    })

def run_script(source, _unused=None):
    frames_out = []
    buf = io.StringIO()
    try:
        code = compile(source, "<student>", "exec")
    except SyntaxError as ex:
        return json.dumps({"error": "SyntaxError: " + str(ex), "frames": [], "result_repr": None, "stdout": "", "script": True, "error_line": ex.lineno or 0})
    ns = {}

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<student>":
            return None
        if event not in ("line", "call", "return"):
            return tracer
        if len(frames_out) >= 650:
            raise RuntimeError("Stopped after 650 steps. A loop kept going, so the picture stopped.")
        frames_out.append(_snapshot(frame, event, arg, buf))
        return tracer

    old = sys.stdout
    sys.stdout = buf
    err = None
    try:
        sys.settrace(tracer)
        exec(code, ns, ns)
    except Exception as ex:
        err = type(ex).__name__ + ": " + str(ex)
    finally:
        sys.settrace(None)
        sys.stdout = old
    stdout = buf.getvalue()
    if len(stdout) > 4000:
        stdout = stdout[:4000] + "\\n… output truncated"
    shown = stdout.strip() if stdout.strip() else "None"
    return json.dumps({
        "error": err,
        "frames": frames_out,
        "result_repr": shown,
        "stdout": stdout,
        "script": True,
    })
`;

  const state = {
    open: false,
    view: "map",
    topicId: null,
    testIndex: 0,
    reveal: false,
    rate: 1,
    fontSize: 15,
    pickQuery: "",
    pickStatus: "all",
    playing: null,
    runToken: 0,
    you: emptyTrace(),
    sol: emptyTrace(),
    tests: [],
    timer: null,
    free: false,
    blank: false,
    lens: "you",
  };

  let activeIds = {};
  let motionToken = 0;
  let motions = [];
  const wireAt = new Map();

  const FREE_CODE = `nums = [4, 1, 7]
total = 0
for x in nums:
    total = total + x
print("The total is", total)
`;

  const SAMPLE_CODE = {
    array: FREE_CODE,
    stack: `stack = []
stack.append("plate")
stack.append("cup")
top = stack.pop()
print(top, stack)
`,
    queue: `queue = []
queue.append("Ada")
queue.append("Bo")
first = queue.pop(0)
print(first, queue)
`,
    dict: `ages = {}
ages["Ada"] = 36
ages["Bo"] = 41
print(ages["Ada"])
`,
  };

  const ui = {};
  let pyodide = null;
  let pyodideLoading = null;
  let booted = false;

  function emptyTrace() {
    return { frames: [], i: 0, error: null, errorLine: 0, stdout: "", result: null, running: false, note: "" };
  }

  function loadStore() {
    try {
      const raw = JSON.parse(localStorage.getItem(STORE_KEY) || "{}");
      return { status: raw.status || {}, code: raw.code || {} };
    } catch (err) {
      return { status: {}, code: {} };
    }
  }

  function saveStore(store) {
    localStorage.setItem(STORE_KEY, JSON.stringify(store));
  }

  function problems() {
    return window.DSA_PROBLEMS || {};
  }

  function courseMap() {
    const nav = document.querySelector(".layout > nav > ul");
    if (!nav) return [];
    const sections = [];
    nav.querySelectorAll(":scope > li").forEach((li) => {
      const a = li.querySelector(":scope > a");
      if (!a) return;
      const topics = [];
      li.querySelectorAll(":scope > ul > li > a").forEach((link) => {
        const href = link.getAttribute("href") || "";
        if (!href.startsWith("#topic-")) return;
        topics.push({ id: href.slice(1), title: link.textContent.replace(/\s+/g, " ").trim() });
      });
      if (!topics.length) return;
      sections.push({
        id: (a.getAttribute("href") || "").replace("#", ""),
        title: a.textContent.replace(/\s+/g, " ").trim(),
        topics,
      });
    });
    return sections;
  }

  function topicMeta(id) {
    for (const section of courseMap()) {
      const topic = section.topics.find((t) => t.id === id);
      if (topic) return { section, topic };
    }
    return null;
  }

  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function pyFmt(node) {
    if (!node) return "?";
    switch (node.t) {
      case "none":
        return "None";
      case "bool":
        return node.v ? "True" : "False";
      case "int":
      case "float":
        return String(node.v);
      case "str":
        return "'" + String(node.v).replace(/\\/g, "\\\\").replace(/'/g, "\\'") + "'";
      case "list":
        return "[" + node.v.map(pyFmt).join(", ") + "]";
      case "tuple":
        return "(" + node.v.map(pyFmt).join(", ") + (node.v.length === 1 ? ",)" : ")");
      case "set":
        return "{" + (node.v.length ? node.v.map(pyFmt).join(", ") : "") + "}";
      case "dict":
        return "{" + node.v.map(([k, v]) => pyFmt(k) + ": " + pyFmt(v)).join(", ") + "}";
      case "alias":
        return "same object #" + node.id;
      default:
        return String(node.v);
    }
  }

  function compact(node) {
    const text = pyFmt(node);
    return text.length > 88 ? text.slice(0, 85) + "..." : text;
  }

  function dictGet(node, key) {
    if (!node || node.t !== "dict") return null;
    for (const pair of node.v) {
      if (pair[0] && pair[0].t === "str" && pair[0].v === key) return pair[1];
    }
    return null;
  }

  function isScalar(node) {
    return node && (node.t === "int" || node.t === "float" || node.t === "str" || node.t === "bool" || node.t === "none");
  }

  function isHeapItem(node) {
    if (isScalar(node)) return true;
    return !!(node && node.t === "tuple" && node.v.length && node.v.every(isScalar));
  }

  function isScalarList(node) {
    return node && (node.t === "list" || node.t === "tuple") && node.v.every(isScalar);
  }

  function isMatrix(node) {
    return node && node.t === "list" && node.v.length > 0 && node.v.every((row) => row.t === "list" && row.v.every(isScalar));
  }

  function topFrame(frame) {
    const stack = (frame && frame.stack) || [];
    return stack[stack.length - 1] || { fn: "", line: 0, locals: {} };
  }

  function localsOf(frame) {
    return topFrame(frame).locals || {};
  }

  function loopRoles(source) {
    const roles = {};
    String(source || "").split("\n").forEach((line) => {
      const match = /^\s*for\s+([A-Za-z_]\w*)\s+in\s+(.+?)\s*:\s*(?:#.*)?$/.exec(line);
      if (!match) return;
      const expr = match[2].trim();
      if (/^range\s*\(/.test(expr)) roles[match[1]] = { mode: "index", over: "" };
      else {
        const ident = /^([A-Za-z_]\w*)/.exec(expr);
        roles[match[1]] = { mode: "item", over: ident ? ident[1] : "" };
      }
    });
    return roles;
  }

  function itemCursor(frames, index, name) {
    const here = frames && frames[index];
    if (!here || !name) return -1;
    const fn = topFrame(here).fn;
    let count = -1;
    let last = "";
    for (let step = 0; step <= index; step += 1) {
      const frame = frames[step];
      if (!frame || topFrame(frame).fn !== fn) continue;
      const node = localsOf(frame)[name];
      if (!isScalar(node) || node.t === "none") continue;
      const key = JSON.stringify(node);
      if (key === last) continue;
      last = key;
      count += 1;
    }
    return count;
  }

  function sourceLine(source, lineNo) {
    const lines = String(source || "").split("\n");
    return lines[(lineNo || 1) - 1] || "";
  }

  function changedPairs(prevFrame, frame) {
    const now = localsOf(frame);
    const prev = prevFrame && topFrame(prevFrame).fn === topFrame(frame).fn ? localsOf(prevFrame) : {};
    const pairs = [];
    Object.keys(now).forEach((name) => {
      const before = prev[name] ? JSON.stringify(prev[name]) : null;
      const after = JSON.stringify(now[name]);
      if (before !== after) pairs.push([name, now[name], prev[name]]);
    });
    return pairs;
  }

  function shortValue(node) {
    const text = compact(node);
    return text.length > 28 ? text.slice(0, 26) + "…" : text;
  }

  function clampIndex(index, length) {
    if (!length) return 0;
    return Math.min(length - 1, Math.max(0, index));
  }

  function stdoutAt(stdout, outN) {
    return String(stdout || "").slice(0, outN || 0);
  }

  function whyLine(frame) {
    if (!frame) return "Run the program to record a step.";
    if (frame.e === "call" && frame.fn === "<module>") return "Python starts at the top of the file.";
    if (frame.e === "call") return "This step runs because " + frame.fn + " was called.";
    if (frame.e === "return") return "This step runs because " + frame.fn + " finished.";
    return "This step runs because the previous recorded step handed control to this line.";
  }

  function nextFact(trace, source) {
    if (!trace || !trace.frames) return "No steps are recorded.";
    const nxt = trace.frames[trace.i + 1];
    if (!nxt) return "This is the last recorded step.";
    const line = sourceLine(source, nxt.line).trim();
    if (nxt.e === "call" && nxt.fn !== "<module>") return "Next, Python enters " + nxt.fn + (line ? " at `" + line + "`." : ".");
    if (nxt.e === "return" && nxt.fn !== "<module>") return "Next, " + nxt.fn + " returns" + (nxt.ret ? " " + shortValue(nxt.ret) : "") + ".";
    return line ? "Next line: `" + line + "`." : "Next, Python moves to line " + nxt.line + ".";
  }

  function errorHint(error) {
    const text = String(error || "");
    if (text.startsWith("SyntaxError")) return "Python could not read this line. Check quotes, colons, and parentheses.";
    if (text.startsWith("IndentationError")) return "The spaces at the start of this line do not match the block above it.";
    if (text.startsWith("NameError")) return "This name is not stored yet. Define it on an earlier line, or check the spelling.";
    if (text.startsWith("TypeError")) return "This operation does not match the kind of value stored. Open Variables to see the types.";
    if (text.startsWith("IndexError") || text.startsWith("KeyError")) return "The program asked for a position or key that is not in that collection.";
    if (text.startsWith("ZeroDivisionError")) return "A number was divided by zero.";
    if (text.startsWith("RecursionError")) return "A function kept calling itself until Python stopped the run.";
    if (text.indexOf("650 steps") >= 0) return "The picture stopped at 650 steps so the page stays responsive. Use a shorter loop or a smaller input.";
    return "";
  }

  function layoutKind(frame) {
    if (!frame) return "simple";
    const locals = localsOf(frame);
    const calls = (frame.stack || []).filter((item) => item.fn && item.fn !== "<module>");
    if (calls.length > 1) return "recursion";
    if (["heap", "pq", "minheap", "maxheap"].some((name) => locals[name] && (locals[name].t === "list" || locals[name].t === "tuple"))) return "heap";
    if (locals.graph) return "graph";
    if (Object.keys(locals).some((name) => isTree(locals[name]))) return "tree";
    if (Object.keys(locals).some((name) => isLink(locals[name]))) return "linked";
    if (Object.keys(locals).some((name) => isScalarList(locals[name]) || (locals[name] && locals[name].t === "str"))) return "array";
    return "simple";
  }

  function stepStats(trace) {
    const frames = (trace && trace.frames) || [];
    const index = trace ? trace.i || 0 : 0;
    const seen = frames.slice(0, Math.min(frames.length, index + 1));
    const frame = frames[index] || null;
    const prev = index > 0 ? frames[index - 1] : null;
    return {
      step: frames.length ? index + 1 : 0,
      total: frames.length,
      calls: seen.filter((item) => item.e === "call" && item.fn && item.fn !== "<module>").length,
      depth: frame ? (frame.stack || []).filter((item) => item.fn && item.fn !== "<module>").length : 0,
      changed: frame ? changedPairs(prev, frame).length : 0,
      printed: frame ? stdoutAt(trace.stdout, frame.out_n).length : 0,
    };
  }

  function sameFrozen(a, b) {
    return JSON.stringify(a) === JSON.stringify(b);
  }

  function listChange(prevNode, node) {
    const before = (prevNode && prevNode.v) || [];
    const after = (node && node.v) || [];
    if (before.length === after.length) {
      const diff = [];
      after.forEach((item, index) => {
        if (!sameFrozen(before[index], item)) diff.push(index);
      });
      if (diff.length === 2 && sameFrozen(before[diff[0]], after[diff[1]]) && sameFrozen(before[diff[1]], after[diff[0]])) {
        return { op: "swap", i: diff[0], j: diff[1] };
      }
      if (diff.length === 1) return { op: "write", i: diff[0] };
      if (diff.length > 1) return { op: "mutate" };
      return null;
    }
    if (after.length === before.length + 1) {
      for (let index = 0; index < after.length; index += 1) {
        const trial = after.slice(0, index).concat(after.slice(index + 1));
        if (trial.every((item, at) => sameFrozen(item, before[at]))) return { op: "insert", i: index, value: after[index] };
      }
    }
    if (before.length === after.length + 1) {
      for (let index = 0; index < before.length; index += 1) {
        const trial = before.slice(0, index).concat(before.slice(index + 1));
        if (trial.every((item, at) => sameFrozen(item, after[at]))) return { op: "remove", i: index, value: before[index] };
      }
    }
    return { op: "mutate" };
  }

  function trackListIds(frames, index) {
    const ids = {};
    let serial = 1;
    const last = Math.min((frames || []).length - 1, Math.max(0, index || 0));
    if (!frames || !frames.length || last < 0) return ids;
    for (let step = 0; step <= last; step += 1) {
      const now = localsOf(frames[step]);
      const sameFn = step > 0 && topFrame(frames[step - 1]).fn === topFrame(frames[step]).fn;
      const priorLocals = sameFn ? localsOf(frames[step - 1]) : {};
      Object.keys(now).forEach((name) => {
        const node = now[name];
        if (!node || (node.t !== "list" && node.t !== "tuple") || !node.v || !node.v.every(isScalar)) return;
        const prior = priorLocals[name];
        const old = ids[name];
        if (!prior || !old || (prior.t !== "list" && prior.t !== "tuple") || old.length !== prior.v.length) {
          ids[name] = node.v.map(() => name + "-" + (serial++));
          return;
        }
        const change = listChange(prior, node);
        if (!change) return;
        if (change.op === "swap" && old.length === node.v.length) {
          const next = old.slice();
          const held = next[change.i];
          next[change.i] = next[change.j];
          next[change.j] = held;
          ids[name] = next;
        } else if (change.op === "insert" && old.length + 1 === node.v.length) {
          const next = old.slice();
          next.splice(change.i, 0, name + "-" + (serial++));
          ids[name] = next;
        } else if (change.op === "remove" && old.length - 1 === node.v.length) {
          const next = old.slice();
          next.splice(change.i, 1);
          ids[name] = next;
        } else if (old.length === node.v.length) {
          ids[name] = old.slice();
        } else {
          ids[name] = node.v.map((_, at) => old[at] || (name + "-" + (serial++)));
        }
      });
    }
    return ids;
  }

  function motionMs(rate) {
    const wait = { 0.5: 1040, 1: 520, 1.5: 340, 2: 260 }[rate] || 520;
    return Math.max(140, Math.min(420, Math.round(wait * 0.72)));
  }

  function deriveEvents(prev, frame, trace, source) {
    const events = [];
    if (!frame) return events;
    const line = frame.line || 0;
    const now = localsOf(frame);
    const before = prev && topFrame(prev).fn === topFrame(frame).fn ? localsOf(prev) : {};
    const handled = new Set();
    const stacks = new Set(["stack", "st", "path"]);
    const queues = new Set(["queue", "q", "dq"]);
    const heaps = new Set(["heap", "pq", "minheap", "maxheap"]);
    if (frame.e === "call") events.push({ type: "call", fn: frame.fn, line, mode: "generic" });
    if (frame.e === "return") events.push({ type: "return", fn: frame.fn, line, value: frame.ret || null, mode: "generic" });
    Object.keys(now).forEach((name) => {
      const next = now[name];
      const prior = before[name];
      if (!next || (next.t !== "list" && next.t !== "tuple")) return;
      if (!prior || (prior.t !== "list" && prior.t !== "tuple")) return;
      const change = listChange(prior, next);
      if (!change) return;
      handled.add(name);
      if (change.op === "insert" && stacks.has(name) && change.i === next.v.length - 1) {
        events.push({ type: "push", name, line, i: change.i, value: change.value, mode: "smart" });
        return;
      }
      if (change.op === "remove" && stacks.has(name) && change.i === prior.v.length - 1) {
        events.push({ type: "pop", name, line, i: change.i, value: change.value, mode: "smart" });
        return;
      }
      if (change.op === "insert" && queues.has(name) && change.i === next.v.length - 1) {
        events.push({ type: "enqueue", name, line, i: change.i, value: change.value, mode: "smart" });
        return;
      }
      if (change.op === "remove" && queues.has(name) && change.i === 0) {
        events.push({ type: "dequeue", name, line, i: 0, value: change.value, mode: "smart" });
        return;
      }
      if (change.op === "swap" && heaps.has(name)) {
        const child = Math.max(change.i, change.j);
        const parent = Math.min(change.i, change.j);
        let heap = null;
        if (parent === Math.floor((child - 1) / 2)) heap = sameFrozen(prior.v[child], next.v[parent]) ? "sift-up" : "sift-down";
        events.push({ type: "swap", name, line, i: change.i, j: change.j, heap, mode: heap ? "smart" : "generic" });
        return;
      }
      events.push({ type: change.op, name, line, i: change.i, j: change.j, value: change.value, mode: "generic" });
    });
    const pointers = new Set(["i", "j", "k", "ii", "jj", "left", "right", "mid", "lo", "hi", "low", "high", "start", "end", "slow", "fast", "idx", "index", "p", "u", "v", "row", "col", "write", "read", "l", "r", "pos", "min_idx", "max_idx", "best", "gap"]);
    const roles = loopRoles(source || (trace && trace.source) || "");
    Object.keys(now).forEach((name) => {
      if (!pointers.has(name) || (roles[name] && roles[name].mode === "item")) return;
      const next = now[name];
      const prior = before[name];
      if (!next || next.t !== "int") return;
      if (prior && prior.t === "int" && prior.v === next.v) return;
      handled.add(name);
      events.push({ type: "pointer", name, line, from: prior && prior.t === "int" ? prior.v : null, to: next.v, mode: "smart" });
    });
    Object.keys(now).forEach((name) => {
      const next = now[name];
      const prior = before[name];
      if (!isLink(next) && !isTree(next)) return;
      ["next", "left", "right"].forEach((field) => {
        const afterField = dictGet(next, field);
        const beforeField = prior ? dictGet(prior, field) : null;
        const afterId = afterField && (afterField.id || (afterField.t === "alias" ? afterField.id : null));
        const beforeId = beforeField && (beforeField.id || (beforeField.t === "alias" ? beforeField.id : null));
        const afterNone = !afterField || afterField.t === "none";
        const beforeNone = !beforeField || beforeField.t === "none";
        if (afterNone && beforeNone) return;
        if (afterId === beforeId && afterNone === beforeNone) return;
        handled.add(name);
        events.push({ type: isTree(next) ? "tree-link" : "link", name, line, field, from: beforeNone ? null : beforeId, to: afterNone ? null : afterId, mode: "smart" });
      });
    });
    ["seen", "visited", "vis"].forEach((name) => {
      const next = now[name];
      const prior = before[name];
      if (!next || (next.t !== "set" && next.t !== "list")) return;
      const grew = next.v && prior && prior.v && next.v.length === prior.v.length + 1;
      if (!grew) return;
      handled.add(name);
      events.push({ type: "visited", name, line, mode: "smart" });
    });
    Object.keys(now).forEach((name) => {
      if (handled.has(name)) return;
      const next = now[name];
      const prior = before[name];
      if (next && next.t === "dict" && prior && prior.t === "dict") {
        const beforeKeys = new Set((prior.v || []).map((pair) => JSON.stringify(pair[0])));
        const wrote = (next.v || []).some((pair) => {
          const key = JSON.stringify(pair[0]);
          if (!beforeKeys.has(key)) return true;
          const old = (prior.v || []).find((item) => JSON.stringify(item[0]) === key);
          return !old || !sameFrozen(old[1], pair[1]);
        });
        if (wrote) {
          handled.add(name);
          events.push({ type: "map-write", name, line, mode: "generic" });
        }
      }
    });
    ["dp", "grid", "mat", "matrix", "table"].forEach((name) => {
      if (!isMatrix(now[name]) || !isMatrix(before[name])) return;
      now[name].v.forEach((row, r) => {
        row.v.forEach((cell, c) => {
          const old = before[name].v[r] && before[name].v[r].v[c];
          if (!sameFrozen(old, cell)) events.push({ type: "table-write", name, line, r, c, mode: "smart" });
        });
      });
      handled.add(name);
    });
    Object.keys(now).forEach((name) => {
      if (handled.has(name)) return;
      if (!before[name]) events.push({ type: "create", name, line, value: now[name], mode: "generic" });
      else if (!sameFrozen(before[name], now[name])) events.push({ type: "assign", name, line, value: now[name], mode: "generic" });
    });
    Object.keys(before).forEach((name) => {
      if (!now[name]) events.push({ type: "delete", name, line, mode: "generic" });
    });
    if (trace && (frame.out_n || 0) > ((prev && prev.out_n) || 0)) {
      events.push({ type: "print", line, text: stdoutAt(trace.stdout, frame.out_n).slice((prev && prev.out_n) || 0), mode: "generic" });
    }
    if (trace && trace.error && trace.frames && frame === trace.frames[trace.frames.length - 1]) {
      events.push({ type: "exception", line, message: trace.error, mode: "generic" });
    }
    return events;
  }

  function describeEvent(event) {
    if (!event) return "";
    if (event.type === "push") return "Push " + shortValue(event.value) + " onto " + event.name + ".";
    if (event.type === "pop") return "Pop " + shortValue(event.value) + " from " + event.name + ".";
    if (event.type === "enqueue") return "Enqueue " + shortValue(event.value) + " on " + event.name + ".";
    if (event.type === "dequeue") return "Dequeue " + shortValue(event.value) + " from " + event.name + ".";
    if (event.type === "swap") return "Swap " + event.name + "[" + event.i + "] with [" + event.j + "]" + (event.heap ? " (" + event.heap + ")." : ".");
    if (event.type === "insert") return "Insert into " + event.name + " at index " + event.i + ".";
    if (event.type === "remove") return "Remove " + event.name + "[" + event.i + "].";
    if (event.type === "write") return "Write " + event.name + "[" + event.i + "].";
    if (event.type === "pointer") return event.name + " moves" + (event.from === null ? "" : " from " + event.from) + " to " + event.to + ".";
    if (event.type === "link" || event.type === "tree-link") return event.name + "." + event.field + " now points to " + (event.to == null ? "nothing" : "#" + event.to) + ".";
    if (event.type === "visited") return event.name + " records one more visited item.";
    if (event.type === "map-write") return event.name + " stores a key.";
    if (event.type === "table-write") return event.name + "[" + event.r + "][" + event.c + "] changes.";
    if (event.type === "print") return "Printed text.";
    if (event.type === "exception") return event.message;
    if (event.type === "call") return event.fn === "<module>" ? "The program starts." : "Call " + event.fn + ".";
    if (event.type === "return") return "Return from " + event.fn + ".";
    if (event.type === "create") return "Create " + event.name + ".";
    if (event.type === "delete") return "Remove the name " + event.name + ".";
    if (event.type === "assign") return "Update " + event.name + ".";
    return "";
  }

  function describeEvents(events) {
    return (events || []).slice(0, 3).map(describeEvent).filter(Boolean).join(" ");
  }

  function narration(frame, prev, source) {
    if (!frame) return "Press Run to watch this code step by step.";
    const line = sourceLine(source, frame.line).trim();
    const changes = changedPairs(prev, frame);
    const changeText = changes.slice(0, 3).map(([name, value]) => name + " is now " + shortValue(value)).join("; ");
    if (frame.e === "call") {
      if (frame.fn === "<module>") return "The program starts. Python makes a place to remember the values.";
      const args = Object.keys(localsOf(frame)).slice(0, 4).map((name) => name + "=" + shortValue(localsOf(frame)[name])).join(", ");
      return "Enter " + frame.fn + "(" + args + "). Python creates a new memory frame for this call.";
    }
    if (frame.e === "return") {
      if (frame.fn === "<module>") return "Finished.";
      const extra = frame.final ? " This answer is the output of the program." : " The caller receives this value.";
      return "Return " + shortValue(frame.ret) + " from " + frame.fn + "." + extra;
    }
    if (/^print\s*\(/.test(line)) {
      return "This print writes text into the output. " + (changeText ? "Memory also changes: " + changeText + "." : "The stored data stays as it is.");
    }
    if (/^(if|elif|while|assert)\b/.test(line)) {
      return "Decision: " + line + ". " + (changeText ? "Then " + changeText + "." : "The next step follows the branch that is true.");
    }
    if (/^for\b/.test(line)) {
      return "Loop step. " + (changeText ? changeText + "." : "The loop variable moves to the next item.");
    }
    if (changeText) return "Write into memory: " + changeText + ".";
    if (line) return "Run `" + line + "`. The flow moves forward. Memory does not change on this line.";
    return "The flow moves to the next step.";
  }

  function shortStep(frame, prev, source) {
    if (!frame) return "";
    if (frame.e === "call") return frame.fn === "<module>" ? "start" : "call " + frame.fn;
    if (frame.e === "return") return frame.fn === "<module>" ? "done" : "return " + shortValue(frame.ret);
    const changes = changedPairs(prev, frame);
    if (changes.length) return changes[0][0] + " = " + shortValue(changes[0][1]);
    const line = sourceLine(source, frame.line).trim();
    return line.length > 36 ? line.slice(0, 34) + "…" : line || "step";
  }

  function outputStory(frame, trace) {
    if (!frame) return "Output shows up when the program prints or returns a value.";
    if (trace.script && frame.final) {
      if (trace.error && frame === trace.frames[trace.frames.length - 1]) return "The program stopped. " + trace.error;
      const printed = (trace.stdout || "").trim();
      if (printed) return "The program finished. The words it printed are in the box above.";
      return "The program finished. Nothing was printed. The remembered values are in the boxes above.";
    }
    if (trace.error && frame === trace.frames[trace.frames.length - 1]) {
      return "The run stopped with an error, so a normal return value was not produced. " + trace.error;
    }
    if (frame.final) {
      const printed = (trace.stdout || "").slice(0, frame.out_n || 0).trim();
      return "The function finished. The answer is " + pyFmt(frame.ret) + (printed ? ". Printed text is shown above that answer." : ".");
    }
    const printed = (trace.stdout || "").slice(0, frame.out_n || 0);
    if (printed) return "Some text has been printed. The function has not returned yet.";
    return "Nothing has come out yet. The program is still storing values. Output appears when it prints or returns.";
  }

  function injectStyle() {
    if (document.getElementById("vl-style")) return;
    const style = document.createElement("style");
    style.id = "vl-style";
    style.textContent = `
      .vl-launch, .vl-banner-btn, .vl-jump, .vl-nav-btn {
        font-family: var(--font-sans, "DM Sans", system-ui, sans-serif);
        cursor: pointer;
      }
      .vl-launch-bar {
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        flex: none;
        z-index: 2;
      }
      body.course-page > header {
        justify-content: flex-start;
        gap: 0.6rem;
        padding: 0 1rem;
      }
      body.course-page > header h1 {
        min-width: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
      .vl-launch {
        position: static;
        transform: none;
        border: 1px solid rgba(61, 156, 253, 0.45);
        background: rgba(61, 156, 253, 0.16);
        color: #e8eef4;
        border-radius: 999px;
        padding: 0.35rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 700;
        white-space: nowrap;
      }
      .vl-launch:hover { background: #3d9cfd; color: #0f1419; }
      .vl-nav-btn {
        display: block;
        width: calc(100% - 1.5rem);
        margin: 0 0.75rem 0.8rem;
        text-align: left;
        border: 1px solid rgba(61, 156, 253, 0.35);
        background: rgba(61, 156, 253, 0.12);
        color: #9ed0ff;
        border-radius: 8px;
        padding: 0.45rem 0.7rem;
        font-size: 0.82rem;
        font-weight: 700;
      }
      .vl-banner {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        align-items: center;
        margin: 0 0 1.5rem;
        padding: 1.1rem 1.2rem;
        border: 1px solid rgba(61, 156, 253, 0.28);
        background: linear-gradient(135deg, rgba(61,156,253,.14), rgba(124,92,255,.12));
        border-radius: 16px;
      }
      .vl-banner h2 {
        font-family: var(--font-display, Fraunces, Georgia, serif);
        font-size: 1.35rem;
        margin: 0.15rem 0 0.35rem;
      }
      .vl-banner p { margin: 0; color: var(--text-muted, #8fa3b8); max-width: 62ch; }
      .vl-kicker {
        margin: 0;
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 700;
        color: #7cc4ff;
      }
      .vl-banner-btn, .vl-jump {
        border: 0;
        background: #3d9cfd;
        color: #071018;
        font-weight: 800;
        border-radius: 999px;
        padding: 0.55rem 0.9rem;
        white-space: nowrap;
      }
      .vl-jump { margin: 0.35rem 0 0.9rem; }
      .layout > nav a.vl-done::after { content: " ✓"; color: #4ade80; font-weight: 800; }
      body.vl-open { overflow: hidden; }
      .vl-root {
        position: fixed;
        inset: 0;
        z-index: 860;
        background: #0c1218;
        color: #e8eef4;
        display: flex;
        flex-direction: column;
        font-family: var(--font-sans, "DM Sans", system-ui, sans-serif);
      }
      .vl-root[hidden] { display: none !important; }
      .vl-top {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.65rem 0.8rem;
        border-bottom: 1px solid rgba(255,255,255,.08);
        background: #121820;
        flex: none;
      }
      .vl-top h2 {
        font-family: var(--font-display, Fraunces, Georgia, serif);
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
        flex: 1;
        min-width: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .vl-top button, .vl-transport button, .vl-tests button, .vl-editor-actions button, .vl-pane-bar button {
        font-family: inherit;
        cursor: pointer;
      }
      .vl-btn {
        border: 1px solid rgba(255,255,255,.12);
        background: #1a222d;
        color: #e8eef4;
        border-radius: 8px;
        padding: 0.38rem 0.65rem;
        font-size: 0.78rem;
        font-weight: 700;
      }
      .vl-btn.primary { background: #3d9cfd; color: #071018; border-color: #3d9cfd; }
      .vl-btn.ghost { background: transparent; }
      .vl-body { flex: 1; min-height: 0; overflow: hidden; display: flex; flex-direction: column; }
      .vl-map { padding: 1rem 1rem 2.5rem; max-width: 1160px; margin: 0 auto; }
      .vl-map-head { display: flex; justify-content: space-between; gap: 1rem; align-items: end; margin-bottom: 0.8rem; }
      .vl-map-head h3 { font-family: var(--font-display, Fraunces, Georgia, serif); font-size: 1.7rem; margin: 0.2rem 0; }
      .vl-map-head p, .vl-progress { color: #8fa3b8; margin: 0; }
      .vl-tools { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.8rem 0 1rem; }
      .vl-tools input, .vl-tools select, .vl-transport select {
        background: #1a222d;
        color: #e8eef4;
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 8px;
        padding: 0.4rem 0.55rem;
        font: inherit;
      }
      .vl-section {
        border: 1px solid rgba(255,255,255,.08);
        background: #141b24;
        border-radius: 14px;
        padding: 0.8rem;
        margin: 0 0 0.7rem;
      }
      .vl-section h4 { margin: 0 0 0.55rem; font-size: 0.92rem; }
      .vl-chips { display: flex; flex-wrap: wrap; gap: 0.4rem; }
      .vl-chip {
        border: 1px solid rgba(255,255,255,.1);
        background: #0f1419;
        color: #d5dee8;
        border-radius: 999px;
        padding: 0.28rem 0.6rem;
        font-size: 0.75rem;
        cursor: pointer;
        text-align: left;
      }
      .vl-chip small { display: block; color: #8fa3b8; font-weight: 500; }
      .vl-chip.is-solved { border-color: rgba(74,222,128,.45); color: #bbf7d0; }
      .vl-chip.is-tried { border-color: rgba(251,191,36,.45); }
      .vl-work {
        height: 100%;
        flex: 1;
        min-height: 0;
        display: grid;
        grid-template-columns: minmax(280px, 1.05fr) 6px minmax(300px, 1fr);
        min-height: 0;
      }
      .vl-col { min-width: 0; min-height: 0; display: flex; flex-direction: column; border-right: 1px solid rgba(255,255,255,.08); }
      .vl-col:last-child { border-right: 0; }
      .vl-col-h {
        padding: 0.45rem 0.7rem;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        border-bottom: 1px solid rgba(255,255,255,.08);
        flex: none;
      }
      .vl-lens { display: flex; align-items: center; gap: 0.35rem; text-transform: none; letter-spacing: 0; font-size: 0.78rem; }
      .vl-lens button { border-radius: 999px; padding: 0.22rem 0.55rem; }
      .vl-sol .vl-col-h { color: #d4c4ff; }
      .vl-you .vl-code { flex: none; max-height: 88px; overflow: hidden; margin: 0 0 0.35rem; }
      .vl-you .vl-scroll {
        overflow: hidden;
        display: flex;
        flex-direction: column;
        padding: 0.55rem 0.7rem 0.45rem;
      }
      .vl-watch {
        flex: 1;
        min-height: 0;
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
      }
      .vl-live {
        flex: 1;
        min-height: 0;
        display: grid;
        grid-template-columns: minmax(0, 1.45fr) minmax(150px, 0.62fr);
        grid-template-rows: minmax(0, 1fr);
        gap: 0.35rem;
      }
      .vl-live > .vl-picture,
      .vl-live > .vl-dock { min-width: 0; min-height: 0; overflow: hidden; }
      .vl-dock {
        min-height: 0;
        overflow: auto;
        display: flex;
        flex-direction: column;
        gap: 0.28rem;
        padding: 0.35rem 0.45rem;
        border-radius: 12px;
        background: rgba(255,255,255,.03);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
      }
      .vl-stats, .vl-calls { margin: 0; color: #9fb0c3; font-size: 0.72rem; line-height: 1.35; }
      .vl-calls b { color: #e8eef4; font-weight: 700; }
      .vl-vtable { width: 100%; border-collapse: collapse; font-size: 0.72rem; }
      .vl-vtable th, .vl-vtable td { text-align: left; padding: 0.16rem 0.2rem; border-bottom: 1px solid rgba(255,255,255,.06); }
      .vl-vtable tr.is-changed td { background: rgba(250,204,21,.16); }
      .vl-vtable tr.is-linked td, .vl-var.is-linked, .vl-ptr.is-linked, .vl-cell.is-linked { outline: 1px solid #7cc4ff; }
      .vl-back div.is-ref { box-shadow: inset 3px 0 0 #7cc4ff; }
      .vl-dots { display: flex; flex-wrap: wrap; gap: 0.22rem; flex: 1 0 100%; }
      .vl-dot {
        width: 0.55rem;
        height: 0.55rem;
        padding: 0;
        border-radius: 99px;
        border: 0;
        background: rgba(255,255,255,.22);
        cursor: pointer;
      }
      .vl-dot.is-past { background: rgba(61,156,253,.7); }
      .vl-dot.is-now { background: #facc15; }
      .vl-explain { margin: 0; color: #c5d2e0; font-size: 0.78rem; line-height: 1.35; }
      .vl-explain b { color: #f4f7ff; }
      .vl-nowline {
        flex: none;
        background: rgba(250,204,21,.12);
        border-left: 3px solid #facc15;
        border-radius: 10px;
        padding: 0.45rem 0.65rem;
      }
      .vl-nowline b { display: block; font-size: 0.98rem; line-height: 1.35; }
      .vl-nowline code {
        display: block;
        margin-top: 0.2rem;
        color: #fff6d0;
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.84rem;
      }
      .vl-rail { flex: none; display: flex; flex-wrap: wrap; align-items: center; gap: 0.45rem; }
      .vl-rail input[type="range"] { flex: 1; accent-color: #facc15; }
      .vl-rail span { flex: none; color: #8fa3b8; font-size: 0.72rem; font-variant-numeric: tabular-nums; }
      .vl-picture {
        position: relative;
        flex: 1;
        min-height: 0;
        height: 100%;
        overflow: hidden;
        border-radius: 16px;
        background:
          radial-gradient(circle at 50% 0%, rgba(61,156,253,.16), transparent 55%),
          #101820;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);
      }
      .vl-instep {
        position: absolute;
        z-index: 2;
        top: 0.55rem;
        left: 0.75rem;
        right: 0.75rem;
        margin: 0;
        color: #fff6d0;
        font-size: 0.86rem;
        line-height: 1.35;
        pointer-events: none;
      }
      .vl-instep code {
        display: block;
        margin-top: 0.12rem;
        color: #facc15;
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.82rem;
      }
      .vl-instep.is-bad { color: #fecaca; }
      .vl-fit {
        position: absolute;
        inset: 0;
        box-sizing: border-box;
        padding: 3.2rem 0.45rem 0.4rem;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .vl-picture .vl-card {
        margin: 0;
        border: 0;
        background: transparent;
        width: max-content;
        max-width: none;
        flex: none;
        box-shadow: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.55rem;
      }
      .vl-picture .vl-card h5, .vl-picture .vl-legend, .vl-picture .vl-intro { display: none; }
      .vl-caption {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #9fb0c3;
      }
      .vl-outbar {
        flex: none;
        min-height: 5.2rem;
        max-height: 8.4rem;
        overflow: auto;
        white-space: pre-wrap;
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.9rem;
        line-height: 1.4;
        color: #bbf7d0;
        background: #07140d;
        border-radius: 10px;
        padding: 0.45rem 0.6rem;
      }
      .vl-outbar.is-err { background: #2a1215; color: #fecaca; }
      .vl-scroll { overflow: auto; padding: 0.7rem; flex: 1; }
      .vl-problem h3 { margin: 0.2rem 0 0.4rem; font-family: var(--font-display, Fraunces, Georgia, serif); font-size: 1.25rem; }
      .vl-problem p, .vl-problem li { color: #b7c5d3; font-size: 0.88rem; }
      .vl-problem ol { margin: 0.3rem 0 0.7rem 1.1rem; }
      .vl-sig { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.78rem; color: #d6e6ff; background: #121820; padding: 0.35rem 0.5rem; border-radius: 8px; }
      .vl-editor {
        width: 100%;
        min-height: 220px;
        resize: vertical;
        background: #0f1419;
        color: #e8eef4;
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 10px;
        padding: 0.6rem;
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 12.5px;
        line-height: 1.5;
        tab-size: 4;
      }
      .vl-editor-actions, .vl-tests { display: flex; flex-wrap: wrap; gap: 0.35rem; margin: 0.45rem 0; }
      .vl-suggest {
        position: fixed;
        z-index: 40;
        min-width: 220px;
        max-width: 320px;
        max-height: 240px;
        overflow: auto;
        margin: 0;
        padding: 0.28rem;
        list-style: none;
        background: #121820;
        color: #e8eef4;
        border-radius: 12px;
        box-shadow: 0 16px 40px rgba(0,0,0,.4), inset 0 0 0 1px rgba(255,255,255,.1);
      }
      .vl-suggest button {
        display: flex;
        width: 100%;
        gap: 0.6rem;
        align-items: center;
        text-align: left;
        background: transparent;
        color: inherit;
        border: 0;
        border-radius: 8px;
        padding: 0.32rem 0.5rem;
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.82rem;
        cursor: pointer;
      }
      .vl-suggest button.is-on,
      .vl-suggest button:hover { background: rgba(61,156,253,.28); }
      .vl-suggest small { margin-left: auto; color: #8fa3b8; font-size: 0.68rem; }
      .vl-line {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.78rem;
        background: rgba(61,156,253,.12);
        border-left: 3px solid #3d9cfd;
        padding: 0.4rem 0.55rem;
        border-radius: 6px;
        margin-bottom: 0.4rem;
        color: #d6eaff;
      }
      .vl-line.is-live { background: rgba(250,204,21,.16); border-left-color: #facc15; color: #fff6d0; }
      .vl-line.is-bad { background: rgba(248,113,113,.16); border-left-color: #f87171; color: #fecaca; }
      .vl-grade { font-size: 0.8rem; font-weight: 700; margin: 0.2rem 0 0.4rem; }
      .vl-grade.ok { color: #4ade80; }
      .vl-grade.bad { color: #fbbf24; }
      .vl-test {
        border: 1px solid rgba(255,255,255,.1);
        background: #121820;
        color: #d5dee8;
        border-radius: 8px;
        padding: 0.25rem 0.45rem;
        font-size: 0.72rem;
        cursor: pointer;
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      }
      .vl-test.is-on { outline: 2px solid #3d9cfd; }
      .vl-test.pass { border-color: rgba(74,222,128,.5); }
      .vl-test.fail { border-color: rgba(248,113,113,.55); }
      .vl-card {
        background: #121820;
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 12px;
        padding: 0.55rem 0.6rem;
        margin: 0 0 0.55rem;
      }
      .vl-card h5 { margin: 0 0 0.35rem; font-size: 0.72rem; letter-spacing: .05em; text-transform: uppercase; color: #8fa3b8; }
      .vl-narration { font-size: 0.86rem; line-height: 1.45; margin: 0; }
      .vl-intro { color: #8fa3b8; font-size: 0.75rem; margin: 0.3rem 0 0; }
      .vl-flowstrip { position: relative; display: flex; flex-direction: column; gap: 0.28rem; max-height: 280px; overflow: auto; padding-bottom: 0.2rem; }
      .vl-fstep {
        width: auto;
        display: flex;
        gap: 0.45rem;
        align-items: baseline;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,.1);
        background: #0f1419;
        color: #b7c5d3;
        text-align: left;
        padding: 0.35rem 0.5rem;
        font-size: 0.78rem;
        cursor: pointer;
      }
      .vl-fstep.is-now { border-color: #facc15; color: #fff6d0; background: rgba(250,204,21,.16); }
      .vl-fstep.is-past { opacity: 0.72; }
      .vl-fnum { flex: none; min-width: 3.2rem; font-weight: 800; color: #facc15; }
      .vl-ftext { display: flex; flex-direction: column; min-width: 0; }
      .vl-ftext b { font-weight: 700; word-break: break-word; }
      .vl-ftext small { color: #8fa3b8; font-size: 0.72rem; }
      .vl-cells { display: flex; flex-wrap: nowrap; gap: 0.55rem; align-items: flex-end; justify-content: center; padding-top: 2.1rem; }
      .vl-board { position: relative; display: inline-block; }
      .vl-stage { position: relative; }
      .vl-flow { display: none; }
      .vl-cell {
        width: 72px;
        min-height: 76px;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,.12);
        background: #0f1419;
        text-align: center;
        position: relative;
        padding: 0.2rem 0.15rem 1.15rem;
      }
      .vl-cell.is-swap, .vl-node.is-swap { box-shadow: inset 0 0 0 2px #7cc4ff; }
      .vl-stack i.is-top::after, .vl-queue i.is-front::after, .vl-queue i.is-rear::after {
        display: block;
        margin-top: 0.12rem;
        font-size: 0.62rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        color: #facc15;
      }
      .vl-stack i.is-top::after { content: "TOP"; }
      .vl-queue i.is-front::after { content: "FRONT"; }
      .vl-queue i.is-rear:not(.is-front)::after { content: "REAR"; color: #7cc4ff; }
      .vl-queue i.is-front.is-rear::after { content: "FRONT · REAR"; }
      .vl-motion-ghost {
        position: fixed;
        z-index: 870;
        display: flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
        border-radius: 8px;
        background: rgba(248,113,113,.4);
        color: #fff;
        font: 700 0.75rem/1.2 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        pointer-events: none;
      }
      .vl-cell.is-changed {
        background: rgba(251,191,36,.22);
        border-color: #fbbf24;
        animation: vl-pulse 0.55s ease;
      }
      .vl-cell.is-read { outline: 2px solid #7cc4ff; outline-offset: -2px; animation: vl-pulse 0.7s ease; }
      .vl-cell.is-seen { opacity: 0.45; }
      .vl-cell.is-scan {
        border-color: #facc15;
        background: rgba(250,204,21,.16);
        box-shadow: 0 10px 22px rgba(250,204,21,.22);
        z-index: 2;
      }
      .vl-cell.is-found { border-color: #86efac; background: rgba(134,239,172,.18); }
      .vl-cursor { position: absolute; z-index: 3; pointer-events: none; }
      .vl-cursor b {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transform: translateX(-50%);
        background: #facc15;
        color: #1c1400;
        font-size: 0.75rem;
        font-weight: 800;
        box-shadow: 0 8px 18px rgba(250,204,21,.35);
      }
      .vl-wires line.vl-stem { stroke: #facc15; stroke-width: 2; }
      .vl-scanline { margin: 0.45rem 0 0; color: #d6e2ee; font-size: 0.82rem; text-align: center; }
      .vl-linkstage, .vl-treestage { position: relative; }
      .vl-wires {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        overflow: visible;
        pointer-events: none;
      }
      .vl-wires line { stroke: #7cc4ff; stroke-width: 2; fill: none; }
      .vl-links, .vl-treestage .vl-tree { position: relative; z-index: 1; }
      .vl-cell .vl-idx { display: block; color: #8fa3b8; font-size: 0.65rem; }
      .vl-cell .vl-val { display: block; font-weight: 800; font-size: 1rem; word-break: break-all; }
      .vl-ptrs { display: flex; flex-direction: column; gap: 0.05rem; margin-top: 0.15rem; }
      .vl-ptr { font-size: 0.68rem; font-weight: 800; animation: vl-bob 0.9s ease-in-out infinite; }
      .vl-vars { display: flex; flex-wrap: wrap; gap: 0.45rem; margin-top: 0.55rem; }
      .vl-var {
        min-width: 92px;
        border-radius: 14px;
        border: 1px solid rgba(124,196,255,.45);
        background: #101820;
        padding: 0.55rem 0.8rem 0.7rem;
        text-align: center;
        box-shadow: 0 8px 18px rgba(0,0,0,.22);
      }
      .vl-var small { display: block; color: #7cc4ff; font-size: 0.68rem; font-weight: 800; letter-spacing: 0.03em; }
      .vl-var b { display: block; margin-top: 0.2rem; font-size: 1.05rem; }
      .vl-heap { display: flex; flex-direction: column; align-items: center; gap: 0.55rem; margin: 0.3rem 0; }
      .vl-heap-row { display: flex; justify-content: center; gap: 0.8rem; }
      .vl-node.is-now { outline: 2px solid #facc15; outline-offset: 2px; }
      @keyframes vl-pulse {
        0% { transform: translateY(0) scale(1); }
        40% { transform: translateY(-7px) scale(1.06); }
        100% { transform: translateY(0) scale(1); }
      }
      @keyframes vl-bob {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
      }
      .vl-bars { display: flex; align-items: flex-end; gap: 0.3rem; min-height: 120px; }
      .vl-bar { width: 28px; background: #3d9cfd; border-radius: 5px 5px 0 0; position: relative; }
      .vl-bar.is-changed { background: #fbbf24; }
      .vl-bar span { position: absolute; top: -1.05rem; left: 0; right: 0; text-align: center; font-size: 0.65rem; }
      .vl-kv { display: flex; flex-wrap: wrap; gap: 0.35rem; }
      .vl-kv div, .vl-chipvar {
        background: #0f1419;
        border: 1px solid rgba(255,255,255,.1);
        border-radius: 8px;
        padding: 0.25rem 0.4rem;
        font-size: 0.75rem;
      }
      .vl-kv div.is-changed, .vl-chipvar.is-changed { border-color: #fbbf24; background: rgba(251,191,36,.12); }
      .vl-stack { display: flex; flex-direction: column-reverse; align-items: center; gap: 0.35rem; }
      .vl-stack i, .vl-queue i {
        font-style: normal;
        background: #0f1419;
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 8px;
        min-width: 96px;
        text-align: center;
        padding: 0.5rem 0.75rem 0.35rem;
        font-weight: 700;
      }
      .vl-stack i.is-top { border-color: #3d9cfd; }
      .vl-queue { display: flex; gap: 0.35rem; align-items: flex-end; justify-content: center; flex-wrap: wrap; }
      .vl-queue i.is-front { border-color: #4ade80; }
      .vl-pile { display: flex; flex-direction: column; align-items: center; gap: 0.45rem; }
      .vl-ends {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        width: 100%;
        min-width: 210px;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.05em;
      }
      .vl-ends b.top, .vl-ends b.rear { color: #7cc4ff; }
      .vl-ends b.front { color: #4ade80; }
      .vl-ends span { color: #8fa3b8; font-weight: 650; }
      .vl-pile.is-stack .vl-stack {
        min-width: 150px;
        min-height: 86px;
        padding: 0.5rem 0.75rem 0.25rem;
        border-left: 3px solid rgba(124,196,255,.75);
        border-right: 3px solid rgba(124,196,255,.75);
        border-bottom: 10px solid #3d9cfd;
        border-radius: 0 0 14px 14px;
        background: linear-gradient(#0c141c, #15202b);
      }
      .vl-pile .vl-stack i, .vl-pile .vl-queue i {
        min-width: 132px;
        min-height: 52px;
        border-radius: 12px;
        font-size: 1.05rem;
        box-shadow: 0 5px 0 rgba(0,0,0,.28);
      }
      .vl-pile .vl-stack i.is-top {
        background: #16324d;
        border-color: #7cc4ff;
        color: #f4fbff;
      }
      .vl-pile.is-queue .vl-queue {
        flex-wrap: nowrap;
        justify-content: flex-start;
        padding: 0.75rem 0.8rem 0.6rem;
        border-radius: 16px;
        background: linear-gradient(90deg, rgba(74,222,128,.2), rgba(16,24,32,.15) 22%, rgba(16,24,32,.15) 78%, rgba(124,196,255,.22));
        box-shadow: inset 0 0 0 1px rgba(255,255,255,.08);
      }
      .vl-pile .vl-queue i.is-front { background: #123222; border-color: #4ade80; }
      .vl-pile .vl-queue i.is-rear { background: #122433; border-color: #7cc4ff; }
      .vl-pile i.is-empty {
        border-style: dashed;
        color: #8fa3b8;
        box-shadow: none;
        font-weight: 650;
      }
      .vl-links { display: flex; flex-wrap: wrap; gap: 0.2rem; align-items: center; }
      .vl-node {
        width: 54px;
        height: 54px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        border: 2px solid #7cc4ff;
        padding: 0.15rem;
        background: #101820;
        font-weight: 800;
        box-sizing: border-box;
      }
      .vl-node small { display: block; font-weight: 700; color: #7cc4ff; font-size: 0.62rem; }
      .vl-node.is-changed { border-color: #fbbf24; }
      .vl-arrow { color: #8fa3b8; font-weight: 800; }
      .vl-tree { display: flex; flex-direction: column; align-items: center; gap: 0.25rem; }
      .vl-tree-kids { display: flex; gap: 0.8rem; align-items: flex-start; }
      .vl-grid { border-collapse: collapse; }
      .vl-table { border-collapse: collapse; margin-top: 0.2rem; }
      .vl-table th, .vl-table td, .vl-grid td {
        border: 1px solid rgba(255,255,255,.14);
        min-width: 2.4rem;
        height: 2rem;
        padding: 0.2rem 0.45rem;
        text-align: center;
        font-size: 0.78rem;
        font-weight: 700;
        background: #0f1419;
      }
      .vl-table th { color: #9fb0c3; font-size: 0.68rem; letter-spacing: 0.04em; text-transform: uppercase; background: #17202a; }
      .vl-table tr.is-changed td { background: rgba(251,191,36,.2); }
      .vl-set { display: flex; flex-wrap: wrap; gap: 0.4rem; justify-content: center; }
      .vl-set i {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-style: normal;
        font-weight: 800;
        border: 2px solid #86efac;
        background: #101820;
      }
      .vl-grid td.is-changed { background: rgba(251,191,36,.2); }
      .vl-grid td.is-here { outline: 2px solid #3d9cfd; outline-offset: -2px; }
      .vl-bits { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.8rem; }
      .vl-bits b { display: inline-block; width: 1.15rem; text-align: center; border-radius: 4px; }
      .vl-bits b.on { background: rgba(61,156,253,.25); color: #fff; }
      .vl-graph { width: 360px; max-width: none; height: auto; display: block; margin: 0 auto; overflow: visible; }
      .vl-key { display: flex; flex-wrap: wrap; gap: 0.65rem; justify-content: center; margin: 0.45rem 0 0.2rem; color: #9fb0c3; font-size: 0.72rem; }
      .vl-key b { display: inline-block; width: 0.7rem; height: 0.7rem; border-radius: 50%; margin-right: 0.28rem; vertical-align: -1px; }
      .vl-graph circle.is-hot { filter: drop-shadow(0 0 6px #facc15); }
      .vl-frame {
        border: 1px solid rgba(255,255,255,.1);
        border-radius: 10px;
        padding: 0.4rem;
        margin: 0 0 0.4rem;
      }
      .vl-frame.is-now { border-color: rgba(61,156,253,.6); }
      .vl-frame strong { display: block; margin-bottom: 0.25rem; font-size: 0.78rem; }
      .vl-out {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        white-space: pre-wrap;
        background: #07140d;
        color: #bbf7d0;
        border-radius: 10px;
        padding: 0.55rem;
        min-height: 4.2rem;
        font-size: 0.8rem;
      }
      .vl-out.is-err { background: #2a1215; color: #fecaca; }
      .vl-out-ready { box-shadow: inset 0 0 0 1px rgba(74,222,128,.4); }
      .vl-transport {
        display: flex;
        gap: 0.3rem;
        align-items: center;
        padding: 0.4rem 0.55rem;
        border-top: 1px solid rgba(255,255,255,.08);
        flex: none;
        background: #10161d;
      }
      .vl-transport .vl-count { margin-left: auto; color: #8fa3b8; font-size: 0.72rem; font-variant-numeric: tabular-nums; }
      .vl-code {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 12px;
        line-height: 1.45;
        background: #0f1419;
        border-radius: 10px;
        padding: 0.4rem 0.45rem;
        overflow: auto;
        max-height: 180px;
        margin-bottom: 0.5rem;
      }
      .vl-code div.is-now { background: rgba(124,92,255,.28); border-radius: 4px; }
      .vl-pane-bar { display: none; gap: 0.35rem; padding: 0.4rem 0.6rem; border-bottom: 1px solid rgba(255,255,255,.08); }
      .vl-err { color: #fecaca; font-size: 0.8rem; }
      .vl-legend { color: #8fa3b8; font-size: 0.7rem; margin: 0.35rem 0 0; }
      .vl-map { max-width: 1160px; }
      .vl-road-actions { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; }
      .vl-road-more { display: flex; gap: 0.45rem; flex-wrap: wrap; max-width: 1100px; margin: 0.85rem auto 0; }
      .vl-tree-wrap { overflow-x: auto; padding: 0.6rem 0 0.8rem; }
      .vl-tree-wrap > .vl-tree {
        position: relative;
        width: 1100px;
        height: 1020px;
        margin: 0.2rem auto 0;
        border-radius: 18px;
        background-color: #14161c;
        background-image: radial-gradient(rgba(255,255,255,.16) 1.1px, transparent 1.2px);
        background-size: 16px 16px;
      }
      .vl-edges { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; overflow: visible; }
      .vl-edges path { fill: none; stroke: rgba(186, 198, 220, 0.55); stroke-width: 2; stroke-linecap: round; transition: stroke 0.25s ease, opacity 0.25s ease, stroke-width 0.25s ease; }
      .vl-edges path.is-hot { stroke: #f4f7ff; stroke-width: 2.8; stroke-dasharray: 7 9; animation: vl-flow 0.7s linear infinite; }
      .vl-edges path.is-dim { opacity: 0.14; }
      .vl-cardnode {
        position: absolute;
        z-index: 2;
        transform: translate(-50%, -50%);
        width: max-content;
        min-width: 128px;
        max-width: 168px;
        border: 0;
        border-radius: 10px;
        background: #3c4d7a;
        color: #f5f7ff;
        padding: 0.55rem 0.7rem 0.48rem;
        font: 700 0.78rem/1.3 var(--font-sans, "DM Sans", system-ui, sans-serif);
        text-align: center;
        cursor: pointer;
        box-shadow: 0 10px 22px rgba(0,0,0,.28);
        transition: transform 0.2s ease, background 0.2s ease, opacity 0.25s ease, box-shadow 0.2s ease;
      }
      .vl-cardnode:hover, .vl-cardnode.is-hot {
        background: #5168a3;
        transform: translate(-50%, -54%) scale(1.04);
        z-index: 3;
        box-shadow: 0 14px 28px rgba(0,0,0,.34);
      }
      .vl-cardnode.is-dim { opacity: 0.28; }
      .vl-cardnode.is-open { outline: 2px solid #f4f7ff; outline-offset: 2px; }
      .vl-cardnode.is-done { box-shadow: inset 0 -3px 0 #4ade80, 0 10px 22px rgba(0,0,0,.28); }
      .vl-cardnode .vl-count { display: block; margin-top: 0.15rem; font-size: 0.68rem; font-weight: 650; opacity: 0.9; }
      .vl-search {
        width: min(280px, 100%);
        margin: 0 0 0.55rem;
        padding: 0.4rem 0.55rem;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,.14);
        background: #0f1419;
        color: #e8eef4;
        font: inherit;
      }
      .vl-views { display: none; }
      .vl-split { width: 6px; cursor: col-resize; background: rgba(255,255,255,.06); }
      .vl-split:hover { background: rgba(61,156,253,.45); }
      .vl-root.is-focus [data-problem] .vl-kicker,
      .vl-root.is-focus [data-problem] h3,
      .vl-root.is-focus [data-problem] > p,
      .vl-root.is-focus [data-problem] ol,
      .vl-root.is-focus .vl-tests { display: none; }
      .vl-root.is-light { background: #f4f7fb; color: #1c2836; }
      .vl-root.is-light .vl-top,
      .vl-root.is-light .vl-col,
      .vl-root.is-light .vl-col-h { background: #fff; color: #1c2836; border-color: #d5deea; }
      .vl-root.is-light .vl-codebox,
      .vl-root.is-light .vl-gutter,
      .vl-root.is-light .vl-editor,
      .vl-root.is-light .vl-search { background: #f8fafc; color: #1c2836; }
      .vl-root.is-light .vl-suggest { background: #fff; color: #1c2836; box-shadow: 0 16px 40px rgba(20,32,48,.16), inset 0 0 0 1px #d5deea; }
      .vl-root.is-light .vl-suggest small { color: #5d6d7e; }
      .vl-root.is-light .vl-nowline,
      .vl-root.is-light .vl-outbar,
      .vl-root.is-light .vl-panel { color: #1c2836; }
      .vl-back div.is-now { animation: vl-lineglow 1.2s ease-in-out infinite; }
      .vl-pick .vl-section { animation: vl-rise 0.28s ease; }
      .vl-pick-head { display: flex; justify-content: space-between; align-items: center; gap: 0.6rem; margin-bottom: 0.65rem; }
      .vl-pick-head h4 { margin: 0; }
      .vl-pick .vl-chips { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 0.55rem; }
      .vl-pick .vl-chip { width: auto; border-radius: 12px; padding: 0.6rem 0.7rem; text-align: left; }
      @keyframes vl-flow { to { stroke-dashoffset: -32; } }
      @keyframes vl-rise { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
      @keyframes vl-lineglow { 50% { background: rgba(250,204,21,.5); } }
      .vl-meter { display: block; height: 3px; margin: 0.38rem auto 0; width: 72%; background: rgba(255,255,255,.22); border-radius: 99px; overflow: hidden; }
      .vl-meter i { display: block; height: 100%; background: #3dd68c; width: 0; }
      .vl-pathbox {
        max-width: 980px;
        margin: 0.75rem auto 0;
        min-height: 3.4rem;
        background: #171d28;
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 12px;
        padding: 0.7rem 0.9rem;
        color: #d5e2f5;
      }
      .vl-pathbox strong { display: block; margin-bottom: 0.2rem; color: #f4f7ff; }
      .vl-pathbox p { margin: 0.15rem 0; }
      .vl-pick { max-width: 980px; margin: 0.7rem auto 0; }
      .vl-extra-lessons { max-width: 980px; margin: 0.8rem auto 0; display: grid; gap: 0.6rem; }
      .vl-studio-top { display: flex; justify-content: space-between; gap: 0.6rem; align-items: center; margin-bottom: 0.55rem; }
      .vl-modes { display: flex; gap: 0.35rem; flex-wrap: wrap; }
      .vl-codebox {
        display: grid;
        grid-template-columns: 3.2rem minmax(0, 1fr);
        min-height: 320px;
        border-radius: 14px;
        overflow: hidden;
        background: #101820;
        box-shadow: inset 0 0 0 1px rgba(61,156,253,.18);
      }
      .vl-gutter {
        margin: 0;
        padding: 0.85rem 0.35rem;
        overflow: hidden;
        background: #0c141c;
        color: #7d8b9a;
        font: 15px/1.55 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        text-align: right;
        user-select: none;
        white-space: pre;
      }
      .vl-gutter div { min-height: 1.55em; }
      .vl-gutter div.is-now,
      .vl-gutter div.is-bad {
        color: #1a1404;
        background: #facc15;
        border-radius: 6px;
        font-weight: 800;
      }
      .vl-gutter div.is-bad { color: #fff; background: #f87171; }
      .vl-codebox .vl-stage { position: relative; min-height: 220px; height: 100%; }
      .vl-back {
        position: absolute;
        inset: 0;
        margin: 0;
        padding: 0.85rem 0.9rem;
        overflow: hidden;
        pointer-events: none;
        color: transparent;
        white-space: pre;
        font: 15px/1.55 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        tab-size: 4;
      }
      .vl-back div { min-height: 1.55em; border-radius: 4px; }
      .vl-back div.is-now { background: rgba(250,204,21,.28); box-shadow: inset 3px 0 0 #facc15; }
      .vl-back div.is-bad { background: rgba(248,113,113,.28); box-shadow: inset 3px 0 0 #f87171; }
      .vl-codebox .vl-editor {
        position: relative;
        width: 100%;
        height: 100%;
        min-height: 320px;
        margin: 0;
        border: 0;
        border-radius: 0;
        background: transparent;
        box-shadow: none;
        resize: vertical;
        color: #e8eef4;
        font-size: 15px;
        line-height: 1.55;
        padding: 0.85rem 0.9rem;
        white-space: pre;
        overflow: auto;
      }
      .vl-run {
        font-size: 0.95rem;
        padding: 0.62rem 1rem;
        border-radius: 12px;
      }
      .vl-btn:disabled { opacity: 0.55; cursor: progress; }
      .vl-lang {
        flex: none;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        color: #9bd0ff;
        border: 1px solid rgba(124,196,255,.45);
        border-radius: 999px;
        padding: 0.18rem 0.55rem;
      }
      .vl-why { margin: 0 0 0.7rem; color: #b7c5d3; }
      .vl-why summary { cursor: pointer; font-weight: 800; color: #e8eef4; }
      .vl-lead { font-size: 1.02rem; line-height: 1.45; }
      .vl-work.is-free { grid-template-columns: minmax(280px, 1fr) 6px minmax(300px, 1.15fr); }
      .vl-work.is-free .vl-sol { display: none !important; }
      @media (max-width: 1100px) {
        .vl-pane-bar { display: flex; }
        .vl-work { display: flex; flex-direction: column; height: auto; flex: 1; min-height: 0; }
        .vl-col { display: none; border-right: 0; }
        .vl-col.is-pane { display: flex; flex: 1; min-height: 0; height: auto; }
        .vl-split { display: none; }
        .vl-live { grid-template-columns: minmax(0, 1fr) minmax(132px, 0.42fr); }
      }
      @media (max-width: 768px) {
        .vl-launch-bar { position: static; transform: none; }
        .vl-banner { flex-direction: column; align-items: flex-start; }
      }
      @media (prefers-reduced-motion: reduce) {
        .vl-out-ready { box-shadow: none; }
        .vl-cell.is-changed, .vl-node.is-changed, .vl-var.is-changed, .vl-stack i.is-top, .vl-queue i.is-front, .vl-bar.is-changed, .vl-grid td.is-changed, .vl-cell.is-enter, .vl-cell.is-read, .vl-ptr,
        .vl-edges path.is-hot, .vl-cardnode, .vl-pick .vl-section, .vl-nowline, .vl-picture, .vl-back div.is-now {
          animation: none;
        }
      }
    `;
    document.head.appendChild(style);
  }

  function ensureRoot() {
    if (ui.root) return;
    const root = document.createElement("div");
    root.className = "vl-root";
    root.hidden = true;
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.setAttribute("aria-label", "DSA visual lab");
    root.innerHTML = `
      <div class="vl-top">
        <button type="button" class="vl-btn ghost" data-act="back">Roadmap</button>
        <button type="button" class="vl-btn" data-act="blank">New code</button>
        <h2 data-title>Visual Lab</h2>
        <button type="button" class="vl-btn" data-act="lesson">Read lesson</button>
        <button type="button" class="vl-btn" data-act="reveal">Show solution code</button>
        <button type="button" class="vl-btn ghost" data-act="focus" title="Hide the lesson text and keep the editor and Watch panel">Focus</button>
        <button type="button" class="vl-btn ghost" data-act="theme" title="Switch the lab between dark and light">Theme</button>
        <span class="vl-lang" data-lang hidden>Python 3</span>
        <button type="button" class="vl-btn ghost" data-act="home" hidden>Portfolio</button>
        <button type="button" class="vl-btn ghost" data-act="close">Close</button>
      </div>
      <div class="vl-pane-bar">
        <button type="button" class="vl-btn" data-pane="problem">Code</button>
        <button type="button" class="vl-btn" data-pane="you">Watch</button>
      </div>
      <div class="vl-body" data-body></div>
    `;
    document.body.appendChild(root);
    ui.root = root;
    ui.title = root.querySelector("[data-title]");
    ui.body = root.querySelector("[data-body]");
    ui.back = root.querySelector("[data-act=back]");
    ui.lesson = root.querySelector("[data-act=lesson]");
    ui.playboth = null;
    ui.reveal = root.querySelector("[data-act=reveal]");
    root.addEventListener("click", onRootClick);
    applyUiPrefs();
  }

  function loadUi() {
    try { return JSON.parse(localStorage.getItem(UI_KEY) || "{}"); } catch (err) { return {}; }
  }

  function saveUi() {
    localStorage.setItem(UI_KEY, JSON.stringify({
      fontSize: state.fontSize,
      rate: state.rate,
      theme: ui.root && ui.root.classList.contains("is-light") ? "light" : "dark",
      focus: !!(ui.root && ui.root.classList.contains("is-focus")),
    }));
  }

  function applyUiPrefs() {
    const saved = loadUi();
    if (saved.fontSize) state.fontSize = saved.fontSize;
    if (saved.rate && RATES[saved.rate]) state.rate = saved.rate;
    if (saved.theme === "light") ui.root.classList.add("is-light");
    if (saved.focus) ui.root.classList.add("is-focus");
  }

  function toggleFocus() {
    ui.root.classList.toggle("is-focus");
    saveUi();
  }

  function toggleTheme() {
    ui.root.classList.toggle("is-light");
    saveUi();
  }

  function applyCodeSize() {
    const size = state.fontSize + "px";
    [ui.editor, ui.gutter, ui.back].forEach((el) => {
      if (el) el.style.fontSize = size;
    });
  }

  function onRootClick(event) {
    const act = event.target.closest("[data-act]")?.dataset.act;
    if (act === "close") closeLab();
    if (act === "home") leaveEditor();
    if (act === "back") showMap();
    if (act === "lesson") openLesson();
    if (act === "reveal") toggleReveal();
    if (act === "focus") toggleFocus();
    if (act === "theme") toggleTheme();
    if (act === "playboth") play("both");
    if (act === "playground") showPlayground();
    if (act === "blank") openBlankEditor();
    const pane = event.target.closest("[data-pane]")?.dataset.pane;
    if (pane) setPane(pane);
  }

  function setPane(name) {
    ui.root.querySelectorAll(".vl-col").forEach((col) => {
      col.classList.toggle("is-pane", col.dataset.col === name);
    });
    ui.root.querySelectorAll("[data-pane]").forEach((btn) => {
      btn.classList.toggle("primary", btn.dataset.pane === name);
    });
    requestAnimationFrame(revealCurrentStep);
  }

  function stopPlay() {
    state.playing = null;
    if (state.timer) {
      clearTimeout(state.timer);
      clearInterval(state.timer);
    }
    state.timer = null;
    if (ui.playboth) ui.playboth.textContent = "Play both";
  }

  function play(which) {
    if (state.playing === which) {
      stopPlay();
      return;
    }
    stopPlay();
    state.playing = which;
    if (which === "both" && ui.playboth) ui.playboth.textContent = "Pause";
    const tick = () => {
      if (state.playing !== which) return;
      let moved = false;
      if (which === "you" || which === "both") moved = step("you", 1) || moved;
      if (which === "sol" || which === "both") moved = step("sol", 1) || moved;
      if (!moved) {
        stopPlay();
        return;
      }
      const wait = Math.max(RATES[state.rate] || 520, motionMs(state.rate) + 60);
      state.timer = setTimeout(tick, wait);
    };
    state.timer = setTimeout(tick, 80);
  }

  function step(side, delta) {
    const trace = state[side];
    if (!trace.frames.length) return false;
    const next = clampIndex(trace.i + delta, trace.frames.length);
    if (next === trace.i && delta !== 0) return false;
    trace.i = next;
    paintSide(side);
    return true;
  }

  function jump(side, index) {
    stopPlay();
    const trace = state[side];
    if (!trace.frames.length) return;
    trace.i = clampIndex(index, trace.frames.length);
    paintSide(side);
  }

  function openLab() {
    ensureRoot();
    state.open = true;
    ui.root.hidden = false;
    document.body.classList.add("vl-open");
  }

  function closeLab() {
    stopPlay();
    state.open = false;
    if (ui.root) ui.root.hidden = true;
    document.body.classList.remove("vl-open");
    if (location.hash.startsWith("#vl")) {
      history.pushState(null, "", location.pathname + location.search);
    }
  }

  function showMap() {
    stopPlay();
    openLab();
    state.view = "map";
    state.topicId = null;
    if (location.hash !== "#vl") history.pushState(null, "", "#vl");
    ui.title.textContent = "Course roadmap";
    ui.back.hidden = true;
    ui.lesson.hidden = true;
    ui.reveal.hidden = true;
    ui.root.querySelector(".vl-pane-bar").hidden = true;
    paintMap();
  }

  function showTopic(id) {
    if (id === "playground") {
      showPlayground();
      return;
    }
    const problem = problems()[id];
    const meta = topicMeta(id);
    if (!problem || !meta) {
      showMap();
      return;
    }
    stopPlay();
    openLab();
    state.view = "work";
    state.topicId = id;
    state.free = false;
    state.lens = "you";
    state.testIndex = 0;
    state.you = emptyTrace();
    state.sol = emptyTrace();
    state.tests = problem.tests.map(() => ({ status: "idle", got: "", error: "" }));
    const hash = "#vl/" + id;
    if (location.hash !== hash) history.pushState(null, "", hash);
    ui.title.textContent = meta.topic.title;
    ui.back.hidden = false;
    ui.lesson.hidden = false;
    ui.reveal.hidden = false;
    ui.root.querySelector(".vl-pane-bar").hidden = false;
    const opened = loadStore();
    if (opened.status[id] !== "solved") {
      opened.status[id] = opened.status[id] || "tried";
      saveStore(opened);
      paintNavMarks();
    }
    paintWorkspace();
  }

  function openEditorWith(code) {
    state.seedCode = String(code || "");
    state.blank = false;
    showPlayground();
  }

  function openBlankEditor() {
    const saved = loadStore();
    const current = ui.editor && state.view === "work" ? ui.editor.value : (saved.code["free:play"] || "");
    if (current.trim() && !window.confirm("Open a blank editor? The code in this playground will be replaced.")) return;
    state.blank = true;
    showPlayground();
  }

  function showPlayground() {
    stopPlay();
    openLab();
    state.view = "work";
    state.topicId = null;
    state.free = true;
    state.testIndex = 0;
    state.you = emptyTrace();
    state.sol = emptyTrace();
    state.tests = [];
    if (!editorOnly() && location.hash !== "#vl/playground") history.pushState(null, "", "#vl/playground");
    ui.title.textContent = editorOnly() ? "Python editor" : "My own code";
    ui.back.hidden = editorOnly();
    ui.lesson.hidden = true;
    ui.reveal.hidden = true;
    paintEditorHome();
    ui.root.querySelector(".vl-pane-bar").hidden = false;
    state.lens = "you";
    paintWorkspace();
  }

  function openLesson() {
    if (store.status[id] !== "solved") {
      store.status[id] = store.status[id] || "tried";
      saveStore(store);
      paintNavMarks();
    }
  }

  function openLesson() {
    const id = state.topicId;
    closeLab();
    if (!id) return;
    location.hash = id;
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function toggleReveal() {
    state.reveal = !state.reveal;
    localStorage.setItem(REVEAL_KEY, state.reveal ? "1" : "0");
    ui.reveal.textContent = state.reveal ? "Hide solution code" : "Show solution code";
    if (state.reveal && !state.free) chooseLens("sol");
    else paintSide(shownSide());
  }

  const ROAD = [
    { id: "arrays", name: "Arrays & Hashing", x: 50, y: 8, parents: [] },
    { id: "twopointers", name: "Two Pointers", x: 34, y: 20, parents: ["arrays"] },
    { id: "stack", name: "Stack", x: 68, y: 20, parents: ["arrays"] },
    { id: "binary", name: "Binary Search", x: 16, y: 33, parents: ["twopointers"] },
    { id: "window", name: "Sliding Window", x: 40, y: 33, parents: ["twopointers"] },
    { id: "linked", name: "Linked List", x: 74, y: 33, parents: ["stack"] },
    { id: "trees", name: "Trees", x: 44, y: 46, parents: ["binary", "window", "linked"] },
    { id: "tries", name: "Tries", x: 26, y: 58, parents: ["trees"] },
    { id: "backtracking", name: "Backtracking", x: 64, y: 58, parents: ["trees"] },
    { id: "heap", name: "Heap / Priority Queue", x: 28, y: 70, parents: ["tries"] },
    { id: "graphs", name: "Graphs", x: 50, y: 70, parents: ["backtracking"] },
    { id: "dp1", name: "1-D Dynamic Programming", x: 76, y: 70, parents: ["backtracking"] },
    { id: "intervals", name: "Intervals", x: 14, y: 82, parents: ["heap"] },
    { id: "greedy", name: "Greedy", x: 32, y: 82, parents: ["heap"] },
    { id: "advgraphs", name: "Advanced Graphs", x: 50, y: 82, parents: ["heap", "graphs"] },
    { id: "dp2", name: "2-D Dynamic Programming", x: 68, y: 82, parents: ["graphs", "dp1"] },
    { id: "bits", name: "Bit Manipulation", x: 86, y: 82, parents: ["dp1"] },
    { id: "math", name: "Math & Geometry", x: 68, y: 94, parents: ["advgraphs", "dp2", "bits"] },
  ];

  let roadPick = null;
  let roadHover = null;
  let roadObserver = null;

  function topicGroup(id) {
    const match = /^topic-(\d+)-(\d+)$/.exec(id);
    if (!match) return "more";
    const section = Number(match[1]);
    const n = Number(match[2]);
    if (section <= 3) return "start";
    if (section === 4 || section === 18) return "math";
    if (section === 5 && n === 4) return "twopointers";
    if (section === 5 && n === 5) return "window";
    if (section === 5 && n === 9) return "binary";
    if (section === 5) return "arrays";
    if (section === 6 && n >= 2 && n <= 4) return "binary";
    if (section === 6) return "arrays";
    if (section === 7 && n >= 12) return "tries";
    if (section === 7) return "arrays";
    if (section === 8) return "linked";
    if (section === 9 && n === 8) return "heap";
    if (section === 9) return "stack";
    if (section === 10) return "arrays";
    if (section === 11 && n === 12) return "tries";
    if (section === 11) return "trees";
    if (section === 12) return "heap";
    if (section === 13 && n >= 16) return "advgraphs";
    if (section === 13) return "graphs";
    if (section === 14) return "backtracking";
    if (section === 15 && [7, 10, 12, 13, 14, 15, 16, 17, 18, 20].indexOf(n) >= 0) return "dp2";
    if (section === 15) return "dp1";
    if (section === 16) return "bits";
    if (section === 17 && (n === 1 || n === 5 || n === 6)) return "intervals";
    if (section === 17) return "greedy";
    return "more";
  }

  function roadNode(id) {
    return ROAD.find((node) => node.id === id);
  }

  function ancestorSet(id) {
    const seen = new Set();
    const walk = (nodeId) => {
      if (seen.has(nodeId)) return;
      seen.add(nodeId);
      const node = roadNode(nodeId);
      (node ? node.parents : []).forEach(walk);
    };
    walk(id);
    return seen;
  }

  function learningChains(id) {
    const node = roadNode(id);
    if (!node) return [];
    if (!node.parents.length) return [[node.name]];
    const chains = [];
    node.parents.forEach((parentId) => {
      learningChains(parentId).forEach((chain) => chains.push(chain.concat(node.name)));
    });
    return chains;
  }

  function paintMap() {
    const store = loadStore();
    const map = courseMap();
    const all = map.flatMap((section) => section.topics);
    const solved = all.filter((topic) => store.status[topic.id] === "solved").length;
    const grouped = {};
    all.forEach((topic) => {
      const key = topicGroup(topic.id);
      if (!grouped[key]) grouped[key] = [];
      grouped[key].push(topic);
    });
    ui.body.innerHTML = `
      <div class="vl-map">
        <div class="vl-map-head">
          <div>
            <p class="vl-kicker">Learn in order</p>
            <h3>Roadmap</h3>
            <p>Hover a card to light the path you should learn first. Click a card to open only that card’s problems.</p>
          </div>
          <div class="vl-road-actions">
            <p class="vl-progress"><strong>${solved}</strong> / ${all.length} solved</p>
            <button type="button" class="vl-btn primary" data-act="playground">Run my own code</button>
          </div>
        </div>
        <div class="vl-tree-wrap">
          <div class="vl-tree" data-tree>
            <svg class="vl-edges" data-edges preserveAspectRatio="none"></svg>
          </div>
        </div>
        <div class="vl-pathbox" data-path><strong>Hover a card</strong><p>The path lights up from the start to that card.</p></div>
        <div class="vl-road-more">
          <button type="button" class="vl-btn" data-group="start">Foundations</button>
          <button type="button" class="vl-btn" data-group="more">Also in this course</button>
        </div>
        <div class="vl-pick" data-pick></div>
      </div>
    `;
    const tree = ui.body.querySelector("[data-tree]");
    const svg = ui.body.querySelector("[data-edges]");
    const pathBox = ui.body.querySelector("[data-path]");
    const pick = ui.body.querySelector("[data-pick]");
    const groupButtons = [...ui.body.querySelectorAll("[data-group]")];
    const byId = {};
    ROAD.forEach((node) => { byId[node.id] = node; });
    const buttons = [];
    const paths = [];

    function layoutEdges() {
      const width = tree.clientWidth;
      const height = tree.clientHeight;
      if (!width || !height) return;
      svg.setAttribute("viewBox", "0 0 " + width + " " + height);
      const origin = tree.getBoundingClientRect();
      paths.forEach((path) => {
        const from = tree.querySelector('[data-node="' + path.dataset.from + '"]');
        const to = tree.querySelector('[data-node="' + path.dataset.to + '"]');
        if (!from || !to) return;
        const a = from.getBoundingClientRect();
        const b = to.getBoundingClientRect();
        const x1 = a.left + a.width / 2 - origin.left;
        const y1 = a.bottom - origin.top;
        const x2 = b.left + b.width / 2 - origin.left;
        const y2 = b.top - origin.top;
        const bend = Math.max(28, (y2 - y1) / 2);
        path.setAttribute("d", "M " + x1 + " " + y1 + " C " + x1 + " " + (y1 + bend) + ", " + x2 + " " + (y2 - bend) + ", " + x2 + " " + y2);
        if (!path.dataset.drawn) {
          const len = path.getTotalLength();
          path.style.strokeDasharray = String(len);
          path.style.strokeDashoffset = String(len);
          path.dataset.drawn = "1";
          requestAnimationFrame(() => {
            path.style.transition = "stroke-dashoffset 0.65s ease, stroke 0.25s ease, opacity 0.25s ease, stroke-width 0.25s ease";
            path.style.strokeDashoffset = "0";
          });
          path.addEventListener("transitionend", (event) => {
            if (event.propertyName !== "stroke-dashoffset") return;
            path.style.strokeDasharray = "";
            path.style.strokeDashoffset = "";
          }, { once: true });
        }
      });
    }

    ROAD.forEach((node) => {
      node.parents.forEach((parentId) => {
        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        path.dataset.from = parentId;
        path.dataset.to = node.id;
        svg.appendChild(path);
        paths.push(path);
      });
    });

    function openGroup(id) {
      roadPick = roadPick === id ? null : id;
      paintPick();
      buttons.forEach((item) => item.classList.toggle("is-open", item.dataset.node === roadPick));
      groupButtons.forEach((item) => item.classList.toggle("primary", item.dataset.group === roadPick));
      if (roadPick && pick.firstElementChild) pick.firstElementChild.scrollIntoView({ behavior: "smooth", block: "nearest" });
      requestAnimationFrame(layoutEdges);
    }
    ROAD.forEach((node) => {
      const topics = grouped[node.id] || [];
      const done = topics.filter((topic) => store.status[topic.id] === "solved").length;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "vl-cardnode" + (roadPick === node.id ? " is-open" : "") + (topics.length && done === topics.length ? " is-done" : "");
      btn.style.left = node.x + "%";
      btn.style.top = node.y + "%";
      btn.dataset.node = node.id;
      const pct = topics.length ? Math.round((done / topics.length) * 100) : 0;
      btn.innerHTML = esc(node.name) + '<span class="vl-count">' + done + "/" + topics.length + " solved</span>" + '<span class="vl-meter"><i style="width:' + pct + '%"></i></span>';
      btn.addEventListener("mouseenter", () => showPath(node.id));
      btn.addEventListener("focus", () => showPath(node.id));
      btn.addEventListener("click", () => openGroup(node.id));
      tree.appendChild(btn);
      buttons.push(btn);
    });
    tree.addEventListener("mouseleave", () => showPath(null));

    function showPath(id) {
      roadHover = id;
      const hot = id ? ancestorSet(id) : null;
      buttons.forEach((btn) => {
        btn.classList.toggle("is-hot", !!(hot && hot.has(btn.dataset.node)));
        btn.classList.toggle("is-dim", !!(hot && !hot.has(btn.dataset.node)));
      });
      paths.forEach((path) => {
        const on = !!(hot && hot.has(path.dataset.from) && hot.has(path.dataset.to));
        path.classList.toggle("is-hot", on);
        path.classList.toggle("is-dim", !!(hot && !on));
      });
      if (!id) {
        pathBox.innerHTML = "<strong>Hover a card</strong><p>The path lights up from the start to that card.</p>";
        return;
      }
      const node = byId[id];
      const chains = learningChains(id).slice().sort((a, b) => a.length - b.length);
      if (!node.parents.length) {
        pathBox.innerHTML = "<strong>Start here</strong><p>" + esc(node.name) + " is the first card. Learn it before the cards below it.</p>";
        return;
      }
      const before = chains[0].slice(0, -1).map(esc).join("  →  ");
      const direct = node.parents.map((parentId) => esc(byId[parentId].name));
      const extra = direct.length > 1
        ? "<p>The lit cards are everything that comes before this one. It sits after " + direct.join(", ") + ".</p>"
        : "<p>The lit cards are the ones to learn before this one.</p>";
      pathBox.innerHTML = "<strong>Learn this first</strong><p>" + before + "  →  <strong>" + esc(node.name) + "</strong></p>" + extra;
    }

    function paintPick() {
      pick.innerHTML = "";
      if (!roadPick) return;
      const node = byId[roadPick];
      const titles = { start: "Foundations", more: "Also in this course" };
      const title = node ? node.name : (titles[roadPick] || "Problems");
      const topics = grouped[roadPick] || [];
      const card = document.createElement("section");
      card.className = "vl-section";
      const head = document.createElement("div");
      head.className = "vl-pick-head";
      head.innerHTML = "<h4>" + esc(title) + " · " + topics.length + " problems</h4>";
      const close = document.createElement("button");
      close.type = "button";
      close.className = "vl-btn ghost";
      close.textContent = "Close";
      close.addEventListener("click", () => openGroup(roadPick));
      head.appendChild(close);
      card.appendChild(head);
      const tools = document.createElement("div");
      tools.className = "vl-editor-actions";
      const search = document.createElement("input");
      search.className = "vl-search";
      search.type = "search";
      search.placeholder = "Search problems";
      search.value = state.pickQuery;
      search.setAttribute("aria-label", "Search problems");
      search.addEventListener("input", () => {
        state.pickQuery = search.value;
        paintPick();
        const again = pick.querySelector(".vl-search");
        if (again) {
          again.focus();
          again.selectionStart = again.selectionEnd = again.value.length;
        }
      });
      tools.appendChild(search);
      [["all", "All"], ["tried", "Started"], ["solved", "Solved"]].forEach(([id, label]) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "vl-btn" + (state.pickStatus === id ? " primary" : "");
        btn.textContent = label;
        btn.addEventListener("click", () => {
          state.pickStatus = id;
          paintPick();
        });
        tools.appendChild(btn);
      });
      card.appendChild(tools);
      const chips = document.createElement("div");
      chips.className = "vl-chips";
      const query = state.pickQuery.trim().toLowerCase();
      const shown = topics.filter((topic) => {
        const status = store.status[topic.id] || "";
        if (state.pickStatus === "solved" && status !== "solved") return false;
        if (state.pickStatus === "tried" && !status) return false;
        if (!query) return true;
        const problem = problems()[topic.id];
        const hay = (topic.title + " " + (problem ? problem.title : "")).toLowerCase();
        return hay.indexOf(query) >= 0;
      });
      if (!shown.length) {
        const empty = document.createElement("p");
        empty.textContent = topics.length ? "No problems match this search." : "No problems are filed under this card yet.";
        card.appendChild(empty);
      }
      shown.forEach((topic) => {
        const status = store.status[topic.id] || "";
        const problem = problems()[topic.id];
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "vl-chip" + (status === "solved" ? " is-solved" : status ? " is-tried" : "");
        chip.innerHTML = esc(topic.title) + (problem ? "<small>" + esc(problem.title) + "</small>" : "");
        chip.addEventListener("click", () => showTopic(topic.id));
        chips.appendChild(chip);
      });
      card.appendChild(chips);
      pick.appendChild(card);
    }

    groupButtons.forEach((btn) => {
      btn.classList.toggle("primary", btn.dataset.group === roadPick);
      btn.addEventListener("click", () => openGroup(btn.dataset.group));
    });
    if (roadObserver) roadObserver.disconnect();
    roadObserver = new ResizeObserver(() => layoutEdges());
    roadObserver.observe(tree);
    requestAnimationFrame(layoutEdges);
    paintPick();
    if (roadHover) showPath(roadHover);
  }

  function bindSplit(handle) {
    handle.addEventListener("pointerdown", (event) => {
      event.preventDefault();
      const work = handle.parentElement;
      const move = (ev) => {
        const rect = work.getBoundingClientRect();
        const x = Math.min(0.72, Math.max(0.28, (ev.clientX - rect.left) / rect.width));
        work.style.gridTemplateColumns = x + "fr 6px " + (1 - x) + "fr";
      };
      const up = () => {
        window.removeEventListener("pointermove", move);
        window.removeEventListener("pointerup", up);
      };
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", up);
    });
  }

  function currentProblem() {
    return problems()[state.topicId];
  }

  function currentCode() {
    return ui.editor ? ui.editor.value : "";
  }

  function paintWorkspace() {
    const problem = state.free ? null : currentProblem();
    const meta = state.topicId ? topicMeta(state.topicId) : null;
    const store = loadStore();
    const key = state.free ? "free:" + (state.topicId || "play") : state.topicId;
    const saved = key ? store.code[key] : "";
    ui.reveal.textContent = state.reveal ? "Hide solution code" : "Show solution code";
    ui.reveal.hidden = !!state.free || !problem;
    ui.body.innerHTML = `
      <div class="vl-work${state.free ? " is-free" : ""}">
        <section class="vl-col vl-problem is-pane" data-col="problem">
          <div class="vl-col-h">${editorOnly() ? "Python" : "Write code"}</div>
          <div class="vl-scroll vl-problem" data-problem></div>
        </section>
        <div class="vl-split" data-split title="Drag to resize"></div>
        <section class="vl-col vl-you" data-col="you">
          <div class="vl-col-h vl-lens">
            <button type="button" class="vl-btn${state.lens === "sol" ? "" : " primary"}" data-lens="you">My code</button>
            ${state.free ? "" : '<button type="button" class="vl-btn' + (state.lens === "sol" ? " primary" : "") + '" data-lens="sol">Lesson answer</button>'}
          </div>
          <div class="vl-scroll" data-viz="you"></div>
          <div class="vl-transport" data-transport="you"></div>
        </section>
      </div>
    `;
    ui.youViz = ui.body.querySelector('[data-viz="you"]');
    ui.solViz = ui.youViz;
    const split = ui.body.querySelector("[data-split]");
    if (split) bindSplit(split);
    ui.body.querySelectorAll("[data-lens]").forEach((btn) => {
      btn.addEventListener("click", () => chooseLens(btn.dataset.lens));
    });
    const box = ui.body.querySelector("[data-problem]");
    const lessonProblem = currentProblem();
    let intro = `
      <p class="vl-kicker">Playground</p>
      <h3>Run any Python</h3>
      <p>Type a program. Press Run. Each line, the stored values, and the printed words show up on the right.</p>
    `;
    if (lessonProblem && meta && !state.free) {
      const examples = lessonProblem.tests
        .map((test) => `<li><code>${esc(test.call)}</code> → <code>${esc(test.expect)}</code></li>`)
        .join("");
      intro = `
        <p class="vl-kicker">${esc(meta.section.title)}</p>
        <h3>${esc(lessonProblem.title)}</h3>
        <p>${esc(lessonProblem.prompt)}</p>
        <details class="vl-why">
          <summary>Why this works</summary>
          <p>${esc(lessonProblem.idea)}</p>
          <ol>${lessonProblem.steps.map((step) => `<li>${esc(step)}</li>`).join("")}</ol>
        </details>
        <p>Examples</p>
        <ul>${examples}</ul>
      `;
    }
    const modes = lessonProblem ? `
      <div class="vl-modes">
        <button type="button" class="vl-btn${state.free ? "" : " primary"}" data-mode="lesson">Practice this problem</button>
        <button type="button" class="vl-btn${state.free ? " primary" : ""}" data-mode="free">My own code</button>
      </div>
    ` : "";
    box.innerHTML = `
      ${modes}
      ${lessonProblem && meta && !state.free ? intro : ""}
      <div class="vl-codebox">
        <div class="vl-gutter" data-gutter></div>
        <div class="vl-stage">
          <div class="vl-back" data-back></div>
          <textarea class="vl-editor" wrap="off" spellcheck="false" aria-label="Your Python code" placeholder="${editorOnly() ? "Write Python here" : ""}" autocomplete="off"></textarea>
        </div>
      </div>
      <div class="vl-editor-actions">
        <button type="button" class="vl-btn primary vl-run" data-run title="Run Python (Ctrl or Cmd + Enter)">${editorOnly() ? "Run Python" : "Run and watch"}</button>
        ${lessonProblem && !state.free ? '<button type="button" class="vl-btn" data-grade>Check examples</button>' : ""}
        <button type="button" class="vl-btn ghost" data-reset>Reset</button>
        <button type="button" class="vl-btn ghost" data-copy>Copy</button>
        <button type="button" class="vl-btn ghost" data-tidy>Tidy</button>
        <button type="button" class="vl-btn ghost" data-font="-1" title="Smaller text">A−</button>
        <button type="button" class="vl-btn ghost" data-font="1" title="Larger text">A+</button>
        ${state.free ? '<select data-sample aria-label="Sample program"><option value="">Sample program</option><option value="array">Array total</option><option value="stack">Stack</option><option value="queue">Queue</option><option value="dict">Dictionary</option></select>' : ""}
      </div>
      <div class="vl-grade" data-grade-msg></div>
      <div class="vl-tests" data-tests></div>
    `;
    ui.editor = box.querySelector("textarea");
    ui.gutter = box.querySelector("[data-gutter]");
    ui.back = box.querySelector("[data-back]");
    const fallback = state.free || !lessonProblem ? FREE_CODE : lessonProblem.starter;
    const oldStarter = "# Change anything, then press Run.\n" + FREE_CODE;
    const seeded = state.seedCode != null;
    const seed = state.seedCode;
    state.seedCode = null;
    const useBlank = !!state.blank;
    state.blank = false;
    const stored = typeof saved === "string" && saved !== oldStarter ? saved : fallback;
    ui.editor.value = useBlank ? "" : seeded ? seed : stored;
    ui.line = box.querySelector("[data-line]");
    ui.grade = box.querySelector("[data-grade-msg]");
    ui.tests = box.querySelector("[data-tests]");
    ui.editor.addEventListener("keydown", (event) => {
      if (suggestKey(event)) return;
      if (event.key === "Tab") {
        event.preventDefault();
        const start = ui.editor.selectionStart;
        const end = ui.editor.selectionEnd;
        ui.editor.value = ui.editor.value.slice(0, start) + "    " + ui.editor.value.slice(end);
        ui.editor.selectionStart = ui.editor.selectionEnd = start + 4;
        onCodeEdited();
      }
    });
    ui.editor.addEventListener("input", () => {
      onCodeEdited();
      suggestRefresh(false);
    });
    if (useBlank || seeded) {
      onCodeEdited();
      setPane("problem");
      ui.editor.focus();
    }
    ui.editor.addEventListener("scroll", syncEditorScroll);
    markPointer(0, false);
    applyCodeSize();
    box.querySelector("[data-run]").addEventListener("click", () => runUser(true));
    const gradeBtn = box.querySelector("[data-grade]");
    if (gradeBtn) gradeBtn.addEventListener("click", () => runUser(false));
    box.querySelector("[data-reset]").addEventListener("click", () => {
      const starter = state.free || !lessonProblem ? FREE_CODE : lessonProblem.starter;
      if (ui.editor.value !== starter && !window.confirm("Replace the editor with the starter code?")) return;
      ui.editor.value = starter;
      onCodeEdited();
    });
    box.querySelector("[data-copy]").addEventListener("click", () => {
      const text = ui.editor.value;
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text);
    });
    box.querySelector("[data-tidy]").addEventListener("click", () => {
      ui.editor.value = ui.editor.value.split("\n").map((line) => line.replace(/[ \t]+$/g, "")).join("\n");
      onCodeEdited();
    });
    box.querySelectorAll("[data-font]").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.fontSize = Math.min(22, Math.max(12, state.fontSize + Number(btn.dataset.font)));
        applyCodeSize();
        saveUi();
      });
    });
    const sample = box.querySelector("[data-sample]");
    if (sample) {
      sample.addEventListener("change", () => {
        const next = SAMPLE_CODE[sample.value];
        if (!next) return;
        if (ui.editor.value.trim() && ui.editor.value !== next && !window.confirm("Replace the editor with this sample?")) {
          sample.value = "";
          return;
        }
        ui.editor.value = next;
        sample.value = "";
        onCodeEdited();
      });
    }
    box.querySelectorAll("[data-mode]").forEach((btn) => {
      btn.addEventListener("click", () => {
        persistCode();
        state.free = btn.dataset.mode === "free";
        state.lens = "you";
        state.you = emptyTrace();
        state.sol = emptyTrace();
        paintWorkspace();
      });
    });
    paintTests();
    paintSide("you");
    if (!state.free) paintSide("sol");
    setPane("problem");
    if (!state.free) ensureSolutionTrace();
    clearTimeout(refreshTimer);
    if (ui.editor && ui.editor.value.trim() && !state.you.frames.length && !state.you.running) {
      const token = ++state.runToken;
      state.you.note = "Drawing the path from this code…";
      paintSide("you");
      refreshTimer = setTimeout(() => refreshPicture(token), 350);
    }
  }

  function persistCode() {
    if (!ui.editor) return;
    const store = loadStore();
    const key = state.free ? "free:" + (state.topicId || "play") : state.topicId;
    if (!key) return;
    store.code[key] = ui.editor.value;
    saveStore(store);
  }

  function paintTests() {
    if (!ui.tests) return;
    ui.tests.innerHTML = "";
    const problem = state.free ? null : currentProblem();
    if (!problem) return;
    problem.tests.forEach((test, index) => {
      const result = state.tests[index] || { status: "idle" };
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "vl-test" + (index === state.testIndex ? " is-on" : "") + (result.status === "pass" ? " pass" : result.status === "fail" ? " fail" : "");
      btn.textContent = test.call + (result.status === "pass" ? " ✓" : result.status === "fail" ? " ✗" : "");
      btn.title = result.error || (result.got ? "Your return: " + result.got : "Expected " + test.expect);
      btn.addEventListener("click", () => {
        state.testIndex = index;
        paintTests();
        state.you = emptyTrace();
        state.sol = emptyTrace();
        paintSide("you");
        paintSide("sol");
        ensureSolutionTrace();
      });
      ui.tests.appendChild(btn);
    });
  }

  function paintNavMarks() {
    const store = loadStore();
    document.querySelectorAll(".layout > nav a[href^='#topic-']").forEach((link) => {
      const id = (link.getAttribute("href") || "").slice(1);
      link.classList.toggle("vl-done", store.status[id] === "solved");
    });
  }

  async function loadPy() {
    if (pyodide) return pyodide;
    if (!pyodideLoading) {
      pyodideLoading = (async () => {
        if (!window.loadPyodide) {
          await new Promise((resolve, reject) => {
            const script = document.createElement("script");
            script.src = PYODIDE_BASE + "pyodide.js";
            script.onload = resolve;
            script.onerror = () => reject(new Error("Python engine failed to download. Check your connection and try again."));
            document.head.appendChild(script);
          });
        }
        const engine = await window.loadPyodide({ indexURL: PYODIDE_BASE });
        engine.runPython(TRACER);
        pyodide = engine;
        return engine;
      })();
    }
    return pyodideLoading;
  }

  async function pythonCall(fn, source, call) {
    const engine = await loadPy();
    engine.globals.set("_vl_src", source);
    engine.globals.set("_vl_call", call);
    const raw = engine.runPython(fn + "(_vl_src, _vl_call)");
    return JSON.parse(String(raw));
  }

  async function ensureSolutionTrace() {
    const problem = currentProblem();
    if (!problem) return;
    const call = problem.tests[state.testIndex].call;
    const key = state.topicId + "\n" + call;
    if (state.sol.key === key && state.sol.frames.length) return;
    state.sol = emptyTrace();
    state.sol.running = true;
    state.sol.key = key;
    paintSide("sol");
    try {
      const data = await pythonCall("run_traced", problem.solution, call);
      if (state.sol.key !== key) return;
      state.sol = {
        frames: data.frames || [],
        i: 0,
        error: data.error,
        stdout: data.stdout || "",
        result: data.result_repr,
        running: false,
        key,
      };
    } catch (err) {
      state.sol = emptyTrace();
      state.sol.error = err.message || String(err);
      state.sol.key = key;
    }
    paintSide("sol");
  }

  function hasTopLevelWork(source) {
    return String(source || "").split("\n").some((line) => {
      if (/^\s/.test(line)) return false;
      const text = line.trim();
      if (!text || text.startsWith("#")) return false;
      if (/^(def|class|@|import|from)\b/.test(text)) return false;
      return true;
    });
  }

  function applyUserTrace(data, script) {
    state.you = {
      frames: data.frames || [],
      i: 0,
      error: data.error,
      errorLine: data.error_line || 0,
      stdout: data.stdout || "",
      result: data.result_repr,
      running: false,
      script: !!script,
      note: "",
    };
    paintSide("you");
  }

  let refreshTimer = 0;

  function syncEditorScroll() {
    if (!ui.editor) return;
    if (ui.back) {
      ui.back.scrollTop = ui.editor.scrollTop;
      ui.back.scrollLeft = ui.editor.scrollLeft;
    }
    if (ui.gutter) ui.gutter.scrollTop = ui.editor.scrollTop;
  }

  function markPointer(line, bad) {
    if (!ui.editor || !ui.gutter || !ui.back) return;
    const lines = ui.editor.value.split("\n");
    const cls = bad ? "is-bad" : "is-now";
    ui.gutter.innerHTML = lines.map((_, index) => {
      const on = index + 1 === line;
      return "<div" + (on ? " class=\"" + cls + "\"" : "") + ">" + (on ? "▶" : String(index + 1)) + "</div>";
    }).join("");
    ui.back.innerHTML = lines.map((text, index) => {
      const on = index + 1 === line;
      return "<div" + (on ? " class=\"" + cls + "\"" : "") + ">" + (esc(text) || " ") + "</div>";
    }).join("");
    if (line > 0 && ui.back.children[line - 1]) {
      const row = ui.back.children[line - 1];
      const top = row.offsetTop;
      const viewTop = ui.editor.scrollTop;
      const viewBottom = viewTop + ui.editor.clientHeight;
      if (top < viewTop + 8 || top + row.offsetHeight > viewBottom - 8) {
        ui.editor.scrollTop = Math.max(0, top - ui.editor.clientHeight * 0.35);
      }
    }
    syncEditorScroll();
    if (ui.line) {
      ui.line.classList.toggle("is-live", line > 0 && !bad);
      ui.line.classList.toggle("is-bad", line > 0 && !!bad);
    }
  }

  function onCodeEdited() {
    persistCode();
    stopPlay();
    clearTimeout(refreshTimer);
    const token = ++state.runToken;
    state.you = emptyTrace();
    state.you.note = "You changed the code. The path is being drawn from these new lines.";
    if (ui.grade) {
      ui.grade.className = "vl-grade";
      ui.grade.textContent = "";
    }
    paintSide("you");
    refreshTimer = setTimeout(() => {
      refreshPicture(token);
    }, 700);
  }

  async function refreshPicture(token) {
    if (!ui.editor || token !== state.runToken) return;
    const source = ui.editor.value;
    if (!source.trim()) {
      state.you = emptyTrace();
      state.you.note = "Type some Python. The steps will follow the lines you write.";
      paintSide("you");
      return;
    }
    const lesson = state.free ? null : currentProblem();
    const hasSolve = /(^|\n)\s*def\s+solve\s*\(/.test(source);
    const ownProgram = state.free || !lesson || !hasSolve || hasTopLevelWork(source);
    if (hasSolve && !hasTopLevelWork(source) && ownProgram) {
      state.you = emptyTrace();
      state.you.note = "Add a line that uses your function, such as print(solve([1, 2, 3])). Then the steps inside it will show.";
      paintSide("you");
      return;
    }
    state.you.running = true;
    state.you.note = "";
    paintSide("you");
    try {
      await loadPy();
      if (token !== state.runToken) return;
      const data = ownProgram
        ? await pythonCall("run_script", source, "")
        : await pythonCall("run_traced", source, lesson.tests[state.testIndex].call);
      if (token !== state.runToken) return;
      applyUserTrace(data, ownProgram || !!data.script);
    } catch (err) {
      if (token !== state.runToken) return;
      state.you = emptyTrace();
      state.you.error = err.message || String(err);
      paintSide("you");
    }
  }

  async function runUser(traceSelected) {
    if (!ui.editor) return;
    const lesson = state.free ? null : currentProblem();
    stopPlay();
    clearTimeout(refreshTimer);
    state.lens = "you";
    document.querySelectorAll("[data-lens]").forEach((btn) => {
      btn.classList.toggle("primary", btn.dataset.lens === "you");
    });
    const token = ++state.runToken;
    const source = ui.editor.value;
    if (editorOnly() && !source.trim()) {
      ui.grade.className = "vl-grade";
      ui.grade.textContent = "Write Python, then run it.";
      return;
    }
    const hasSolve = /(^|\n)\s*def\s+solve\s*\(/.test(source);
    const ownProgram = state.free || !lesson || !hasSolve || hasTopLevelWork(source);
    ui.grade.className = "vl-grade";
    ui.grade.textContent = "Running Python…";
    setPane("you");
    const runBtn = ui.root.querySelector("[data-run]");
    if (runBtn) runBtn.disabled = true;
    try {
      await loadPy();
      if (token !== state.runToken) return;
      if (lesson && hasSolve) {
        const results = [];
        for (const test of lesson.tests) {
          results.push(await pythonCall("run_plain", source, test.call));
          if (token !== state.runToken) return;
        }
        state.tests = results.map((result, index) => {
          const expect = lesson.tests[index].expect;
          const pass = !result.error && result.result_repr === expect;
          return { status: pass ? "pass" : "fail", got: result.result_repr || "", error: result.error || "" };
        });
        const passed = state.tests.filter((item) => item.status === "pass").length;
        const store = loadStore();
        if (passed === lesson.tests.length) {
          store.status[state.topicId] = "solved";
          ui.grade.className = "vl-grade ok";
          ui.grade.textContent = "All " + passed + " examples match. Your answer is right.";
        } else {
          store.status[state.topicId] = "tried";
          ui.grade.className = "vl-grade bad";
          ui.grade.textContent = passed + " of " + lesson.tests.length + " examples match. Step through the picture and see where a value changes.";
        }
        saveStore(store);
        paintNavMarks();
        paintTests();
      } else if (ui.grade) {
        ui.grade.className = "vl-grade";
        ui.grade.textContent = hasSolve && !hasTopLevelWork(source)
          ? "Add a line that calls solve, such as print(solve([1, 2, 3]))."
          : "";
      }
      if (!traceSelected) return;
      state.you = emptyTrace();
      state.you.running = true;
      state.you.script = ownProgram;
      paintSide("you");
      const data = ownProgram
        ? await pythonCall("run_script", source, "")
        : await pythonCall("run_traced", source, lesson.tests[state.testIndex].call);
      if (token !== state.runToken) return;
      applyUserTrace(data, ownProgram || !!data.script);
      if (lesson && !ownProgram) await ensureSolutionTrace();
      else if (lesson && hasSolve) await ensureSolutionTrace();
    } catch (err) {
      if (token !== state.runToken) return;
      ui.grade.className = "vl-grade bad";
      ui.grade.textContent = err.message || String(err);
    } finally {
      if (token === state.runToken && runBtn) runBtn.disabled = false;
    }
  }

  function watchFrame(side, trace, source, problem, sentence) {
    const wrap = document.createElement("div");
    const frame = trace.frames.length ? trace.frames[trace.i] : null;
    const prev = frame ? trace.frames[trace.i - 1] || null : null;
    wrap.className = "vl-watch is-" + (frame ? layoutKind(frame) : "simple");
    if (trace.frames.length > 1) {
      const rail = document.createElement("div");
      rail.className = "vl-rail";
      const range = document.createElement("input");
      range.type = "range";
      range.min = "0";
      range.max = String(trace.frames.length - 1);
      range.value = String(trace.i);
      range.setAttribute("aria-label", "Which step to show");
      range.addEventListener("input", () => jump(side, Number(range.value)));
      const count = document.createElement("span");
      count.textContent = (trace.i + 1) + " / " + trace.frames.length;
      rail.appendChild(range);
      rail.appendChild(count);
      if (trace.frames.length <= 16) {
        const dots = document.createElement("div");
        dots.className = "vl-dots";
        trace.frames.forEach((item, index) => {
          const dot = document.createElement("button");
          dot.type = "button";
          dot.className = "vl-dot" + (index === trace.i ? " is-now" : index < trace.i ? " is-past" : "");
          dot.title = "Step " + (index + 1) + (sourceLine(source, item.line).trim() ? ": " + sourceLine(source, item.line).trim() : "");
          dot.addEventListener("click", () => jump(side, index));
          dots.appendChild(dot);
        });
        rail.appendChild(dots);
      }
      wrap.appendChild(rail);
    }
    const live = document.createElement("div");
    live.className = "vl-live";
    const picture = document.createElement("div");
    picture.className = "vl-picture";
    const step = document.createElement("div");
    step.className = "vl-instep" + (trace.error ? " is-bad" : "");
    const title = document.createElement("b");
    title.textContent = sentence;
    step.appendChild(title);
    if (frame) {
      const code = document.createElement("code");
      const line = sourceLine(source, frame.line).trim();
      code.textContent = line || "line " + frame.line;
      step.appendChild(code);
    }
    picture.appendChild(step);
    if (frame) {
      const fit = document.createElement("div");
      fit.className = "vl-fit";
      fit.appendChild(memoryCard(frame, prev, problem, true, trace, source));
      picture.appendChild(fit);
    }
    live.appendChild(picture);
    if (frame) live.appendChild(variablesDock(frame, prev, trace));
    wrap.appendChild(live);
    wrap.appendChild(outputBar(frame, trace));
    bindWatchHover(wrap, side === "you");
    return wrap;
  }

  function variablesDock(frame, prev, trace) {
    const dock = document.createElement("aside");
    dock.className = "vl-dock";
    const stats = stepStats(Object.assign({}, trace, { i: trace.i }));
    const line = document.createElement("p");
    line.className = "vl-stats";
    const bits = ["Step " + stats.step + "/" + stats.total];
    if (stats.calls) bits.push(stats.calls + (stats.calls === 1 ? " call" : " calls"));
    if (stats.depth) bits.push("depth " + stats.depth);
    if (stats.changed) bits.push(stats.changed + (stats.changed === 1 ? " name changed" : " names changed"));
    if (stats.printed) bits.push(stats.printed + " characters printed");
    line.textContent = bits.join(" · ");
    dock.appendChild(line);
    const calls = (frame.stack || []).filter((item) => item.fn && item.fn !== "<module>");
    if (calls.length) {
      const stack = document.createElement("p");
      stack.className = "vl-calls";
      stack.textContent = "Call stack: ";
      calls.forEach((item, index) => {
        const name = document.createElement("b");
        name.textContent = item.fn + (index < calls.length - 1 ? " → " : "");
        name.title = "Line " + item.line;
        stack.appendChild(name);
      });
      dock.appendChild(stack);
    }
    const changed = new Set(changedPairs(prev, frame).map((pair) => pair[0]));
    const locals = localsOf(frame);
    const names = Object.keys(locals);
    const table = document.createElement("table");
    table.className = "vl-vtable";
    names.slice(0, 8).forEach((name) => {
      const node = locals[name];
      const row = document.createElement("tr");
      row.dataset.name = name;
      row.title = "Highlights this name in the picture and in your code";
      if (changed.has(name)) row.className = "is-changed";
      [name, pyFmt(node)].forEach((text) => {
        const td = document.createElement("td");
        td.textContent = text;
        row.appendChild(td);
      });
      table.appendChild(row);
    });
    if (!names.length) {
      const row = document.createElement("tr");
      const td = document.createElement("td");
      td.textContent = "Nothing stored yet.";
      row.appendChild(td);
      table.appendChild(row);
    }
    dock.appendChild(table);
    if (names.length > 8) {
      const more = document.createElement("p");
      more.className = "vl-stats";
      more.textContent = (names.length - 8) + " more names are stored in this frame.";
      dock.appendChild(more);
    }
    return dock;
  }

  function explainStrip(frame, prev, trace, source) {
    const p = document.createElement("p");
    p.className = "vl-explain";
    if (!frame) {
      p.textContent = trace.error || "Run the code to record each step.";
      return p;
    }
    const ops = describeEvents(deriveEvents(prev, frame, trace, source));
    let text = ops || nextFact(trace, source);
    if (!ops) text = nextFact(trace, source);
    else if (nextFact(trace, source)) text = ops + " " + nextFact(trace, source);
    if (trace.error && frame === trace.frames[trace.frames.length - 1]) {
      const hint = errorHint(trace.error);
      text = trace.error + (hint ? " " + hint : "");
    }
    p.textContent = text;
    return p;
  }

  function bindWatchHover(wrap, mine) {
    wrap.querySelectorAll("[data-name]").forEach((el) => {
      el.addEventListener("mouseenter", () => highlightName(wrap, el.dataset.name, mine));
      el.addEventListener("mouseleave", () => clearNameHighlight(wrap));
    });
  }

  function highlightName(wrap, name, mine) {
    wrap.querySelectorAll("[data-name]").forEach((el) => {
      el.classList.toggle("is-linked", el.dataset.name === name);
    });
    if (!mine || !ui.editor || !ui.back) return;
    const safe = name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const pattern = new RegExp("\\b" + safe + "\\b");
    const lines = ui.editor.value.split("\n");
    Array.from(ui.back.children).forEach((row, index) => {
      row.classList.toggle("is-ref", pattern.test(lines[index] || ""));
    });
  }

  function clearNameHighlight(wrap) {
    wrap.querySelectorAll(".is-linked").forEach((el) => el.classList.remove("is-linked"));
    if (ui.back) Array.from(ui.back.children).forEach((row) => row.classList.remove("is-ref"));
  }

  const PY_WORDS = [
    ["False", "keyword"], ["None", "keyword"], ["True", "keyword"], ["and", "keyword"], ["as", "keyword"],
    ["assert", "keyword"], ["break", "keyword"], ["class", "keyword"], ["continue", "keyword"], ["def", "keyword"],
    ["elif", "keyword"], ["else", "keyword"], ["except", "keyword"], ["finally", "keyword"], ["for", "keyword"],
    ["from", "keyword"], ["global", "keyword"], ["if", "keyword"], ["import", "keyword"], ["in", "keyword"],
    ["is", "keyword"], ["lambda", "keyword"], ["not", "keyword"], ["or", "keyword"], ["pass", "keyword"],
    ["raise", "keyword"], ["return", "keyword"], ["try", "keyword"], ["while", "keyword"], ["with", "keyword"],
    ["yield", "keyword"],
    ["print", "builtin"], ["len", "builtin"], ["range", "builtin"], ["int", "builtin"], ["str", "builtin"],
    ["float", "builtin"], ["bool", "builtin"], ["list", "builtin"], ["dict", "builtin"], ["set", "builtin"],
    ["tuple", "builtin"], ["sum", "builtin"], ["min", "builtin"], ["max", "builtin"], ["abs", "builtin"],
    ["sorted", "builtin"], ["reversed", "builtin"], ["enumerate", "builtin"], ["zip", "builtin"], ["map", "builtin"],
    ["filter", "builtin"], ["any", "builtin"], ["all", "builtin"], ["input", "builtin"], ["open", "builtin"],
    ["round", "builtin"], ["type", "builtin"], ["isinstance", "builtin"], ["super", "builtin"],
  ];
  const PY_METHODS = {
    list: ["append", "pop", "insert", "remove", "sort", "reverse", "clear", "copy", "count", "index", "extend"],
    str: ["split", "join", "strip", "lower", "upper", "replace", "startswith", "endswith", "find", "count", "format"],
    dict: ["get", "keys", "values", "items", "pop", "update", "clear", "setdefault"],
    set: ["add", "remove", "discard", "update", "clear"],
    deque: ["append", "appendleft", "pop", "popleft", "clear", "extend"],
  };
  let suggestBox = null;
  let suggestItems = [];
  let suggestIndex = 0;
  let suggestFrom = 0;
  let suggestTo = 0;

  function closeSuggest() {
    const open = !!suggestBox;
    if (suggestBox) suggestBox.remove();
    suggestBox = null;
    suggestItems = [];
    return open;
  }

  function namesInCode(source) {
    const names = [];
    const seen = new Set(PY_WORDS.map((item) => item[0]));
    String(source || "").split("\n").forEach((line) => {
      const found = [];
      const def = /^\s*(?:def|class)\s+([A-Za-z_]\w*)/.exec(line);
      if (def) found.push(def[1]);
      const assign = /^\s*([A-Za-z_]\w*)\s*=/.exec(line);
      if (assign) found.push(assign[1]);
      const loop = /^\s*for\s+([A-Za-z_]\w*)\s+in\b/.exec(line);
      if (loop) found.push(loop[1]);
      found.forEach((name) => {
        if (seen.has(name)) return;
        seen.add(name);
        names.push(name);
      });
    });
    return names;
  }

  function guessType(source, name) {
    const safe = name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const match = new RegExp("(^|\\n)\\s*" + safe + "\\s*=\\s*([^\\n]+)").exec(source);
    if (!match) return "";
    const rhs = match[2].trim();
    if (rhs.indexOf("deque(") === 0) return "deque";
    if (rhs.indexOf("[") === 0 || rhs.indexOf("list(") === 0) return "list";
    if (rhs.indexOf("dict(") === 0 || (rhs.indexOf("{") === 0 && rhs.indexOf(":") >= 0)) return "dict";
    if (rhs.indexOf("set(") === 0 || rhs.indexOf("{") === 0) return "set";
    if (rhs.charAt(0) === '"' || rhs.charAt(0) === "'" || rhs.indexOf("str(") === 0) return "str";
    return "";
  }

  function suggestChoices(source, kind, base, prefix) {
    const start = prefix.toLowerCase();
    const pool = [];
    if (kind === "attr") {
      const typed = guessType(source, base);
      const methods = typed && PY_METHODS[typed] ? PY_METHODS[typed] : [].concat(PY_METHODS.list, PY_METHODS.dict, PY_METHODS.str, PY_METHODS.set);
      const seen = new Set();
      methods.forEach((name) => {
        if (seen.has(name) || name.toLowerCase().indexOf(start) !== 0) return;
        seen.add(name);
        pool.push({ label: name, kind: typed || "method", insert: name });
      });
      return pool.slice(0, 8);
    }
    namesInCode(source).forEach((name) => {
      if (name.toLowerCase().indexOf(start) === 0) pool.push({ label: name, kind: "yours", insert: name });
    });
    PY_WORDS.forEach((item) => {
      if (item[0].toLowerCase().indexOf(start) === 0) pool.push({ label: item[0], kind: item[1], insert: item[0] });
    });
    return pool.slice(0, 8);
  }

  function caretPoint(editor) {
    const style = getComputedStyle(editor);
    const rect = editor.getBoundingClientRect();
    const before = editor.value.slice(0, editor.selectionStart);
    const lines = before.split("\n");
    const probe = document.createElement("span");
    probe.textContent = "0000000000";
    probe.style.cssText = "position:absolute;left:-9999px;top:0;visibility:hidden;font:" + style.font;
    document.body.appendChild(probe);
    const charW = probe.getBoundingClientRect().width / 10 || 8;
    probe.remove();
    const lineH = parseFloat(style.lineHeight) || 22;
    const col = lines[lines.length - 1].length;
    return {
      left: rect.left + (parseFloat(style.paddingLeft) || 0) + col * charW - editor.scrollLeft,
      top: rect.top + (parseFloat(style.paddingTop) || 0) + lines.length * lineH - editor.scrollTop,
    };
  }

  function paintSuggest() {
    if (!suggestBox) return;
    suggestBox.innerHTML = "";
    suggestItems.forEach((item, index) => {
      const li = document.createElement("li");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = index === suggestIndex ? "is-on" : "";
      btn.innerHTML = esc(item.label) + "<small>" + esc(item.kind) + "</small>";
      btn.addEventListener("mousedown", (event) => {
        event.preventDefault();
        suggestIndex = index;
        acceptSuggest();
      });
      li.appendChild(btn);
      suggestBox.appendChild(li);
    });
    const current = suggestBox.querySelector(".is-on");
    if (current) current.scrollIntoView({ block: "nearest" });
  }

  function suggestRefresh(force) {
    const editor = ui.editor;
    if (!editor || document.activeElement !== editor) {
      closeSuggest();
      return;
    }
    const pos = editor.selectionStart;
    if (pos !== editor.selectionEnd) {
      closeSuggest();
      return;
    }
    const upto = editor.value.slice(0, pos);
    const dotted = /([A-Za-z_]\w*)\.([A-Za-z_]\w*)$/.exec(upto) || /([A-Za-z_]\w*)\.$/.exec(upto);
    const named = /([A-Za-z_]\w*)$/.exec(upto);
    let kind = "name";
    let base = "";
    let prefix = "";
    if (dotted) {
      kind = "attr";
      base = dotted[1];
      prefix = dotted[2] || "";
      suggestFrom = pos - prefix.length;
    } else if (named) {
      prefix = named[1];
      suggestFrom = pos - prefix.length;
    }
    suggestTo = pos;
    if (!force && kind === "name" && prefix.length < 1) {
      closeSuggest();
      return;
    }
    suggestItems = suggestChoices(editor.value, kind, base, prefix).filter((item) => item.insert !== prefix);
    if (!suggestItems.length) {
      closeSuggest();
      return;
    }
    suggestIndex = 0;
    if (!suggestBox) {
      suggestBox = document.createElement("ul");
      suggestBox.className = "vl-suggest";
      suggestBox.setAttribute("role", "listbox");
      ui.root.appendChild(suggestBox);
    }
    const point = caretPoint(editor);
    const left = Math.max(8, Math.min(point.left, window.innerWidth - 240));
    const top = Math.min(point.top + 2, window.innerHeight - 160);
    suggestBox.style.left = left + "px";
    suggestBox.style.top = top + "px";
    paintSuggest();
  }

  function acceptSuggest() {
    const editor = ui.editor;
    const item = suggestItems[suggestIndex];
    if (!editor || !item) return;
    const call = item.kind === "builtin" || item.kind === "method" || item.kind === "list" || item.kind === "dict" || item.kind === "str" || item.kind === "set" || item.kind === "deque";
    const spaced = item.kind === "keyword" && /^(if|elif|else|for|while|def|class|try|except|finally|with|return|import|from|raise|yield)$/.test(item.insert);
    const insert = item.insert + (call ? "()" : spaced ? " " : "");
    const next = editor.value.slice(0, suggestFrom) + insert + editor.value.slice(suggestTo);
    closeSuggest();
    editor.value = next;
    editor.selectionStart = editor.selectionEnd = suggestFrom + insert.length - (call ? 1 : 0);
    onCodeEdited();
  }

  function suggestKey(event) {
    if ((event.ctrlKey || event.metaKey) && event.key === " ") {
      event.preventDefault();
      suggestRefresh(true);
      return true;
    }
    if (!suggestBox) return false;
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      const step = event.key === "ArrowDown" ? 1 : -1;
      suggestIndex = (suggestIndex + step + suggestItems.length) % suggestItems.length;
      paintSuggest();
      return true;
    }
    if (event.key === "Enter" || event.key === "Tab") {
      event.preventDefault();
      acceptSuggest();
      return true;
    }
    if (event.key === "Escape") {
      event.preventDefault();
      event.stopPropagation();
      closeSuggest();
      return true;
    }
    return false;
  }

  function fitWatch(picture, fit) {
    const card = fit.firstElementChild;
    if (!card) return;
    const step = picture.querySelector(".vl-instep");
    const stepH = step ? step.offsetHeight : 0;
    fit.style.paddingTop = (stepH + 16) + "px";
    fit.style.transform = "none";
    fit.style.width = "";
    card.style.transform = "none";
    card.style.width = "max-content";
    card.style.maxWidth = "none";
    const box = getComputedStyle(fit);
    const availW = Math.max(32, fit.clientWidth - parseFloat(box.paddingLeft) - parseFloat(box.paddingRight) - 8);
    const availH = Math.max(32, fit.clientHeight - parseFloat(box.paddingTop) - parseFloat(box.paddingBottom) - 8);
    const needW = Math.max(card.scrollWidth, card.offsetWidth, 1);
    const needH = Math.max(card.scrollHeight, card.offsetHeight, 1);
    let scale = Math.min(availW / needW, availH / needH);
    if (!isFinite(scale) || scale <= 0) scale = 1;
    scale = Math.min(scale, 2.4);
    card.style.transformOrigin = "center center";
    card.style.transform = Math.abs(scale - 1) > 0.04 ? "scale(" + scale + ")" : "";
    const bounds = picture.getBoundingClientRect();
    const boxes = ".vl-var, .vl-cell, .vl-node, .vl-queue i, .vl-stack i, .vl-set i, .vl-table, .vl-grid, .vl-caption, .vl-key, .vl-cursor, .vl-graph circle, .vl-graph text";
    for (let guard = 0; guard < 8; guard += 1) {
      let over = 0;
      card.querySelectorAll(boxes).forEach((el) => {
        const rect = el.getBoundingClientRect();
        if (rect.width < 1 && rect.height < 1) return;
        over = Math.max(over, bounds.left + 8 - rect.left, rect.right - (bounds.right - 8), bounds.top + stepH + 14 - rect.top, rect.bottom - (bounds.bottom - 8));
      });
      if (over <= 1 || scale < 0.18) break;
      const span = Math.max(bounds.width, bounds.height, 1);
      scale *= Math.max(0.55, (span - over - 10) / span);
      card.style.transform = "scale(" + scale + ")";
    }
  }

  function outputBar(frame, trace) {
    const bar = document.createElement("div");
    const failed = !!(trace.error && frame && frame === trace.frames[trace.frames.length - 1]);
    bar.className = "vl-outbar" + (failed ? " is-err" : "");
    if (!frame) {
      bar.textContent = trace.error || "Printed words show up here.";
      return bar;
    }
    const printed = stdoutAt(trace.stdout, frame.out_n).trim();
    const lines = printed ? printed.split("\n") : [];
    const shown = lines.length > 14 ? lines.slice(-14) : lines;
    let text = shown.join("\n");
    if (lines.length > 14) text = "…\n" + text;
    const quiet = trace.script && frame.final && (!frame.ret || frame.ret.t === "none");
    if (!quiet && frame.final) text = (text ? text + "\n" : "") + "answer " + pyFmt(frame.ret);
    if (failed) text = (text ? text + "\n" : "") + trace.error;
    bar.textContent = text || "Nothing printed yet.";
    return bar;
  }

  function shownSide() {
    return state.lens === "sol" && !state.free ? "sol" : "you";
  }

  function chooseLens(name) {
    state.lens = name === "sol" && !state.free ? "sol" : "you";
    document.querySelectorAll("[data-lens]").forEach((btn) => {
      btn.classList.toggle("primary", btn.dataset.lens === state.lens);
    });
    if (state.lens === "sol") ensureSolutionTrace().then(() => { if (shownSide() === "sol") paintSide("sol"); });
    else paintSide("you");
  }

  function snapshotVids(root) {
    const map = new Map();
    if (!root) return map;
    root.querySelectorAll("[data-vid]").forEach((el) => {
      const vid = el.dataset.vid;
      if (!vid) return;
      const rect = el.getBoundingClientRect();
      if (rect.width < 1 && rect.height < 1) return;
      map.set(vid, { left: rect.left, top: rect.top, width: rect.width, height: rect.height, text: (el.textContent || "").trim().slice(0, 24) });
    });
    return map;
  }

  function cancelMotion() {
    motionToken += 1;
    motions.forEach((anim) => { try { anim.cancel(); } catch (err) { /* already finished */ } });
    motions = [];
    document.querySelectorAll(".vl-motion-ghost").forEach((el) => el.remove());
  }

  function fitScale(el) {
    const card = el.closest(".vl-card");
    const host = card || el.closest(".vl-fit");
    if (!host) return 1;
    const match = /scale\(([^)]+)\)/.exec(host.style.transform || "");
    const scale = match ? Number(match[1]) : 1;
    return scale > 0 ? scale : 1;
  }

  function applyMotion(root, prevMap) {
    if (!root) return;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const token = motionToken;
    const ms = motionMs(state.rate);
    const seen = new Set();
    root.querySelectorAll(".vl-picture").forEach((picture) => {
      const fit = picture.querySelector(".vl-fit");
      if (fit) fitWatch(picture, fit);
    });
    drawWires(root, reduced ? 0 : ms);
    if (!reduced && prevMap && prevMap.size) {
    root.querySelectorAll("[data-vid]").forEach((el) => {
      const vid = el.dataset.vid;
      if (!vid) return;
      seen.add(vid);
      const prev = prevMap.get(vid);
      if (!prev) {
        const enter = el.animate(
          [{ transform: "translateY(-8px)" }, { transform: "translateY(0)" }],
          { duration: Math.min(ms, 220), easing: "cubic-bezier(.2,.8,.2,1)" }
        );
        motions.push(enter);
        return;
      }
      const next = el.getBoundingClientRect();
      const scale = fitScale(el);
      const dx = (prev.left - next.left) / scale;
      const dy = (prev.top - next.top) / scale;
      if (Math.abs(dx) < 0.6 && Math.abs(dy) < 0.6) {
        const nowText = (el.textContent || "").trim().slice(0, 24);
        if (vid.indexOf("var-") === 0 && prev.text !== nowText) {
          const value = el.querySelector("b") || el;
          const change = value.animate(
            [{ opacity: 0, transform: "translateY(8px)" }, { opacity: 1, transform: "translateY(0)" }],
            { duration: Math.min(ms, 280), easing: "ease" }
          );
          motions.push(change);
        }
        return;
      }
      const anim = el.animate(
        [{ transform: "translate(" + dx + "px," + dy + "px)" }, { transform: "translate(0px,0px)" }],
        { duration: ms, easing: "cubic-bezier(.2,.7,.2,1)", fill: "both" }
      );
      motions.push(anim);
      anim.onfinish = () => { if (token === motionToken) anim.cancel(); };
    });
    prevMap.forEach((rect, vid) => {
      if (seen.has(vid) || vid.indexOf("ptr-") === 0 || vid.indexOf("node-") === 0 || vid.indexOf("g-") === 0 || vid.indexOf("var-") === 0) return;
      const ghost = document.createElement("div");
      ghost.className = "vl-motion-ghost";
      ghost.textContent = rect.text;
      ghost.style.left = rect.left + "px";
      ghost.style.top = rect.top + "px";
      ghost.style.width = Math.max(rect.width, 28) + "px";
      ghost.style.height = Math.max(rect.height, 22) + "px";
      document.body.appendChild(ghost);
      const anim = ghost.animate(
        [{ opacity: 1, transform: "translateY(0)" }, { opacity: 0, transform: "translateY(-16px)" }],
        { duration: ms, easing: "ease", fill: "forwards" }
      );
      motions.push(anim);
      anim.onfinish = () => ghost.remove();
    });
    }
  }

  function svgEl(name, attrs) {
    const el = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.keys(attrs || {}).forEach((key) => el.setAttribute(key, String(attrs[key])));
    return el;
  }

  function localPoint(stageRect, rect, scale) {
    return {
      x: (rect.left + rect.width / 2 - stageRect.left) / scale,
      y: (rect.top - stageRect.top) / scale,
    };
  }

  function drawWires(root, ms) {
    if (!root) return;
    root.querySelectorAll(".vl-board").forEach((stage) => {
      const svg = stage.querySelector(".vl-wires");
      if (!svg) return;
      const scale = fitScale(stage);
      const stageRect = stage.getBoundingClientRect();
      svg.setAttribute("width", String(stage.clientWidth || 1));
      svg.setAttribute("height", String(Math.max(stage.clientHeight || 1, 1)));
      svg.replaceChildren();
      const cells = [...stage.querySelectorAll(".vl-cell")];
      const cursor = stage.querySelector(".vl-cursor");
      const aim = cursor ? Number(cursor.dataset.aim) : -1;
      if (!cells.length || aim < 0 || !cells[aim]) return;
      const tip = localPoint(stageRect, cells[aim].getBoundingClientRect(), scale);
      cursor.style.left = tip.x + "px";
      cursor.style.top = (tip.y - 28) + "px";
      const picture = stage.closest(".vl-picture");
      if (picture && scale) {
        const pad = 8;
        const bounds = picture.getBoundingClientRect();
        const box = cursor.getBoundingClientRect();
        let dx = 0;
        let dy = 0;
        if (box.top < bounds.top + pad) dy = (bounds.top + pad - box.top) / scale;
        if (box.left < bounds.left + pad) dx = (bounds.left + pad - box.left) / scale;
        if (box.right > bounds.right - pad) dx = (bounds.right - pad - box.right) / scale;
        if (dx || dy) {
          cursor.style.left = (tip.x + dx) + "px";
          cursor.style.top = (tip.y - 28 + dy) + "px";
        }
      }
      const stemTop = parseFloat(cursor.style.top) + 20;
      svg.appendChild(svgEl("line", { x1: tip.x, y1: Math.min(stemTop, tip.y), x2: tip.x, y2: tip.y + 2, class: "vl-stem" }));
    });
    root.querySelectorAll(".vl-linkstage, .vl-treestage").forEach((stage) => {
      const svg = stage.querySelector(".vl-wires");
      if (!svg) return;
      const scale = fitScale(stage);
      const stageRect = stage.getBoundingClientRect();
      svg.setAttribute("width", String(stage.clientWidth || 1));
      svg.setAttribute("height", String(stage.clientHeight || 1));
      svg.replaceChildren();
      if (!svg.querySelector("#vl-head")) {
        const defs = svgEl("defs");
        const marker = svgEl("marker", { id: "vl-head", markerWidth: "8", markerHeight: "8", refX: "7", refY: "3", orient: "auto" });
        marker.appendChild(svgEl("path", { d: "M0,0 L8,3 L0,6 Z", fill: "#7cc4ff" }));
        defs.appendChild(marker);
        svg.appendChild(defs);
      }
      const pairs = [];
      if (stage.classList.contains("vl-linkstage")) {
        stage.querySelectorAll(".vl-node[data-next]").forEach((box) => {
          const target = stage.querySelector('[data-vid="' + box.dataset.next + '"]');
          if (target && box.dataset.vid) pairs.push([box, target, box.dataset.vid]);
        });
      } else {
        stage.querySelectorAll(".vl-tree").forEach((tree) => {
          const parent = tree.querySelector(":scope > .vl-node");
          if (!parent) return;
          tree.querySelectorAll(":scope > .vl-tree-kids > .vl-tree > .vl-node").forEach((kid) => {
            pairs.push([parent, kid, (parent.dataset.vid || "p") + ">" + (kid.dataset.vid || "c")]);
          });
        });
      }
      pairs.forEach(([from, to, key]) => {
        const a = from.getBoundingClientRect();
        const b = to.getBoundingClientRect();
        const x1 = (a.right - stageRect.left) / scale;
        const y1 = (a.top + a.height / 2 - stageRect.top) / scale;
        const x2 = (b.left - stageRect.left) / scale;
        const y2 = (b.top + b.height / 2 - stageRect.top) / scale;
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", String(x1));
        line.setAttribute("y1", String(y1));
        line.setAttribute("x2", String(x2));
        line.setAttribute("y2", String(y2));
        line.setAttribute("marker-end", "url(#vl-head)");
        svg.appendChild(line);
        const prev = wireAt.get(key);
        if (prev && ms > 0) {
          const anim = line.animate(
            [
              { x1: prev.x1, y1: prev.y1, x2: prev.x2, y2: prev.y2 },
              { x1: x1, y1: y1, x2: x2, y2: y2 }
            ],
            { duration: ms, easing: "cubic-bezier(.2,.7,.2,1)", fill: "both" }
          );
          motions.push(anim);
          anim.onfinish = () => anim.cancel();
        }
        wireAt.set(key, { x1: x1, y1: y1, x2: x2, y2: y2 });
      });
    });
  }

  function paintSide(side) {
    if (side !== shownSide()) return;
    const host = ui.youViz;
    const transport = ui.body && ui.body.querySelector('[data-transport="you"]');
    if (!host || !transport) return;
    const problem = currentProblem() || { viz: "flow", focus: [], solution: "" };
    const trace = state[side];
    const source = side === "you" ? currentCode() : (problem.solution || "");
    const motionBefore = snapshotVids(host);
    cancelMotion();
    activeIds = trackListIds(trace.frames || [], trace.frames && trace.frames.length ? trace.i : 0);
    if (!trace.frames || !trace.frames.length) wireAt.clear();
    host.innerHTML = "";
    try {
    const live = true;
    const mine = side === "you";
    if (side === "sol" && state.reveal && problem.solution) host.appendChild(codeBlock(problem.solution, trace));
    if (trace.running) {
      if (live) host.appendChild(watchFrame(side, trace, source, problem, mine ? "Reading your code. The boxes will appear in a moment." : "Reading the lesson answer."));
      else host.appendChild(card("Working", "Reading your code and drawing each line it runs."));
      if (mine) markPointer(0, false);
    } else if (!trace.frames.length) {
      const message = trace.error
        ? trace.error
        : trace.note
          ? trace.note
          : side === "you"
            ? "Type any Python. One picture will show the line, the boxes, and what gets printed."
            : "The lesson answer is loading.";
      if (live) host.appendChild(watchFrame(side, trace, source, problem, message));
      else host.appendChild(card(side === "you" ? "Your program" : "Lesson answer", message));
      if (mine) {
        const badLine = trace.error ? (trace.errorLine || 0) : 0;
        markPointer(badLine, !!badLine);
        if (ui.line) {
          ui.line.textContent = badLine
            ? "This line needs a fix. " + trace.error
            : trace.note
              ? trace.note
              : "Press Run, or change the code. The yellow line shows where Python is.";
        }
      }
    } else {
      const frame = trace.frames[trace.i];
      const prev = trace.frames[trace.i - 1] || null;
      const bad = !!(trace.error && trace.i === trace.frames.length - 1);
      if (live) host.appendChild(watchFrame(side, trace, source, problem, narration(frame, prev, source)));
      else {
        host.appendChild(card("This step", narration(frame, prev, source)));
        host.appendChild(flowCard(trace, source, side));
        host.appendChild(memoryCard(frame, prev, problem, false));
        host.appendChild(outputCard(frame, trace));
      }
      if (mine && ui.line) {
        const text = sourceLine(source, frame.line).trim();
        ui.line.textContent = bad
          ? "Python stopped on this line. " + trace.error
          : "Python is on the yellow line" + (text ? ": " + text : ".");
        markPointer(frame.line, bad);
      }
    }
    paintTransport(transport, side);
    } catch (err) {
      host.appendChild(card("Picture", err && err.message ? err.message : "The picture could not be drawn."));
      paintTransport(transport, side);
    }
    applyMotion(host, motionBefore);
  }

  function card(title, text) {
    const el = document.createElement("section");
    el.className = "vl-card";
    const h = document.createElement("h5");
    h.textContent = title;
    const p = document.createElement("p");
    p.className = "vl-narration vl-lead";
    p.textContent = text;
    el.appendChild(h);
    el.appendChild(p);
    return el;
  }

  function codeBlock(source, trace) {
    const pre = document.createElement("div");
    pre.className = "vl-code";
    const line = trace.frames.length ? trace.frames[trace.i].line : 0;
    source.split("\n").forEach((text, index) => {
      const row = document.createElement("div");
      if (index + 1 === line) row.className = "is-now";
      row.textContent = (index + 1) + "  " + text;
      pre.appendChild(row);
    });
    return pre;
  }

  function flowCard(trace, source, side) {
    const el = document.createElement("section");
    el.className = "vl-card";
    const h = document.createElement("h5");
    h.textContent = side === "you" ? "The path your code took" : "The path the lesson took";
    el.appendChild(h);
    const strip = document.createElement("div");
    strip.className = "vl-flowstrip";
    trace.frames.forEach((frame, index) => {
      const prev = trace.frames[index - 1] || null;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "vl-fstep" + (index === trace.i ? " is-now" : index < trace.i ? " is-past" : "");
      const num = document.createElement("span");
      num.className = "vl-fnum";
      num.textContent = frame.e === "call" && frame.fn === "<module>" ? "start" : frame.e === "return" && frame.fn === "<module>" ? "done" : "L" + frame.line;
      btn.appendChild(num);
      const text = document.createElement("span");
      text.className = "vl-ftext";
      const code = sourceLine(source, frame.line).trim();
      const change = shortStep(frame, prev, source);
      const main = document.createElement("b");
      main.textContent = code || change || "step";
      text.appendChild(main);
      if (code && change && change !== code) {
        const small = document.createElement("small");
        small.textContent = change;
        text.appendChild(small);
      }
      btn.appendChild(text);
      btn.addEventListener("click", () => jump(side, index));
      strip.appendChild(btn);
    });
    el.appendChild(strip);
    const intro = document.createElement("p");
    intro.className = "vl-intro";
    intro.textContent = side === "you"
      ? "Each row is a line your program really ran. Yellow matches the yellow line in your code. Change the code and this path changes."
      : "Each row is a line of the lesson answer. Yellow is the line it is on right now.";
    el.appendChild(intro);
    requestAnimationFrame(revealCurrentStep);
    return el;
  }

  function revealCurrentStep() {
    document.querySelectorAll(".vl-flowstrip").forEach((strip) => {
      const current = strip.querySelector(".is-now");
      if (!current || !strip.clientHeight) return;
      const top = current.getBoundingClientRect().top - strip.getBoundingClientRect().top + strip.scrollTop;
      strip.scrollTop = Math.max(0, top - 8);
    });
  }

  function memoryCard(frame, prev, problem, live, trace, source) {
    const el = document.createElement("section");
    el.className = "vl-card";
    const h = document.createElement("h5");
    h.textContent = "What the computer remembers";
    el.appendChild(h);
    const hero = document.createElement("div");
    hero.className = "vl-stage";
    if (live) renderLive(hero, frame, prev, trace, source);
    else renderHero(hero, frame, prev, problem);
    el.appendChild(hero);
    const legend = document.createElement("p");
    legend.className = "vl-legend";
    legend.textContent = "Boxes are values in memory. A yellow box just changed. A bouncing name is a pointer on that spot.";
    el.appendChild(legend);
    return el;
  }

  function aliasLabel(locals, id, selfName) {
    const owner = Object.keys(locals).find((name) => name !== selfName && locals[name] && locals[name].id === id && locals[name].t !== "alias");
    return owner ? "same object as " + owner : "same object #" + id;
  }

  function outputCard(frame, trace) {
    const el = document.createElement("section");
    el.className = "vl-card";
    const h = document.createElement("h5");
    h.textContent = "What came out";
    el.appendChild(h);
    const pre = document.createElement("pre");
    pre.className = "vl-out" + (trace.error && frame === trace.frames[trace.frames.length - 1] ? " is-err" : "");
    const printed = (trace.stdout || "").slice(0, frame.out_n || 0);
    let text = printed;
    const quietReturn = trace.script && frame.final && (!frame.ret || frame.ret.t === "none");
    if (quietReturn) {
      pre.classList.add("vl-out-ready");
      text = printed.trim() ? printed : "Finished. Nothing was printed.";
    } else if (frame.final) {
      pre.classList.add("vl-out-ready");
      text += (text && !text.endsWith("\n") ? "\n" : "") + "return " + pyFmt(frame.ret);
    } else if (!text) {
      text = "… still running, no output yet";
    }
    if (trace.error && frame === trace.frames[trace.frames.length - 1]) {
      text += (text ? "\n" : "") + trace.error;
    }
    pre.textContent = text;
    el.appendChild(pre);
    const story = document.createElement("p");
    story.className = "vl-intro";
    story.textContent = outputStory(frame, trace);
    el.appendChild(story);
    return el;
  }

  function paintTransport(host, side) {
    const trace = state[side];
    host.innerHTML = "";
    const mk = (label, act) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "vl-btn";
      btn.textContent = label;
      btn.addEventListener("click", act);
      host.appendChild(btn);
      return btn;
    };
    mk("Restart", () => jump(side, 0)).title = "Back to the first recorded step (Alt+Home)";
    mk("Prev", () => { stopPlay(); step(side, -1); }).title = "Previous recorded step (Alt+Left)";
    const playBtn = mk(state.playing === side ? "Pause" : "Play", () => play(side));
    playBtn.title = "Play or pause (Alt+Space)";
    if (state.playing === side) playBtn.classList.add("primary");
    mk("Next", () => { stopPlay(); step(side, 1); }).title = "Next recorded step (Alt+Right)";
    mk("Last", () => jump(side, (trace.frames.length || 1) - 1));
    const speed = document.createElement("select");
    speed.setAttribute("aria-label", "Playback speed");
    [0.5, 1, 1.5, 2].forEach((rate) => {
      const option = document.createElement("option");
      option.value = String(rate);
      option.textContent = rate + "×";
      if (rate === state.rate) option.selected = true;
      speed.appendChild(option);
    });
    speed.addEventListener("change", () => {
      state.rate = Number(speed.value);
      saveUi();
      const which = state.playing;
      if (which) {
        stopPlay();
        play(which);
      }
    });
    host.appendChild(speed);
    const count = document.createElement("span");
    count.className = "vl-count";
    count.textContent = trace.frames.length ? trace.i + 1 + " / " + trace.frames.length : "0 / 0";
    host.appendChild(count);
  }

  function renderLive(host, frame, prev, trace, source) {
    const locals = localsOf(frame);
    const prevLocals = prev ? localsOf(prev) : {};
    const events = deriveEvents(prev, frame, trace, source);
    const scratch = { viz: "flow", focus: Object.keys(locals), extra: null };
    const used = new Set();
    const scan = { frames: (trace && trace.frames) || [], index: trace ? trace.i : 0, source: source || "" };
    let structure = false;
    if (drawLiveGraph(host, locals, used)) structure = true;
    if (renderHeap(host, locals, prevLocals, used, events)) structure = true;
    if (renderPile(host, locals, "stack", true, used, events)) structure = true;
    if (renderPile(host, locals, "queue", false, used, events)) structure = true;
    if (!structure && renderTree(host, frame)) structure = true;
    if (!structure && renderLinked(host, frame)) structure = true;
    if (renderMatrix(host, locals, prevLocals, scratch, used, sourceLine(source, frame.line))) structure = true;
    if (renderQueens(host, locals, used)) structure = true;
    let drawLocals = locals;
    if (!Object.keys(locals).some((name) => isScalarList(locals[name]) || stringIsIndexed(locals[name], locals))) {
      const extra = Object.assign({}, locals);
      (frame.stack || []).forEach((item) => {
        Object.keys(item.locals || {}).forEach((name) => {
          if (!extra[name] && isScalarList(item.locals[name])) extra[name] = item.locals[name];
        });
      });
      drawLocals = extra;
    }
    renderRecords(host, drawLocals, prevLocals, used);
    renderLists(host, drawLocals, prevLocals, scratch, used, events, scan);
    renderScalarCards(host, locals, prevLocals, used);
    const calls = (frame.stack || []).filter((item) => item.fn && item.fn !== "<module>");
    if (calls.length > 1) {
      const note = document.createElement("p");
      note.className = "vl-intro";
      note.textContent = "These cards are function calls that have not finished yet. The top card is the one running now.";
      host.appendChild(note);
      renderRecursion(host, frame);
    }
  }

  function renderHero(host, frame, prev, problem) {
    problem = problem || { viz: "flow", focus: [], extra: null };
    const locals = localsOf(frame);
    const prevLocals = prev ? localsOf(prev) : {};
    const viz = problem.viz || "flow";
    if (viz === "graph" || problem.extra) {
      if (renderGraph(host, locals, problem)) return;
    }
    if ((viz === "heap") && renderHeap(host, locals, prevLocals)) return;
    if (viz === "tree" && renderTree(host, locals)) return;
    if (viz === "linked" && renderLinked(host, locals)) return;
    if ((viz === "matrix" || viz === "dp") && renderMatrix(host, locals, prevLocals, problem)) return;
    if (viz === "bits" && renderBits(host, locals, problem)) return;
    if (viz === "stack" && renderPile(host, locals, "stack", true)) return;
    if (viz === "queue" && renderPile(host, locals, "queue", false)) return;
    if (viz === "hash" && renderHash(host, locals, prevLocals, problem)) return;
    if (viz === "bars" && renderBars(host, locals, prevLocals, problem)) return;
    if (viz === "recursion") renderRecursion(host, frame);
    renderLists(host, locals, prevLocals, problem);
    renderScalarCards(host, locals, prevLocals, new Set());
  }

  function focusNames(problem, locals) {
    const names = (((problem && problem.focus) || [])).filter((name) => locals[name]);
    return names.length ? names : Object.keys(locals).slice(0, 8);
  }

  function changedSet(prevNode, node) {
    const out = new Set();
    if (!node || (node.t !== "list" && node.t !== "tuple")) return out;
    const prev = prevNode && prevNode.v ? prevNode.v : [];
    node.v.forEach((item, index) => {
      if (JSON.stringify(prev[index]) !== JSON.stringify(item)) out.add(index);
    });
    return out;
  }

  function pointersFor(listNode, locals, roles, line, listName) {
    const map = new Map();
    if (!listNode) return map;
    const add = (name, index) => {
      if (index < 0 || index >= listNode.v.length) return;
      if (!map.has(index)) map.set(index, []);
      if (map.get(index).indexOf(name) < 0) map.get(index).push(name);
    };
    Object.keys(locals).forEach((name) => {
      const value = locals[name];
      if (!POINTER_NAMES.has(name) || !value || value.t !== "int") return;
      if (roles && roles[name] && roles[name].mode === "item") return;
      add(name, value.v);
    });
    subscripts(line, listName).forEach((part) => {
      if (part.op) return;
      const value = locals[part.name];
      if (!value || value.t !== "int") return;
      if (roles && roles[part.name] && roles[part.name].mode === "item") return;
      add(part.name, value.v);
    });
    return map;
  }

  function indexSpan(pointerMap, length, cursor) {
    const lowNames = { left: 1, lo: 1, low: 1, start: 1, l: 1 };
    const highNames = { right: 1, hi: 1, high: 1, end: 1, r: 1 };
    let lo = null;
    let hi = null;
    pointerMap.forEach((names, index) => {
      names.forEach((name) => {
        const bare = String(name).split(/\s*[+-]/)[0];
        if (lowNames[bare]) lo = lo == null ? index : Math.min(lo, index);
        if (highNames[bare]) hi = hi == null ? index : Math.max(hi, index);
      });
    });
    if (lo != null && hi != null && lo <= hi && hi < length) return { lo: lo, hi: hi };
    let count = 0;
    pointerMap.forEach((names) => { if (names.length) count += 1; });
    if (count >= 2) return null;
    if (cursor >= 0 && cursor < length) return { lo: cursor, hi: length - 1 };
    return null;
  }

  function eventsFor(events, name) {
    return (events || []).filter((event) => event.name === name);
  }

  function stringIsIndexed(node, locals) {
    if (!node || node.t !== "str" || !node.v || node.v.length < 1 || node.v.length > 32) return false;
    return Object.keys(locals).some((key) => {
      if (!POINTER_NAMES.has(key)) return false;
      const value = locals[key];
      return value && value.t === "int" && value.v >= 0 && value.v < node.v.length;
    });
  }

  function renderLists(host, locals, prevLocals, problem, used, events, scan) {
    const names = focusNames(problem, locals).filter((name) => {
      if (used && used.has(name)) return false;
      return isScalarList(locals[name]) || stringIsIndexed(locals[name], locals);
    });
    if (!names.length) {
      const fallback = Object.keys(locals).find((name) => (!used || !used.has(name)) && isScalarList(locals[name]));
      if (fallback) names.push(fallback);
    }
    if (!names.length) return false;
    const roles = loopRoles(scan && scan.source);
    names.slice(0, 3).forEach((name) => {
      if (used) used.add(name);
      const node = locals[name];
      const label = document.createElement("div");
      label.className = "vl-caption";
      label.textContent = name;
      host.appendChild(label);
      const walk = walkFor(roles, name, locals, scan);
      const frame = scan && scan.frames ? scan.frames[scan.index || 0] : null;
      const line = frame ? sourceLine(scan.source, frame.line) : "";
      if (used) {
        const limit = node.t === "str" ? node.v.length : node.v.length;
        Object.keys(locals).forEach((key) => {
          if (!locals[key] || locals[key].t !== "int") return;
          const onLine = subscripts(line, name).some((part) => part.name === key);
          if (!POINTER_NAMES.has(key) && !onLine) return;
          const index = locals[key].v;
          if (index >= 0 && index < limit) used.add(key);
        });
      }
      const partners = partnerHits(line, name, locals, node.t === "str" ? node.v.length : node.v.length);
      if (node.t === "str") renderStringCells(host, name, node, prevLocals[name], locals, eventsFor(events, name), activeIds[name] || [], walk, roles, partners, line);
      else renderCells(host, node, prevLocals[name], locals, eventsFor(events, name), activeIds[name] || [], walk, roles, partners, line, name);
      if (walk && walk.index >= 0) host.appendChild(scanLine(walk, locals, node));
    });
    return true;
  }

  function subscripts(line, listName) {
    const found = [];
    if (!line || !listName) return found;
    const pattern = new RegExp("\\b" + listName + "\\s*\\[\\s*([A-Za-z_]\\w*)\\s*(?:([+-])\\s*(\\d+))?\\s*\\]", "g");
    let match;
    while ((match = pattern.exec(line))) {
      found.push({ name: match[1], op: match[2] || "", delta: match[3] ? Number(match[3]) : 0 });
    }
    return found;
  }

  function walkFor(roles, listName, locals, scan) {
    const itemName = Object.keys(roles).find((key) => roles[key].mode === "item" && (!roles[key].over || roles[key].over === listName));
    if (itemName && scan && scan.frames) {
      const index = itemCursor(scan.frames, scan.index || 0, itemName);
      if (index >= 0) return { name: itemName, index };
    }
    const frame = scan && scan.frames ? scan.frames[scan.index || 0] : null;
    const line = frame ? sourceLine(scan.source, frame.line) : "";
    const direct = subscripts(line, listName).filter((part) => !part.op && locals[part.name] && locals[part.name].t === "int");
    if (direct.length) {
      const name = direct[direct.length - 1].name;
      return { name, index: locals[name].v };
    }
    const mentioned = Object.keys(roles).filter((key) => roles[key] && roles[key].mode === "index" && locals[key] && locals[key].t === "int" && new RegExp("\\b" + key + "\\b").test(line));
    if (!mentioned.length) return null;
    const indexName = mentioned[mentioned.length - 1];
    return { name: indexName, index: locals[indexName].v };
  }

  function partnerHits(line, listName, locals, length) {
    const hits = new Map();
    subscripts(line, listName).forEach((part) => {
      if (!part.op) return;
      const base = locals[part.name];
      if (!base || base.t !== "int") return;
      const index = part.op === "+" ? base.v + part.delta : base.v - part.delta;
      if (index < 0 || index >= length) return;
      const label = part.name + part.op + part.delta;
      if (!hits.has(index)) hits.set(index, []);
      if (hits.get(index).indexOf(label) < 0) hits.get(index).push(label);
    });
    return hits;
  }

  function scanLine(walk, locals, node) {
    const line = document.createElement("p");
    line.className = "vl-scanline";
    const item = node.t === "str" ? { t: "str", v: node.v.charAt(walk.index) } : node.v[walk.index];
    const shown = item ? pyFmt(item).replace(/^'|'$/g, "") : "";
    let text = walk.name + " is looking at box " + walk.index + (shown ? " (" + shown + ")" : "");
    const match = Object.keys(locals).find((key) => key !== walk.name && isScalar(locals[key]) && locals[key].t !== "none" && locals[key].t !== "bool" && item && JSON.stringify(locals[key]) === JSON.stringify(item));
    if (match) text += ". " + match + " is " + pyFmt(locals[match]).replace(/^'|'$/g, "") + ". They match.";
    line.textContent = text;
    return line;
  }

  function renderCells(host, node, prevNode, locals, ops, vids, walk, roles, partners, line, listName) {
    const wrap = document.createElement("div");
    wrap.className = "vl-cells";
    const changed = changedSet(prevNode, node);
    const pointers = pointersFor(node, locals, roles, line, listName);
    const beside = partners || new Map();
    const marked = ops || [];
    const identities = vids || [];
    const cursor = walk && walk.index >= 0 && walk.index < node.v.length ? walk.index : -1;
    const span = indexSpan(pointers, node.v.length, cursor);
    node.v.forEach((item, index) => {
      const cell = document.createElement("div");
      const neighbor = beside.get(index) || [];
      const scanning = index === cursor;
      const found = scanning && walk && Object.keys(locals).some((key) => key !== walk.name && isScalar(locals[key]) && JSON.stringify(locals[key]) === JSON.stringify(item));
      const outside = span && !neighbor.length && (index < span.lo || index > span.hi);
      cell.className = "vl-cell"
        + (changed.has(index) ? " is-changed" : "")
        + (neighbor.length ? " is-read" : "")
        + (outside ? " is-seen" : "")
        + (scanning ? " is-scan" : "")
        + (found ? " is-found" : "");
      if (identities[index]) cell.dataset.vid = identities[index];
      if (marked.some((event) => event.type === "swap" && (event.i === index || event.j === index))) cell.classList.add("is-swap");
      if (marked.some((event) => (event.type === "insert" || event.type === "push" || event.type === "enqueue") && event.i === index)) cell.classList.add("is-enter");
      const idx = document.createElement("span");
      idx.className = "vl-idx";
      idx.textContent = String(index);
      const val = document.createElement("span");
      val.className = "vl-val";
      val.textContent = pyFmt(item).replace(/^'|'$/g, "");
      cell.appendChild(idx);
      cell.appendChild(val);
      const ptrs = (pointers.get(index) || []).concat(neighbor);
      if (ptrs.length) {
        const row = document.createElement("div");
        row.className = "vl-ptrs";
        ptrs.forEach((name, n) => {
          const p = document.createElement("span");
          p.className = "vl-ptr";
          p.dataset.name = name;
          p.dataset.vid = "ptr-" + name;
          p.title = name + " points at this cell";
          p.style.color = ["#7cc4ff", "#f9a8d4", "#86efac", "#fcd34d"][n % 4];
          p.textContent = "↑ " + name;
          row.appendChild(p);
        });
        cell.appendChild(row);
      }
      wrap.appendChild(cell);
    });
    const board = document.createElement("div");
    board.className = "vl-board";
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", "vl-wires");
    board.appendChild(svg);
    if (cursor >= 0 && walk) {
      const chip = document.createElement("span");
      chip.className = "vl-cursor";
      chip.dataset.vid = "ptr-" + walk.name;
      chip.dataset.aim = String(cursor);
      const label = document.createElement("b");
      label.textContent = walk.name;
      chip.appendChild(label);
      board.appendChild(chip);
    }
    board.appendChild(wrap);
    host.appendChild(board);
  }

  function renderScalarCards(host, locals, prevLocals, used) {
    const wrap = document.createElement("div");
    wrap.className = "vl-vars";
    Object.keys(locals).forEach((name) => {
      if (used && used.has(name)) return;
      const value = locals[name];
      if (!isScalar(value)) return;
      const card = document.createElement("div");
      const changed = JSON.stringify((prevLocals && prevLocals[name]) || null) !== JSON.stringify(value);
      card.className = "vl-var" + (changed ? " is-changed" : "");
      card.dataset.name = name;
      card.dataset.vid = "var-" + name;
      card.title = name;
      const lab = document.createElement("small");
      lab.textContent = name;
      const val = document.createElement("b");
      val.textContent = pyFmt(value);
      card.appendChild(lab);
      card.appendChild(val);
      wrap.appendChild(card);
    });
    if (wrap.childNodes.length) host.appendChild(wrap);
  }

  function renderHeap(host, locals, prevLocals, used, events) {
    const name = ["heap", "pq", "minheap", "maxheap"].find((item) => {
      const node = locals[item];
      return node && (node.t === "list" || node.t === "tuple") && node.v.length && node.v.every(isHeapItem);
    });
    if (!name) return false;
    if (used) used.add(name);
    const node = locals[name];
    const changed = changedSet(prevLocals[name], node);
    const swaps = eventsFor(events, name).filter((event) => event.type === "swap");
    const caption = document.createElement("div");
    caption.className = "vl-caption";
    caption.textContent = name;
    host.appendChild(caption);
    const tree = document.createElement("div");
    tree.className = "vl-heap";
    let index = 0;
    let level = 0;
    while (index < node.v.length && level < 5) {
      const row = document.createElement("div");
      row.className = "vl-heap-row";
      const count = Math.min(node.v.length - index, 2 ** level);
      for (let col = 0; col < count; col += 1) {
        const at = index + col;
        const box = document.createElement("div");
        box.className = "vl-node" + (changed.has(at) ? " is-changed" : "") + (swaps.some((event) => event.i === at || event.j === at) ? " is-swap" : "");
        if ((activeIds[name] || [])[at]) box.dataset.vid = activeIds[name][at];
        const small = document.createElement("small");
        small.textContent = String(at);
        box.appendChild(small);
        box.appendChild(document.createTextNode(pyFmt(node.v[at]).replace(/^'|'$/g, "")));
        row.appendChild(box);
      }
      tree.appendChild(row);
      index += count;
      level += 1;
    }
    host.appendChild(tree);
    return true;
  }

  function renderStringCells(host, name, node, prevNode, locals, ops, vids, walk, roles, partners, line) {
    const fake = { t: "list", v: node.v.split("").map((ch) => ({ t: "str", v: ch })) };
    const prev = prevNode && prevNode.t === "str"
      ? { t: "list", v: prevNode.v.split("").map((ch) => ({ t: "str", v: ch })) }
      : null;
    renderCells(host, fake, prev, locals, ops, vids, walk, roles, partners, line, name);
    const wrap = host.lastElementChild;
    if (wrap) wrap.dataset.vid = "var-" + name;
  }

  function renderBars(host, locals, prevLocals, problem) {
    const name = focusNames(problem, locals).find((item) => isScalarList(locals[item]) && locals[item].v.every((cell) => cell.t === "int" || cell.t === "float"))
      || Object.keys(locals).find((item) => isScalarList(locals[item]));
    if (!name) return false;
    const node = locals[name];
    const nums = node.v.map((cell) => Number(cell.v) || 0);
    const max = Math.max(...nums.map((n) => Math.abs(n)), 1);
    const changed = changedSet(prevLocals[name], node);
    const bars = document.createElement("div");
    bars.className = "vl-bars";
    nums.forEach((num, index) => {
      const bar = document.createElement("div");
      bar.className = "vl-bar" + (changed.has(index) ? " is-changed" : "");
      bar.style.height = Math.max(8, (Math.abs(num) / max) * 100) + "px";
      const span = document.createElement("span");
      span.textContent = String(num);
      bar.appendChild(span);
      bars.appendChild(bar);
    });
    host.appendChild(bars);
    const pointers = pointersFor(node, locals);
    const note = document.createElement("p");
    note.className = "vl-intro";
    const bits = [];
    pointers.forEach((names, index) => bits.push(names.join(", ") + " at index " + index));
    note.textContent = name + (bits.length ? " · " + bits.join(" · ") : "");
    host.appendChild(note);
    return true;
  }

  function dictTable(node, prev) {
    const table = document.createElement("table");
    table.className = "vl-table";
    const head = document.createElement("tr");
    ["key", "value"].forEach((label) => {
      const th = document.createElement("th");
      th.textContent = label;
      head.appendChild(th);
    });
    table.appendChild(head);
    const prevMap = new Map(((prev && prev.t === "dict" ? prev.v : []) || []).map(([key, value]) => [pyFmt(key), JSON.stringify(value)]));
    node.v.forEach(([key, value]) => {
      const tr = document.createElement("tr");
      if (prevMap.get(pyFmt(key)) !== JSON.stringify(value)) tr.className = "is-changed";
      [pyFmt(key), compact(value)].forEach((text) => {
        const td = document.createElement("td");
        td.textContent = text;
        tr.appendChild(td);
      });
      table.appendChild(tr);
    });
    if (!node.v.length) {
      const tr = document.createElement("tr");
      const td = document.createElement("td");
      td.colSpan = 2;
      td.textContent = "empty";
      tr.appendChild(td);
      table.appendChild(tr);
    }
    return table;
  }

  function setCircles(node) {
    const row = document.createElement("div");
    row.className = "vl-set";
    (node.v || []).forEach((item) => {
      const circle = document.createElement("i");
      circle.textContent = pyFmt(item).replace(/^'|'$/g, "");
      row.appendChild(circle);
    });
    if (!node.v || !node.v.length) row.textContent = "empty";
    return row;
  }

  function renderRecords(host, locals, prevLocals, used) {
    Object.keys(locals).forEach((name) => {
      if (used && used.has(name)) return;
      const node = locals[name];
      if (!node) return;
      let body = null;
      if (node.t === "dict" && !isLink(node) && !isTree(node)) body = dictTable(node, prevLocals[name]);
      else if (node.t === "set") body = setCircles(node);
      if (!body) return;
      if (used) used.add(name);
      const caption = document.createElement("div");
      caption.className = "vl-caption";
      caption.textContent = name;
      host.appendChild(caption);
      host.appendChild(body);
    });
  }

  function matrixCells(line, listName, locals) {
    const hits = [];
    if (!line || !listName) return hits;
    const pattern = new RegExp("\\b" + listName + "\\s*\\[\\s*([A-Za-z_]\\w*)\\s*(?:([+-])\\s*(\\d+))?\\s*\\]\\s*\\[\\s*([A-Za-z_]\\w*)\\s*(?:([+-])\\s*(\\d+))?\\s*\\]", "g");
    const at = (name, op, delta) => {
      const base = locals[name];
      if (!base || base.t !== "int") return null;
      if (op === "+") return base.v + delta;
      if (op === "-") return base.v - delta;
      return base.v;
    };
    let match;
    while ((match = pattern.exec(line))) {
      const row = at(match[1], match[2] || "", match[3] ? Number(match[3]) : 0);
      const col = at(match[4], match[5] || "", match[6] ? Number(match[6]) : 0);
      if (row != null && col != null) hits.push([row, col]);
    }
    return hits;
  }

  function matrixTable(node, prev, locals, line, listName) {
    const table = document.createElement("table");
    table.className = "vl-grid";
    const hits = matrixCells(line, listName, locals);
    const rowIndex = locals.i && locals.i.t === "int" ? locals.i.v : locals.row && locals.row.t === "int" ? locals.row.v : null;
    const colIndex = locals.j && locals.j.t === "int" ? locals.j.v : locals.col && locals.col.t === "int" ? locals.col.v : null;
    const previous = isMatrix(prev) ? prev : null;
    node.v.forEach((row, r) => {
      const tr = document.createElement("tr");
      row.v.forEach((cell, c) => {
        const td = document.createElement("td");
        td.textContent = pyFmt(cell);
        const before = previous && previous.v[r] && previous.v[r].v[c];
        if (!before || JSON.stringify(before) !== JSON.stringify(cell)) td.classList.add("is-changed");
        const aimed = hits.length ? hits.some((pair) => pair[0] === r && pair[1] === c) : r === rowIndex && c === colIndex;
        if (aimed) td.classList.add("is-here");
        tr.appendChild(td);
      });
      table.appendChild(tr);
    });
    return table;
  }

  function renderHash(host, locals, prevLocals, problem) {
    const name = focusNames(problem, locals).find((item) => locals[item] && locals[item].t === "dict" && !isLink(locals[item]) && !isTree(locals[item]))
      || Object.keys(locals).find((item) => locals[item] && locals[item].t === "dict" && !isLink(locals[item]) && !isTree(locals[item]));
    if (!name) return false;
    const caption = document.createElement("div");
    caption.className = "vl-caption";
    caption.textContent = name;
    host.appendChild(caption);
    host.appendChild(dictTable(locals[name], prevLocals[name]));
    return true;
  }

  function renderPile(host, locals, kind, stackMode, used, events) {
    const names = (stackMode ? ["stack", "st", "path"] : ["queue", "q", "dq"]).filter((item) => {
      return locals[item] && (locals[item].t === "list" || locals[item].t === "tuple");
    });
    if (!names.length) return false;
    names.slice(0, 2).forEach((name) => renderOnePile(host, locals, name, stackMode, used, events));
    return true;
  }

  function renderOnePile(host, locals, name, stackMode, used, events) {
    if (used) used.add(name);
    const pile = document.createElement("div");
    pile.className = "vl-pile " + (stackMode ? "is-stack" : "is-queue");
    const cap = document.createElement("div");
    cap.className = "vl-caption";
    cap.textContent = name;
    pile.appendChild(cap);
    const ends = document.createElement("div");
    ends.className = "vl-ends";
    ends.innerHTML = stackMode
      ? "<b class=\"top\">TOP</b><span>push and pop here</span>"
      : "<b class=\"front\">FRONT</b><span>leaves first</span><b class=\"rear\">REAR</b>";
    pile.appendChild(ends);
    const wrap = document.createElement("div");
    wrap.className = stackMode ? "vl-stack" : "vl-queue";
    const items = locals[name].v;
    const ops = eventsFor(events, name);
    const vids = activeIds[name] || [];
    items.forEach((item, index) => {
      const el = document.createElement("i");
      const atEnd = stackMode ? index === items.length - 1 : index === 0;
      el.className = atEnd ? (stackMode ? "is-top" : "is-front") : "";
      if (!stackMode && index === items.length - 1) el.classList.add("is-rear");
      if (vids[index]) el.dataset.vid = vids[index];
      if (ops.some((event) => (event.type === "push" || event.type === "enqueue") && event.i === index)) el.classList.add("is-enter");
      el.textContent = compact(item);
      wrap.appendChild(el);
    });
    if (!items.length) {
      const empty = document.createElement("i");
      empty.className = "is-empty";
      empty.textContent = "empty";
      wrap.appendChild(empty);
    }
    pile.appendChild(wrap);
    host.appendChild(pile);
    return true;
  }

  function renderBits(host, locals, problem) {
    const names = focusNames(problem, locals).filter((name) => locals[name] && locals[name].t === "int");
    if (!names.length) return false;
    names.slice(0, 4).forEach((name) => {
      const row = document.createElement("div");
      row.className = "vl-bits";
      const value = locals[name].v;
      const width = Math.abs(value) > 255 ? 16 : 8;
      const bits = [];
      for (let i = width - 1; i >= 0; i -= 1) {
        const on = (Number(value) >> i) & 1;
        bits.push("<b class=\"" + (on ? "on" : "") + "\">" + on + "</b>");
      }
      row.innerHTML = esc(name + " " + value + "  ") + bits.join("");
      host.appendChild(row);
    });
    return true;
  }

  function renderMatrix(host, locals, prevLocals, problem, used, line) {
    const names = ["dp", "grid", "mat", "matrix", "board", "table"].concat((problem && problem.focus) || []);
    const picked = [];
    names.forEach((item) => {
      if (picked.indexOf(item) >= 0 || !isMatrix(locals[item])) return;
      picked.push(item);
    });
    if (!picked.length) {
      const any = Object.keys(locals).find((item) => isMatrix(locals[item]));
      if (any) picked.push(any);
    }
    if (!picked.length) return false;
    picked.slice(0, 2).forEach((name) => {
      if (used) used.add(name);
      const caption = document.createElement("div");
      caption.className = "vl-caption";
      caption.textContent = name;
      host.appendChild(caption);
      host.appendChild(matrixTable(locals[name], prevLocals[name], locals, line, name));
    });
    return true;
  }

  function renderQueens(host, locals, used) {
    const nNode = locals.n;
    const place = locals.placement;
    if (!nNode || nNode.t !== "int" || !place || place.t !== "list" || !place.v.length) return false;
    const n = nNode.v;
    if (n < 1 || n > 8) return false;
    const pairs = place.v.every((item) => item.t === "tuple" && item.v.length >= 2 && item.v[0].t === "int" && item.v[1].t === "int");
    if (!pairs) return false;
    if (used) used.add("placement");
    const queens = new Set(place.v.map((item) => item.v[0].v + "," + item.v[1].v));
    const caption = document.createElement("div");
    caption.className = "vl-caption";
    caption.textContent = "board";
    host.appendChild(caption);
    const table = document.createElement("table");
    table.className = "vl-grid";
    for (let r = 0; r < n; r += 1) {
      const tr = document.createElement("tr");
      for (let c = 0; c < n; c += 1) {
        const td = document.createElement("td");
        if (queens.has(r + "," + c)) {
          td.textContent = "Q";
          td.classList.add("is-here");
        }
        tr.appendChild(td);
      }
      table.appendChild(tr);
    }
    host.appendChild(table);
    return true;
  }

  function nodeIndex(source) {
    const bags = source && source.stack ? source.stack.map((item) => item.locals || {}) : [source || {}];
    const byId = new Map();
    const visit = (node) => {
      if (!node || node.t === "alias" || node.t === "none") return;
      if (node.id && byId.has(node.id)) return;
      if (node.id && (node.t === "dict" || node.t === "list" || node.t === "tuple")) byId.set(node.id, node);
      if (node.t === "dict") node.v.forEach((pair) => visit(pair[1]));
      else if (node.t === "list" || node.t === "tuple") node.v.forEach(visit);
    };
    const locals = {};
    bags.forEach((bag) => {
      Object.keys(bag).forEach((key) => {
        locals[key] = bag[key];
        visit(bag[key]);
      });
    });
    return { locals, byId };
  }

  function deref(node, byId) {
    if (node && node.t === "alias") return byId.get(node.id) || null;
    return node;
  }

  function isLink(node) {
    if (!node || node.t !== "dict") return false;
    const keys = new Set(node.v.map((pair) => (pair[0] && pair[0].t === "str" ? pair[0].v : "")));
    return keys.has("val") && keys.has("next") && !keys.has("left");
  }

  function isTree(node) {
    if (!node || node.t !== "dict") return false;
    const keys = new Set(node.v.map((pair) => (pair[0] && pair[0].t === "str" ? pair[0].v : "")));
    return keys.has("val") && (keys.has("left") || keys.has("right"));
  }

  function linkHeads(locals, byId) {
    const links = Object.keys(locals).filter((name) => isLink(deref(locals[name], byId)));
    const childIds = new Set();
    links.forEach((name) => {
      const node = deref(locals[name], byId);
      const next = node && deref(dictGet(node, "next"), byId);
      if (next && next.id) childIds.add(next.id);
    });
    const heads = links.filter((name) => {
      const node = deref(locals[name], byId);
      return node && !childIds.has(node.id);
    });
    const preferred = ["head", "list1", "list2", "first", "second"].filter((name) => heads.indexOf(name) >= 0);
    const chosen = preferred.length ? preferred : heads;
    return (chosen.length ? chosen : links).slice(0, 2);
  }

  function renderLinked(host, source) {
    const { locals, byId } = nodeIndex(source);
    const names = linkHeads(locals, byId);
    if (!names.length) return false;
    names.slice(0, 2).forEach((name) => {
      const caption = document.createElement("div");
      caption.className = "vl-caption";
      caption.textContent = name;
      host.appendChild(caption);
      const stage = document.createElement("div");
      stage.className = "vl-linkstage";
      const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.classList.add("vl-wires");
      stage.appendChild(svg);
      const row = document.createElement("div");
      row.className = "vl-links";
      let node = deref(locals[name], byId);
      const seen = new Set();
      for (let guard = 0; node && guard < 16; guard += 1) {
        if (node.t === "alias" || (node.id && seen.has(node.id))) break;
        if (!isLink(node)) break;
        if (node.id) seen.add(node.id);
        const box = document.createElement("div");
        box.className = "vl-node";
        if (node.id) box.dataset.vid = "node-" + node.id;
        const next = deref(dictGet(node, "next"), byId);
        const nextId = next && next.t !== "none" && next.id ? next.id : null;
        if (nextId) box.dataset.next = "node-" + nextId;
        const labels = Object.keys(locals).filter((key) => {
          const value = locals[key];
          return value && key !== name && ((value.t === "alias" && value.id === node.id) || value.id === node.id);
        });
        if (labels.length) {
          box.classList.add("is-now");
          const small = document.createElement("small");
          small.textContent = labels.join(" ");
          box.appendChild(small);
        }
        box.appendChild(document.createTextNode(pyFmt(dictGet(node, "val"))));
        row.appendChild(box);
        if (!next || next.t === "none") break;
        node = next;
      }
      stage.appendChild(row);
      host.appendChild(stage);
    });
    return true;
  }

  function renderTree(host, source) {
    const { locals, byId } = nodeIndex(source);
    const name = ["tree", "root", "node"].find((item) => isTree(deref(locals[item], byId)))
      || Object.keys(locals).find((item) => isTree(deref(locals[item], byId)));
    if (!name) return false;
    const stage = document.createElement("div");
    stage.className = "vl-treestage";
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.classList.add("vl-wires");
    stage.appendChild(svg);
    stage.appendChild(treeNode(deref(locals[name], byId), locals, 0));
    host.appendChild(stage);
    return true;
  }

  function treeNode(node, locals, depth) {
    const wrap = document.createElement("div");
    wrap.className = "vl-tree";
    if (!node || node.t === "none" || depth > 5) {
      wrap.textContent = "·";
      return wrap;
    }
    if (node.t === "alias") {
      wrap.textContent = "↺ #" + node.id;
      return wrap;
    }
    if (!isTree(node)) {
      wrap.textContent = compact(node);
      return wrap;
    }
    const box = document.createElement("div");
    box.className = "vl-node";
    if (node.id) box.dataset.vid = "node-" + node.id;
    const labels = Object.keys(locals).filter((key) => {
      const value = locals[key];
      return value && value.id === node.id && (value.t === "alias" || value.t === "dict");
    });
    if (labels.length) {
      box.classList.add("is-now");
      const small = document.createElement("small");
      small.textContent = labels.join(" ");
      box.appendChild(small);
    }
    box.appendChild(document.createTextNode(pyFmt(dictGet(node, "val"))));
    wrap.appendChild(box);
    const kids = document.createElement("div");
    kids.className = "vl-tree-kids";
    kids.appendChild(treeNode(dictGet(node, "left"), locals, depth + 1));
    kids.appendChild(treeNode(dictGet(node, "right"), locals, depth + 1));
    wrap.appendChild(kids);
    return wrap;
  }

  function adjacencyOf(node) {
    if (!node) return null;
    if (isLink(node) || isTree(node)) return null;
    const edges = [];
    const ids = [];
    const add = (id) => { if (ids.indexOf(id) < 0) ids.push(id); };
    if (node.t === "dict") {
      let lists = 0;
      node.v.forEach(([key, value]) => {
        if (!key || (key.t !== "int" && key.t !== "str")) return;
        add(key.v);
        if (!value || value.t !== "list") return;
        lists += 1;
        value.v.forEach((nxt) => {
          if (nxt.t === "int" || nxt.t === "str") {
            add(nxt.v);
            edges.push([key.v, nxt.v]);
          } else if ((nxt.t === "list" || nxt.t === "tuple") && nxt.v[0] && (nxt.v[0].t === "int" || nxt.v[0].t === "str")) {
            add(nxt.v[0].v);
            edges.push([key.v, nxt.v[0].v]);
          }
        });
      });
      if (!edges.length || lists < 1) return null;
      return { nodes: ids, edges };
    }
    if (node.t === "list" && node.v.length > 1 && node.v.every((row) => row.t === "list" && row.v.every((item) => item.t === "int"))) {
      const count = node.v.length;
      const inRange = node.v.every((row) => row.v.every((item) => item.v >= 0 && item.v < count));
      if (!inRange) return null;
      node.v.forEach((row, index) => {
        add(index);
        row.v.forEach((nxt) => {
          add(nxt.v);
          edges.push([index, nxt.v]);
        });
      });
      if (!edges.length) return null;
      return { nodes: ids, edges };
    }
    return null;
  }

  function graphLevels(nodes, edges, root) {
    const kids = new Map();
    nodes.forEach((id) => kids.set(String(id), []));
    edges.forEach(([from, to]) => {
      if (!kids.has(String(from))) kids.set(String(from), []);
      if (!kids.has(String(to))) kids.set(String(to), []);
      kids.get(String(from)).push(String(to));
    });
    const start = root != null && kids.has(String(root)) ? String(root) : String(nodes[0]);
    const level = new Map();
    const queue = [start];
    level.set(start, 0);
    while (queue.length) {
      const current = queue.shift();
      kids.get(current).forEach((next) => {
        if (level.has(next)) return;
        level.set(next, level.get(current) + 1);
        queue.push(next);
      });
    }
    kids.forEach((value, id) => { if (!level.has(id)) level.set(id, (level.get(start) || 0) + 1); });
    return level;
  }

  function drawLiveGraph(host, locals, used) {
    const name = (locals.graph && adjacencyOf(locals.graph) ? "graph" : null)
      || Object.keys(locals).find((item) => adjacencyOf(locals[item]));
    if (!name) return false;
    if (used) {
      used.add(name);
      ["visited", "seen", "vis"].forEach((item) => { if (locals[item]) used.add(item); });
    }
    return renderGraph(host, locals, { focus: [name] });
  }

  function renderGraph(host, locals, problem) {
    problem = problem || {};
    const named = problem.focus && problem.focus[0] && locals[problem.focus[0]] ? problem.focus[0] : "";
    const sourceName = named || (locals.graph ? "graph" : "");
    let parsed = sourceName ? adjacencyOf(locals[sourceName]) : null;
    const extra = problem.extra;
    let nodes = parsed ? parsed.nodes : extra && extra.nodes ? extra.nodes.slice() : [];
    let edges = parsed ? parsed.edges : extra && extra.edges ? extra.edges.slice() : [];
    if (!nodes.length) return false;
    const root = locals.start && (locals.start.t === "int" || locals.start.t === "str") ? locals.start.v : nodes[0];
    const level = graphLevels(nodes, edges, root);
    const rows = new Map();
    level.forEach((depth, id) => {
      if (!rows.has(depth)) rows.set(depth, []);
      rows.get(depth).push(id);
    });
    const depths = [...rows.keys()].sort((a, b) => a - b);
    const width = 360;
    const rowH = 64;
    const pos = new Map();
    depths.forEach((depth) => {
      const row = rows.get(depth);
      row.forEach((id, index) => {
        const x = row.length === 1 ? width / 2 : 48 + (index * (width - 96)) / (row.length - 1);
        pos.set(id, [x, 32 + depth * rowH]);
      });
    });
    const height = 48 + depths.length * rowH;
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 " + width + " " + height);
    svg.classList.add("vl-graph");
    const marker = svgEl("marker", { id: "vl-gedge", markerWidth: "8", markerHeight: "8", refX: "7", refY: "3", orient: "auto" });
    marker.appendChild(svgEl("path", { d: "M0,0 L8,3 L0,6 Z", fill: "#8fb4d4" }));
    const defs = svgEl("defs");
    defs.appendChild(marker);
    svg.appendChild(defs);
    const seen = new Set();
    ["seen", "visited", "vis", "order"].forEach((name) => {
      const value = locals[name];
      if (!value) return;
      if (value.t === "list" || value.t === "set" || value.t === "tuple") {
        value.v.forEach((item) => { if (item.t === "int" || item.t === "str") seen.add(String(item.v)); });
      }
    });
    const currentNode = ["node", "u", "cur", "at"].map((name) => locals[name]).find((value) => value && (value.t === "int" || value.t === "str"));
    edges.forEach((edge) => {
      const a = pos.get(String(edge[0]));
      const b = pos.get(String(edge[1]));
      if (!a || !b) return;
      const dx = b[0] - a[0];
      const dy = b[1] - a[1];
      const len = Math.hypot(dx, dy) || 1;
      const line = svgEl("line", {
        x1: a[0] + (dx / len) * 20,
        y1: a[1] + (dy / len) * 20,
        x2: b[0] - (dx / len) * 22,
        y2: b[1] - (dy / len) * 22,
        stroke: "#8fb4d4",
        "stroke-width": "2",
        "marker-end": "url(#vl-gedge)",
      });
      svg.appendChild(line);
    });
    nodes.forEach((id) => {
      const p = pos.get(String(id));
      if (!p) return;
      const isCurrent = currentNode && String(currentNode.v) === String(id);
      const visited = seen.has(String(id));
      const circle = svgEl("circle", {
        cx: p[0],
        cy: p[1],
        r: "18",
        fill: isCurrent ? "#facc15" : visited ? "#2563eb" : "#17202a",
        stroke: isCurrent ? "#fde68a" : visited ? "#93c5fd" : "#64748b",
        "stroke-width": isCurrent ? "3" : "2",
        class: isCurrent ? "is-hot" : "",
      });
      circle.dataset.vid = "g-" + id;
      svg.appendChild(circle);
      svg.appendChild(svgEl("text", {
        x: p[0],
        y: p[1] + 4,
        "text-anchor": "middle",
        fill: isCurrent ? "#1c1400" : "#e8eef4",
        "font-size": "13",
        "font-weight": "700",
      })).textContent = String(id);
    });
    if (sourceName) {
      const caption = document.createElement("div");
      caption.className = "vl-caption";
      caption.textContent = sourceName;
      host.appendChild(caption);
    }
    host.appendChild(svg);
    const key = document.createElement("p");
    key.className = "vl-key";
    key.innerHTML = "<span><b style=\"background:#facc15\"></b>Current</span><span><b style=\"background:#2563eb\"></b>Visited</span><span><b style=\"background:#17202a;box-shadow:inset 0 0 0 2px #64748b\"></b>Not yet</span>";
    host.appendChild(key);
    return true;
  }

  function renderRecursion(host, frame) {
    const stack = document.createElement("div");
    stack.className = "vl-stack";
    (frame.stack || []).forEach((item, index) => {
      const el = document.createElement("i");
      el.className = index === frame.stack.length - 1 ? "is-top" : "";
      const args = Object.keys(item.locals).slice(0, 3).map((name) => name + "=" + shortValue(item.locals[name])).join(", ");
      el.textContent = item.fn + "(" + args + ")";
      stack.appendChild(el);
    });
    host.appendChild(stack);
  }

  function renderFocus(host, locals, prevLocals, problem) {
    const wrap = document.createElement("div");
    wrap.className = "vl-kv";
    focusNames(problem, locals).forEach((name) => {
      const chip = document.createElement("div");
      const changed = JSON.stringify(prevLocals[name] || null) !== JSON.stringify(locals[name]);
      chip.className = changed ? "is-changed" : "";
      chip.textContent = name + " = " + compact(locals[name]);
      wrap.appendChild(chip);
    });
    host.appendChild(wrap);
  }

  function syncFromHash() {
    const hash = location.hash;
    if (hash === "#vl") showMap();
    else if (hash.startsWith("#vl/")) showTopic(decodeURIComponent(hash.slice(4)));
    else if (state.open) closeLab();
  }

  function bootChrome() {
    injectStyle();
    const header = document.querySelector("body > header");
    if (header && !header.querySelector(".vl-launch-bar")) {
      const bar = document.createElement("div");
      bar.className = "vl-launch-bar";
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "vl-launch";
      btn.textContent = "Visual Lab";
      btn.addEventListener("click", showMap);
      bar.appendChild(btn);
      const editorBtn = document.createElement("button");
      editorBtn.type = "button";
      editorBtn.className = "vl-launch";
      editorBtn.textContent = "Open editor";
      editorBtn.addEventListener("click", () => { location.href = pythonEditorHref(); });
      bar.appendChild(editorBtn);
      header.appendChild(bar);
    }
    const nav = document.querySelector(".layout > nav");
    if (nav && !nav.querySelector(".vl-nav-btn")) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "vl-nav-btn";
      btn.textContent = "Visual Lab roadmap";
      btn.addEventListener("click", showMap);
      const heading = nav.querySelector("h2");
      if (heading) heading.insertAdjacentElement("afterend", btn);
    }
    document.querySelectorAll("pre .code-run-btn").forEach((btn) => {
      const pre = btn.closest("pre");
      const fresh = btn.cloneNode(true);
      fresh.title = "Open this code in the editor";
      btn.replaceWith(fresh);
      fresh.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        const codeEl = pre.querySelector("code");
        const text = (codeEl ? codeEl.textContent : pre.textContent).trim();
        try { sessionStorage.setItem("vl-seed-code", text); } catch (err) { /* private mode */ }
        location.href = pythonEditorHref();
      });
    });
    const main = document.querySelector(".layout > main");
    if (main && !main.querySelector(".vl-banner")) {
      const banner = document.createElement("section");
      banner.className = "vl-banner";
      banner.innerHTML = `
        <div>
          <p class="vl-kicker">Visual Lab</p>
          <h2>See the flow, the memory, and the output</h2>
          <p>Every topic has a problem. Hover the roadmap to see what to learn first, then run your own Python and watch each step.</p>
        </div>
        <button type="button" class="vl-banner-btn">Open the full roadmap</button>
      `;
      banner.querySelector("button").addEventListener("click", showMap);
      main.insertBefore(banner, main.firstChild);
    }
    document.querySelectorAll("section[id^='topic-']").forEach((section) => {
      if (section.querySelector(".vl-jump")) return;
      const heading = section.querySelector("h2");
      if (!heading) return;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "vl-jump";
      btn.textContent = "Solve and visualize";
      btn.addEventListener("click", () => showTopic(section.id));
      heading.insertAdjacentElement("afterend", btn);
    });
    paintNavMarks();
    window.addEventListener("resize", () => {
      if (!ui.root || ui.root.hidden) return;
      ui.root.querySelectorAll(".vl-picture").forEach((picture) => {
        const fit = picture.querySelector(".vl-fit");
        if (fit) fitWatch(picture, fit);
      });
    });
    document.addEventListener("mousedown", (event) => {
      if (!suggestBox) return;
      if (suggestBox.contains(event.target)) return;
      if (event.target === ui.editor) return;
      closeSuggest();
    });
    state.reveal = localStorage.getItem(REVEAL_KEY) === "1";
    document.addEventListener("keydown", (event) => {
      if (!state.open) return;
        if (event.key === "Escape") {
          if (closeSuggest()) return;
          if (editorOnly()) return;
          event.preventDefault();
          event.stopImmediatePropagation();
          closeLab();
        }
      if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
        event.preventDefault();
        event.stopImmediatePropagation();
        runUser(true);
        return;
      }
      if (!event.altKey) return;
      const side = shownSide();
      if (event.key === "ArrowRight") {
        event.preventDefault();
        stopPlay();
        step(side, 1);
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        stopPlay();
        step(side, -1);
      } else if (event.key === " " || event.code === "Space") {
        event.preventDefault();
        play(side);
      } else if (event.key === "Home") {
        event.preventDefault();
        jump(side, 0);
      }
    }, true);
    window.__vlOpenEditor = openEditorWith;
    try {
      const seed = sessionStorage.getItem("vl-seed-code");
      if (seed != null) {
        sessionStorage.removeItem("vl-seed-code");
        state.seedCode = seed;
      }
    } catch (err) { /* storage blocked */ }
    window.addEventListener("hashchange", syncFromHash);
    window.addEventListener("popstate", syncFromHash);
    if (location.hash === "#vl" || location.hash.startsWith("#vl/")) syncFromHash();
    else if (state.seedCode != null) showPlayground();
  }

  function editorOnly() {
    return document.documentElement.getAttribute("data-editor") === "standalone";
  }

  function courseFile() {
    const name = (location.pathname.split("/").pop() || "").split("?")[0];
    if (name !== "dsa-master-course.html" && name !== "Foundations_of_Artificial_Intelligence.html") return "";
    return name + (location.hash || "");
  }

  function pythonEditorHref() {
    const back = courseFile();
    return back ? "code-editor.html?from=" + encodeURIComponent(back) : "code-editor.html";
  }

  function editorFrom() {
    if (!editorOnly()) return "";
    let raw = "";
    try { raw = new URLSearchParams(location.search).get("from") || ""; } catch (err) { return ""; }
    if (/^(dsa-master-course|Foundations_of_Artificial_Intelligence)\.html(?:#[\w./~%-]*)?$/.test(raw)) return raw;
    return "";
  }

  function leaveEditor() {
    location.href = editorFrom() || "index.html";
  }

  function paintEditorHome() {
    if (!ui.root) return;
    const home = ui.root.querySelector("[data-act=home]");
    const badge = ui.root.querySelector("[data-lang]");
    const closeBtn = ui.root.querySelector("[data-act=close]");
    if (!editorOnly()) {
      if (home) home.hidden = true;
      if (badge) badge.hidden = true;
      return;
    }
    const back = editorFrom();
    if (home) {
      home.hidden = false;
      home.textContent = back ? "Close" : "Portfolio";
      home.title = back ? "Return to the course" : "Go to the portfolio";
    }
    if (badge) badge.hidden = false;
    if (closeBtn) closeBtn.hidden = true;
    ui.back.hidden = true;
  }

  function bootStandalone() {
    injectStyle();
    window.addEventListener("resize", () => {
      if (!ui.root || ui.root.hidden) return;
      ui.root.querySelectorAll(".vl-picture").forEach((picture) => {
        const fit = picture.querySelector(".vl-fit");
        if (fit) fitWatch(picture, fit);
      });
    });
    document.addEventListener("mousedown", (event) => {
      if (!suggestBox) return;
      if (suggestBox.contains(event.target)) return;
      if (event.target === ui.editor) return;
      closeSuggest();
    });
    state.reveal = localStorage.getItem(REVEAL_KEY) === "1";
    document.addEventListener("keydown", (event) => {
      if (!state.open) return;
      if (event.key === "Escape") {
        if (closeSuggest()) return;
        if (editorFrom()) {
          event.preventDefault();
          leaveEditor();
        }
        return;
      }
      if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
        event.preventDefault();
        runUser(true);
      }
    }, true);
    window.__vlOpenEditor = openEditorWith;
    try {
      const seed = sessionStorage.getItem("vl-seed-code");
      if (seed != null) {
        sessionStorage.removeItem("vl-seed-code");
        state.seedCode = seed;
      }
    } catch (err) { /* storage blocked */ }
    showPlayground();
    document.title = "Python editor";
    if (ui.root) ui.root.setAttribute("aria-label", "Python editor");
  }

  function init() {
    if (booted) return;
    if (editorOnly()) {
      booted = true;
      bootStandalone();
      return;
    }
    if (!window.DSA_PROBLEMS || !document.querySelector(".layout > nav")) return;
    booted = true;
    bootChrome();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
