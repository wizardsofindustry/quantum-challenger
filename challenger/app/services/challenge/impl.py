"""Declares :class:`ChallengeService`."""
import hmac
import secrets
import string

import challenger.environ
from .base import BaseChallengeService


class ChallengeService(BaseChallengeService):
    """Provides an interface to send text and voice challenges to
    phonenumbers and email addresses.
    """
    valid_mechanims = ('voice', 'sms')
    code_charset = string.digits

    def _generate_code(self):
        """Generates a random numeric string consisting of six characters."""
        return ''.join([secrets.choice(self.code_charset) for x in range(6)])

    def challenge(self, dto):
        """Issue a challenge to the specified recipient."""
        if dto.using not in self.valid_mechanims:
            self._on_invalid_delivery_mechanism(dto)
        return getattr(self, f'_challenge_{dto.using}')(dto)

    def _challenge_sms(self, dto):
        assert dto.using == 'sms'
        dto['code'] = self._generate_code()
        dto['message'] = dto.message.format(code=dto.code)\
            if dto.get('message') else str(dto.code)
        if self.repo.exists(dto.using, dto.sender, dto.recipient):
            self._on_duplicate_challenge(dto)
        self.repo.persist(dto)
        self.sms.send(sender=dto.sender, recipient=dto.recipient,
            message=dto.message)
        return self.dto(code=dto.code)\
            if challenger.environ.DEBUG else self.dto({})

    def retry(self, dto):
        """Retry a challenge for the specified recipient."""
        if dto.using not in self.valid_mechanims:
            self._on_invalid_delivery_mechanism(dto)
        return getattr(self, f'_retry_{dto.using}')(dto)

    def verify(self, dto):
        """Verifies the client-provided verification code against the
        code that was persistent for the sender and recipient.
        """
        dao = self.repo.get(dto)
        if dao is None:
            return self.dto(success=False, attempts=None)

        is_valid = hmac.compare_digest(dto.code, dao.code)
        if not is_valid:
            assert isinstance(dao.attempts, int)
            dao.attempts += 1
            self.repo.persist_dao(dao)
        else:
            self.repo.delete(dao.using, dao.sender, dao.recipient)

        return self.dto(success=is_valid, attempts=dao.attempts)

    def _retry_sms(self, dto):
        dao = self.repo.get(dto)
        if dao is None:
            self._on_recipient_not_challenged(dto)
        self.sms.send(sender=dao.sender, recipient=dao.recipient,
            message=dao.message)

    def _on_duplicate_challenge(self, dto): #pylint: disable=unused-argument
        raise self.AlreadyChallenged()

    def _on_recipient_not_challenged(self, dto):
        raise self.ChallengeDoesNotExist([dto.sender, dto.recipient],
            name='Challenge')

    def _on_invalid_delivery_mechanism(self, dto):
        raise self.InvalidDeliveryChannel(
            errors={'using': [f"Not valid delivery mechanism: {dto.using}"]})
