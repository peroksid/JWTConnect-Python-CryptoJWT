import sys

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed448
from cryptography.hazmat.primitives.asymmetric import ed25519

from ..exception import BadSignature
from ..exception import Unsupported
from . import Signer


class EDDSASigner(Signer):
    def sign(self, msg, key):
        """
        Create a signature over a message as defined in RFC7515 using an
        Octet Key Pair key

        :param msg: The message
        :param key: An Ed25519PrivateKey or Ed448PrivateKey instance
        :return:
        """

        if not isinstance(key, (ed25519.Ed25519PrivateKey, ed448.Ed448PrivateKey)):
            raise TypeError(
                "The private key must be an instance of Ed25519PrivateKey or Ed448PrivateKey"
            )

        return key.sign(msg)

    def verify(self, msg, sig, key):
        """
        Verify a message signature

        :param msg: The message
        :param sig: A signature
        :param key: A Ed25519PublicKey or Ed448PublicKey to use for the verification.
        :raises: BadSignature if the signature can't be verified.
        :return: True
        """
        if not isinstance(key, (ed25519.Ed25519PublicKey, ed448.Ed448PublicKey)):
            raise TypeError(
                "The public key must be an instance of Ed25519PublicKey or Ed448PublicKey"
            )

        try:
            key.verify(sig, msg)
        except InvalidSignature as err:
            raise BadSignature(err)
        else:
            return True
