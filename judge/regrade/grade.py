# /// script
# requires-python = ">=3.11"
# dependencies = ["swebench==4.0.3", "datasets==2.16.1", "fastcore<1.11"]
# ///
"""Re-grade a saved SWE-bench test log exactly as the task's verifier does. Usage: grade.py config.json log.txt"""
import json, sys
from swebench.harness.grading import get_logs_eval, get_eval_tests_report, get_resolution_status
from swebench.harness.test_spec.test_spec import make_test_spec
from swebench.harness.constants import ResolvedStatus, EvalType, PASS_TO_PASS, FAIL_TO_PASS, KEY_INSTANCE_ID, FAIL_ONLY_REPOS, START_TEST_OUTPUT, END_TEST_OUTPUT
datum = json.load(open(sys.argv[1])); spec = make_test_spec(datum)
content = open(sys.argv[2]).read()
open(sys.argv[2], "w").write(f"{START_TEST_OUTPUT}\n{content}\n{END_TEST_OUTPUT}")
status, found = get_logs_eval(spec, sys.argv[2])
ok = False
if found:
    ref = {KEY_INSTANCE_ID: spec.instance_id, FAIL_TO_PASS: spec.FAIL_TO_PASS, PASS_TO_PASS: spec.PASS_TO_PASS}
    rep = get_eval_tests_report(status, ref, eval_type=EvalType.FAIL_ONLY if spec.repo in FAIL_ONLY_REPOS else EvalType.PASS_AND_FAIL)
    ok = get_resolution_status(rep) == ResolvedStatus.FULL.value
print("RESOLVED" if ok else ("UNRESOLVED" if found else "NOTFOUND"))
