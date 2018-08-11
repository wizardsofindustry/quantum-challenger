"""The validation schema for ``#/components/schema/Health`` objects,
see ``./etc/openapi.yml``).
"""
import sq.schema


class Health(sq.schema.Schema):

    #: Indicates the date and time at which the application instance was
    #: started, in milliseconds since the UNIX epoch.
    started = sq.schema.fields.Integer(
        required=True,
        allow_none=False
    )

    #: Current application instance lifetime, in milliseconds.
    uptime = sq.schema.fields.Integer(
        required=True,
        allow_none=False
    )


#pylint: skip-file
