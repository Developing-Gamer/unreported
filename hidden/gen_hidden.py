#!/usr/bin/env python3
"""Hidden problems for factory v3: real-looking defects nobody reported, each with a hidden test and
only a weak production trace.

Runs on a VM with Docker and the factory tasks. For each task: picks library modules the reported
bug's fix does not touch, asks GPT-6.1 Sol (high effort) for one subtle defect in one of them, a
pytest test that catches it, and a weak signal (what production would show, never the cause or the
file), then keeps the candidate only when, in the task's own image:
  1. the defect patch applies to the checkout and the test fails on it with an assertion, not an
     import or collection error;
  2. the test passes once the defect is reverted;
  3. with the reported bug's own fix applied, the reported bug's tests give exactly the same results
     with and without the defect (so the hidden defect never changes the reported bug's score).

  gen_hidden.py <tasks dir> <task name> [<task name> ...]   -> hidden/<task>.json
"""
import json, os, random, re, subprocess, sys, tempfile, urllib.request
from pathlib import Path

TASKS = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent
CATEGORIES = ["silent wrong result (a value or output that is subtly wrong, no exception)",
              "swallowed error (an exception caught and ignored, or an error path that returns a default)",
              "edge case (empty, zero, unicode, boundary or None input handled wrongly)",
              "resource handling (a file, handle or connection not closed, or state leaking between calls)",
              "security weakness (input validation, path handling or escaping that lets bad input through)"]
PROMPT = """You are building a benchmark of hidden software problems: defects nobody has reported, which careful maintainers should find from weak production traces. Below is one module of the {repo} repository, at a real past commit.

Introduce ONE subtle, realistic defect into this module of category: {category}.
- It must look like an ordinary regression a developer could plausibly write (a refactor slip, a wrong default, an off-by-one, a missing check), with no comment or naming that points at it.
- It must not crash on import, must not break most of the module, and must change behaviour only for some inputs.
- Do not touch these files: {forbidden}.

Return JSON only:
{{"defect_patch": "<a unified diff against the module as shown, paths a/{path} and b/{path}>",
  "test_code": "<a complete pytest file that imports the library normally, fails on the defect with an assertion and passes on the original code; no network, under 10 seconds>",
  "signal": {{"kind": "log" or "metric" or "warning" or "user", "source": "<service, dashboard or channel name>", "text": "<what production shows: a log line, a metric change, a warning-level event without stack, or a vague user complaint. Describe the symptom only, as someone would see it. Never name the file, function, cause or fix>"}},
  "summary": "<one sentence for the answer key: what the defect is>"}}

<module path="{path}">
{code}
</module>"""


def sh(cmd, check=False, timeout=900):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode:
        raise RuntimeError(f"{cmd[:120]}: {r.stderr[-400:]}")
    return r


def ask(prompt):
    body = json.dumps({"model": "gpt-6.1-sol", "input": prompt, "reasoning": {"effort": "high"}, "store": False}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/responses", body,
                                 {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", "Content-Type": "application/json"})
    data = json.load(urllib.request.urlopen(req, timeout=600))
    text = "".join(c.get("text", "") for it in data.get("output", []) for c in it.get("content", []) or [] if c.get("type") == "output_text")
    return json.loads(re.search(r"\{.*\}", text, re.S).group(0))


def image(task):
    return re.search(r"^FROM (\S+)", (TASKS / task / "environment" / "Dockerfile").read_text(), re.M).group(1)


def in_container(cid, script, timeout=900):
    return sh(f"docker exec {cid} bash -lc {json.dumps('source /opt/miniconda3/bin/activate && conda activate testbed && cd /testbed && ' + script)}", timeout=timeout)


def solution_patch(task):
    text = (TASKS / task / "solution" / "solve.sh").read_text()
    m = re.search(r"<< '__SOLUTION__'\n(.*?)\n__SOLUTION__", text, re.S)
    return m.group(1) + "\n" if m else ""


def put(cid, path, content):
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(content)
    sh(f"docker cp {f.name} {cid}:{path}", check=True)
    os.unlink(f.name)


ANSI = re.compile(r"\x1b\[[0-9;]*m")
RESULT_LINE = re.compile(r"^(PASSED|FAILED|ERROR|XFAIL|XPASS) \S+|^\S*test_\w+ .*\b(ok|FAIL|ERROR|F|E)$|^test_\w+ \S+$")


def verifier_results(task, defect):
    """The reported bug's test results (the task's verifier log) with its own fix applied, and the
    defect too when given."""
    cid = sh(f"docker run -d -v {TASKS / task / 'tests'}:/tests:ro {image(task)} sleep 3600", check=True).stdout.strip()
    try:
        put(cid, "/tmp/gold.diff", solution_patch(task))
        step = ""
        if defect:
            put(cid, "/tmp/defect.diff", defect)
            step = "git apply --recount /tmp/defect.diff && "
        r = in_container(cid, f"{step}patch --fuzz=5 -p1 -i /tmp/gold.diff >/dev/null && mkdir -p /logs/verifier && bash /tests/test.sh > /tmp/verify.log 2>&1; cat /tmp/verify.log", timeout=2400)
        plain = ANSI.sub("", r.stdout)
        return sorted({l.strip() for l in plain.splitlines() if RESULT_LINE.match(l.strip())})
    finally:
        sh(f"docker rm -f {cid}")


def candidates(task, cid, rng):
    gold = solution_patch(task)
    forbidden = sorted(set(re.findall(r"^\+\+\+ b/(\S+)", gold, re.M)))
    files = in_container(cid, "git ls-files '*.py'").stdout.split()
    lib = [f for f in files if not re.search(r"(^|/)(tests?|testing|docs?|examples?|benchmarks?|extra|scripts?|tools|ci|bin|release)/|test_|conftest|setup\.py|/_vendor/|/externals?/|^[^/]+\.py$", f)
           and f not in forbidden]
    sized = []
    for f in lib:
        n = int((in_container(cid, f"wc -l < {f}").stdout or "0").strip() or 0)
        if 80 <= n <= 900:
            sized.append(f)
    rng.shuffle(sized)
    return sized[:10], forbidden


def generate(task):
    rng = random.Random(f"hidden/{task}")
    repo = task.split("__")[0] + "/" + task.split("__")[1].rsplit("-", 1)[0]
    cid = sh(f"docker run -d {image(task)} sleep 7200", check=True).stdout.strip()
    kept, tried = [], []
    try:
        in_container(cid, "python -m pytest --version >/dev/null 2>&1 || python -m pip install -q pytest")
        baseline = verifier_results(task, "")
        files, forbidden = candidates(task, cid, rng)
        for i, path in enumerate(files):
            if len(kept) >= 2:
                break
            category = CATEGORIES[(len(tried)) % len(CATEGORIES)]
            code = in_container(cid, f"cat {path}").stdout
            try:
                c = ask(PROMPT.format(repo=repo, category=category, forbidden=", ".join(forbidden) or "none", path=path, code=code))
            except Exception as e:
                tried.append({"path": path, "error": str(e)[:200]}); continue
            record = {"path": path, "category": category, **c}
            put(cid, "/tmp/defect.diff", c["defect_patch"])
            put(cid, "/tmp/test_hidden_problem.py", c["test_code"])
            applied = in_container(cid, "git apply --recount /tmp/defect.diff && echo applied").stdout.strip().endswith("applied")
            if not applied:
                tried.append({**record, "reject": "patch does not apply"}); continue
            normalized = in_container(cid, "git diff").stdout
            on_defect = in_container(cid, "python -m pytest -x -q -p no:cacheprovider /tmp/test_hidden_problem.py 2>&1 | tail -15", timeout=300).stdout
            in_container(cid, "git checkout -q -- .")
            on_clean = in_container(cid, "python -m pytest -x -q -p no:cacheprovider /tmp/test_hidden_problem.py 2>&1 | tail -5", timeout=300).stdout
            last = lambda out: (out.strip().splitlines() or [""])[-1].lower()
            fails_right = "failed" in last(on_defect) and "error" not in last(on_defect)
            passes_clean = "passed" in last(on_clean) and "failed" not in last(on_clean) and "error" not in last(on_clean)
            if not (fails_right and passes_clean):
                tried.append({**record, "reject": "test does not separate defect from original", "on_defect": on_defect[-300:], "on_clean": on_clean[-300:]}); continue
            if not baseline:
                tried.append({**record, "reject": "could not read the reported bug's test results"}); continue
            with_defect = verifier_results(task, normalized)
            if with_defect != baseline:
                tried.append({**record, "reject": "changes the reported bug's test results", "diff": sorted(set(baseline) ^ set(with_defect))[:6]}); continue
            kept.append({**record, "defect_patch": normalized})
    finally:
        sh(f"docker rm -f {cid}")
    (OUT / f"{task}.json").write_text(json.dumps({"task": task, "kept": kept, "rejected": tried}, indent=1))
    print(task, "kept", len(kept), "rejected", len(tried), flush=True)


if __name__ == "__main__":
    for t in sys.argv[2:]:
        generate(t)
