"""Contains the concrete implementation of :class:`BaseChallengeCtrl`."""
from .base import BaseChallengeCtrl


class ChallengeCtrl(BaseChallengeCtrl):
    """Exposes handler functions for ``POST`` and ``PUT`` requests
    to the ``/challenge`` endpoint.
    """

    async def post(self, request, *args, **kwargs):
        """Create a new challenge to the recipient specified in the
        request entity.
        """
        self.service.challenge(request.payload)
        return self.render_to_response(ctx={}, status_code=202)

    async def put(self, request, *args, **kwargs):
        """Re-issue a challenge to the recipient specified in the
        request entity.
        """
        self.service.retry(request.payload)
        return self.render_to_response(ctx={}, status_code=202)
