"""Contains the concrete implementation of :class:`BaseChallengeCtrl`."""
from .base import BaseChallengeCtrl


class ChallengeCtrl(BaseChallengeCtrl):

    async def post(self, request, *args, **kwargs):
        raise NotImplementedError("Subclasses must override this method.")

    async def put(self, request, *args, **kwargs):
        raise NotImplementedError("Subclasses must override this method.")
