import sq.interfaces.http

try:
    from .endpoints import urlpatterns
except ImportError:
    urlpatterns = None


class WSGIApplication(sq.interfaces.http.WSGIApplication):

    def __init__(self, logger=None, is_operational=None):
        super(WSGIApplication, self).__init__(urlpatterns=urlpatterns,
            logger=logger, is_operational=is_operational)


# pylint: skip-file
# !!! SG MANAGED FILE -- DO NOT EDIT !!!
