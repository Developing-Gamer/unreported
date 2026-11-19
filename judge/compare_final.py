#!/usr/bin/env python3
"""Final PR comparison for the fix-only replays (GPT judge): a rerun (-xN job) replaces the original
trial of the same task; tasks whose replay fix never ran are reported separately."""
import glob, json, re

F = "../runs/fleet/"
PARTS = ["root_cause", "fix", "scope", "tests", "description", "total"]


def ran_dirs(prefix):
    """task -> True when some trial's fix session produced a report (reruns win)."""
    out = {}
    for d in sorted(glob.glob(f"{F}{prefix}-*/{prefix}-*/*__*/"), key=lambda d: "-x" in d):
        task = d.rstrip("/").split("/")[-1].rsplit("__", 1)[0]
        ok = False
        for f in glob.glob(d + "agent/sd-*-fix.result.json"):
            try:
                ok = ok or bool(json.load(open(f)).get("report"))
            except Exception:
                pass
        out[task] = ok if "-x" in d else out.get(task, False) or ok
    return out


def rows(path, system):
    out = {}
    for r in sorted(json.load(open(path)), key=lambda r: "-x" in r["job"]):  # reruns last, so they win
        if re.sub(r"-(p|h|q|e|x|y|t|u|w)?\d+$", "", r["job"]) == system:
            out[r["task"]] = r
    return out


def score(r, ts, p):
    return sum(((r[t]["judge"] or {}).get("gpt") or {}).get(p) or 0 for t in ts) / len(ts)


for model, cc, full, ff, rp, rf in [("Opus (shipped: Opus investigates, Sonnet fixes)", "f4o-cc", "f9s-sd", "results-f9s.json", "rpo0", "results-rpo.json"),
                                    ("Sonnet", "f4c-cc", "f7c-sd", "results-f7c.json", "rpc0", "results-rpc.json")]:
    data = [("Claude Code", rows("results-final.json", cc)), ("Bonzai full run", rows(ff, full)), ("Bonzai own diff", rows(rf, rp))]
    ran = ran_dirs(rp)
    common = sorted(set.intersection(*(set(r) for _, r in data)))
    ok = [t for t in common if ran.get(t)]
    print(f"\n{model}: {len(ok)} of {len(common)} tasks where the replayed fix ran; not run: {[t for t in common if not ran.get(t)]}")
    print(f"{'':18}" + "".join(f"{p:>12}" for p in PARTS) + f"{'reported':>10}")
    for n, r in data:
        print(f"{n:18}" + "".join(f"{score(r, ok, p):12.1f}" for p in PARTS) + f"{sum(r[t]['resolved'] for t in ok):>10}")
    # All tasks: where the replay did not run a fix, keep the full run's own score for that task.
    allr = {t: (data[2][1][t] if ran.get(t) else data[1][1][t]) for t in common}
    print(f"{'all tasks, Bonzai':18}" + "".join(f"{score(allr, common, p):12.1f}" for p in PARTS) + f"{sum(allr[t]['resolved'] for t in common):>10}")
    print(f"{'all tasks, CC':18}" + "".join(f"{score(data[0][1], common, p):12.1f}" for p in PARTS) + f"{sum(data[0][1][t]['resolved'] for t in common):>10}")
