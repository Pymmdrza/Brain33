import os, requests, base64
import json
from requests_html import HTMLSession
import codecs, random, hashlib, ecdsa, sys, time
from bit import Key
from bit.format import bytes_to_wif
import requests_random_user_agent
from rich.console import Console

cl = Console()


Color = b'Y2xhc3MgQ29sb3IoKToKICAgIFJlZCA9ICdcMzNbMzFtJwogICAgR3JlZW4gPSAnXDMzWzMybScKICAgIFllbGxvdyA9ICdcMzNbMzNtJwogICAgQmx1ZSA9ICdcMzNbMzRtJwogICAgTWFnZW50YSA9ICdcMzNbMzVtJwogICAgQ3lhbiA9ICdcMzNbMzZtJwogICAgV2hpdGUgPSAnXDMzWzM3bScKICAgIEdyZXkgPSAnXDMzWzJtJwogICAgUmVzZXQgPSAnXDAzM1swbScKCgpSZWQgPSBDb2xvci5SZWQKR3JlZW4gPSBDb2xvci5HcmVlbgpZZWxsb3cgPSBDb2xvci5ZZWxsb3cKQ3lhbiA9IENvbG9yLkN5YW4KTWFnZW50YSA9IENvbG9yLk1hZ2VudGEKV2hpdGUgPSBDb2xvci5XaGl0ZQpSZXNldCA9IENvbG9yLlJlc2V0'
txs = b'ZGVmIEdldFRyYW5zYWN0aW9uKHN0cnIpOgogICAgbGlua191cmwgPSBmImh0dHBzOi8vYnRjMS50cmV6b3IuaW8vYWRkcmVzcy97c3Rycn0iCiAgICB0cnk6CiAgICAgICAgUyA9IEhUTUxTZXNzaW9uKCkKICAgICAgICBSZXEgPSBTLmdldChsaW5rX3VybCkKICAgICAgICB4cGF0aCA9ICIvaHRtbC9ib2R5L21haW4vZGl2L2RpdlsyXS9kaXZbMV0vdGFibGUvdGJvZHkvdHJbNF0vdGRbMl0iCiAgICAgICAgTWV0YWRhdGEgPSBSZXEuaHRtbC54cGF0aCh4cGF0aCkKICAgICAgICByZXR1cm4gTWV0YWRhdGFbMF0udGV4dAogICAgZXhjZXB0OgogICAgICAgIHJldHVybiAiLTEi'

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
