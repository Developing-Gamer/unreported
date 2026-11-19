Fix import of non-test `__init__.py` files during collection (#6194)

Root cause: `Package.collect()` called `self._mount_obj_if_needed()` unconditionally (added in 5.2.3 so that marks such as `pytestmark = pytest.mark.skip` in a package's `__init__.py` are honoured, #5830). Since every directory containing an `__init__.py` is turned into a `Package` node, this imported every `__init__.py` under the rootdir, even ones in directories with no tests and which do not match `python_files`, so e.g. a Windows-only package failed collection on Linux.

Change: `Package.collect()` now delegates to `_collect_nodes()` (the previous body) and mounts the package object lazily, just before yielding the first child node. Packages that contain nothing collectable are no longer imported, while packages with tests are still imported during collection so their marks apply (test_skip_package keeps passing).

Verification: added `test_does_not_import_unmatched_init_py` in testing/test_collection.py (fails before, passes after). Ran testing/test_collection.py, testing/test_skipping.py (incl. `test_skip_package`) and testing/python; no new failures compared to baseline. Added changelog/6194.bugfix.rst.
