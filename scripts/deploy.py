from brownie import companyToken, network, accounts, config
import brownie
from scripts.automation_scripts import get_account
from web3 import Web3

initial_supply = 0 
max_fee = 20000000000
priority_fee = 1500000000

# companyNameVault = defaultOperators[0] (Testnet, to be changed to companyName Capital Vault)
# administrator = defaultOperators[1] (delegate of CFO, Testnet)
defaultOperators = ["0x965067c63dc2E70A905367E7915966079Ea5785B", "0x70196d2C1CB073716ddA3987B0aC4D036EA024B0"]
    #companyVault: "0xb1Fc5675094Bd70859425E418fd247B7dc21472A"  
    #adil: "0xEcDA1249Af9498C7486f0b9D6774d75C02D7927a"
    #Janis: "0x965067c63dc2E70A905367E7915966079Ea5785B",
    #Roy: "0x70196d2C1CB073716ddA3987B0aC4D036EA024B0",

def deploySYNtoken(fromWallet):
    account = get_account(fromWallet)
    print("Account retrieved, back in deploy. Deploying contract...")
    synToken = companyToken.deploy(
        initial_supply,
        defaultOperators,
        {"from": account, "max_fee": max_fee, "priority_fee": priority_fee},

    )
    # max fee can not be bigger than priority fee and 9 zeros in order to get 1gwei from wei so 1000000000wei = 1gwei
    if type(synToken) == brownie.network.contract.ProjectContract:
        print("CONGRATULIEREN ! Contract deployed.")
    else:
        print("UH OH ! Something went wrong.")
    return synToken


def main():
    deploySYNtoken("JH")
