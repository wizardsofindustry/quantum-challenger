from .base import BaseTextMessageService


class TextMessageService(BaseTextMessageService):

    def send(self, sender, recipient, message):
        raise NotImplementedError("Subclasses must override this method.")
