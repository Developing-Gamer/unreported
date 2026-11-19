from types import SimpleNamespace

from django.db.backends.oracle.creation import DatabaseCreation


def test_distinct_test_users_have_distinct_database_signatures():
    def make_creation(alias, test_user):
        return DatabaseCreation(
            SimpleNamespace(
                alias=alias,
                settings_dict={
                    "ENGINE": "django.db.backends.oracle",
                    "HOST": "localhost",
                    "PORT": "1521",
                    "NAME": "ORCL",
                    "USER": "app_admin",
                    "PASSWORD": "unused",
                    "TEST": {"USER": test_user},
                },
            )
        )

    primary = make_creation("default", "test_primary")
    reporting = make_creation("reporting", "test_reporting")

    assert primary.test_db_signature() != reporting.test_db_signature(), (
        "Explicitly different Oracle test users must identify separate test databases."
    )
