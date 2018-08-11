from werkzeug.routing import Map

from .health import HealthEndpoint
from .version import VersionEndpoint
from .verify import VerifyEndpoint
from .challenge import ChallengeEndpoint


urlpatterns = Map([
    HealthEndpoint.as_rule(),
    VersionEndpoint.as_rule(),
    VerifyEndpoint.as_rule(),
    ChallengeEndpoint.as_rule(),
])


# !!! SG MANAGED FILE -- DO NOT EDIT -- VERSION:  !!!
