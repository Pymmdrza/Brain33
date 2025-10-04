import sys
import time
import hashlib
import requests
from pathlib import Path
from rich.console import Console
from libcrypto import PrivateKey
from dataclasses import dataclass
from typing import Tuple, Optional, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed


BANNER = """[yellow]
██████╗ ██████╗  █████╗ ██╗███╗   ██╗[/yellow][white] ██████╗ ██████╗ [/white]
[yellow]██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║[/yellow][white] ╚════██╗╚════██╗[/white]
[yellow]██████╔╝██████╔╝███████║██║██╔██╗ ██║[/yellow][white]  █████╔╝ █████╔╝[/white]
[yellow]██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║[/yellow][white]  ╚═══██╗ ╚═══██╗[/white]
[yellow]██████╔╝██║  ██║██║  ██║██║██║ ╚████║[/yellow][white] ██████╔╝██████╔╝[/white]
[yellow]╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝[/yellow][white] ╚═════╝ ╚═════╝ [/white]

[white]Official Website:[/white] [cyan]https://Mmdrza.Com[/cyan]
[white]Github:[/white] [cyan]https://github.com/Pymmdrza[/cyan]
[white]Email:[/white] [cyan]PyMmdrza@Gmail.Com[/cyan]
"""

API_TIMEOUT = 8
MAX_RETRIES = 2
REQUEST_DELAY = 0.1


@dataclass
class WalletInfo:
    passphrase: str
    private_key: str
    decimal: str
    compressed_address: str
    uncompressed_address: str
    compressed_txs: int = 0
    uncompressed_txs: int = 0
    compressed_balance: int = 0
    uncompressed_balance: int = 0


class BlockchainAPI:
    BASE_URL = "https://blockchain.info/balance?active="
    HEADERS = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    @classmethod
    def get_address_info(cls, addresses: Tuple[str, str]) -> Dict[str, Dict]:
        """
        Fetch balance and transaction count for multiple addresses.
        Returns dict with address as key and info as value.
        """
        url = f"{cls.BASE_URL}{addresses[0]}|{addresses[1]}"

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(url, timeout=API_TIMEOUT, headers=cls.HEADERS)
                if response.status_code == 200:
                    return response.json()
                time.sleep(REQUEST_DELAY * (attempt + 1))
            except requests.RequestException:
                if attempt == MAX_RETRIES - 1:
                    return {}
                time.sleep(REQUEST_DELAY * (attempt + 1))
        return {}


class CryptoWallet:
    @staticmethod
    def generate_from_passphrase(passphrase: str) -> WalletInfo:
        """
        Generate wallet information from passphrase.
        Returns WalletInfo object with all necessary data.
        """
        private_key = hashlib.sha256(passphrase.encode('utf-8')).hexdigest()

        pvk = PrivateKey(private_key)
        pub_compressed = pvk.get_public_key(compressed=True)
        pub_uncompressed = pvk.get_public_key(compressed=False)

        return WalletInfo(
            passphrase=passphrase,
            private_key=private_key,
            decimal=str(int(private_key, 16)),
            compressed_address=pub_compressed.get_address(),
            uncompressed_address=pub_uncompressed.get_address()
        )


class WalletScanner:
    def __init__(self, wordlist_file: str):
        self.wordlist_file = wordlist_file
        self.console = Console()
        self.total_scanned = 0
        self.total_found = 0
        self.total_value = 0
        self.session = requests.Session()

    def load_wordlist(self) -> list:
        """Load wordlist from file."""
        try:
            with open(self.wordlist_file, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.console.print(f"[red]Error: File '{self.wordlist_file}' not found.[/red]")
            sys.exit(1)
        except Exception as e:
            self.console.print(f"[red]Error reading file: {e}[/red]")
            sys.exit(1)

    def update_terminal_title(self):
        """Update terminal title with current statistics."""
        sys.stdout.write(
            f"\x1b]2;Scanned:{self.total_scanned} | Found:{self.total_found} | Value:{self.total_value}\x07"
        )
        sys.stdout.flush()

    def format_output(self, prefix: str, info: str, highlight: bool = False) -> str:
        """Format output line with consistent styling."""
        color = "green" if highlight else "cyan"
        stats = f"[white]S:[/white][cyan]{self.total_scanned}[/cyan] [white]F:[/white][cyan]{self.total_found}[/cyan] [white]V:[/white][cyan]{self.total_value}[/cyan]"
        return f"[grey46]MMDRZA.Com [/grey46] {stats}  [{color}]{info}[/{color}]"

    def print_wallet_info(self, wallet: WalletInfo, found: bool = False):
        """Print wallet information with consistent formatting."""
        color = "green" if found else "dark_blue"

        self.console.print(self.format_output(
            color,
            f"[grey66]Pass:[/grey66] [white on {color}]{wallet.passphrase}[/white on {color}]",
            found
        ))

        self.console.print(self.format_output(
            color,
            f"[white]Comp:[/white] {wallet.compressed_address} [white]TXS:[/white][cyan]{wallet.compressed_txs}[/cyan]",
            found
        ))

        self.console.print(self.format_output(
            color,
            f"[white]Unco:[/white] {wallet.uncompressed_address} [white]TXS:[/white][cyan]{wallet.uncompressed_txs}[/cyan]",
            found
        ))

        self.console.print(self.format_output(
            color,
            f"[grey46]Priv:[/grey46] [white]{wallet.private_key}[/white]",
            found
        ))

    def save_found_wallet(self, wallet: WalletInfo, has_balance: bool = False):
        """Save found wallet to appropriate file."""
        filename = "ValueFound.txt" if has_balance else "TxsFound.txt"

        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"Passphrase: {wallet.passphrase}\n")
            f.write(f"Private Key: {wallet.private_key}\n")
            f.write(f"Decimal: {wallet.decimal}\n")
            f.write(f"Compressed: {wallet.compressed_address} | TXS: {wallet.compressed_txs} | Balance: {wallet.compressed_balance}\n")
            f.write(f"Uncompressed: {wallet.uncompressed_address} | TXS: {wallet.uncompressed_txs} | Balance: {wallet.uncompressed_balance}\n")
            f.write(f"{'=' * 50}\n")

    def process_wallet(self, passphrase: str) -> None:
        """Process a single wallet passphrase."""
        wallet = CryptoWallet.generate_from_passphrase(passphrase)

        api_data = BlockchainAPI.get_address_info(
            (wallet.compressed_address, wallet.uncompressed_address)
        )

        if api_data:
            comp_info = api_data.get(wallet.compressed_address, {})
            uncomp_info = api_data.get(wallet.uncompressed_address, {})

            wallet.compressed_txs = comp_info.get('n_tx', 0)
            wallet.uncompressed_txs = uncomp_info.get('n_tx', 0)
            wallet.compressed_balance = comp_info.get('final_balance', 0)
            wallet.uncompressed_balance = uncomp_info.get('final_balance', 0)

        self.total_scanned += 1
        self.update_terminal_title()

        has_transactions = wallet.compressed_txs > 0 or wallet.uncompressed_txs > 0
        has_balance = wallet.compressed_balance > 0 or wallet.uncompressed_balance > 0

        if has_transactions or has_balance:
            self.total_found += 1
            if has_balance:
                self.total_value += 1

            self.print_wallet_info(wallet, found=True)
            self.save_found_wallet(wallet, has_balance)
        else:
            self.print_wallet_info(wallet, found=False)

        time.sleep(REQUEST_DELAY)

    def run(self):
        """Main scanner loop."""
        wordlist = self.load_wordlist()

        if not wordlist:
            self.console.print("[red]Wordlist is empty.[/red]")
            return

        self.console.print(f"[green]Loaded {len(wordlist)} passphrases. Starting scan...[/green]\n")

        try:
            for passphrase in wordlist:
                self.process_wallet(passphrase)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Scan interrupted by user.[/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]Error during scan: {e}[/red]")
        finally:
            self.console.print(f"\n[green]Scan completed. Total: {self.total_scanned} | Found: {self.total_found} | Value: {self.total_value}[/green]")


def main():
    console = Console()
    console.clear()
    console.print(BANNER)

    # if file name not in argv
    argv = sys.argv
    if len(argv) > 1:
        filename = argv[1]
    else:
        console.print("[green]Enter wordlist file path (Example: [bold white]words.txt[/bold white]):[/green]")
        filename = input(" [INPUT] File Path : ").strip()

    # if no filename exit
    # check path is file
    if not Path(filename).is_file():
        console.print(f"[red]File '{filename}' does not exist or is not a file.[/red]")
        sys.exit(1)


    scanner = WalletScanner(filename)
    scanner.run()


if __name__ == "__main__":
    main()
