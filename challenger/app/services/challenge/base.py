import ioc
from sq.exceptions import DuplicateEntity
from sq.exceptions import ObjectDoesNotExist
from sq.service import Service


class BaseChallengeService(Service):
    repo = ioc.class_property('ChallengeRepository')

    AlreadyChallenged = type('AlreadyChallenged', (DuplicateEntity,), {})
    ChallengeDoesNotExist = type('ChallengeDoesNotExist', (ObjectDoesNotExist,), {})

    def challenge(self, dto):
        raise NotImplementedError("Subclasses must override this method.")

    def retry(self, dto):
        raise NotImplementedError("Subclasses must override this method.")


# pylint: skip-file
