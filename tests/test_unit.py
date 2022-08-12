import pytest
from brownie import network, accounts
from scripts.deploy import initial_supply, defaultOperators, deploySYNtoken
from scripts.automation_scripts import get_account
from scripts.contractFunctions import *
from web3 import Web3

# ganache-cli --fork https://rinkeby.infura.io/v3/9a683af859ec496e9cad16fbd65e61b1

@pytest.fixture
def sc():
    return deploySYNtoken("VR")

#Fund accouts
def test_FundMe():
    if network.show_active() == "development":
        accounts[0].transfer(get_account("JH"), "5 ether")
        accounts[1].transfer(get_account("RH"), "5 ether")
        accounts[2].transfer(get_account("AA"), "5 ether")
        accounts[3].transfer(get_account("VR"), "5 ether")
    else:
        pytest.skip("only for local testing")

# Checks state of smart contract on deployment
def test_DeploymentState(sc):
    errors = []
    
    if not sc.vaultContract() == defaultOperators[0]:
        errors.append("vaultContract was not set correctly on deployment")
    if not sc.administrator() == defaultOperators[1]:
        errors.append("administrator was not set correctly on deployment")
    if not sc.defaultOperators() == defaultOperators:
        errors.append("defaultOperators were not set correctly on deployment")
    if not sc.totalSupply() == initial_supply:
        errors.append("total supply was not set correctly on deployment")
    if not sc.balanceOf(sc.vaultContract()) == initial_supply:
        errors.append("initial supply was not set correctly on deployment")
    if sc.paused():
        errors.append("paused flag should be false on deployment")
    if sc.whitelistEnabled():
        errors.append("whitelistEnabled flag should be false on deployment")

    # assert no error message has been registered
    assert not errors


# Mint tokens to Vault
def test_MintTokens(sc):
    tokens_to_add = Web3.toWei(1000, "ether")

    if network.show_active() == "development":
        with brownie.reverts("Money printer for the Fed goes brrrr, but not for you. You are not an operator."):
            mintTokensToVault(tokens_to_add,"AA", sc)

    mintTokensToVault(tokens_to_add,"RH", sc)
    assert sc.balanceOf(sc.vaultContract()) == initial_supply + tokens_to_add, "tokens were not minted to the vault correctly"

    mintTokensToVault(tokens_to_add,"JH", sc)
    assert sc.balanceOf(sc.vaultContract()) == initial_supply + 2 * tokens_to_add, "tokens were not minted to the vault correctly"
    assert sc.totalSupply() == initial_supply + 2 * tokens_to_add, "Incorrect total supply"


# Send tokens to individual wallets
def test_vaultContractSendIndividual(sc):
    amount_to_send = Web3.toWei(1000, "ether")

    if network.show_active() == "development":
        with brownie.reverts("Sneaky, but not smart. Only the admin or vault can perform this action!"):
            sendTokensToIndividualAddress(get_account("RH"), amount_to_send, "AA", sc)   
        
    sendTokensToIndividualAddress(get_account("AA"), amount_to_send, "RH", sc)
    assert sc.balanceOf(sc.vaultContract()) == sc.totalSupply() - amount_to_send, "Incorrect balance of vaultContract"
    assert sc.balanceOf(get_account("AA")) == amount_to_send, "Incorrect balance of recipient"
    
    sendTokensToIndividualAddress(get_account("AA"), amount_to_send, "JH", sc)
    assert sc.balanceOf(sc.vaultContract()) == sc.totalSupply() - 2 * amount_to_send, "Incorrect balance of vaultContract"
    assert sc.balanceOf(get_account("AA")) == 2 * amount_to_send, "Incorrect balance of recipient"


# Send tokens to multiple addresses
def test_vaultContractSendMultiple(sc):

    if network.show_active() == "development":
        with brownie.reverts("Sneaky, but not smart. Only the admin or vault can perform this action!"):
            sendTokensToMultipleAddresses([get_account("RH"), get_account("JH")], brownie.convert.to_uint(sc.totalSupply()/4), "AA", sc)
    
        with brownie.reverts("Insufficient tokens"):
            sendTokensToMultipleAddresses([get_account("RH"), get_account("AA")], brownie.convert.to_uint(sc.totalSupply()/2) + 1, "JH", sc)

    sendTokensToMultipleAddresses([get_account("RH"), get_account("AA")], brownie.convert.to_uint(sc.totalSupply()/4), "RH", sc)
    assert sc.balanceOf(sc.vaultContract()) == brownie.convert.to_uint(sc.totalSupply()/2)
    assert sc.balanceOf(get_account("RH")) == brownie.convert.to_uint(sc.totalSupply()/4)
    assert sc.balanceOf(get_account("AA")) == brownie.convert.to_uint(sc.totalSupply()/4)

    sendTokensToMultipleAddresses([get_account("RH"), get_account("AA")], brownie.convert.to_uint(sc.totalSupply()/4), "JH", sc)
    assert sc.balanceOf(sc.vaultContract()) == 0
    assert sc.balanceOf(get_account("RH")) == brownie.convert.to_uint(sc.totalSupply()/2)
    assert sc.balanceOf(get_account("AA")) == brownie.convert.to_uint(sc.totalSupply()/2)


# Request Payout
def test_RequestPayout(sc):
    amount_to_send = Web3.toWei(1000, "ether")

    sendTokensToIndividualAddress(get_account("AA"), amount_to_send, "JH", sc)
    requestPayout_tx = requestPayout(amount_to_send, "", "AA", sc)
    assert requestPayout_tx.events["Payout"]["from"] == get_account("AA")
    assert requestPayout_tx.events["Payout"]["amount"] == amount_to_send


# Operator Send
def test_OperatorSend(sc):
    amount_to_send = Web3.toWei(1000, "ether")
    sendTokensToIndividualAddress(get_account("AA"), amount_to_send, "JH", sc)

    if network.show_active() == "development":
        with brownie.reverts("You are not the boss of me. You are not the boss of anyone. Only an operator can move funds."):
            operatorSend(get_account("AA"), sc.vaultContract(), amount_to_send, "AA", sc)
    
        with brownie.reverts("Watch yourself! An operator can only send tokens to the vaultContract."):
            operatorSend(get_account("AA"), get_account("RH"), amount_to_send, "RH", sc)

    operatorSend_tx = operatorSend(get_account("AA"), sc.vaultContract(), amount_to_send, "RH", sc)
    assert sc.balanceOf(sc.vaultContract()) == sc.totalSupply(), "Incorrect balance of vaultContract"
    assert sc.balanceOf(get_account("AA")) == 0, "Incorrect balance of holder"
    assert operatorSend_tx.events["Payout"]["from"] == get_account("AA")
    assert operatorSend_tx.events["Payout"]["amount"] == amount_to_send


# Operator Burn
def test_OperatorBurn(sc):
    amount_to_burn = Web3.toWei(1000, "ether")

    if network.show_active() == "development":
        with brownie.reverts("M.C. Hammer: Duh da ra-duh duh-da duh-da, Cant Touch This. You are not an operator."):
            operatorBurn(sc.vaultContract(), amount_to_burn, "AA", sc)
    
        with brownie.reverts("Trying to be mean? An operator can only burn tokens in the vaultContract."):
            operatorBurn(get_account("AA"), amount_to_burn, "RH", sc)

    operatorBurn(sc.vaultContract(), amount_to_burn, "RH", sc)
    assert sc.balanceOf(sc.vaultContract()) == initial_supply - amount_to_burn, "Incorrect balance of vaultContract"
    assert sc.totalSupply() == initial_supply - amount_to_burn, "Incorrect total supply"


# Pause contract
def test_PauseContract(sc):
    amount_to_send = Web3.toWei(1000, "ether")

    if network.show_active() == "development":
        with brownie.reverts("You are missing a promotion to the board of directors. Only the admin can perform this action!"):
            pauseContract("JH", sc)

        with brownie.reverts("You are missing a promotion to the board of directors. Only the admin can perform this action!"):
            pauseContract("AA", sc)

    pauseContract("RH", sc)
    assert sc.paused(), "pause flag should be true"

    if network.show_active() == "development":
        with brownie.reverts("Pausable: paused"):
            sendTokensToIndividualAddress(get_account("AA"), amount_to_send, "JH", sc)
    
        with brownie.reverts("Pausable: paused"):
            sendTokensToMultipleAddresses([get_account("AA")], amount_to_send, "JH", sc)

        with brownie.reverts("Pausable: paused"):
            send(get_account("AA"), amount_to_send, "JH", sc)

        with brownie.reverts("Pausable: paused"):
            transfer(get_account("AA"), amount_to_send, "JH", sc)
    
        with brownie.reverts("Pausable: paused"):
            mintTokensToVault(amount_to_send, "JH", sc)

        with brownie.reverts("Pausable: paused"):
            operatorBurn(sc.vaultContract(), amount_to_send, "JH", sc)

        with brownie.reverts("Pausable: paused"):
            operatorSend(get_account("AA"), sc.vaultContract(), amount_to_send, "JH", sc)
        
        with brownie.reverts("Pausable: paused"):
            requestPayout(amount_to_send, "", "AA", sc)

        with brownie.reverts("You are missing a promotion to the board of directors. Only the admin can perform this action!"):
            unpauseContract("JH", sc)

        with brownie.reverts("You are missing a promotion to the board of directors. Only the admin can perform this action!"):
            unpauseContract("AA", sc)

    unpauseContract("RH", sc)
    assert not sc.paused(), "paused flag should be false"

    sendTokensToIndividualAddress(get_account("AA"), amount_to_send, "JH", sc)
    assert sc.balanceOf(sc.vaultContract()) == sc.totalSupply() - amount_to_send, "Incorrect balance of vaultContract"
    assert sc.balanceOf(get_account("AA")) == amount_to_send, "Incorrect balance of recipient"


# Whitelist tests
def test_Whitelist(sc):
    amount_to_send = Web3.toWei(1000, "ether")

    sendTokensToIndividualAddress(get_account("AA"), amount_to_send, "JH", sc)
    
    if network.show_active() == "development":
        with brownie.reverts("Nice try, but user transfers are not enabled."):
            send(get_account("RH"), amount_to_send, "AA", sc)

        with brownie.reverts("Nice try, but user transfers are not enabled."):
            transfer(get_account("RH"), amount_to_send, "AA", sc)
    
        with brownie.reverts("You are missing a promotion to the board of directors. Only the admin can perform this action!"):
            activateWhitelist("AA", sc)
    
    activateWhitelist("RH", sc)
    assert sc.whitelistEnabled(), "whitelistEnabled flag should be true"

    if network.show_active() == "development":
        with brownie.reverts("Oops, the recipient is not a whitelisted address."):
            send(get_account("RH"), amount_to_send/2, "AA", sc)

        with brownie.reverts("Oops, the recipient is not a whitelisted address."):
            transfer(get_account("RH"), amount_to_send/2, "AA", sc)
    
        with brownie.reverts("Gotta ask the host before you add +1s. You are not an operator."):
            whitelistUsers([get_account("RH"), get_account("AA")], "AA", sc)

    whitelistUsers([get_account("RH"), get_account("AA")], "RH", sc)
    assert sc.isWhitelistedAddress(get_account("RH"))
    assert sc.isWhitelistedAddress(get_account("AA"))

    send(get_account("RH"), amount_to_send/2, "AA", sc)
    transfer(get_account("RH"), amount_to_send/2, "AA", sc)
    assert sc.balanceOf(get_account("AA")) == 0, "Incorrect balance of holder 1"
    assert sc.balanceOf(get_account("RH")) == amount_to_send, "Incorrect balance of holder 2"

    if network.show_active() == "development":
        with brownie.reverts("Do you not like them? Host your own party if you want to kick them out. You are not an operator."):
            removeFromWhitelist([get_account("RH"), get_account("AA")], "AA", sc)
    
    removeFromWhitelist_tx = removeFromWhitelist([get_account("AA")], "RH", sc)
    assert sc.isWhitelistedAddress(get_account("RH"))
    assert not sc.isWhitelistedAddress(get_account("AA"))
    assert len(removeFromWhitelist_tx.events) == 0

    if network.show_active() == "development":
        with brownie.reverts("Oops, the recipient is not a whitelisted address."):
            send(get_account("AA"), amount_to_send/2, "RH", sc)

        with brownie.reverts("Oops, the recipient is not a whitelisted address."):
            transfer(get_account("AA"), amount_to_send/2, "RH", sc)

    assert sc.balanceOf(get_account("RH")) == amount_to_send, "Incorrect balance of holder"
    removeFromWhitelist_tx = removeFromWhitelist([get_account("RH")], "RH", sc)
    assert sc.balanceOf(get_account("RH")) == 0, "Incorrect balance of holder"
    assert sc.balanceOf(sc.vaultContract()) == initial_supply, "Incorrect balance of vaultContract"
    assert removeFromWhitelist_tx.events["Payout"]["from"] == get_account("RH")
    assert removeFromWhitelist_tx.events["Payout"]["amount"] == amount_to_send

    if network.show_active() == "development":
        with brownie.reverts("You are missing a promotion to the board of directors. Only the admin can perform this action!"):
            deactivateWhitelist("AA", sc)

        with brownie.reverts("You are missing a promotion to the board of directors. Only the admin can perform this action!"):
            deactivateWhitelist("JH", sc)
    
    deactivateWhitelist("RH", sc)
    assert not sc.whitelistEnabled(), "whitelistEnabled flag should be false"

    if network.show_active() == "development":
        with brownie.reverts("Nice try, but user transfers are not enabled."):
            send(get_account("AA"), amount_to_send, "RH", sc)
    
        with brownie.reverts("Nice try, but user transfers are not enabled."):
            transfer(get_account("AA"), amount_to_send, "RH", sc)
    

# defaultOperators
def test_DefaultOperators(sc):
    assert not sc.isOperatorFor(get_account("AA"), get_account("AA"))

    if network.show_active() == "development":
        with brownie.reverts("With great power comes great responsibility. You have neither. Only the admin or vault can do this!"):
            authorizeOperator(get_account("AA"), "AA", sc)

    authorizeOperator(get_account("AA"), "RH", sc)
    assert sc.isOperatorFor(get_account("AA"), get_account("AA"))

    if network.show_active() == "development":
        with brownie.reverts("Tut, tut. You cannot take powers you do not even have yourself. Only the admin or vault can do this!"):
            revokeOperator(get_account("AA"), "AA", sc)

    revokeOperator(get_account("AA"), "RH", sc)
    assert not sc.isOperatorFor(get_account("AA"), get_account("AA"))

    revokeOperator(get_account("RH"), "JH", sc)
    assert not sc.isOperatorFor(get_account("RH"), get_account("AA"))

    authorizeOperator(get_account("RH"), "JH", sc)
    assert sc.isOperatorFor(get_account("RH"), get_account("AA"))

# change Adminsitrator
def test_ChangeAdminstrator(sc):
    assert sc.administrator() == get_account("RH")

    if network.show_active() == "development":
        with brownie.reverts("Getting power hungry? Only the vault contract can perform this action!"):
            setAdmin(get_account("AA"), "AA", sc)

        with brownie.reverts("Getting power hungry? Only the vault contract can perform this action!"):
            setAdmin(get_account("AA"), "RH", sc)

    setAdmin(get_account("AA"), "JH", sc)
    assert sc.administrator() == get_account("AA")


# change vault
def test_ChangeVault(sc):
    assert sc.vaultContract() == get_account("JH")

    if network.show_active() == "development":
        with brownie.reverts("Getting power hungry? Only the vault contract can perform this action!"):
            setVault(get_account("AA"), "AA", sc)

        with brownie.reverts("Getting power hungry? Only the vault contract can perform this action!"):
            setVault(get_account("AA"), "RH", sc)

    setVault(get_account("AA"), "JH", sc)
    assert sc.vaultContract() == get_account("AA")
    



def main():
    test_DeploymentState(sc)
    test_MintTokens(sc)
    test_vaultContractSendIndividual(sc)
    test_vaultContractSendMultiple(sc)
    test_RequestPayout(sc)
    test_OperatorSend(sc)
    test_OperatorBurn(sc)
    test_PauseContract(sc)
    test_Whitelist(sc)
    test_DefaultOperators(sc)
    test_ChangeAdminstrator(sc)
    test_ChangeVault(sc)




    
    
    








