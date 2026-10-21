#!/usr/bin/env python3
"""Build dsa-problems.js and check every solution. Run from this directory."""

import json
import re
import signal
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROBLEMS = []


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


def add(tid, title, viz, focus, prompt, idea, steps, hint, solution, calls, extra=None, expect=None):
    solution = textwrap.dedent(solution).strip() + "\n"
    def_line = next(line for line in solution.splitlines() if line.startswith("def solve"))
    starter = def_line + "\n    # " + " ".join(hint.split()) + "\n    pass\n"
    PROBLEMS.append({
        "id": tid,
        "title": title,
        "viz": viz,
        "focus": focus,
        "prompt": prompt,
        "idea": idea,
        "steps": steps,
        "hint": hint,
        "starter": starter,
        "solution": solution,
        "calls": calls,
        "extra": extra,
        "expect": expect,
    })


def count_steps(source, call):
    steps = {"n": 0}
    ns = {}
    exec(compile(source, "<student>", "exec"), ns, ns)

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<student>":
            return None
        if event in ("line", "call", "return"):
            steps["n"] += 1
            if steps["n"] > 620:
                raise RuntimeError("too many steps")
        return tracer

    sys.settrace(tracer)
    try:
        eval(compile(call, "<student-call>", "eval"), ns, ns)
    finally:
        sys.settrace(None)
    return steps["n"]


def run_call(source, call):
    ns = {}
    exec(compile(source, "<student>", "exec"), ns, ns)
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(2)
    try:
        return eval(compile(call, "<student-call>", "eval"), ns, ns)
    finally:
        signal.alarm(0)


def main():
    from dsa_lab_catalog import register
    register(add)
    html = (ROOT / "dsa-master-course.html").read_text()
    seen = []
    for tid in re.findall(r'href="#(topic-\d+-\d+)"', html):
        if tid not in seen:
            seen.append(tid)
    by_id = {}
    for item in PROBLEMS:
        if item["id"] in by_id:
            raise SystemExit("duplicate problem " + item["id"])
        by_id[item["id"]] = item
    missing = [tid for tid in seen if tid not in by_id]
    extra = [tid for tid in by_id if tid not in seen]
    if missing or extra:
        raise SystemExit("missing %s\nextra %s" % (missing, extra))

    out = {}
    for tid in seen:
        item = by_id[tid]
        results = []
        for call in item["calls"]:
            try:
                value = run_call(item["solution"], call)
            except Exception as ex:
                raise SystemExit("%s %s failed: %s" % (tid, call, ex))
            again = run_call(item["solution"], call)
            if repr(value) != repr(again):
                raise SystemExit("%s %s is not deterministic" % (tid, call))
            if isinstance(value, set):
                raise SystemExit("%s returns a set" % tid)
            try:
                count_steps(item["solution"], call)
            except Exception as ex:
                raise SystemExit("%s %s trace: %s" % (tid, call, ex))
            results.append(value)
        if item["expect"] is not None and results != item["expect"]:
            raise SystemExit("%s expected %r got %r" % (tid, item["expect"], results))
        out[tid] = {
            "title": item["title"],
            "viz": item["viz"],
            "focus": item["focus"],
            "prompt": item["prompt"],
            "idea": item["idea"],
            "steps": item["steps"],
            "hint": item["hint"],
            "starter": item["starter"],
            "solution": item["solution"],
            "tests": [{"call": call, "expect": repr(value)} for call, value in zip(item["calls"], results)],
        }
        if item["extra"]:
            out[tid]["extra"] = item["extra"]
        print("%s %s -> %s" % (tid, item["calls"][0], repr(results[0])[:80]))

    target = ROOT / "dsa-problems.js"
    target.write_text("window.DSA_PROBLEMS = " + json.dumps(out, ensure_ascii=True, separators=(",", ":")) + ";\n")
    print("wrote", target, "topics", len(out))


if __name__ == "__main__":
    main()
