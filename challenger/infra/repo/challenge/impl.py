from .base import BaseChallengeRepository


class ChallengeRepository(BaseChallengeRepository):

    def persist(self, dto):
        raise NotImplementedError("Subclasses must override this method.")

    def exists(self, using, recipient):
        raise NotImplementedError("Subclasses must override this method.")

    def delete(self, using, recipient):
        raise NotImplementedError("Subclasses must override this method.")
