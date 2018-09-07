import json
import unittest
from unittest.mock import MagicMock

import ioc
import sq.exceptions
import sq.test
import quantum.exceptions

from .... import environ
from ....infra import orm
from ..endpoints import ChallengeEndpoint


class CreatePhonenumberChallengeTestCase(sq.test.SystemTestCase):
    metadata = orm.Relation.metadata

    def setUp(self):
        super(CreatePhonenumberChallengeTestCase, self).setUp()
        self.endpoint = ChallengeEndpoint()
        self.service = ioc.require('ChallengeService')
        self.repo = ioc.require('ChallengeRepository')

        ioc.require('RequestFactory').post = MagicMock()
        response = self.request(
            self.endpoint.handle,
            method='POST',
            accept="application/json",
            json={
                'purpose': 'SUBJECT_REGISTRATION',
                'using': 'sms',
                'sender': 'Challenger',
                'recipient': "+31612345678",
                'message': "Your activation code is {code}"
            }
        )
        assert response.status_code == 202

    @sq.test.integration
    def test_create_challenge_phonenumber_sms(self):
        dto=self.dto(
            purpose='SUBJECT_REGISTRATION',
            using='sms',
            sender='Challenger',
            recipient="+31687654321",
            message="Your activation code is {code}"
        )
        response = self.request(
            self.endpoint.handle,
            method='POST',
            accept="application/json",
            json=dto
        )
        self.assertEqual(response.status_code, 202)
        self.assertTrue(self.repo.exists('SUBJECT_REGISTRATION',
            'sms', 'Challenger', '+31687654321'))

        # Ensure that DEBUG=1
        response = json.loads(response.response[0])
        result = self.service.verify(dto | response)

    @unittest.skipIf(not environ.DEBUG, "Run in debug mode only")
    @sq.test.integration
    def test_create_challenge_phonenumber_sms_returns_code_in_debug(self):
        dto=self.dto(
            purpose='SUBJECT_REGISTRATION',
            using='sms',
            sender='Challenger',
            recipient="+31687654321",
            message="Your activation code is {code}"
        )
        response = self.request(
            self.endpoint.handle,
            method='POST',
            accept="application/json",
            json=dto
        )
        self.assertEqual(response.status_code, 202)
        self.assertTrue(self.repo.exists('SUBJECT_REGISTRATION',
            'sms', 'Challenger', '+31687654321'))

        # Ensure that DEBUG=1
        result = json.loads(response.response[0])
        self.assertEqual(response.status_code, 202)
        self.assertIn('code', result)

    @sq.test.integration
    def test_challenge_fails_with_invalid_mechanism_sms(self):
        with self.assertRaises(self.service.InvalidDeliveryChannel):
            response = self.request(
                self.endpoint.handle,
                method='PUT',
                accept="application/json",
                json={
                    'purpose': 'SUBJECT_REGISTRATION',
                    'using': 'invalid',
                    'sender': 'Challenger',
                    'recipient': "+31612345678",
                    'message': "Your activation code is {code}"
                }
            )

    @sq.test.integration
    def test_challenge_numeric_sender_must_be_max_18_characters(self):
        with self.assertRaises(quantum.exceptions.UnprocessableEntity):
            response = self.request(
                self.endpoint.handle,
                method='PUT',
                accept="application/json",
                json={
                    'purpose': 'SUBJECT_REGISTRATION',
                    'using': 'sms',
                    'sender': '1234567890123456789',
                    'recipient': "+31612345678",
                    'message': "Your activation code is {code}"
                }
            )

    @sq.test.integration
    def test_challenge_alphanumeric_sender_must_be_max_11_characters(self):
        with self.assertRaises(quantum.exceptions.UnprocessableEntity):
            response = self.request(
                self.endpoint.handle,
                method='PUT',
                accept="application/json",
                json={
                    'purpose': 'SUBJECT_REGISTRATION',
                    'using': 'sms',
                    'sender': '1234567890ab',
                    'recipient': "+31612345678",
                    'message': "Your activation code is {code}"
                }
            )

    @sq.test.integration
    def test_retry_fails_with_invalid_mechanism_sms(self):
        with self.assertRaises(self.service.InvalidDeliveryChannel):
            response = self.request(
                self.endpoint.handle,
                method='POST',
                accept="application/json",
                json={
                    'purpose': 'SUBJECT_REGISTRATION',
                    'using': 'invalid',
                    'sender': 'Challenger',
                    'recipient': "+31612345678",
                    'message': "Your activation code is {code}"
                }
            )

    @sq.test.integration
    def test_retry_fails_with_non_existing_challenge_sms(self):
        with self.assertRaises(self.service.ChallengeDoesNotExist):
            response = self.request(
                self.endpoint.handle,
                method='PUT',
                accept="application/json",
                json={
                    'purpose': 'SUBJECT_REGISTRATION',
                    'using': 'sms',
                    'sender': 'Challenger',
                    'recipient': "+31687654321",
                    'message': "Your activation code is {code}"
                }
            )
            self.fail(response.response[0])

    @sq.test.integration
    def test_retry_challenge_phonenumber_sms(self):
        dto=self.dto(
            purpose='SUBJECT_REGISTRATION',
            using='sms',
            sender='Challenger',
            recipient="+31612345678",
            message="Your activation code is {code}"
        )
        response = self.request(
            self.endpoint.handle,
            method='PUT',
            accept="application/json",
            json=dto
        )
        self.assertEqual(response.status_code, 202)

    @unittest.skipIf(not environ.DEBUG, "Run in debug mode only")
    @sq.test.integration
    def test_retry_challenge_phonenumber_sms_contains_code_in_debug(self):
        dto=self.dto(
            purpose='SUBJECT_REGISTRATION',
            using='sms',
            sender='Challenger',
            recipient="+31612345678",
            message="Your activation code is {code}"
        )
        response = self.request(
            self.endpoint.handle,
            method='PUT',
            accept="application/json",
            json=dto
        )
        self.assertEqual(response.status_code, 202)
        result = json.loads(response.response[0])
        self.assertIn('code', result)

    @sq.test.integration
    def test_phonenumber_must_be_valid_itu_e164_sms(self):
        with self.assertRaises(quantum.exceptions.UnprocessableEntity):
            response = self.request(
                self.endpoint.handle,
                method='POST',
                accept="application/json",
                json={
                    'purpose': 'SUBJECT_REGISTRATION',
                    'using': 'sms',
                    'sender': 'Challenger',
                    'recipient': "0612345678",
                    'message': "Your activation code is {code}"
                }
            )

    @sq.test.integration
    def test_message_must_contain_token_sms(self):
        with self.assertRaises(quantum.exceptions.UnprocessableEntity):
            response = self.request(
                self.endpoint.handle,
                method='POST',
                accept="application/json",
                json={
                    'purpose': 'SUBJECT_REGISTRATION',
                    'using': 'sms',
                    'sender': 'Challenger',
                    'recipient': "+31687654321",
                    'message': "Your activation code is"
                }
            )

    @sq.test.integration
    def test_message_may_not_exceed_140_sms(self):
        with self.assertRaises(quantum.exceptions.UnprocessableEntity):
            response = self.request(
                self.endpoint.handle,
                method='POST',
                accept="application/json",
                json={
                    'purpose': 'SUBJECT_REGISTRATION',
                    'using': 'sms',
                    'sender': 'Challenger',
                    'recipient': "+31687654321",
                    'message': "{code}" + (135*'a')
                }
            )

    @sq.test.integration
    def test_cannot_create_duplicate_challenge_sms(self):
        with self.assertRaises(self.service.AlreadyChallenged):
            response = self.request(
                self.endpoint.handle,
                method='POST',
                accept="application/json",
                json={
                    'purpose': 'SUBJECT_REGISTRATION',
                    'using': 'sms',
                    'sender': 'Challenger',
                    'recipient': "+31612345678",
                    'message': "Your activation code is {code}"
                }
            )


#pylint: skip-file
