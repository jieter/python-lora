from __future__ import print_function

from lxml import etree

from .crypto import loramac_decrypt


class LoRaPayload(object):
    '''Wrapper for an actility LoRa Payload'''
    def __init__(self, xmlstr):
        self.payload = etree.fromstring(xmlstr)

        if self.payload.tag != '{http://uri.actility.com/lora}DevEUI_uplink':
            raise ValueError('LoraPayload expects an XML-string as argument')

    def __getattr__(self, name):
        '''Get the (text) contents of an element in the DevEUI_uplink XML, allows'''
        try:
            return self.payload.find('{http://uri.actility.com/lora}' + name).text
        except AttributeError:
            print('Could not find attribute with name: {}'.format(name))

    def decrypt(self, key, dev_addr):
        sequence_counter = int(self.FCntUp)

        return loramac_decrypt(self.payload_hex, sequence_counter, key, dev_addr)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        help_text = [
            'Usage: python payload.py <filename> <key> <dev_addr>'
            '<filename>: filename of an XML containing DevEUI_uplink',
            '<key>: key as 16-byte hex-encoded string',
            '<dev_addr>: DevAddr as 4-byte hex-encoded string'
            '',
            'python payload.py payload.xml AABBCCDDEEFFAABBCCDDEEFFAABBCCDD 00112233'
        ]
        print('\n'.join(help_text))
        sys.exit()
    _, payload_filename, key, dev_addr = sys.argv

    print('\nInput file ', payload_filename)
    with open(payload_filename) as payload_file:
        payload = LoRaPayload(payload_file.read())
        payload_hex = payload.payload_hex
        print('payload_hex from xml:', payload_hex)
        print('DevEUI from xml', payload.DevEUI)
        print('sequence_counter (lsb first)', ''.join('{:02x}'.format(x) for x in payload.sequence_counter_list))

        plaintext = payload.decrypt(key, dev_addr)

        print('decrypted', ''.join('{:02x}'.format(x) for x in plaintext))
