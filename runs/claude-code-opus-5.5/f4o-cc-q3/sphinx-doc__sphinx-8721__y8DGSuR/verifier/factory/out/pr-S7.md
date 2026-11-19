search (nl): lowercase words before Dutch stemming so all-caps headings are found

## Root cause
`SearchDutch.stem` in `sphinx/search/nl.py` ran `self.stemmer.stemWord(word).lower()`, so it stemmed first and lowercased afterwards. Every other language does it the other way round (`stemWord(word.lower())`). The Snowball Dutch stemmer only treats lowercase letters as vowels, so uppercase input is returned unchanged. For example, `HANDLEIDINGEN` was indexed as `handleidingen`, but the JS search lowercases the query before stemming and looks up `handleid`. Pages whose words appear only in all-caps (such as headings) were therefore not found.

## Change
Lowercase before stemming: `return self.stemmer.stemWord(word.lower())`. This matches the other languages and the JS side (`stemmer.stemWord(tmp[i].toLowerCase())`).

## Verification
- New test `tests/test_search.py::test_dutch_stemmer_is_case_insensitive` checks that `HANDLEIDINGEN`, `Handleidingen` and `handleidingen` all stem to `handleid`. It fails before the change and passes after.
- `pytest tests/test_search.py`: the only failures are `test_meta_keys_are_handled_for_language_en/de`, which also fail on the unmodified checkout.
