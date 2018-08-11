"""Start the main :mod:`challenger` application using the
specified command-line parameters.
"""
import argparse
import logging
import os
import sys

import yaml

import sq.runtime


DEPLOYMENT_ENV = os.getenv('QUANTUM_DEPLOYMENT_ENV') or 'production'

# This is a hook to load secrets or other environment variables
# from YAML-encoded file, for example when using Docker Swarm
# secrets.
if os.getenv('CHALLENGER_SECRETS'):
    with open(os.getenv('CHALLENGER_SECRETS')) as f:
        secrets = yaml.safe_load(f.read()) #pylint: disable=invalid-name
    for key, value in secrets.items():
        if not key.startswith('CHALLENGER'):
            continue
        os.environ[key] = str(value)

    del secrets


os.environ['SQ_ENVIRON_PREFIX'] = 'CHALLENGER'
DEFAULT_SECRET_KEY = "b9d3fc670302b2191fd341814ee98a13ec2070657f816cf2f93d2dc282277657"
os.environ.setdefault('CHALLENGER_SECRET_KEY', "b9d3fc670302b2191fd341814ee98a13ec2070657f816cf2f93d2dc282277657")
os.environ.setdefault('CHALLENGER_RDBMS_DSN', "postgresql+psycopg2://challenger:challenger@rdbms:5432/challenger")
os.environ.setdefault('CHALLENGER_HTTP_ADDR', "0.0.0.0")
os.environ.setdefault('CHALLENGER_HTTP_PORT', "8443")


class MainProcess(sq.runtime.MainProcess):
    """The main :mod:`challenger` process manager."""
    framerate = 10
    components = [
        sq.runtime.HttpServer,
    ]


parser = argparse.ArgumentParser() #pylint: disable=invalid-name
parser.add_argument('-c', dest='config',
    default='./etc/challenger.conf',
    help="specifies the runtime configuration file (default: %(default)s)")
parser.add_argument('--loglevel',
    help="specifies the logging verbosity (default: %(default)s)",
    choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], default='INFO')


if __name__ == '__main__':
    logger = logging.getLogger('challenger') #pylint: disable=invalid-name
    args = parser.parse_args() #pylint: disable=invalid-name
    p = MainProcess(args, logger=logger) #pylint: disable=invalid-name

    if DEFAULT_SECRET_KEY == os.getenv('CHALLENGER_SECRET_KEY'):
        logger.critical("The application is started using the default secret key")
        if DEPLOYMENT_ENV == 'production':
            logger.critical("DEFAULT_SECRET_KEY may not be used in production")
            sys.exit(128)


    try:
        sys.exit(p.start() or 0)
    except Exception: #pylint: disable=broad-except
        logger.exception("Fatal exception caused program termination")
        sys.exit(1)


# !!! SG MANAGED FILE -- DO NOT EDIT !!!
