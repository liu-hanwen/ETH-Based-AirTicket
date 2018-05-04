import json
import web3
import os
import subprocess
from web3 import Web3, TestRPCProvider, HTTPProvider
# from solc import compile_source
from web3.contract import ConciseContract

def compile_source(src):
    print('Start to compile source...')
    filename = '/tmp/' + str(hash(src))
    files_before = subprocess.check_output('ls').decode('utf8').split('\n')
    with open(filename, 'w') as f:
        f.write(src)
    subprocess.check_call("solcjs --abi --bin %s \n exit 0" % filename, shell=True)
    ret = {}

    files_after = subprocess.check_output('ls').decode('utf8').split('\n')
    files_same = set(files_before) & set(files_after)

    targets = [file for file in files_after if file not in files_same]
    for target in targets:
        if '.abi' == target[-4:]:
            with open(target, 'r') as f:
                ret['abi'] = json.load(f)
        elif '.bin' == target[-4:]:
            with open(target, 'r') as f:
                ret['bin'] = f.read()
    print('Compiled!\nThe return is:\n' , ret)
    return ret


# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.0;

contract Greeter {
    string public greeting;

    function Greeter() {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() constant returns (string) {
        return greeting;
    }
}
'''


# web3.py instance
w3 = Web3(HTTPProvider('http://localhost:8545'))

contract_interface = compile_source(contract_source_code)
# with open('Greeter_sol_Greeter.abi', 'r') as f:
#     contract_interface['abi'] = json.load(f)

# with open('Greeter_sol_Greeter.bin', 'r') as f:
#     contract_interface['bin'] = f.read()

# Instantiate and deploy contract

contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0]})

# Get tx receipt to get contract address
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']

# Contract instance in concise mode
contract_instance = w3.eth.contract(abi=contract_interface['abi'], address=contract_address, ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object
print('Contract value: {}'.format(contract_instance.greet()))
contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[0]})
print('Setting value to: Nihao')
print('Contract value: {}'.format(contract_instance.greet()))