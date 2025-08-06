from web3 import Web3
import sqlite3
import json

# Connect to Ganache (or Infura if using live network)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Change if needed
w3.eth.default_account = w3.eth.accounts[0]

# Load contract ABI and address
with open('donor_abi.json') as f:
    abi = json.load(f)

contract_address = '0xdbdE54eb04c0fFCf1984AB992013e7C1e7cb20bd'  # Replace with your deployed contract address
contract = w3.eth.contract(address=contract_address, abi=abi)

# Connect to SQLite DB
conn = sqlite3.connect('donor_data.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM donors")
rows = cursor.fetchall()

for row in rows:
    donor_id, name, blood_group, gender, age, timestamp = row
    tx_hash = contract.functions.registerDonor(
        donor_id, name, blood_group, gender, age, timestamp
    ).transact()
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Uploaded donor {name} to blockchain.")

conn.close()
