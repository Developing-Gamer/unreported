Fixed Oracle test_db_signature() ignoring TEST["USER"], making aliases with different test schemas share one test database

## Overview
On Oracle, two aliases that share a login (`USER`) but configure different `TEST["USER"]` schemas got identical `test_db_signature()` values. `get_unique_databases_and_mirrors()` therefore grouped them and `setup_databases()` made the second alias a mirror of the first, copying its test USER/PASSWORD. The reporting alias then read the default alias's test schema and saw its fixtures.

## Details
- `django/db/backends/oracle/creation.py`: `test_db_signature()` now uses `self._test_database_user()` (the effective test user, `TEST["USER"]` or the `test_`-prefixed `USER`) instead of `settings_dict["USER"]`.
- `tests/backends/oracle/test_creation.py`: `TestDbSignatureTests` (runs without an Oracle connection) checks that different test users give different signatures, identical test users give identical ones, and the default test user still distinguishes different `USER`s.

Evidence: Oracle CI support channel — "The reporting alias can now see fixtures inserted through the default alias during tests, even though we configured separate test schemas."

## Verification
`cd tests && PYTHONPATH=/testbed python runtests.py backends.oracle.test_creation.TestDbSignatureTests`: before the fix `test_different_test_users` fails (`('localhost','1521','django.db.backends.oracle','xe','app') == (same)`); after, 3 tests pass. Not run against a live Oracle database.
