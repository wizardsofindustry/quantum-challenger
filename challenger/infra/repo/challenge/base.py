import ioc
from sq.persistence import Repository


class BaseChallengeRepository(Repository):
    session = ioc.class_property('DatabaseSessionFactory')

    def persist(self, dto):
        raise NotImplementedError("Subclasses must override this method.")

    def exists(self, using, sender, recipient):
        raise NotImplementedError("Subclasses must override this method.")

    def delete(self, using, sender, recipient):
        raise NotImplementedError("Subclasses must override this method.")

    def get(self, dto):
        raise NotImplementedError("Subclasses must override this method.")

    def persist_dao(self, dao):
        raise NotImplementedError("Subclasses must override this method.")


# pylint: skip-file
