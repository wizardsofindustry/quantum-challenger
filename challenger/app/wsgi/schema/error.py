"""The validation schema for ``#/components/schema/Error`` objects,
see ``./etc/openapi.yml``).
"""
import sq.schema


class Error(sq.schema.Schema):

    #: Specifies the exception condition that occurred.
    code = sq.schema.fields.String(
        required=True,
        allow_none=False
    )

    #: Error message targeted at the end-user.
    message = sq.schema.fields.String(
        required=True,
        allow_none=False
    )

    #: A message providing a more detailed explanation of the error
    #: condition that occurred.
    detail = sq.schema.fields.String(
        allow_none=False
    )

    #: A hint indicating on how to resolve the situation.
    hint = sq.schema.fields.String(
        allow_none=False
    )

    #: An identifier for this specific exception condition, which may be
    #: used for debugging purposes.
    id = sq.schema.fields.UUID(
        allow_none=False
    )


#pylint: skip-file
