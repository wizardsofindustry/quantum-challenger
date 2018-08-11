"""Contains the concrete implementation of :class:`BaseVerifyCtrl`."""
from .base import BaseVerifyCtrl


class VerifyCtrl(BaseVerifyCtrl):

    async def post(self, request, *args, **kwargs):
        raise NotImplementedError("Subclasses must override this method.")
