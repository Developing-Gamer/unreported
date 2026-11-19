from sphinx.builders.gettext import Catalog, MsgOrigin


def test_repeated_message_preserves_each_source_occurrence():
    catalog = Catalog()
    first = MsgOrigin('intro.rst', 10)
    second = MsgOrigin('guide/setup.rst', 32)

    catalog.add('Save your changes before continuing.', first)
    catalog.add('Save your changes before continuing.', second)

    messages = list(catalog)
    assert len(messages) == 1
    assert messages[0].text == 'Save your changes before continuing.'
    assert messages[0].locations == [
        ('intro.rst', 10),
        ('guide/setup.rst', 32),
    ]
    assert messages[0].uuids == [first.uid, second.uid]
