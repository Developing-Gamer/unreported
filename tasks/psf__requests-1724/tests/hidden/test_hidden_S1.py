import sys


def test_missing_pop_requires_an_explicit_default(monkeypatch):
    # Supply compatibility aliases for this Python 2-era backport on Python 3.
    if sys.version_info[0] >= 3:
        import _thread
        import collections
        import collections.abc

        monkeypatch.setitem(sys.modules, 'dummy_thread', _thread)
        for name in ('Mapping', 'MutableMapping', 'Callable'):
            if not hasattr(collections, name):
                monkeypatch.setattr(
                    collections, name, getattr(collections.abc, name),
                    raising=False,
                )

    from requests.packages.urllib3.packages.ordered_dict import OrderedDict

    pending = OrderedDict([('job-17', 'ready')])
    fallback = object()
    assert pending.pop('unknown-job', fallback) is fallback

    raised = False
    try:
        pending.pop('unknown-job')
    except KeyError as error:
        raised = True
        assert error.args == ('unknown-job',)

    assert raised, 'Removing a missing key without a default must raise KeyError'
    assert pending.items() == [('job-17', 'ready')]
    assert pending.pop('job-17') == 'ready'
    assert len(pending) == 0
