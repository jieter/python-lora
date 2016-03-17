# python-lora

Python wrapper for LoRa payloads from Thingpark/Actility.
Allowing decryption of the payload.

- Depends on [cryptography]
- Based on crypto code in [Lora-net/LoRaMac-node]
- Tested with python 2.7, 3.4 and 3.5
- Available on [pypi]

## Usage

`pip install python-lora`

```python
from lora.payload import LoRaPayload

xmlstr = '''<?xml version="1.0" encoding="UTF-8"?>
<DevEUI_uplink xmlns="http://uri.actility.com/lora">[...]
<FCntUp>2</FCntUp>[...]
<payload_hex>[...]</payload_hex>[...]
</DevEUI_uplink>'''

payload = LoRaPayload(xmlstr)

key = 'AABBCCDDEEFFAABBCCDDEEFFAABBCCDD'
dev_addr = '00112233'
plaintext = payload.decrypt(key, dev_addr)
```

You can also use `loramac_decrypt` without the XML wrapper:
```python
>>> from lora.crypto import loramac_decrypt
>>> payload = '11daf7a44d5e2bbe557176e9e6c8da'
>>> sequence_counter = 2
>>> key = 'AABBCCDDEEFFAABBCCDDEEFFAABBCCDD'
>>> dev_addr = '00112233'
>>> loramac_decrypt(payload, sequence_counter, key, dev_addr)
[222, 59, 24, 8, 7, 155, 237, 158, 103, 125, 93, 34, 161, 204, 33]
```

[cryptography]: https://cryptography.io/
[pypi]: https://pypi.python.org/pypi/python-lora
[Lora-net/LoRaMac-node]: https://github.com/Lora-net/LoRaMac-node/blob/master/src/mac/LoRaMacCrypto.c#L108
