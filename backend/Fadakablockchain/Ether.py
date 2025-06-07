from web3 import Web3
import os

ETH_RPC = os.getenv("ETH_RPC_URL")
PRIVATE_KEY = os.getenv("ETH_PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ETH_ACCOUNT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(ETH_RPC))

@app.post("/blockchain/send", response_model=BlockchainResponse)
async def send_tx(tx: BlockchainTx, user: User = Depends(get_current_user)):
    try:
        nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        tx_dict = {
            'nonce': nonce,
            'to': tx.to_address,
            'value': w3.to_wei(tx.amount, 'ether'),
            'gas': 21000,
            'gasPrice': w3.eth.gas_price,
            'data': tx.data.encode() if tx.data else b'',
        }
        signed_tx = w3.eth.account.sign_transaction(tx_dict, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return BlockchainResponse(tx_hash=tx_hash.hex(), status="submitted")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")
