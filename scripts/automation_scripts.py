from brownie import network, accounts, config

def get_account(Name):
    return accounts.add(config["wallets"][Name]["from_key"])
