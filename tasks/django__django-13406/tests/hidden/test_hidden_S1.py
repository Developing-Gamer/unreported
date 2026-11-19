import datetime

import pytest

from django.utils.dateformat import format as date_format


@pytest.mark.parametrize(
    'value, expected',
    [
        (datetime.date(2018, 12, 31), '2019-1'),
        (datetime.date(2019, 12, 30), '2020-1'),
        (datetime.date(2021, 1, 1), '2020-53'),
        (datetime.date(2021, 1, 3), '2020-53'),
        (datetime.date(2021, 1, 4), '2021-1'),
        (datetime.date(2021, 6, 16), '2021-24'),
    ],
)
def test_iso_week_year_stays_aligned_with_week_number(value, expected):
    assert date_format(value, 'o-W') == expected
