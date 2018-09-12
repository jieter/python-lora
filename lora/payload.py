from __future__ import print_function

from xml.etree import ElementTree

from .crypto import loramac_decrypt

WKT_POINT_FMT = "SRID=4326;POINT({lng} {lat})"


class LoRaPayload(object):
    """Wrapper for an actility LoRa Payload"""

    XMLNS = "{http://uri.actility.com/lora}"

    def __init__(self, xmlstr):
        self.payload = ElementTree.fromstring(xmlstr)

        if self.payload.tag != self.XMLNS + "DevEUI_uplink":
            raise ValueError(
                "LoRaPayload expects an XML-string containing a "
                "DevEUI_uplink tag as root element as argument"
            )

    def __getattr__(self, name):
        """
        Get the (text) contents of an element in the DevEUI_uplink XML, allows
        accessing them as properties of the objects:

        >>> payload = LoRaPayload('<?xml version="1.0" encoding="UTF-8"?>...')
        >>> payload.payload_xml
        '11daf7a44d5e2bbe557176e9e6c8da'
        """
        try:
            return self.payload.find(self.XMLNS + name).text
        except AttributeError:
            print("Could not find tag with name: {}".format(name))

    def decrypt(self, key, dev_addr):
        """
        Decrypt the actual payload in this LoraPayload.

        key: 16-byte hex-encoded AES key. (i.e. AABBCCDDEEFFAABBCCDDEEFFAABBCCDD)
        dev_addr: 4-byte hex-encoded DevAddr (i.e. AABBCCDD)
        """
        sequence_counter = int(self.FCntUp)

        return loramac_decrypt(self.payload_hex, sequence_counter, key, dev_addr)

    def Lrr_location(self):
        """
        Return the location of the LRR (Wireless base station/Gateway)
        """
        return WKT_POINT_FMT.format(lng=float(self.LrrLON), lat=float(self.LrrLAT))
