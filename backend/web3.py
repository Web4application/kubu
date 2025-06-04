from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://your-node-url'))

contract_address = '0xYourContractAddress'
abi = [...]  # ABI from compiled contract

contract = w3.eth.contract(address=contract_address, abi=abi)
account = w3.eth.account.privateKeyToAccount('YOUR_PRIVATE_KEY')

def log_anomaly_to_chain(metric: str, value: float):
    tx = contract.functions.logAnomaly(metric, int(value)).buildTransaction({
        'from': account.address,
        'nonce': w3.eth.getTransactionCount(account.address),
        'gas': 200000,
        'gasPrice': w3.toWei('50', 'gwei')
    })
    signed_tx = account.signTransaction(tx)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash.hex()
