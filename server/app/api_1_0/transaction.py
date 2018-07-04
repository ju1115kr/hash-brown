# -*- coding: utf-8 -*-
from . import api
import time
import json
from time import sleep
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

def getStarContract(address = None):
    web3 = Web3(Web3.HTTPProvider("http://35.234.3.182:8545"))
    web3.personal.unlockAccount(web3.eth.accounts[5], "12341234", 0)
    
    
    abi = '[\
    {\
    "constant": true,\
    "inputs": [],\
    "name": "getUserId",\
    "outputs": [\
    {\
    "name": "_targetUserId",\
    "type": "uint8"\
    }\
    ],\
    "payable": false,\
    "stateMutability": "view",\
    "type": "function"\
    },\
    {\
    "constant": true,\
    "inputs": [],\
    "name": "getStars",\
    "outputs": [\
    {\
    "name": "_starCount",\
    "type": "uint8"\
    }\
    ],\
    "payable": false,\
    "stateMutability": "view",\
    "type": "function"\
    },\
    {\
    "inputs": [\
    {\
    "name": "_targetUserId",\
    "type": "uint8"\
    },\
    {\
    "name": "_starCount",\
    "type": "uint8"\
    }\
    ],\
    "payable": true,\
    "stateMutability": "payable",\
    "type": "constructor"\
    }\
    ]'

    bytecode = "60806040818152806101138339810160405280516020909101516000805460ff191660ff9384161761ff001916610100939092169290920217815560ca90819061004990396000f30060806040526004361060485763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416632ebcb6538114604d578063b3a21849146075575b600080fd5b348015605857600080fd5b50605f6087565b6040805160ff9092168252519081900360200190f35b348015608057600080fd5b50605f6090565b60005460ff1690565b600054610100900460ff16905600a165627a7a723058206d7e0a86624805f441c66b25adc4f1077dd64f1e294a5b0ed79ce8293e2339680029"
    # Instantiate and deploy contract
    
    if address != None:
        contract = web3.eth.contract(address = address,abi=abi, bytecode=bytecode)
    else :
        contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    return web3,contract

@api.route('/transaction/star/<string:address>', methods=['GET'])
def GetTransactionStar(address):
    web3,contract = getStarContract(address)
    return str(contract.call().getStars())

@api.route('/transaction/star/<int:targetID>/<int:likeCount>/', methods=['GET'])
def SettransactionStar(targetID,likeCount):
    web3,contract = getStarContract()
    # Get transaction hash from deployed contract
    tx_hash = contract.deploy(args= [targetID,likeCount],transaction={'from': web3.eth.accounts[5], 'gas': 2900000})
    
    while web3.eth.getTransactionReceipt(tx_hash) is None :
        sleep(1)
    
    tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
    contract_address = tx_receipt['contractAddress']

    return contract_address

#abi = contract_interface['abi']
#contract_instance = w3.eth.contract(address=contract_address, abi=abi,ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object
#print('Contract value: {}'.format(contract_instance.greet()))
#contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[5]})
#print('Setting value to: Nihao')
#print('Contract value: {}'.format(contract_instance.greet()))