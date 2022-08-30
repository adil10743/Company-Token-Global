from scripts.deploy import max_fee, priority_fee
from scripts.automation_scripts import get_account

gas_limit = 100000
allow_revert = 1

def pauseContract(fromWallet, sc):
    if not sc.paused():
        account = get_account(fromWallet)
        sc.pauseContract({"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})
        print("Contract paused")
    else:
        print("Contract was already paused")

def unpauseContract(fromWallet, sc):
    if sc.paused():
        account = get_account(fromWallet)
        sc.unpauseContract({"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})
        print("Contract unpaused")
    else:
        print("Contract was already unpaused")

def activateWhitelist(fromWallet, sc):
    if not sc.whitelistEnabled():
        account = get_account(fromWallet)
        sc.activateWhitelist({"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})
        print("Whitelist enabled")
    else: 
        print("Whitelist was already enabled")

def deactivateWhitelist(fromWallet, sc):
    if sc.whitelistEnabled():
        account = get_account(fromWallet)
        sc.deactivateWhitelist({"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})
        print("Whitelist disabled")
    else: 
        print("Whitelist was already disabled")

def authorizeOperator(address, fromWallet, sc):
    account = get_account(fromWallet)
    sc.authorizeOperator(address, {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})

def revokeOperator(address, fromWallet, sc):
    account = get_account(fromWallet)
    sc.revokeOperator(address, {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})

def setAdmin(address, fromWallet, sc):
    account = get_account(fromWallet)
    sc.setAdministrator(address, {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})
    print("admin: ", address)

def setVault(address, fromWallet, sc):
    account = get_account(fromWallet)
    sc.setVault(address, {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})
    print("Vault: ", address)

def sendTokensToIndividualAddress(recipient, amount, fromWallet, sc):
    account = get_account(fromWallet)
    sc.sendTokensToIndividualAddress(recipient, amount, "", {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})

def sendTokensToMultipleAddresses(listOfAddresses_To_Send_To, amountToSend, fromWallet, sc):
    account = get_account(fromWallet)
    sc.sendTokensToMultipleAddresses(listOfAddresses_To_Send_To, amountToSend, "", {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})

def operatorSend(sender, recipient, amount, fromWallet, sc):
    account = get_account(fromWallet)
    operatorSend_tx = sc.operatorSend(sender, recipient, amount, "", "", {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})
    return operatorSend_tx

def operatorBurn(burnAccount, amount, fromWallet, sc):
    account = get_account(fromWallet)
    sc.operatorBurn(burnAccount, amount, "", "", {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})

def requestPayout(amount, data, fromWallet, sc):
    account = get_account(fromWallet)
    requestPayout_tx = sc.requestPayout(amount, data, {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})
    return requestPayout_tx

def mintTokensToVault(amount, fromWallet, sc):
    account = get_account(fromWallet)
    sc.mintTokensToVault(amount, {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})

def whitelistUsers(addresses, fromWallet, sc):
    account = get_account(fromWallet)
    sc.whitelistUsers(addresses, {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})

def removeFromWhitelist(addresses, fromWallet, sc):
    account = get_account(fromWallet)
    removeFromWhitelist_tx = sc.removeFromWhitelist(addresses, {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})
    return removeFromWhitelist_tx
    
def send(recipient, amount, fromWallet, sc):
    account = get_account(fromWallet)
    sc.send(recipient, amount, "", {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})

def transfer(recipient, amount, fromWallet, sc):
    account = get_account(fromWallet)
    sc.transfer(recipient, amount, {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})

def transferFrom(holder, recipient, amount, fromWallet, sc):
    account = get_account(fromWallet)
    sc.transferFrom(holder, recipient, amount, {"from": account, "max_fee": max_fee, "priority_fee": priority_fee, "gas_limit": gas_limit, "allow_revert": allow_revert})















