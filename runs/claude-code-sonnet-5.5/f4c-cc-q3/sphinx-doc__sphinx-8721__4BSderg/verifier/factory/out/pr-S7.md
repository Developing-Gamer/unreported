search: lowercase Dutch words before stemming

Root cause: `SearchDutch.stem` in `sphinx/search/nl.py` called `stemmer.stemWord(word).lower()`. The snowball stemmer is case-sensitive, so all-caps words such as `HOOFDSTUKKEN` were not stemmed the way lowercase words are. The index terms for all-caps headings then did not match search queries, which are lowercased and stemmed. Every other language module lowercases first.

Change: `stemWord(word.lower())`. Added a CHANGES entry.

Verification: added `test_dutch_stemmer_lowercases_before_stemming` in tests/test_search.py (fails before, passes after). `test_meta_keys_are_handled_for_language_en` and `_de` already fail in this checkout without my change.
