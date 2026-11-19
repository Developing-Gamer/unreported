Label --pastebin=failed pastes with the assertion location

Root cause: pastebin.py took `reprtraceback.reprentries[0].reprfileloc`, the outermost frame (the test's call into a helper), while the pasted traceback ends at the failing assertion in the last entry.

Change: use `reprentries[-1]`. Added test `test_failed_helper_label_uses_assertion_location` in testing/test_pastebin.py and changelog/6000.bugfix.rst.

Verification: testing/test_pastebin.py passes.
