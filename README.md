# Challenger Verification Service (CVS)

The **Challenger Verification Service (CVS)** provides an API to send challenges
to phonenumbers and email addresses, in order to prove that a **Subject** has access
to it.

## Table of Contents

- [Features](#features)
- [Security considerations](#security-considerations)
- [Installation](#installation)
- [Developing](#developing)

## Features
- Send verification codes to email addresses and phonenumbers.
- Verify that a **Subject** has access to the mailbox or phonenumber by comparing
  a shared secret.

## Security considerations
- This service is deployed in the `citadel` environment. Clients are assumed
  to be *internal* and authorized at the network level.


## Installation & Environment

### Environment variables

The **Challenger Verification Service (CVS)** runtime is configured through environment
variables. The table below provides an overview of the possible values:

| Type  |               Name                |                              Default                              |
|-------|-----------------------------------|-------------------------------------------------------------------|
|literal|`CHALLENGER_RUNTIME`               |`service`                                                          |
|switch |`CHALLENGER_DEBUG`                 |`1`                                                                |
|literal|`CHALLENGER_HTTP_ADDR`             |`0.0.0.0`                                                          |
|literal|`CHALLENGER_HTTP_PORT`             |`8443`                                                             |
|literal|`CHALLENGER_IOC_DEFAULTS`          |`/etc/challenger/ioc.conf`                                         |
|literal|`CHALLENGER_IOC_DIR`               |`/etc/challenger/ioc.conf.d/`                                      |
|literal|`CHALLENGER_MESSAGEBIRD_ACCESS_KEY`|N/A                                                                |
|literal|`CHALLENGER_RDBMS_DSN`             |`postgresql+psycopg2://challenger:challenger@rdbms:5432/challenger`|
|literal|`CHALLENGER_SECRET_KEY`            |`b9d3fc670302b2191fd341814ee98a13ec2070657f816cf2f93d2dc282277657` |



For more information on these variables, refer to the `environ` section of
the projects' `Quantumfile`.

The configured environment is loaded in the `challenger.environ` module.
Environment variables of type `switch` are normalized into `bool` objects; all other
variables are assumed `literal` and parsed as-is.

### Docker
The **Challenger Verification Service (CVS)** is a containerized application. The Docker image may be pulled
by issueing the following command in your terminal:

`docker pull wizardsofindustry/quantum-challenger`

Alternatively, you may follow the steps described in the next section.
### Python
The **Challenger Verification Service (CVS)** application can be installed as a Python package by
running the following command in your terminal:

`pip3 install -r requirements.txt && python3 setup.py install`
