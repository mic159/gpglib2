# coding: spec

from tests.helpers import data

from gpglib.structures import Key

from unittest import TestCase
import nose

describe TestCase, "Consuming rsa keys":
    it "successfully consumes a secret key":
        secret_key = Key(passphrase='blahandstuff').parse(data.get_pgp_key('secret', 'rsa'))
        # Parent key
        self.assertIn(4259707814030784140, secret_key.key_dict())
        # Sub-key
        self.assertIn(5524596192824459786, secret_key.key_dict())

    it "successfully consumes a public key":
        public_key = Key().parse(data.get_pgp_key('public', 'rsa'))
        # Parent key
        self.assertIn(3166937994423974160, public_key.key_dict())
        # Sub-key
        self.assertIn(11980534847294644458, public_key.key_dict())

    it "successfully calls a function to retrieve the passphrase":
        def passphrase_func(message, info):
            return 'blahandstuff'

        secret_key = Key(passphrase=passphrase_func).parse(data.get_pgp_key('secret', 'rsa'))
        # Parent key
        self.assertIn(4259707814030784140, secret_key.key_dict())
        # Sub-key
        self.assertIn(5524596192824459786, secret_key.key_dict())

describe TestCase, "Consuming dsa keys":
    it "successfully consumes a secret key":
        secret_key = Key(passphrase='blahandstuff').parse(data.get_pgp_key('secret', 'dsa'))
        # Parent key
        self.assertIn(7405841044128673154, secret_key.key_dict())
        # Sub-key
        self.assertIn(10470959134280958917, secret_key.key_dict())

    it "successfully consumes a public key":
        public_key = Key().parse(data.get_pgp_key('public', 'dsa'))
        # Parent key
        self.assertIn(7405841044128673154, public_key.key_dict())
        # Sub-key
        self.assertIn(10470959134280958917, public_key.key_dict())

    it "successfully calls a function to retrieve the passphrase":
        def passphrase_func(message, info):
            return 'blahandstuff'

        secret_key = Key(passphrase=passphrase_func).parse(data.get_pgp_key('secret', 'dsa'))
        # Parent key
        self.assertIn(7405841044128673154, secret_key.key_dict())
        # Sub-key
        self.assertIn(10470959134280958917, secret_key.key_dict())
