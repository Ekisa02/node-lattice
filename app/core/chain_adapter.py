from web3 import Web3
from ..config import settings

class ChainAdapter:
    def __init__(self, provider: str = None):
        self.provider = provider or settings.WEB3_HTTP_PROVIDER
        self.w3 = Web3(Web3.HTTPProvider(self.provider))

    def get_transaction(self, tx_hash: str) -> dict:
        tx = self.w3.eth.get_transaction(tx_hash)
        # convert HexBytes to str where needed
        return {
            'hash': tx_hash,
            'from': tx['from'],
            'to': tx['to'],
            'value': tx['value'],
            'gas': tx['gas'],
            'input': tx['input'] if 'input' in tx else None,
            'nonce': tx['nonce'],
        }
