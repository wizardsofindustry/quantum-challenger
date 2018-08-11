"""The validation schema for ``#/components/schema/TextMessageChallenge`` objects,
see ``./etc/openapi.yml``).
"""
import sq.schema


class TextMessageChallenge(sq.schema.Schema):
    """Describes a request to challenge the phonenumber specified in the
    entity.
    """

    #: The sender of the challenge; this will be displayed in the user
    #: device if the delivery mechanism is SMS. If `sender` consists of
    #: alphanumeric characters, its maximum length is `11`. If it consists
    #: of only numeric characters, the maximum length is `18`.
    sender = sq.schema.fields.String(
        required=True,
        allow_none=False
    )

    #: The phonenumber to challenge, in ITU-T E.164 format.
    recipient = sq.schema.fields.Phonenumber(
        required=True,
        allow_none=False
    )

    #: The message to send to the phonenumber. For SMS challenges, this
    #: may not exceed 140 characters and MUST contain the text `{code}`,
    #: which will be replaced with a random string consisting of six
    #: numeric characters. If `message` is null and this object is used to
    #: issue a new challenge, then only the confirmation code will be
    #: sent.
    message = sq.schema.fields.String(
        required=True,
        allow_none=True
    )


#pylint: skip-file
