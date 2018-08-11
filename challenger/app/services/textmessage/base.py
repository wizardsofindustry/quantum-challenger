import ioc
from sq.service import Service


class BaseTextMessageService(Service):
    http = ioc.class_property('RequestFactory')

    def send(self, sender, recipient, message):
        raise NotImplementedError("Subclasses must override this method.")


# pylint: skip-file
