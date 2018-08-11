"""Declares the :class:`ChallengeRepository`."""
import sqlalchemy
import quantum.lib.timezone

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
        """Convert Data Transfer Object (DTO) `dto` to a Data Access Object (DAO)
        and persist it to the persistent storage backend.
        """
        assert dto.using in list(self.models.keys())
        return getattr(self, f'_persist_{dto.using}')(dto)

    def _persist_sms(self, dto):
        return self._persist_voice(dto)

    def _persist_voice(self, dto):
        now = quantum.lib.timezone.now()
        dao = self.models[dto.using](
            recipient=dto.recipient,
            challenged=now,
            expires=now + dto.ttl,
            using=dto.using,
            code=dto.code,
            message=dto.message,
            attempts=0
        )
        self.session.add(dao)
        self.session.flush()

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
