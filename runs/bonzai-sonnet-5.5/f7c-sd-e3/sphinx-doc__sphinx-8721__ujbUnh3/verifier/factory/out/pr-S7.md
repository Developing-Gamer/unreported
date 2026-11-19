Fix Dutch search stemming of uppercase words

## Overview
Pages with all-caps Dutch headings (e.g. `VERWERKING`) could not be found by searching for the words in them. `SearchDutch.stem` stemmed the word first and lowercased afterwards, unlike every other language. Snowball's Dutch suffix rules only match lowercase, so uppercase words were indexed unstemmed (`verwerking`) while the lowercased query was stemmed (`verwerk`), and the two never matched.

## Details
- `sphinx/search/nl.py`: `stem()` now returns `stemWord(word.lower())`, consistent with the other languages. The index builder passes words with their original case, so the language class must lowercase first.
- `tests/test_search.py`: new `test_dutch_stemmer_is_case_insensitive`. It fails before the change (`VERWERKING` and `verwerking` stem differently) and passes after.
- `CHANGES`: entry under Bugs fixed.
- Existing Dutch projects must be rebuilt for the search index to pick up the corrected terms.

## Verification
- `python -m pytest tests/test_search.py -k dutch -q`: fails before, passes after.
- Rest of `tests/test_search.py`: `test_meta_keys_are_handled_for_language_en/de` fail identically on the base commit, and `test_term_in_heading_and_section` fails the same way when run alone (it needs a prior build); none relate to this change.
