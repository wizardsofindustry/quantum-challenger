""""Declares a Python object mapping to the ``phonenumberchallenges`` relation."""
import sqlalchemy

from .base import Relation


class PhonenumberChallenge(Relation):
    """Maintains information about verification challenges sent to a
    (mobile) phonenumber.
    """

    __tablename__ = 'phonenumberchallenges'

    #: Specifies the phonenumber to which the challenge was sent.
    phonenumber = sqlalchemy.Column(
        sqlalchemy.String,
        name='phonenumber',
        primary_key=True,
        nullable=False
    )

    #: The date/time at which the challenge was sent, in milliseconds
    #: since the UNIX epoch.
    challenged = sqlalchemy.Column(
        sqlalchemy.BigInteger,
        name='challenged',
        nullable=False
    )

    #: The delivery mechanism of the challenge confirmation code.
    using = sqlalchemy.Column(
        sqlalchemy.String,
        name='using',
        nullable=False
    )

    #: A shared secret that may be used to verify access to the specified
    #: phonenumber.
    code = sqlalchemy.Column(
        sqlalchemy.String,
        name='code',
        nullable=False
    )

    #: The number of attempts to verify the phonenumber.
    attempts = sqlalchemy.Column(
        sqlalchemy.Integer,
        name='attempts',
        nullable=False
    )


# pylint: skip-file
