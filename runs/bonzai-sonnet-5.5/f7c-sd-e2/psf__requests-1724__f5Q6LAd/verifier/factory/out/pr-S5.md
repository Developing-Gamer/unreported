No pull request: already covered by #1000

The UnicodeDecodeError in ev_s5 (unicode HTTP method on Python 2 reaching httplib with a non-ASCII byte body) has the same root cause as open pull request #1000: `PreparedRequest.prepare_method` only called `.upper()`, leaving a unicode method unicode. #1000 converts it with `to_native_string(self.method.upper())`. `Session.request` builds a `Request` and then calls `prepare_request`, which goes through `prepare_method`, so the one change covers every path. The Session.request change proposed in the investigation is redundant.

No change made here; the fix should be reviewed and merged via #1000.
