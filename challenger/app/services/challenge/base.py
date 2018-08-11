import ioc
from sq.exceptions import DuplicateEntity
from sq.exceptions import ObjectDoesNotExist
from sq.service import Service
from sq.exceptions import UnprocessableEntity


class BaseChallengeService(Service):
    repo = ioc.class_property('ChallengeRepository')
    sms = ioc.class_property('TextMessageService')

    AlreadyChallenged = type('AlreadyChallenged', (DuplicateEntity,), {})
    ChallengeDoesNotExist = type('ChallengeDoesNotExist', (ObjectDoesNotExist,), {})
    InvalidDeliveryChannel = type('InvalidDeliveryChannel', (UnprocessableEntity,), {})

    def challenge(self, dto):
        raise NotImplementedError("Subclasses must override this method.")

    def retry(self, dto):
        raise NotImplementedError("Subclasses must override this method.")


# pylint: skip-file
