Fix regression in 5.2.3: do not import non-test package `__init__.py` files during collection

## Root cause
The 5.2.3 fix for #5830 (skip marks in a package `__init__.py` not applying to the package's first test) added `self._mount_obj_if_needed()` at the top of `Package.collect()` in `src/_pytest/python.py`. That call imports the package's `__init__.py` for every package pytest walks into, even when `__init__.py` does not match `python_files`. Packages that can't be imported on the current platform (or that have import-time side effects) now fail collection with errors like `ERROR collecting foobar/__init__.py`.

## Change
- Removed the eager `self._mount_obj_if_needed()` call from `Package.collect()`. A package's `__init__.py` is imported only when it is needed again: when it matches `python_files`, or when the package's setup/teardown runs.
- This reverts the 5.2.3 change for #5830, as upstream 5.2.4 did. `testing/test_skipping.py::test_skip_package` is now marked `xfail(strict=True)` with the reason, so the known limitation stays documented. Strict mode means the test will flag when #5830 gets a proper fix.
- Added `changelog/6194.bugfix.rst`.

## Verification
- Reproduced the issue's scenario (`foobar/__init__.py` containing `assert False` next to `test_foo.py`). Before the fix it gave 1 error; after the fix, 1 passed.
- New regression test `testing/test_collection.py::test_does_not_eagerly_collect_packages` fails before the change and passes after it.
- `testing/test_collection.py`, `test_skipping.py`, `test_mark.py`, `test_terminal.py`: 353 passed, 7 skipped, 3 xfailed. On a wider run (`testing/python` without the `hypothesis`-dependent `metafunc.py`, `acceptance_test.py`, `test_runner.py`, `test_session.py`, `test_nodes.py`), no new failures compared with before the change. The remaining failures already happened before (they come from the environment, e.g. no `pkg_resources`/setuptools).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
