html: keep URL html_logo / html_favicon intact (fix pages falling back to old branding)

## Overview
When `html_logo` or `html_favicon` is a URL, pages loaded `_static/<basename>` instead, i.e. whatever local `logo.png`/`favicon.ico` the project still ships in `html_static_path` (typically the old branding). Clean rebuilds could not help since the stale file is re-copied each time. The URL is now used as given.

## Details
- `HTMLBuilder.prepare_writing` reduced both settings to `path.basename()` unconditionally, so `setup_resource_paths` could no longer see a URL and prefixed `_static/`. Only non-URL values are now reduced to the basename.
- The pyramid theme used `pathto(logo, 1)`, which points outside `_static`; it now uses `logo_url` like the other themes.
- Tests: new `test-html_logo` root and three tests (URL logo/favicon, local logo, pyramid local logo). Two fail on the base commit.

## Verification
`pytest tests/test_build_html.py tests/test_theming.py` – 534 passed.
