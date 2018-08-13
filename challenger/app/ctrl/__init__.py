"""Contains all controller implementations that are used by the WSGI
appication. See also :class:`~challenger.app.wsgi.application.WSGIApplication`.
"""
from .verify import VerifyCtrl
from .challenge import ChallengeCtrl
