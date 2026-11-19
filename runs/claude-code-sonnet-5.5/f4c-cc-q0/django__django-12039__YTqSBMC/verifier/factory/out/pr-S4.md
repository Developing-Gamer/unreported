Use proper whitespace in CREATE INDEX statements

Root cause: `Columns.__str__` concatenated the column suffix directly onto the quoted column name, producing `"name"DESC`. `IndexColumns.__str__` always appended a space plus the suffix, but `Index` passes `''` for ascending columns, so the output had a trailing space (`"name" text_pattern_ops `).

Change: in `django/db/backends/ddl_references.py`, both classes now add `' ' + suffix` only when the suffix is non-empty. Added tests in `tests/backends/test_ddl_references.py` for `Columns` with a descending suffix and for `IndexColumns` with opclasses, with and without a suffix.

Verification: ran `runtests.py backends.test_ddl_references indexes schema`. 186 tests ran and passed (32 skipped, mostly PostgreSQL-only).
