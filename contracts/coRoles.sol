// SPDX-License-Identifier: MIT
// This contract was designed and deployed by : Someone on behalf of Company.
// This following piece of code complements CompanyTokenGlobal contract. 
// It specifies the roles as well as the on / off function of the overall token contract.

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/Pausable.sol";

contract coRoles is Pausable {
    address public vaultContract;
    address public administrator;
    bool public whitelistEnabled = false;
    mapping(address => bool) public isWhitelistedAddress;

    // This function checks if an address is in an array of addresses and returns "true" if yes, else "false".
    function isInArray(
        address address_to_check, 
        address[] memory target_Array 
    ) internal pure returns (bool)
    {
        for (uint256 x = 0; x < target_Array.length; x++) {
            if (target_Array[x] == address_to_check) {
                return true;
            }
        }
        return false;
    }

    // This function removes an address from an array of addresses.
    function removeAddress(
        address address_to_remove,
        address[] storage target_Array
    ) internal {
        for (uint256 x = 0; x < target_Array.length; x++) {
            if (target_Array[x] == address_to_remove) {
                target_Array[x] = target_Array[target_Array.length - 1];
                target_Array.pop();
                break;
            }
        }
    }

    // The administrator can pause and unpause the contract, enable and disable the whitelisting control settings as well as add and remove defaultOperators.
    // In addition, the administrator is a defaultOperator itself on deployment.
    modifier onlyAdministrator() {
        require(
            _msgSender() == administrator,
            "You are missing a promotion to the board of directors. Only the admin can perform this action!"
        );
        _;
    }

    // The vaultContract can update the administrator address as well as update the address of the vaultContract.
    // In addition, the vaultContract is a defaultOperator itself on deployment.
    modifier onlyVault() {
        require(
            _msgSender() == vaultContract,
            "Getting power hungry? Only the vault contract can perform this action!"
        );
        _;
    }
    
    // This function is called by the administrator to enable transfers between whitelisted addresses.
    function activateWhitelist() public onlyAdministrator
    {
        whitelistEnabled = true;
    }

    // This function is called by the administrator to disable transfers between whitelisted addresses.
    function deactivateWhitelist() public onlyAdministrator {
        whitelistEnabled = false;
    }

    // This function is called by the administrator to pause the contract and preserve the current state of the holdings.
    // It is to be called in case the vested Token contract needs to be updated.
    function pauseContract () public whenNotPaused onlyAdministrator {
        _pause();
    }

    // This function is called by the administrator to unpause the contract.
    function unpauseContract() public whenPaused onlyAdministrator {
        _unpause();
    }
}