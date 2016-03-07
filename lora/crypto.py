from Crypto.Cipher import AES

UP_LINK = 0
DOWN_LINK = 1


def loramac_decrypt(payload_hex, sequence_counter, key, dev_addr):
    '''
    LoraMac decrypt, which is actually encrypting each 16-byte block and XORing
    that with each block of data.

    payload_hex: hex-encoded payload
    sequence_counter: integer, sequence counter (FCntUp)
    key: 16-byte hex-encoded AES key. (i.e. AABBCCDDEEFFAABBCCDDEEFFAABBCCDD)
    dev_addr: 4-byte hex-encoded DevAddr (i.e. AABBCCDD)

    returns an array of byte values.

    This method is based on `void LoRaMacPayloadEncrypt()` in
    https://github.com/Lora-net/LoRaMac-node/blob/master/src/mac/LoRaMacCrypto.c#L108
    '''
    key = key.decode('hex')
    dev_addr = map(ord, dev_addr.decode('hex'))
    buffer = map(ord, payload_hex.decode('hex'))
    size = len(buffer)

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
        0x01,                             # 0 always 0x01
        0x00,                             # 1 always 0x00
        0x00,                             # 2 always 0x00
        0x00,                             # 3 always 0x00
        0x00,                             # 4 always 0x00
        UP_LINK,                          # 5 directions, 0 for uplink, 1 for downlink
        dev_addr[3],                      # 6 devaddr, lsb
        dev_addr[2],                      # 7 devaddr
        dev_addr[1],                      # 8 devaddr
        dev_addr[0],                      # 9 devaddr, msb
        sequence_counter & 0xff,          # 10 sequence counter (FCntUp) lsb
        (sequence_counter >> 8) & 0xff,   # 11 sequence counter
        (sequence_counter >> 16) & 0xff,  # 12 sequence counter
        (sequence_counter >> 24) & 0xff,  # 13 sequence counter (FCntUp) msb
        0x00,                             # 14 always 0x01
        0x00                              # 15 block counter
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
