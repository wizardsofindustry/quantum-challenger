"""Declares the :class:`ChallengeRepository`."""
import sqlalchemy

from ...orm import PhonenumberChallenge
from .base import BaseChallengeRepository


class ChallengeRepository(BaseChallengeRepository):
    """Provides an interface to manipulate the persisted state of the
    :mod:`challenger` application.
    """
    models = {
        'sms': PhonenumberChallenge,
        'voice': PhonenumberChallenge
    }

    def persist(self, dto):
        raise NotImplementedError("Subclasses must override this method.")

    def exists(self, using, recipient):
        """Return a boolean indicating if a challenge over the delivery
        mechanism `using` exists for the specified `recipient`.
        """
        Relation = self.models[using]
        query = sqlalchemy.exists()\
            .where(Relation.recipient == recipient)
        return self.session.query(query).scalar()

    def delete(self, using, recipient):
        raise NotImplementedError("Subclasses must override this method.")
