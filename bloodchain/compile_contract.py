from solcx import compile_standard, install_solc
import json
import os

# Step 1: Install Solidity compiler version
install_solc('0.8.0')

# Step 2: Read the contract source code
with open("DonorStorage.sol", "r") as file:
    contract_source = file.read()

# Step 3: Compile the contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "DonorStorage.sol": {
                "content": contract_source
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.8.0"
)

# Step 4: Save ABI and Bytecode
with open("compiled_donor_contract.json", "w") as file:
    json.dump(compiled_sol, file)

abi = compiled_sol['contracts']['DonorStorage.sol']['DonorStorage']['abi']
bytecode = compiled_sol['contracts']['DonorStorage.sol']['DonorStorage']['evm']['bytecode']['object']

with open("donor_abi.json", "w") as f:
    json.dump(abi, f)

with open("donor_bytecode.txt", "w") as f:
    f.write(bytecode)

print("[✓] Compilation complete. ABI and Bytecode saved to donor_abi.json and donor_bytecode.txt")

