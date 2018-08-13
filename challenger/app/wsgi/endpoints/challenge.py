import ioc
import sq.interfaces.http

from ..schema import Challenge
from ..schema import Challenge


class ChallengeEndpoint(sq.interfaces.http.Endpoint):
    """Deserializes, serializes and validates the structure of the input and output
    (requests and response) to its configured URL endpoint, which exposes the
    following functionality:

        Set a challenge code using the channel specified in the request URI.

    A :class:`ChallengeEndpoint` validates the structure of the request headers,
    URL parameters, query parameters and entity prior to forwarding the
    request to its handler (controller).

    The handler function (e.g., :meth:`~ChallengeCtrl.get()`) may,
    instead of a :class:`~sq.interfaces.http.Response` object, return a tuple
    or a dictionary. The :class:`ChallengeEndpoint` instance will interpret
    these return values as follows:

    -   If the return value is a :class:`dict`, then the endpoint assumes that
        the response code is ``200`` and the object should be included as the
        response body, serialized using the default content type. It is
        considered an error condition if no serializer is specified for
        this content type.
    -   If the return value is a :class:`tuple` with a length of 2, and the
        first element is an :class:`int`, it is considered to hold
        ``(status_code, body)``.
    -   Otherwise, for more granular control over the response, a
        :class:`~sq.interfaces.http.Response` object may be returned.

    If the response body is not a string, it will be serialized using the
    best-matching content type in the client ``Accept`` header. If no
    match is found, the client receives a ``406`` response.

    During serialization, A schema may be selected by :class:`ChallengeEndpoint`
    based on the response status code and content type, if one was defined in
    the OpenAPI definition for this API endpoint.
    """
    pattern = "/challenge"
    ctrl = ioc.class_property("ChallengeCtrl")

    #: The mapping below specifies the schema of structured data in the
    #: request body per content type.
    payload = {
        "post": {
            "application/json": Challenge
        },
        "put": {
            "application/json": Challenge
        }
    }


# pylint: skip-file
# !!! SG MANAGED FILE -- DO NOT EDIT -- VERSION:  !!!
