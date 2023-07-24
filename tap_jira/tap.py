"""tap-jira tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_jira import streams


class TapJira(Tap):
    """tap-jira tap class."""

    name = "tap-jira"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest record date to sync",
        ),
        th.Property(
            "end_date",
            th.DateTimeType,
            description="Latest record date to sync",
        ),
        th.Property(
            "auth",
            th.DiscriminatedUnion(
                "flow",
                oauth=th.ObjectType(
                    th.Property("access_token", th.StringType, required=True, secret=True),
                    additional_properties=False,
                ),
                password=th.ObjectType(
                    th.Property("username", th.StringType, required=True),
                    th.Property("password", th.StringType, required=True, secret=True),
                    additional_properties=False,
                ),
            ),
            required=True,
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.JiraStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.UsersStream(self),
        ]


if __name__ == "__main__":
    TapJira.cli()
