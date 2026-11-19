Restore EUC-TW frequency rank for 仍 so short Traditional Chinese notices are detected

## Overview
Some short EUC-TW encoded notices (e.g. `本仍有效`, `公司仍營`) were detected as ISO-8859-5 by the vendored charade, so `Response.apparent_encoding` / `Response.text` returned garbled characters. Most notices were fine because only short ones with exactly four "frequent" characters, one being 仍, were affected. Entry 82 of `EUCTWCharToFreqOrder` had been changed from 507 to 705 (a duplicate of another entry), so 仍 no longer counted as frequent (rank < 512), the frequent-character count fell to the minimum threshold and EUC-TW confidence became SURE_NO.

## Details
- `requests/packages/charade/euctwfreq.py`: line 55, 705 -> 507 (matches upstream charade 1.0.3 / requests 2.0.1).
- `test_requests.py`: new `TestCharadeEUCTW` with a regression test (iconv-encoded EUC-TW samples must detect as `EUC-TW`) and a check that the frequency table has no duplicated ranks.

## Verification
- Before the fix (Python 2.7 env): both new tests fail (`assert 'ISO-8859-5' == 'EUC-TW'`, `assert 6016 == 6015`).
- After: both pass; `pytest test_requests.py -k "Charade or Encoding"` 8 passed.
- Full `test_requests.py`: one failure from the network-dependent tests (SSL cert verify / HTTP 429 from external hosts), which also fails on the base commit.
