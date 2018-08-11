"""The validation schema for ``#/components/schema/Challenge`` objects,
see ``./etc/openapi.yml``).
"""
import sq.schema

from .textmessagechallenge import TextMessageChallenge


class Challenge(sq.schema.Schema):
    """Issue a challenge to the recipient specified in the entity, using
    the selected delivery mechanism.
    """

    #: Specifies the delivery mechanism for the challenge.
    using = sq.schema.fields.String(
        required=True,
        allow_none=False
    )

    #: Specifies the time-to-live after which the challenge expires, in
    #: milliseconds.
    ttl = sq.schema.fields.Integer(
        allow_none=False,
        missing=86400000
    )

    __oneof__ = [
        TextMessageChallenge
    ]


#pylint: skip-file
