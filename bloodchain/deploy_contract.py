from web3 import Web3
import json

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))
chain_id = 1337  # Ganache local chain ID

# Replace with your Ganache account
my_address = "0x5240932Fb6A7C8Fb136a8A0ad0f95F372053804b"
private_key = "0xe7674697d7744931d65135bf3993f09dc1cc8261e3ec3b5fef6a476b62597a60"  # NEVER expose this in production

# Load ABI and Bytecode
with open("donor_abi.json", "r") as f:
    abi = json.load(f)

with open("donor_bytecode.txt", "r") as f:
    bytecode = f.read()

# Create the contract in Python
DonorStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Build the transaction
nonce = w3.eth.get_transaction_count(my_address)
transaction = DonorStorage.constructor().build_transaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce,
    "gas": 3000000,
    "gasPrice": w3.to_wei("20", "gwei")
})

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
print(f"[⏳] Deploying contract... Tx Hash: {tx_hash.hex()}")

# Wait for the transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print(f"[✅] Contract deployed at address: {contract_address}")

# Save contract address for later use
with open("deployed_contract_address.txt", "w") as f:
    f.write(contract_address)
