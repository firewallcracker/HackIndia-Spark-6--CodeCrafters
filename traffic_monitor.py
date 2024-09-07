# traffic_monitor.py
from web3 import Web3

def monitor_blockchain_traffic():
    # Connect to an Ethereum node
    infura_url = "https://mainnet.infura.io/v3/2a800c8474b544c28da72d77213ed2b1"
    web3 = Web3(Web3.HTTPProvider(infura_url))

    if not web3.is_connected():
        return {"error": "Failed to connect to the Ethereum network"}

    latest_block = web3.eth.get_block('latest')
    block_details = {
        "block_number": latest_block.number,
        "transactions": []
    }

    for tx_hash in latest_block.transactions:
        tx = web3.eth.get_transaction(tx_hash)
        tx_details = {
            "hash": tx_hash.hex(),
            "from": tx['from'],
            "to": tx.get('to'),
            "value": web3.from_wei(tx['value'], 'ether'),
            "gas": tx['gas']
        }
        block_details["transactions"].append(tx_details)

    return block_details



if __name__ == "__main__":
    result = monitor_blockchain_traffic()
    print(result)

