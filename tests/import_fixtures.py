import os
import sys

from lora.payload import LoRaPayload

# Import fixtures from a file containing
#
dev_addr = sys.argv[1] or '00100222'
fixture_filename = '{}.txt'.format(dev_addr)

if not os.exists(fixture_filename):
    print('File containing fixtures does not exist ({})'.format(fixture_filename))
    sys.exit()

fixtures = open(fixture_filename)

filename_fmt = 'fixtures/{}/payload_{}-{}.xml'

enc = 1
plain = 1

for item in fixtures.readlines():
    item = item.strip()

    # skip short lines, not containing xml and comments
    if len(item) < 10 or item[0] == '#':
        continue

    payload = LoRaPayload(item)

    if payload.FPort == '1':
        # not encrypted
        filename = filename_fmt.format(dev_addr, 'plaintext', plain)
        plain += 1
    else:
        filename = filename_fmt.format(dev_addr, 'encrypted', enc)
        enc += 1
        # empty file for expected plaintexts.
        open(filename.replace('.xml', '.txt'), 'w').write('')

    open(filename, 'w').write(item.replace('><', '>\n<'))
