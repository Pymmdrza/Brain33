import hashlib
import multiprocessing
import os, sys, codecs, time
import ecdsa, base64
import requests
from rich.console import Console
from requests_html import HTMLSession
from bit import Key
from bit.format import bytes_to_wif

code = b'Zmlyc3Rfc2VjdGlvbiA9IGInWkdWbUlGQnlhVzUwWDBSbGJHRjVLSE1wT2dvZ0lDQWdabTl5SUdNZ2FXNGdjem9LSUNBZ0lDQWdJQ0J6ZVhNdWMzUmtiM1YwTG5keWFYUmxLR01wQ2lBZ0lDQWdJQ0FnYzNsekxuTjBaRzkxZEM1bWJIVnphQ2dwQ2lBZ0lDQWdJQ0FnZEdsdFpTNXpiR1ZsY0Nnd0xqSXBDZ29LWTI5dWMyOXNaU0E5SUVOdmJuTnZiR1VvS1FwamIyNXpiMnhsTG1Oc1pXRnlLQ2tLWW5KaGFXNHpNeUE5SUdZaUlpSUtXMmR2YkdReFhlS1dpT0tXaU9LV2lPS1dpT0tXaU9LV2lGdDNhR2wwWlYzaWxaZGJMM2RvYVhSbFhTRGlsb2ppbG9qaWxvamlsb2ppbG9qaWxvaGJkMmhwZEdWZDRwV1hXeTkzYUdsMFpWMGdJT0tXaU9LV2lPS1dpT0tXaU9LV2lGdDNhR2wwWlYzaWxaZGJMM2RvYVhSbFhTRGlsb2ppbG9oYmQyaHBkR1ZkNHBXWFd5OTNhR2wwWlYzaWxvamlsb2ppbG9oYmQyaHBkR1ZkNHBXWFd5OTNhR2wwWlYwZ0lDRGlsb2ppbG9oYmQyaHBkR1ZkNHBXWFd5OTNhR2wwWlYxYkwyZHZiR1F4WFZ0dmNtRnVaMlV6WFNEaWxvamlsb2ppbG9qaWxvamlsb2ppbG9oYmQyaHBkR1ZkNHBXWFd5OTNhR2wwWlYwZzRwYUk0cGFJNHBhSTRwYUk0cGFJNHBhSVczZG9hWFJsWGVLVmwxc3ZkMmhwZEdWZElGc3ZiM0poYm1kbE0xMEtXMmR2YkdReFhlS1dpT0tXaUZ0M2FHbDBaVjNpbFpUaWxaRGlsWkJiTDNkb2FYUmxYZUtXaU9LV2lGdDNhR2wwWlYzaWxaZGJMM2RvYVhSbFhlS1dpT0tXaUZ0M2FHbDBaVjNpbFpUaWxaRGlsWkJiTDNkb2FYUmxYZUtXaU9LV2lGdDNhR2wwWlYzaWxaZGJMM2RvYVhSbFhlS1dpT0tXaUZ0M2FHbDBaVjNpbFpUaWxaRGlsWkJiTDNkb2FYUmxYZUtXaU9LV2lGdDNhR2wwWlYzaWxaZGJMM2RvYVhSbFhlS1dpT0tXaUZ0M2FHbDBaVjNpbFpGYkwzZG9hWFJsWGVLV2lPS1dpT0tXaU9LV2lGdDNhR2wwWlYzaWxaZGJMM2RvYVhSbFhTQWc0cGFJNHBhSVczZG9hWFJsWGVLVmtWc3ZkMmhwZEdWZFd5OW5iMnhrTVYxYmIzSmhibWRsTTEwZ1czZG9hWFJsWGVLVm11S1ZrT0tWa09LVmtPS1ZrRnN2ZDJocGRHVmQ0cGFJNHBhSVczZG9hWFJsWGVLVmwrS1ZtdUtWa09LVmtPS1ZrT0tWa0ZzdmQyaHBkR1ZkNHBhSTRwYUlXM2RvYVhSbFhlS1ZsMXN2ZDJocGRHVmRXeTl2Y21GdVoyVXpYUXBiWjI5c1pERmQ0cGFJNHBhSTRwYUk0cGFJNHBhSTRwYUlXM2RvYVhSbFhlS1ZsT0tWblZzdmQyaHBkR1ZkNHBhSTRwYUk0cGFJNHBhSTRwYUk0cGFJVzNkb2FYUmxYZUtWbE9LVm5Wc3ZkMmhwZEdWZDRwYUk0cGFJNHBhSTRwYUk0cGFJNHBhSTRwYUlXM2RvYVhSbFhlS1ZrVnN2ZDJocGRHVmQ0cGFJNHBhSVczZG9hWFJsWGVLVmtWc3ZkMmhwZEdWZDRwYUk0cGFJVzNkb2FYUmxYZUtWbEZzdmQyaHBkR1ZkNHBhSTRwYUlXM2RvYVhSbFhlS1ZseUJiTDNkb2FYUmxYZUtXaU9LV2lGdDNhR2wwWlYzaWxaRmJMM2RvYVhSbFhWc3ZaMjlzWkRGZFcyOXlZVzVuWlROZElDRGlsb2ppbG9qaWxvamlsb2ppbG9oYmQyaHBkR1ZkNHBXVTRwV2RJRnN2ZDJocGRHVmQ0cGFJNHBhSTRwYUk0cGFJNHBhSVczZG9hWFJsWGVLVmxPS1ZuVnN2ZDJocGRHVmRXeTl2Y21GdVoyVXpYUXBiWjI5c1pERmQ0cGFJNHBhSVczZG9hWFJsWGVLVmxPS1ZrT0tWa0ZzdmQyaHBkR1ZkNHBhSTRwYUlXM2RvYVhSbFhlS1ZsMXN2ZDJocGRHVmQ0cGFJNHBhSVczZG9hWFJsWGVLVmxPS1ZrT0tWa0ZzdmQyaHBkR1ZkNHBhSTRwYUlXM2RvYVhSbFhlS1ZsMXN2ZDJocGRHVmQ0cGFJNHBhSVczZG9hWFJsWGVLVmxPS1ZrT0tWa0ZzdmQyaHBkR1ZkNHBhSTRwYUlXM2RvYVhSbFhlS1ZrVnN2ZDJocGRHVmQ0cGFJNHBhSVczZG9hWFJsWGVLVmtWc3ZkMmhwZEdWZDRwYUk0cGFJVzNkb2FYUmxYZUtWa2VLVm1sc3ZkMmhwZEdWZDRwYUk0cGFJVzNkb2FYUmxYZUtWbDFzdmQyaHBkR1ZkNHBhSTRwYUlXM2RvYVhSbFhlS1ZrVnN2ZDJocGRHVmRXeTluYjJ4a01WMWJiM0poYm1kbE0xMGdJRnQzYUdsMFpWM2lsWnJpbFpEaWxaRGlsWkJiTDNkb2FYUmxYZUtXaU9LV2lGdDNhR2wwWlYzaWxaY2c0cFdhNHBXUTRwV1E0cFdRV3k5M2FHbDBaVjNpbG9qaWxvaGJkMmhwZEdWZDRwV1hXeTkzYUdsMFpWMWJMMjl5WVc1blpUTmRDbHRuYjJ4a01WM2lsb2ppbG9qaWxvamlsb2ppbG9qaWxvaGJkMmhwZEdWZDRwV1U0cFdkV3k5M2FHbDBaVjNpbG9qaWxvaGJkMmhwZEdWZDRwV1JXeTkzYUdsMFpWMGdJT0tXaU9LV2lGdDNhR2wwWlYzaWxaRmJMM2RvYVhSbFhlS1dpT0tXaUZ0M2FHbDBaVjNpbFpGYkwzZG9hWFJsWFNBZzRwYUk0cGFJVzNkb2FYUmxYZUtWa1ZzdmQyaHBkR1ZkNHBhSTRwYUlXM2RvYVhSbFhlS1ZrVnN2ZDJocGRHVmQ0cGFJNHBhSVczZG9hWFJsWGVLVmtTRGlsWnBiTDNkb2FYUmxYZUtXaU9LV2lPS1dpT0tXaUZ0M2FHbDBaVjNpbFpGYkwzZG9hWFJsWFZzdloyOXNaREZkVzI5eVlXNW5aVE5kSU9LV2lPS1dpT0tXaU9LV2lPS1dpT0tXaUZ0M2FHbDBaVjNpbFpUaWxaMWJMM2RvYVhSbFhlS1dpT0tXaU9LV2lPS1dpT0tXaU9LV2lGdDNhR2wwWlYzaWxaVGlsWjFiTDNkb2FYUmxYVnN2YjNKaGJtZGxNMTBLVzJkdmJHUXhYVnQzYUdsMFpWM2lsWnJpbFpEaWxaRGlsWkRpbFpEaWxaRGlsWjBnNHBXYTRwV1E0cFdkSUNEaWxacmlsWkRpbFozaWxacmlsWkRpbFowZ0lPS1ZtdUtWa09LVm5lS1ZtdUtWa09LVm5lS1ZtdUtWa09LVm5TQWc0cFdhNHBXUTRwV1E0cFdRNHBXZFd5OTNhR2wwWlYxYkwyZHZiR1F4WFZ0dmNtRnVaMlV6WFZ0M2FHbDBaVjBnNHBXYTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXZElPS1ZtdUtWa09LVmtPS1ZrT0tWa09LVmtPS1ZuU0JiTDNkb2FYUmxYVnN2YjNKaGJtZGxNMTBLNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdtNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1E0cFdRNHBXUTRwV1FDbHR5WldRelhlS1ZsT0tWa09LVmwrS1ZwdUtWa09LVmwrS1ZsT0tWa09LVmwrS1ZsT0tWa09LVmwrS1ZwdUtWa09LVmwrS1ZsT0tWa09LVmwrS1ZsT0tWcHVLVmwrS1ZsT0tWcHVLVmwrS1ZsT0tWa09LVmwrS1ZwdUtWa09LVmwxc3ZjbVZrTTEwZ0lPS1ZrU0FnVzNKbFpERmRXMXRqZVdGdVhTdGJMMk41WVc1ZFhWc3ZjbVZrTVYwZ1cyZHlaV1Z1WFU5bVptbGphV0ZzSUZkbFluTnBkR1U2V3k5bmNtVmxibDBnYUhSMGNITTZMeTlOYldSeWVtRXVRMjl0Q2x0a1lYSnJYM0psWkYzaWxhRGlsWkRpbFozaWxhRGlsYWJpbFozaWxaRWc0cFdSNHBXUklPS1ZwdUtWb09LVnB1S1ZuZUtWb09LVmtPS1ZvK0tWa2VLVmtlS1ZrZUtWa2VLVmtlS1ZrZUtWa2VLVm95RGlsYURpbGFiaWxaMWJMMlJoY210ZmNtVmtYU0FnNHBXUklDQmJjbVZrTVYxYlcyTjVZVzVkSzFzdlkzbGhibDFkV3k5eVpXUXhYVnRuY21WbGJsMGdSMmwwYUhWaUlEcGJMMmR5WldWdVhTQm9kSFJ3Y3pvdkwyZHBkR2gxWWk1amIyMHZVSGx0YldSeWVtRUtXM0psWkROZDRwV3BJQ0RpbGFuaWxacmlsWkRpbFpyaWxaRGlsWjNpbFpyaWxaRGlsWjNpbGFuaWxacmlsWkRpbGFrZzRwV3A0cFdwSU9LVnFlS1ZxU0RpbGFuaWxacmlsWkRpbFozaWxhbmlsWnJpbFpCYkwzSmxaRE5kSUNEaWxaRWdJRnR5WldReFhWdGJZM2xoYmwwcld5OWplV0Z1WFYxYkwzSmxaREZkSUZ0bmNtVmxibDFGYldGcGJDQTZJRnN2WjNKbFpXNWRVSGxOYldSeWVtRkFSMjFoYVd3dVEyOXRDbHRuYjJ4a01WMGc0cFdVNHBXbTRwV1g0cFdVNHBXbTRwV1g0cFdVNHBXbTRwV1g0cFdtNHBXUTRwV1g0cFdVNHBXUTRwV1g0cFdVNHBXUTRwV1hJT0tWbE9LVmtPS1ZsK0tWbE9LVmtPS1ZsK0tWbE9LVnB1S1ZsMXN2WjI5c1pERmRJQ0FnNHBXUklDQmJjbVZrTVYxYlcyTjVZVzVkSzFzdlkzbGhibDFkV3k5eVpXUXhYVnRuY21WbGJsMGdWSGRwZEhSbGNpQTZXeTluY21WbGJsMGdRRkI1VFcxa2NucGhDbHR2Y21GdVoyVXhYU0RpbFpIaWxaSGlsWkhpbFpIaWxaSGlsWkVnNHBXUjRwV1I0cFdnNHBXbTRwV2Q0cFdVNHBXUTRwV2Q0cFdnNHBXUTRwV2pJT0tWa1NBZzRwV1JJT0tWa2VLVmtlS1ZrZUtWa1ZzdmIzSmhibWRsTVYwZ0lDRGlsWkVnSUZ0eVpXUXhYVnRiWTNsaGJsMHJXeTlqZVdGdVhWMWJMM0psWkRGZFcyZHlaV1Z1WFNCTlpXUnBkVzBnT2lCYkwyZHlaV1Z1WFcxa2NucGhMazFsWkdsMWJTNURiMjBLVzJSaGNtdGZiM0poYm1kbFhTRGlsYWtnNHBXcDRwV3BJT0tWcWVLVmtPS1ZxZUtWbmVLVnFlS1ZtdUtWa09LVm11S1ZrT0tWbmVLVnFTRGlsYWx2NHBXYTRwV1E0cFdkNHBXYTRwV1E0cFdkNHBXcElPS1ZxVnN2WkdGeWExOXZjbUZ1WjJWZElDQWc0cFdSSUNCYmNtVmtNVjFiVzJONVlXNWRLMXN2WTNsaGJsMWRXeTl5WldReFhWdG5jbVZsYmwwZ1VHRjBjbVZ2YmpvZ1d5OW5jbVZsYmwxb2RIUndjem92TDNCaGRISmxiMjR1WTI5dEwxQjVUVzFrY25waEN1S1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVnFlS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa09LVmtPS1ZrT0tWa0NBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FLSWlJaUNncGpiMjV6YjJ4bExuQnlhVzUwS0dZaWUySnlZV2x1TXpOOUlpa0tDbklnUFNBMENtTnZjbVZ6SUQwZ01UQUtVSEpwYm5SZlJHVnNZWGtvWmlkRmJuUmxjaUJYYjNKa0lFeHBjM1FnUm1sc1pTQk9ZVzFsSUhkcGRHZ2dWSGx3WlNCR2IzSnRZWFFnTGx4dVhHNWJSWGhoYlhCc1pUb2dWMjl5WkVacGJHVXVkSGgwWFZ4dVhHNG5LUXBtYVd4bGJpQTlJSE4wY2locGJuQjFkQ2duUm1sc1pTQk9ZVzFsSUZ0SVJWSkZYU0IrSURvZ0p5a3AnCgpwYmMgPSBiJ1pHVm1JRWRsZEZSeVlXNXpZV04wYVc5dUtHRmtaSEpsYzNNcE9nb2dJQ0FnYkdsdWExOTFjbXdnUFNCbUltaDBkSEJ6T2k4dlluUmpNaTUwY21WNmIzSXVhVzh2WVdSa2NtVnpjeTk3WVdSa2NtVnpjMzBpQ2lBZ0lDQjBjbms2Q2lBZ0lDQWdJQ0FnVXlBOUlFaFVUVXhUWlhOemFXOXVLQ2tLSUNBZ0lDQWdJQ0JTWlhFZ1BTQlRMbWRsZENoc2FXNXJYM1Z5YkNrS0lDQWdJQ0FnSUNCNGNHRjBhQ0E5SUNJdmFIUnRiQzlpYjJSNUwyMWhhVzR2WkdsMkwyUnBkbHN5WFM5a2FYWmJNVjB2ZEdGaWJHVXZkR0p2WkhrdmRISmJORjB2ZEdSYk1sMGlDaUFnSUNBZ0lDQWdUV1YwWVdSaGRHRWdQU0JTWlhFdWFIUnRiQzU0Y0dGMGFDaDRjR0YwYUNrS0lDQWdJQ0FnSUNCeVpYUjFjbTRnVFdWMFlXUmhkR0ZiTUYwdWRHVjRkQW9nSUNBZ1pYaGpaWEIwT2dvZ0lDQWdJQ0FnSUhKbGRIVnliaUFpTFRFaUNnb0taR1ZtSUVkbGRFSmhiR0Z1WTJVb1lXUmtjbVZ6Y3lrNkNpQWdJQ0JzYVc1clgzVnliQ0E5SUdZaWFIUjBjSE02THk5aWRHTXlMblJ5WlhwdmNpNXBieTloWkdSeVpYTnpMM3RoWkdSeVpYTnpmU0lLSUNBZ0lIUnllVG9LSUNBZ0lDQWdJQ0JUSUQwZ1NGUk5URk5sYzNOcGIyNG9LUW9nSUNBZ0lDQWdJRkpsY1NBOUlGTXVaMlYwS0d4cGJtdGZkWEpzS1FvZ0lDQWdJQ0FnSUhod1lYUm9JRDBnSWk5b2RHMXNMMkp2WkhrdmJXRnBiaTlrYVhZdlpHbDJXekpkTDJScGRsc3hYUzkwWVdKc1pTOTBZbTlrZVM5MGNsc3pYUzkwWkZzeVhTSUtJQ0FnSUNBZ0lDQk5aWFJoWkdGMFlTQTlJRkpsY1M1b2RHMXNMbmh3WVhSb0tIaHdZWFJvS1FvZ0lDQWdJQ0FnSUhKbGRIVnliaUJOWlhSaFpHRjBZVnN3WFM1MFpYaDBDaUFnSUNCbGVHTmxjSFE2Q2lBZ0lDQWdJQ0FnY21WMGRYSnVJQ0l0TVNJPScKCmV4ZWMoYmFzZTY0LmI2NGRlY29kZShmaXJzdF9zZWN0aW9uKS5kZWNvZGUoKSkKCmV4ZWMoYmFzZTY0LmI2NGRlY29kZShwYmMpLmRlY29kZSgpKQ=='

exec(base64.b64decode(code).decode())


def seek(r):
    mylist = []

    with open(filen, newline='', encoding='utf-8') as f:
        for line in f:
            mylist.append(line.strip())

    class xWallet:

        @staticmethod
        def generate_address_from_passphrase(passphrase):
            private_key = str(hashlib.sha256(passphrase.encode('utf-8')).hexdigest())
            caddr, uaddr = xWallet.generated_Uncompressed_Compressed(private_key)
            return private_key, caddr, uaddr

        @staticmethod
        def generated_Uncompressed_Compressed(private_key):
            byte_key = codecs.decode(private_key, 'hex_codec')
            bit1 = Key.from_hex(private_key)
            caddr = bit1.address
            wif2 = bytes_to_wif(byte_key, compressed=False)
            bit2 = Key(wif2)
            uaddr = bit2.address
            return caddr, uaddr

        @staticmethod
        def generate_dec(private_key):
            return int(private_key, 16)

    z = 0
    w = 0
    s = 0
    for i in range(0, len(mylist)):

        sys.stdout.write(f"\x1b]2;T:{z}/Found:{w}/Value:{s}\x07")
        passphrase = mylist[i]
        wallet = xWallet()
        private_key, caddr, uaddr = wallet.generate_address_from_passphrase(passphrase)
        dec = wallet.generate_dec(private_key)
        txs_co = GetTransaction(caddr)
        txs_un = GetTransaction(uaddr)
        ifbtc = '0 BTC'
        console.print(
            f"[red1][[white]MMDRZA.COM[/white]][/red1] ~ [white]SCAN:[/white][cyan]{z} [/cyan]/ [white]Found:[/white][cyan]{w}[/cyan][white] VALUE:[/white][cyan]{s}[/cyan] [gold1]Passphrase:[/gold1][cyan]{passphrase}[/cyan]")
        console.print(
            f"[red1][[white]MMDRZA.COM[/white]][/red1] ~ [white]SCAN:[/white][cyan]{z} [/cyan]/ [white]Found:[/white][cyan]{w}[/cyan][white] VALUE:[/white][cyan]{s}[/cyan] [white]{caddr}[/white] [gold1][TXS:[cyan]{txs_co}[/cyan]][/gold1]")
        console.print(
            f"[red1][[white]MMDRZA.COM[/white]][/red1] ~ [white]SCAN:[/white][cyan]{z} [/cyan]/ [white]Found:[/white][cyan]{w}[/cyan][white] VALUE:[/white][cyan]{s}[/cyan] [white]{uaddr}[/white] [gold1][TXS:[cyan]{txs_un}[/cyan]][/gold1]")
        console.print(
            f"[red1][[white]MMDRZA.COM[/white]][/red1] ~ [white]SCAN:[/white][cyan]{z} [/cyan]/ [white]Found:[/white][cyan]{w}[/cyan][white] VALUE:[/white][cyan]{s}[/cyan] [dark_red]{dec}[/dark_red]")
        console.print(
            f"[red1][[white]MMDRZA.COM[/white]][/red1] ~ [white]SCAN:[/white][cyan]{z} [/cyan]/ [white]Found:[/white][cyan]{w}[/cyan][white] VALUE:[/white][cyan]{s}[/cyan] [red1]{private_key}[/red1]")

        z += 1
        if int(txs_co) > 0 or int(txs_un) > 0:
            w += 1
            co_bal = GetBalance(caddr)
            un_bal = GetBalance(uaddr)

            ff = open('TxsFound__v2.txt', 'a').write(f"Compress: {caddr} TXS:{txs_co}  Passphrase:{passphrase}\n"
                                                     f"unCompress: {uaddr} TXS:{txs_un}\n"
                                                     f"Private: {private_key}\n"
                                                     f"DEC: {dec}\n"
                                                     f"{'=' * 21} MMDRZA.COM {'=' * 21}\n")

            console.print(
                f"[red1][[white]MMDRZA.COM[/white]][/red1] ~ [gold1]SCAN:[/gold1][cyan]{z} [/cyan]/ [green]Found:[/green][cyan]{w}[/cyan][white] VALUE:[/white][cyan]{s}[/cyan] [gold1]Passphrase:[/gold1] [white on blue3]{passphrase}[/white on blue3] ")
            console.print(
                f"[red1][[white]MMDRZA.COM[/white]][/red1] ~ [gold1]SCAN:[/gold1][cyan]{z} [/cyan]/ [green]Found:[/green][cyan]{w}[/cyan][white] VALUE:[/white][cyan]{s}[/cyan] [white on dark_green]{caddr}[/white on dark_green] [gold1][TXS:[cyan]{txs_co}[/cyan]][/gold1]")
            console.print(
                f"[red1][[white]MMDRZA.COM[/white]][/red1] ~ [gold1]SCAN:[/gold1][cyan]{z} [/cyan]/ [green]Found:[/green][cyan]{w}[/cyan][white] VALUE:[/white][cyan]{s}[/cyan] [white on green4]{uaddr}[/white on green4] [gold1][TXS:[cyan]{txs_un}[/cyan]][/gold1]")
            console.print(
                f"[red1][[white]MMDRZA.COM[/white]][/red1] ~ [gold1]SCAN:[/gold1][cyan]{z} [/cyan]/ [green]Found:[/green][cyan]{w}[/cyan][white] VALUE:[/white][cyan]{s}[/cyan] [white on navy_blue]{dec}[/white on navy_blue]")
            console.print(
                f"[red1][[white]MMDRZA.COM[/white]][/red1] ~ [gold1]SCAN:[/gold1][cyan]{z} [/cyan]/ [green]Found:[/green][cyan]{w}[/cyan][white] VALUE:[/white][cyan]{s}[/cyan] [white on blue3]{private_key}[/white on blue3]")
            if co_bal != ifbtc or un_bal != ifbtc:
                s += 1
                ffx = open('ValueFound__v2.txt', 'a').write(f"Compress: {caddr} Balance:{co_bal}\n"
                                                            f"unCompress: {uaddr} Balance:{un_bal}\n"
                                                            f"Private Key: {private_key}\n"
                                                            f"DEC: {dec}\n"
                                                            f"{'=' * 21} MMDRZA.COM {'=' * 21}\n")


seek(r)

t2 = multiprocessing.Thread(target=seek, args=r)
t3 = multiprocessing.Thread(target=GetTransaction, args=r)
t1 = multiprocessing.Thread(target=GetBalance, args=r)
t2.start()
t3.start()
t1.start()
t2.join()
t1.join()
t3.join()
