Fix CountVectorizer.inverse_transform raising NotFittedError when a vocabulary was passed

## Overview
A `CountVectorizer`/`TfidfVectorizer` built with `vocabulary=...` does not need fitting: `transform` and `get_feature_names` build `vocabulary_` from the parameter on demand. `inverse_transform` skipped that step and called `_check_vocabulary()` directly, so it raised `NotFittedError` on the same unfitted estimator. The on-demand validation now lives in `_check_vocabulary`, so every method behaves the same.

## Details
- `_check_vocabulary` calls `_validate_vocabulary()` when `vocabulary_` is missing, then raises `NotFittedError` only if no vocabulary was given.
- Removed the duplicated `hasattr`/`_validate_vocabulary` blocks from `transform` and `get_feature_names`.
- Tests: unfitted vectorizers with a constructor vocabulary support `get_feature_names` and `inverse_transform`; without a vocabulary, `get_feature_names`, `inverse_transform` and `transform` still raise `NotFittedError`.

## Verification
- Before the fix: `pytest sklearn/feature_extraction/tests/test_text.py -k unfitted` gives 2 failed (`NotFittedError: ... Vocabulary wasn't fitted.` from `inverse_transform`), 2 passed.
- After the fix: `pytest sklearn/feature_extraction -q` gives 138 passed, 1 xfailed.
