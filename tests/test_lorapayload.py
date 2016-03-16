import glob
import os
import unittest

from lora.payload import LoRaPayload

FIXTURES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'xmls')


def read(filename):
    with open(filename) as f:
        return f.read().strip()


class TestLoraPayload(unittest.TestCase):
    def test_xmlparsing(self):
        xmlfilename = os.path.join(FIXTURES_PATH, '000015E4', 'payload_1.xml')

        payload = LoRaPayload(read(xmlfilename))
        self.assertEquals(payload.DevLrrCnt, '1')

    def test_lorapayloads(self):
        for device_path in glob.glob(os.path.join(FIXTURES_PATH, '*')):
            # infer dev_addr from fixture path
            dev_addr = os.path.split(device_path)[1]
            # key is in a file called key.hex
            key = read(os.path.join(device_path, 'key.hex'))

            # text all the files ending in xml in the path we just discovered
            for fixture_filename in glob.glob(os.path.join(device_path, 'payload_*.xml')):

                payload = LoRaPayload(read(fixture_filename).encode('UTF-8'))
                plaintext_ints = payload.decrypt(key, dev_addr)

                expected_filename = fixture_filename.replace('.xml', '.txt')
                expected_plaintext = read(expected_filename)

                self.assertEquals(
                    ''.join('{:02x}'.format(x) for x in plaintext_ints),
                    expected_plaintext
                )


if __name__ == '__main__':
    unittest.main()
