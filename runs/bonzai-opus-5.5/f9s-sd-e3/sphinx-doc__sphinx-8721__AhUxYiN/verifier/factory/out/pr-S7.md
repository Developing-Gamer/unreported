Fix Dutch search stemmer skipping all-caps words (lowercase before stemming)

## Overview
Pages with all-caps Dutch headings (e.g. `WERKEN`) could not be found by searching for the words in them. The Dutch stemmer was given the original capitals, and the Snowball Dutch stemmer only recognises lowercase letters, so `WERKEN` was left unstemmed and indexed as `werken`. The browser lowercases the query before stemming (`werken` -> `werk`), so the keys never matched. Dutch now lowercases first, like every other language.

## Details
- `sphinx/search/nl.py`: `SearchDutch.stem` now calls `stemWord(word.lower())` instead of `stemWord(word).lower()`.
- `tests/test_search.py`: new tests that `SearchDutch.stem` gives the same result for `werken`, `Werken`, `WERKEN` (`werk`), and that an all-caps Dutch heading is indexed under the stemmed `werk` in the title mapping.

## Evidence
Before the fix `SearchDutch({}).stem('WERKEN')` returned `'werken'`; after, `'werk'`. Both new tests fail on the base commit and pass now.

## Verification
`python -m pytest tests/test_search.py` -> 13 passed.
