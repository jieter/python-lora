# LoRa Test XMLs

Each subdirectory is the hex encoded DevAddr of a device transmitting some messages and contains:

 - `key.hex` Hex encoded AppSKey
 - One or more `payload_<n>.xml`/`payload_<n>.txt` pairs.
   - Each XML file contains the contents of the POST body actility/thingpark makes to the defined HTTP POST receiver.
   - Each txt file contains the (hex encoded) plaintext payload originally transmitted.
