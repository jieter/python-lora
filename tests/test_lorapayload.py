from __future__ import print_function

import glob
import os
import unittest

from lora.payload import LoRaPayload

FIXTURES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fixtures")


def read(filename):
    """Read a file and strip spaces"""
    with open(filename) as f:
        return f.read().strip()


def fixtures():
    for device_path in glob.glob(os.path.join(FIXTURES_PATH, "*")):
        if device_path.endswith("README.md"):
            continue

        # infer dev_addr from fixture path
        dev_addr = os.path.split(device_path)[1]
        key = read(os.path.join(device_path, "key.hex"))

        # text all the files ending in xml in the path we just discovered
        for fixture_filename in glob.glob(os.path.join(device_path, "payload*.xml")):

            fixture = "/".join(fixture_filename.split("/")[-2:])
            if "plaintext" in fixture_filename:
                expected = None
            else:
                expected = read(fixture_filename.replace(".xml", ".txt"))

            yield (dev_addr, key, fixture, read(fixture_filename), expected)


class TestLoraPayload(unittest.TestCase):
    def test_xmlparsing(self):
        xmlfilename = os.path.join(FIXTURES_PATH, "000015E4", "payload_1.xml")

        payload = LoRaPayload(read(xmlfilename))
        self.assertEquals(payload.DevLrrCnt, "1")
        self.assertEquals(payload.FCntUp, "2")

        self.assertEquals(payload.Lrr_location(), "SRID=4326;POINT(4.36984 52.014877)")

    def test_decrypting_payload(self):
        """Check the decrypted plaintext against a list of expected plaintexts"""
        for dev_addr, key, fixture_filename, xml, expected in fixtures():
            payload = LoRaPayload(xml.encode("UTF-8"))
            plaintext_ints = payload.decrypt(key, dev_addr)

            decrypted_hex = "".join("{:02x}".format(x) for x in plaintext_ints)

            self.assertEquals(
                len(decrypted_hex),
                len(payload.payload_hex),
                "Decryption should not change length of hex string",
            )

            if expected is None:
                # plaintext is in filename, so skip checking the expected outcome
                continue

            self.assertEquals(
                decrypted_hex,
                expected,
                "Decrypted payload {} not as expected: \npayload_hex: {}\ndecrypted:   {}\nexpected:    {}".format(
                    fixture_filename, payload.payload_hex, decrypted_hex, expected
                ),
            )


if __name__ == "__main__":
    unittest.main()
