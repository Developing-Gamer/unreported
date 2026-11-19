from astropy.time import Time
from astropy.timeseries import TimeSeries


def test_added_column_cannot_precede_required_time_column():
    series = TimeSeries(
        time=Time([59000.0, 59000.001], format="mjd", scale="utc"),
        data={"flux": [12.5, 12.7]},
    )

    rejected = False
    try:
        series.add_column([0, 1], name="quality", index=0)
    except ValueError:
        rejected = True

    assert rejected, (
        "A column was silently accepted ahead of the required time column: "
        f"{series.colnames}"
    )
