Fix `import astropy.io.ascii` under `python -OO`

## Root cause
`MetaBaseReader.__init__` in `astropy/io/ascii/core.py` builds reader/writer registry docstrings with `inspect.cleandoc(cls.__doc__)`. Under `python -OO`, docstrings are stripped and `cls.__doc__` is `None`, so `cleandoc` raises `AttributeError: 'NoneType' object has no attribute 'expandtabs'` while the first reader class (`Basic`) is being defined. That makes the whole subpackage impossible to import.

## Change
Use `inspect.cleandoc(cls.__doc__ or "")` for both the reader and writer docstrings.

## Verification
- `python -OO -c "import astropy.io.ascii; from astropy.table import Table; Table.read(['a b','1 2'], format='ascii')"` now succeeds. Before the change it failed with the traceback from the issue.
- New `test_import_with_docstrings_stripped` in `astropy/io/ascii/tests/test_connect.py` runs that import in a `-OO` subprocess. It fails before the fix and passes after it.
