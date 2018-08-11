"""The validation schema for ``#/components/schema/Version`` objects,
see ``./etc/openapi.yml``).
"""
import sq.schema


class Version(sq.schema.Schema):

    #: The application version that is currently running.
    version = sq.schema.fields.String(
        required=True,
        allow_none=False
    )


#pylint: skip-file
