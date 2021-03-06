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

    def persist_dao(self, dao):
        """Persists (updates) a modified Data Access Object (DAO) that we retrieved
        from the persistent storage backend earlier.
        """
        self.session.merge(dao)
        self.session.flush()

    def _persist_sms(self, dto):
        return self._persist_voice(dto)

    def _persist_voice(self, dto):
        now = quantum.lib.timezone.now()
        dao = self.models[dto.using](
            purpose=dto.purpose,
            sender=dto.sender,
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

    def exists(self, purpose, using, sender, recipient):
        """Return a boolean indicating if a challenge over the delivery
        mechanism `using` exists for the specified `recipient`.
        """
        Relation = self.models[using]
        query = sqlalchemy.exists()\
            .where(Relation.purpose == purpose)\
            .where(Relation.sender == sender)\
            .where(Relation.recipient == recipient)
        return self.session.query(query).scalar()

    def get(self, dto):
        """Return a Data Access Object (DAO) based on the delivery method,
        sender and recipient specified in `dto`.
        """
        assert dto.using in list(self.models.keys())
        Relation = self.models[dto.using]
        return self.session.query(Relation)\
            .filter(Relation.purpose == dto.purpose)\
            .filter(Relation.sender == dto.sender)\
            .filter(Relation.recipient == dto.recipient)\
            .first()

    def delete(self, purpose, using, sender, recipient):
        """Deletes the challenge identified by `using`, `sender` and
        `recipient` from the persistent storage backend.
        """
        Relation = self.models[using]
        self.session.query(Relation)\
            .filter(Relation.purpose == purpose)\
            .filter(Relation.using == using)\
            .filter(Relation.sender == sender)\
            .filter(Relation.recipient == recipient)\
            .delete()
        self.session.flush()
