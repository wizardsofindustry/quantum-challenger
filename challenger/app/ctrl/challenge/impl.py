"""Contains the concrete implementation of :class:`BaseChallengeCtrl`."""
import collections

from .base import BaseChallengeCtrl


class ChallengeCtrl(BaseChallengeCtrl):
    """Exposes handler functions for ``POST`` and ``PUT`` requests
    to the ``/challenge`` endpoint.
    """

    def validate_payload(self, request, payload):
        """Validates the payload enclosed with the request."""
        errors = collections.defaultdict(list)
        if '{code}' not in payload.message:
            errors['message'].append(
                "The message must contain the '{code}' replacement token.")
        if len(payload.message) > 140 and payload.using == 'sms':
            errors['message'].append("Message must not exceed 140 characters.")

        if errors:
            self.unprocessable(errors=dict(errors))

    async def post(self, request, *args, **kwargs):
        """Create a new challenge to the recipient specified in the
        request entity.
        """
        return 202, self.service.challenge(request.payload)

    async def put(self, request, *args, **kwargs):
        """Re-issue a challenge to the recipient specified in the
        request entity.
        """
        self.service.retry(request.payload)
        return self.render_to_response(ctx={}, status_code=202)
