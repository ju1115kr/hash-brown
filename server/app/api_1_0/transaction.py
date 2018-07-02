# -*- coding: utf-8 -*-
from . import api
import time
from web3 import Web3, HTTPProvider


@api.route('/transaction', methods=['GET'])
def transaction_test():
    web3 = Web3(Web3.HTTPProvider("http://35.234.3.182:8545"))
    web3.personal.unlockAccount(web3.eth.accounts[12], "12341234", 0)
    web3miner.start(2)
    time.sleep(5)
    web3.miner.stop()
    return web3.eth.accounts[12]
