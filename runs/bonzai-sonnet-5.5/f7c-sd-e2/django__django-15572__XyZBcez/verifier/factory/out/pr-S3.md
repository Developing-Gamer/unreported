Fix Oracle test_db_signature() so aliases with different TEST USER get separate test databases

## Overview
On Oracle, two aliases that share the main `USER` but set different `TEST["USER"]` schemas (e.g. `default` and `reporting`) got the same `test_db_signature()`. `setup_databases()` then treated them as one database and made `reporting` a mirror of `default`, so `reporting` read and wrote the `default` test schema and saw its fixtures. The signature now uses the test user.

## Details
- `django/db/backends/oracle/creation.py`: `test_db_signature()` uses `self._test_database_user()` instead of `settings_dict["USER"]`. With no `TEST["USER"]`, the test user is derived from `USER`, so such aliases still share one test database.
- `tests/backends/oracle/test_creation.py`: new `SimpleTestCase` tests (no Oracle connection needed) for differing, equal and default test users.

## Verification
- New test `test_different_test_users_have_different_signatures` failed before the change (signatures equal) and passes after.
- `runtests.py backends.oracle.test_creation test_utils backends --parallel 1`: OK (skipped=97, Oracle/other-vendor tests).
- Not run on a real Oracle instance.
