#!/usr/bin/env python
from __future__ import print_function

from Crypto.Cipher import AES
from lxml import etree

UP_LINK = 0
DOWN_LINK = 1


class LoraPayload(object):
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

    @property
    def sequence_counter_list(self):
        '''Sequence counter as a tuple of 4 bytes, lsb first'''
        seq = int(self.FCntUp)

        return (seq & 0xff, seq >> 8 & 0xff, seq >> 16 & 0xff, seq >> 24 & 0xff)

    def decrypt(self, key, dev_addr):
        '''
        LoraMac decrypt, which is actually LoraMac encrypt of each 16-byte block
        of bytes and XORing that with every block of data.

        key: 16-byte hex-encoded AES key. (AABBCCDDEEFFAABBCCDDEEFFAABBCCDD)
        dev_addr: 4-byte hex-encoded DevAddr (AABBCCDD)

        returns an array of byte values.

        This method is based on `void LoRaMacPayloadEncrypt()` in
        https://github.com/Lora-net/LoRaMac-node/blob/master/src/mac/LoRaMacCrypto.c#L108
        '''
        key = key.decode('hex')
        dev_addr = map(ord, dev_addr.decode('hex'))
        buffer = map(ord, self.payload_hex.decode('hex'))
        size = len(buffer)
        sequence_counter = self.sequence_counter_list

        bufferIndex = 0
        # block counter
        ctr = 1

        # output buffer, initialize to input buffer size.
        encBuffer = [0x00] * size

        aes = AES.new(key, AES.MODE_ECB)

        def aes_encrypt_block(aBlock):
            '''
            AES encrypt a block.
            aes.encrypt expects a string, so we convert the input to string and
            the return value to bytes again.
            '''
            return map(ord, aes.encrypt(''.join(map(chr, aBlock))))

        # for the definition of this block refer to
        # chapter 4.3.3.1 Encryption in LoRaWAN
        # in the LoRaWAN specification
        aBlock = [
            0x01,                 # 0 always 0x01
            0x00,
            0x00,
            0x00,
            0x00,                 # 1...4 always 0x00
            UP_LINK,              # 5 directions, 0 for uplink, 1 for downlink
            dev_addr[3],          # 6 devaddr, lsb
            dev_addr[2],
            dev_addr[1],
            dev_addr[0],          # 9 devaddr, msb
            sequence_counter[0],  # 10 sequence counter (FCntUp) lsb
            sequence_counter[1],
            sequence_counter[2],
            sequence_counter[3],  # 13 sequence counter (FCntUp) msb
            0x00,                 # 14 always 0x01
            0x00                  # 15 block counter
        ]

        # complete blocks
        while size >= 16:
            aBlock[15] = ctr & 0xFF
            ctr += 1
            sBlock = aes_encrypt_block(aBlock)
            for i in range(16):
                encBuffer[bufferIndex + i] = buffer[bufferIndex + i] ^ sBlock[i]

            size -= 16
            bufferIndex += 16

        # partial blocks
        if size > 0:
            aBlock[15] = ctr & 0xFF
            sBlock = aes_encrypt_block(aBlock)
            for i in range(size):
                encBuffer[bufferIndex + i] = buffer[bufferIndex + i] ^ sBlock[i]

        return encBuffer

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
        payload = LoraPayload(payload_file.read())
        payload_hex = payload.payload_hex
        print('payload_hex from xml:', payload_hex)
        print('DevEUI from xml', payload.DevEUI)
        print('sequence_counter (lsb first)', ''.join('{:02x}'.format(x) for x in payload.sequence_counter_list))

        plaintext = payload.decrypt(key, dev_addr)

        print('decrypted', ''.join('{:02x}'.format(x) for x in plaintext))
