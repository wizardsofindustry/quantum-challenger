import ioc
from sq.persistence import Repository


class BaseChallengeRepository(Repository):
    session = ioc.class_property('DatabaseSessionFactory')

    def persist(self, dto):
        raise NotImplementedError("Subclasses must override this method.")

    def exists(self, using, recipient):
        raise NotImplementedError("Subclasses must override this method.")

    def delete(self, using, recipient):
        raise NotImplementedError("Subclasses must override this method.")


# pylint: skip-file
