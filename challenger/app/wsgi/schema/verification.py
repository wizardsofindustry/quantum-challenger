"""The validation schema for ``#/components/schema/Verification`` objects,
see ``./etc/openapi.yml``).
"""
import sq.schema


class Verification(sq.schema.Schema):
    """Describes a request to verify the confirmation code for a given
    sender and recipient.
    """

    #: Indicates the purpose of this specific challenge.
    purpose = sq.schema.fields.String(
        allow_none=False
    )

    #: Specifies the delivery mechanism for the challenge.
    using = sq.schema.fields.String(
        required=True,
        allow_none=False
    )

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

    #: The secret code that may be used to verify the phonenumber.
    code = sq.schema.fields.String(
        required=True,
        allow_none=False
    )


#pylint: skip-file
