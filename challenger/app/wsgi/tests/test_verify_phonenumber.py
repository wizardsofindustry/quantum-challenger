import json
import unittest
from unittest.mock import MagicMock

import ioc
import sq.exceptions
import sq.test
import quantum.exceptions

from ....infra import orm
from ..endpoints import VerifyEndpoint


class VerifyPhonenumberChallengeTestCase(sq.test.SystemTestCase):
    metadata = orm.Relation.metadata

    def setUp(self):
        super(VerifyPhonenumberChallengeTestCase, self).setUp()
        self.endpoint = VerifyEndpoint()
        self.service = ioc.require('ChallengeService')
        ioc.require('RequestFactory').post = MagicMock()
        dto = self.service.challenge(self.dto({
                'purpose': 'SUBJECT_REGISTRATION',
                'using': 'sms',
                'sender': 'Challenger',
                'recipient': "+31612345678",
                'message': "Your activation code is {code}",
                'ttl': 86400000
            }))
        self.code = dto.code

    @sq.test.integration
    def test_verify_challenge_sent_by_sms(self):
        assert self.code
        response = self.request(
            self.endpoint.handle,
            method='POST',
            accept="application/json",
            json={
                'purpose': 'SUBJECT_REGISTRATION',
                'using': 'sms',
                'sender': 'Challenger',
                'recipient': "+31612345678",
                'code': self.code
            }
        )
        self.assertEqual(response.status_code, 200)

    @sq.test.integration
    def test_verify_fails_with_wrong_code_sms(self):
        response = self.request(
            self.endpoint.handle,
            method='POST',
            accept="application/json",
            json={
                'purpose': 'SUBJECT_REGISTRATION',
                'using': 'sms',
                'sender': 'Challenger',
                'recipient': "+31612345678",
                'code': '123456'
            }
        )
        self.assertEqual(response.status_code, 200)

    @sq.test.integration
    def test_verify_fails_with_non_existing_challenge_code_sms(self):
        response = self.request(
            self.endpoint.handle,
            method='POST',
            accept="application/json",
            json={
                'purpose': 'SUBJECT_REGISTRATION',
                'using': 'sms',
                'sender': 'Challenger',
                'recipient': "+31687654321",
                'code': '123456'
            }
        )
        self.assertEqual(response.status_code, 200)


#pylint: skip-file
