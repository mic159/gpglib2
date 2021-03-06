.. _examples:

Example
=======

.. code-block:: python

    from gpglib.structures import EncryptedMessage, Key

    data = open('tests/data/keys/key.secret.rsa.gpg', 'rb').read()
    key = Key(passphrase='blahandstuff')
    key.parse(data)
    keys = key.key_dict()
    print(keys)

    data = open('tests/data/encrypted/mdc/rsa/aes/zlib/small.gpg', 'rb').read()
    message = EncryptedMessage(keys)
    message.decrypt(data)

    print("Message successfully decrypted data.dump::")
    print(message.plaintext)

    data = open('tests/data/encrypted/mdc/rsa/aes/zlib/big.gpg', 'rb').read()
    message = EncryptedMessage(keys)
    message.decrypt(data)

    print("Message successfully decrypted data.big.dump::")
    print(message.plaintext)
