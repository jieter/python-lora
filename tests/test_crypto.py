import unittest

from lora.crypto import generate_appskey, loramac_decrypt


class TestCrypto(unittest.TestCase):
    def test_loramac_decrypt(self):
        key = "271E403DF4225EEF7E90836494A5B345"
        dev_addr = "000015E4"

        payloads = ((0, "73100b90"), (1, "68d388f0"), (2, "0a12e808"), (3, "e3413bee"))
        expected = "cafebabe"

        for sequence_counter, payload_hex in payloads:
            plaintext_ints = loramac_decrypt(payload_hex, sequence_counter, key, dev_addr)
            plaintext_hex = "".join("{:02x}".format(x) for x in plaintext_ints)

            self.assertEquals(plaintext_hex, expected)

    def test_appskey(self):
        key = generate_appskey()
        self.assertEquals(len(key), 32)

        self.assertNotEquals(key, generate_appskey())
        self.assertNotEquals(generate_appskey(), generate_appskey())
