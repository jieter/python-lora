# python-lora

Python wrapper for LoRa payloads in supporting decryption.

## Usage

```python
from lora.payload import LoRoPayload

xmlstr = '''<?xml version="1.0" encoding="UTF-8"?>
<DevEUI_uplink xmlns="http://uri.actility.com/lora">
[...]
<FCntUp>2</FCntUp>
[...]
<payload_hex>[...]</payload_hex>
[...]
</DevEUI_uplink>'''

payload = LoRaPayload(xmlstr)

key = 'AABBCCDDEEFFAABBCCDDEEFFAABBCCDD'
dev_addr = '00112233'
plaintext = payload.decrypt(key, dev_addr)
```
