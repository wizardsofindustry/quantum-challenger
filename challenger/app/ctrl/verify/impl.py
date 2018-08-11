"""Contains the concrete implementation of :class:`BaseVerifyCtrl`."""
from .base import BaseVerifyCtrl


class VerifyCtrl(BaseVerifyCtrl):
    """Provides request handlers for the ``POST`` method."""

    async def post(self, request, *args, **kwargs):
        """Verifies the code provided in the request entity for the specified
        sender and recipient.
        """
        return self.render_to_response(
            ctx=self.service.verify(request.payload),
            status_code=200)
