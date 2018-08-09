"""Environment variables specified by the application Quantumfile."""
import os

import yaml


DEFAULT_SECRET_KEY = "b9d3fc670302b2191fd341814ee98a13ec2070657f816cf2f93d2dc282277657"

# Set up some variables serving as hints to the Quantum framework.
os.environ['SQ_ENVIRON_PREFIX'] = 'CHALLENGER'


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


# Provide some defaults to the environment prior to assigning the
# module-level constants.
os.environ.setdefault('CHALLENGER_SECRET_KEY',
    "b9d3fc670302b2191fd341814ee98a13ec2070657f816cf2f93d2dc282277657")
os.environ.setdefault('CHALLENGER_HTTP_ADDR',
    "0.0.0.0")
os.environ.setdefault('CHALLENGER_HTTP_PORT',
    "8443")


SECRET_KEY = os.getenv('CHALLENGER_SECRET_KEY')
HTTP_ADDR = os.getenv('CHALLENGER_HTTP_ADDR')
HTTP_PORT = os.getenv('CHALLENGER_HTTP_PORT')
DEPLOYMENT_ENV = os.getenv('QUANTUM_DEPLOYMENT_ENV') or 'production'
CONFIG_DIR = os.getenv('QUANTUM_CONFIG_DIR')
IOC_DIR = os.getenv('QUANTUM_IOC_DIR')
IOC_DEFAULTS = os.getenv('QUANTUM_IOC_DEFAULTS')
TEST_PHASE = os.getenv('SQ_TESTING_PHASE')
