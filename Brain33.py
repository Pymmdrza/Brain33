import os, requests, base64
import json
from requests_html import HTMLSession
import codecs, random, hashlib, ecdsa, sys, time
from bit import Key
from bit.format import bytes_to_wif
import requests_random_user_agent
from rich.console import Console

cl = Console()


e = b'Q29sb3IgPSBiJ1kyeGhjM01nUTI5c2IzSW9LVG9LSUNBZ0lGSmxaQ0E5SUNkY016TmJNekZ0SndvZ0lDQWdSM0psWlc0Z1BTQW5YRE16V3pNeWJTY0tJQ0FnSUZsbGJHeHZkeUE5SUNkY016TmJNek50SndvZ0lDQWdRbXgxWlNBOUlDZGNNek5iTXpSdEp3b2dJQ0FnVFdGblpXNTBZU0E5SUNkY016TmJNelZ0SndvZ0lDQWdRM2xoYmlBOUlDZGNNek5iTXpadEp3b2dJQ0FnVjJocGRHVWdQU0FuWERNeld6TTNiU2NLSUNBZ0lFZHlaWGtnUFNBblhETXpXekp0SndvZ0lDQWdVbVZ6WlhRZ1BTQW5YREF6TTFzd2JTY0tDZ3BTWldRZ1BTQkRiMnh2Y2k1U1pXUUtSM0psWlc0Z1BTQkRiMnh2Y2k1SGNtVmxiZ3BaWld4c2IzY2dQU0JEYjJ4dmNpNVpaV3hzYjNjS1EzbGhiaUE5SUVOdmJHOXlMa041WVc0S1RXRm5aVzUwWVNBOUlFTnZiRzl5TGsxaFoyVnVkR0VLVjJocGRHVWdQU0JEYjJ4dmNpNVhhR2wwWlFwU1pYTmxkQ0E5SUVOdmJHOXlMbEpsYzJWMCcKdHhzID0gYidaR1ZtSUVkbGRGUnlZVzV6WVdOMGFXOXVLSE4wY25JcE9nb2dJQ0FnYkdsdWExOTFjbXdnUFNCbUltaDBkSEJ6T2k4dlluUmpNUzUwY21WNmIzSXVhVzh2WVdSa2NtVnpjeTk3YzNSeWNuMGlDaUFnSUNCMGNuazZDaUFnSUNBZ0lDQWdVeUE5SUVoVVRVeFRaWE56YVc5dUtDa0tJQ0FnSUNBZ0lDQlNaWEVnUFNCVExtZGxkQ2hzYVc1clgzVnliQ2tLSUNBZ0lDQWdJQ0I0Y0dGMGFDQTlJQ0l2YUhSdGJDOWliMlI1TDIxaGFXNHZaR2wyTDNSaFlteGxMM1JpYjJSNUwzUnlXelZkTDNSa1d6SmRJZ29nSUNBZ0lDQWdJRTFsZEdGa1lYUmhJRDBnVW1WeExtaDBiV3d1ZUhCaGRHZ29lSEJoZEdncENpQWdJQ0FnSUNBZ2NtVjBkWEp1SUUxbGRHRmtZWFJoV3pCZExuUmxlSFFLSUNBZ0lHVjRZMlZ3ZERvS0lDQWdJQ0FnSUNCeVpYUjFjbTRnSWkweElnPT0nCg=='

exec(base64.b64decode(e).decode())

exec(base64.b64decode(Color).decode())



def PrivateKeyFromPassphrase(passphrase):
    return str(hashlib.sha256(passphrase.encode('utf-8')).hexdigest())


def AddrFromPrivateKeyBytes(PrivateKey):
    PrivateKey_Bytes: str = codecs.decode(PrivateKey, 'hex_codec')
    bit_compressed = Key.from_hex(PrivateKey)
    address_compressed = bit_compressed.address
    wif_uncompressed = bytes_to_wif(PrivateKey_Bytes, compressed=False)
    bit_uncompressed = Key(wif_uncompressed)
    address_uncompressed = bit_uncompressed.address
    return address_compressed, address_uncompressed


exec(base64.b64decode(txs).decode())
cl.clear()
print(f"{Red}[+]{Reset}{Yellow} Please Enter Word File Name with Type Format:{Reset} ")
filename = str(input("HERE >>> "))

count = 0
found = 0
with open(filename, "r") as bf:
    for word in bf:
        count += 1
        passphrase = word
        PrivateKey = PrivateKeyFromPassphrase(passphrase)
        CoAddr, UnAddr = AddrFromPrivateKeyBytes(PrivateKey)
        txs_co = GetTransaction(CoAddr)
        txs_un: str = GetTransaction(UnAddr)
        if int(txs_co) > 0 or int(txs_un) > 0:
            found += 1
            ff = open('Found.txt', 'a').write(f"Compressed: {CoAddr} : {txs_co}\n"
                                              f"Uncompressed: {UnAddr} : {txs_un}\n"
                                              f"Private Key : {PrivateKey}\n"
                                              f"Passphrase : {passphrase}\n"
                                              f"{'=' * 22} MMDRZA.COM {'=' * 22}\n")
        else:

            print(f"[{Yellow}{count}{Reset} {Red}/{Reset} {Green}Found:{found}{Reset}] {CoAddr}{Red}:{Reset}{txs_co} {Red}#{Reset} {UnAddr}{Red}:{Reset}{txs_un} {Red}={Reset}{Magenta} {passphrase}{Reset}")
