"""Declares :class:`TextMessageService`."""
from .base import BaseTextMessageService


class TextMessageService(BaseTextMessageService):
    """Exposes an interface to send Short Message Service (SMS)
    messages.
    """

    def send(self, sender, recipient, message):
        """Send a SMS message to the specified `recipient`."""
        pass
