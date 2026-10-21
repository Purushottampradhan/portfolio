const assert = require("assert");
const lab = require("./dsa-visual-lab.js");

const prev = {
  e: "line",
  fn: "solve",
  line: 1,
  out_n: 0,
  stack: [{ fn: "solve", locals: { nums: { t: "list", id: 1, v: [{ t: "int", v: 4 }] }, i: { t: "int", v: 0 } } }],
};
const frame = {
  e: "line",
  fn: "solve",
  line: 2,
  out_n: 4,
  stack: [{ fn: "solve", locals: { nums: { t: "list", id: 1, v: [{ t: "int", v: 4 }] }, i: { t: "int", v: 1 } } }],
};
const source = "i = 0\ni = 1\nprint(i)\n";

assert.deepStrictEqual(lab.changedPairs(prev, frame).map((pair) => pair[0]), ["i"]);
assert.strictEqual(lab.clampIndex(-3, 4), 0);
assert.strictEqual(lab.clampIndex(9, 4), 3);
assert.strictEqual(lab.clampIndex(0, 0), 0);
assert.strictEqual(lab.stdoutAt("hi\nthere", 3), "hi\n");
assert.strictEqual(lab.stdoutAt("hi", 0), "");
assert.match(lab.narration(frame, prev, source), /i is now 1/);
assert.match(lab.whyLine(frame), /previous recorded step/);
assert.match(lab.nextFact({ frames: [prev, frame], i: 0 }, source), /Next line: `i = 1`/);
assert.match(lab.nextFact({ frames: [frame], i: 0 }, source), /last recorded step/);
assert.match(lab.errorHint("NameError: name 'x' is not defined"), /not stored/);
assert.match(lab.errorHint("Stopped after 650 steps."), /650 steps/);
assert.strictEqual(lab.sourceLine(source, 2), "i = 1");

const back = lab.changedPairs(frame, prev).map((pair) => pair[0]);
assert.deepStrictEqual(back, ["i"]);

assert.strictEqual(lab.layoutKind({ stack: [{ fn: "solve", locals: {} }, { fn: "walk", locals: {} }] }), "recursion");
assert.strictEqual(lab.layoutKind({ stack: [{ fn: "<module>", locals: { nums: { t: "list", v: [{ t: "int", v: 1 }] } } }] }), "array");
assert.strictEqual(lab.layoutKind(null), "simple");
const stats = lab.stepStats({
  i: 1,
  stdout: "hi",
  frames: [
    { e: "call", fn: "solve", line: 1, out_n: 0, stack: [{ fn: "solve", locals: {} }] },
    frame,
  ],
});
assert.strictEqual(stats.step, 2);
assert.strictEqual(stats.total, 2);
assert.strictEqual(stats.calls, 1);
assert.strictEqual(stats.printed, 2);

function frozenFrame(locals, extra) {
  return Object.assign({ e: "line", fn: "solve", line: 3, out_n: 0, stack: [{ fn: "solve", locals }] }, extra || {});
}
function num(value) {
  return { t: "int", v: value };
}
function nums(values) {
  return { t: "list", id: 1, v: values.map(num) };
}
let ev = lab.deriveEvents(frozenFrame({ nums: nums([1, 2, 3]) }), frozenFrame({ nums: nums([1, 3, 2]) }));
assert.deepStrictEqual([ev.find((event) => event.type === "swap").i, ev.find((event) => event.type === "swap").j], [1, 2]);
ev = lab.deriveEvents(frozenFrame({ nums: nums([1]) }), frozenFrame({ nums: nums([1, 2]) }));
assert.ok(ev.some((event) => event.type === "insert" && event.name === "nums"));
assert.ok(!ev.some((event) => event.type === "push"));
ev = lab.deriveEvents(frozenFrame({ stack: nums([1]) }), frozenFrame({ stack: nums([1, 2]) }));
assert.strictEqual(ev.find((event) => event.type === "push").value.v, 2);
ev = lab.deriveEvents(frozenFrame({ stack: nums([1, 2]) }), frozenFrame({ stack: nums([1]) }));
assert.strictEqual(ev.find((event) => event.type === "pop").value.v, 2);
ev = lab.deriveEvents(frozenFrame({ queue: nums([1, 2]) }), frozenFrame({ queue: nums([2]) }));
assert.strictEqual(ev.find((event) => event.type === "dequeue").value.v, 1);
ev = lab.deriveEvents(frozenFrame({ queue: nums([1, 2]) }), frozenFrame({ queue: nums([1]) }));
assert.ok(ev.some((event) => event.type === "remove"));
assert.ok(!ev.some((event) => event.type === "dequeue"));
ev = lab.deriveEvents(frozenFrame({ i: num(0), nums: nums([4, 9]) }), frozenFrame({ i: num(1), nums: nums([4, 9]) }));
assert.deepStrictEqual([ev.find((event) => event.type === "pointer").from, ev.find((event) => event.type === "pointer").to], [0, 1]);
const linkA = { t: "dict", id: 2, v: [[{ t: "str", v: "val" }, num(1)], [{ t: "str", v: "next" }, { t: "none", v: null }]] };
const linkB = { t: "dict", id: 2, v: [[{ t: "str", v: "val" }, num(1)], [{ t: "str", v: "next" }, { t: "alias", id: 9 }]] };
ev = lab.deriveEvents(frozenFrame({ head: linkA }), frozenFrame({ head: linkB }));
assert.strictEqual(ev.find((event) => event.type === "link").to, 9);
ev = lab.deriveEvents(frozenFrame({ heap: nums([2, 1]) }), frozenFrame({ heap: nums([1, 2]) }));
assert.strictEqual(ev.find((event) => event.type === "swap").heap, "sift-up");
ev = lab.deriveEvents(frozenFrame({ nums: nums([1, 3, 2]) }), frozenFrame({ nums: nums([1, 2, 3]) }));
assert.ok(ev.some((event) => event.type === "swap"));
const last = frozenFrame({ x: num(1) }, { out_n: 2 });
const traced = { stdout: "hi", error: "NameError: x", frames: [last] };
ev = lab.deriveEvents(frozenFrame({}, { out_n: 0 }), last, traced);
assert.ok(ev.some((event) => event.type === "print"));
assert.ok(ev.some((event) => event.type === "exception"));
ev = lab.deriveEvents(null, frozenFrame({}, { e: "call", fn: "solve" }));
assert.ok(ev.some((event) => event.type === "call" && event.fn === "solve"));
assert.match(lab.describeEvents(ev), /Call solve/);

function stepFrame(values) {
  return {
    e: "line",
    fn: "solve",
    line: 1,
    stack: [{ fn: "solve", locals: { nums: { t: "list", v: values.map((value) => ({ t: "int", v: value })) } } }],
  };
}
const steps = [stepFrame([1, 2, 3]), stepFrame([1, 3, 2]), stepFrame([1, 3, 2, 9]), stepFrame([3, 2, 9])];
let ids = lab.trackListIds(steps, 0).nums;
const first = ids[0];
const second = ids[1];
const third = ids[2];
ids = lab.trackListIds(steps, 1).nums;
assert.deepStrictEqual(ids, [first, third, second]);
ids = lab.trackListIds(steps, 2).nums;
assert.strictEqual(ids[0], first);
assert.strictEqual(ids[1], third);
assert.strictEqual(ids[2], second);
assert.ok(ids[3] && ids[3] !== first);
ids = lab.trackListIds(steps, 3).nums;
assert.deepStrictEqual(ids.slice(0, 2), [third, second]);
assert.ok(lab.motionMs(2) < lab.motionMs(0.5));
assert.ok(lab.motionMs(1) >= 140 && lab.motionMs(1) <= 420);

assert.deepStrictEqual(lab.loopRoles("for i in numArray:\n    if i == num:"), { i: { mode: "item", over: "numArray" } });
assert.deepStrictEqual(lab.loopRoles("for i in range(len(nums)):"), { i: { mode: "index", over: "" } });

function scanFrame(fn, names) {
  return { e: "line", fn, line: 2, stack: [{ fn, locals: names }] };
}
const search = [
  scanFrame("solve", { num: { t: "int", v: 1 }, numArray: { t: "list", v: [3, 4, 5, 6, 1].map((v) => ({ t: "int", v })) } }),
  scanFrame("solve", { num: { t: "int", v: 1 }, i: { t: "int", v: 3 }, numArray: { t: "list", v: [] } }),
  scanFrame("solve", { num: { t: "int", v: 1 }, i: { t: "int", v: 4 }, numArray: { t: "list", v: [] } }),
  scanFrame("solve", { num: { t: "int", v: 1 }, i: { t: "int", v: 1 }, numArray: { t: "list", v: [] } }),
];
assert.strictEqual(lab.itemCursor(search, 0, "i"), -1);
assert.strictEqual(lab.itemCursor(search, 1, "i"), 0);
assert.strictEqual(lab.itemCursor(search, 2, "i"), 1);
assert.strictEqual(lab.itemCursor(search, 3, "i"), 2);

console.log("dsa-visual-lab tests passed");
