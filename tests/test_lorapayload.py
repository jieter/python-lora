import glob
import os
import unittest

from lora.payload import LoRaPayload

FIXTURES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')


def read(filename):
    '''Read a file and strip spaces'''
    with open(filename) as f:
        return f.read().strip()


def fixtures():
    for device_path in glob.glob(os.path.join(FIXTURES_PATH, '*')):
        if device_path.endswith('README.md'):
            continue

        # infer dev_addr from fixture path
        dev_addr = os.path.split(device_path)[1]
        key = read(os.path.join(device_path, 'key.hex'))

        # text all the files ending in xml in the path we just discovered
        for fixture_filename in glob.glob(os.path.join(device_path, 'payload_*.xml')):

            yield (
                dev_addr,
                key,
                read(fixture_filename),
                read(fixture_filename.replace('.xml', '.txt'))
            )


class TestLoraPayload(unittest.TestCase):
    def test_xmlparsing(self):
        xmlfilename = os.path.join(FIXTURES_PATH, '000015E4', 'payload_1.xml')

        payload = LoRaPayload(read(xmlfilename))
        self.assertEquals(payload.DevLrrCnt, '1')
        self.assertEquals(payload.FCntUp, '2')

    def test_decrypting_payload(self):
        '''Check the decrypted plaintext against a list of expected plaintexts'''
        for dev_addr, key, xml, expected in fixtures():
            payload = LoRaPayload(xml.encode('UTF-8'))
            plaintext_ints = payload.decrypt(key, dev_addr)

            self.assertEquals(
                ''.join('{:02x}'.format(x) for x in plaintext_ints),
                expected
            )


if __name__ == '__main__':
    unittest.main()
