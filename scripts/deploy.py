from brownie import companyToken
import brownie
from scripts.automation_scripts import get_account
from web3 import Web3

initial_supply = 0 
max_fee = 20000000000
priority_fee = 1500000000

# companyNameVault = defaultOperators[0] (Testnet, to be changed to companyName Capital Vault)
# administrator = defaultOperators[1] (delegate of CFO, Testnet)
defaultOperators = ["0x...", "0x..."] 

def deployCTKtoken(fromWallet):
    account = get_account(fromWallet)
    print("Account retrieved, back in deploy. Deploying contract...")
    coToken = companyToken.deploy(
        initial_supply,
        defaultOperators,
        {"from": account, "max_fee": max_fee, "priority_fee": priority_fee},

    )
    # max fee can not be bigger than priority fee and 9 zeros in order to get 1gwei from wei so 1000000000wei = 1gwei
    if type(coToken) == brownie.network.contract.ProjectContract:
        print("CONGRATULIEREN ! Contract deployed.")
    else:
        print("UH OH ! Something went wrong.")
    return coToken


def main():
    deployCTKtoken("Company")
