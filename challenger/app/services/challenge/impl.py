from .base import BaseChallengeService


class ChallengeService(BaseChallengeService):

    def challenge(self, dto):
        raise NotImplementedError("Subclasses must override this method.")

    def retry(self, dto):
        raise NotImplementedError("Subclasses must override this method.")
