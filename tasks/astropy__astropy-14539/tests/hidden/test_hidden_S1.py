import pytest

from astropy.coordinates.name_resolve import sesame_database


@pytest.mark.parametrize("invalid_database", ["simbda", "SIMBAD", ""])
def test_invalid_database_selection_is_rejected(invalid_database):
    with sesame_database.set("ned"):
        error = None
        try:
            with sesame_database.set(invalid_database):
                pass
        except ValueError as exc:
            error = exc

        assert error is not None, "An invalid database selection was silently accepted"
        assert str(error) == f"Unknown database '{invalid_database}'"
        assert sesame_database.get() == "ned"
