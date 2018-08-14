"""Declares :class:`TextMessageService`."""
import challenger.environ
from .base import BaseTextMessageService


class TextMessageService(BaseTextMessageService):
    """Exposes an interface to send Short Message Service (SMS)
    messages.
    """
    base_url = "https://rest.messagebird.com"

    def send(self, sender, recipient, message):
        """Send a SMS message to the specified `recipient`."""
        headers = {'Accept': "application/json",
            'Authorization': f'AccessKey {challenger.environ.MESSAGEBIRD_ACCESS_KEY}'}
        response = self.http.post(f'{self.base_url}/messages',
            json={
                'originator': sender,
                'recipients': [recipient] if isinstance(recipient, str)\
                    else recipient,
                'body': message
            },
            headers=headers)
        response.raise_for_status()
