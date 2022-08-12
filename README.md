# Company Token Global
This repository contains the smart contract source code for the vested Company Token Global. It uses [Brownie](https://eth-brownie.readthedocs.io/en/stable/index.html) as development framework for compilation, testing and deployment tasks.

## What is the Company Token?
The Company token represents an employee benefits program for Company, a global management consulting company, backed by a pool of cryptocurrency based assets. The token is to be evenly distributed by region to Company employees and holders may redeem tokens with Company for monetary or other rewards. Company retains the right to remove these tokens from individuals according to Company policy. 

## Documentation

The token is implemented as a smart contract on top of the Ethereum blockchain. This smart contract gurantees safety and enforces the rules of participation. The token implements both [ERC20](https://ethereum.org/en/developers/docs/standards/tokens/erc-20/) and [ERC777](https://ethereum.org/en/developers/docs/standards/tokens/erc-777/). Note that the ERC777 "hooks" functionality has been removed but the contract preserves the concept of " default operators". The main contract is split into 3 parts for organisational clarity:

- **coRoles**             (Contract control settings and definition of administrational positions that can be held)
- **coERC777**            (A Company adaptation of the base ERC777 token standard that includes ERC20 functionality)
- **CompanyTokenGlobal**  (Deployment smart contract and Company specific functions)

### Roles

##### defaultOperators
Individuals of delegated power. They can burn and mint Company Tokens in the masterContract. They can also make use of operatorSend() to send Company tokens from holder addresses to the masterContract. Note this is defined as part of ERC777.

##### administrator
0x... -
Set to the CFO, Company. The administrator can pause and unpause the contract, enable and disable whitelisting as well as add and remove defaultOperators. Can send tokens from the masterContract to holders using the sendTokensToIndividualAddress() and sendTokensToMultipleAdddresses().
The administrator is added as a defaultOperator on deployment.

##### masterContract
0x... -
Set to the company vault. The masterContract can update the administrator address as well as updating the address of the masterContract. Can send tokens to holders using the sendTokensToIndividualAddress() and sendTokensToMultipleAddresses().
The masterContract can add and remove defaultOperators and is added as a defaultOperator on deployment.

### Contract Control Settings

##### Paused
A boolean flag controlled by the administrator role which prevents all transfer style functions and preserves the current state of the token holdings.
 It is to be used in the case the vested token contract needs to be terminated and replaced by a new one.

##### whitelistEnabled
A boolean flag controlled by the administrator role which, if not enabled, prevents ERC style peer to peer transfers. If enabled, recipients must be whitelisted.

### Write Methods

The main interactions for token holders will come via the Company requestPayout() function and ERC style functions send(), transfer(), approve(), transferFrom(). ERC style functions are identical to those found in [ERC20](https://ethereum.org/en/developers/docs/standards/tokens/erc-20/) and [ERC777](https://ethereum.org/en/developers/docs/standards/tokens/erc-777/) documentation but with added contract settings restrictions.
Other functions are to be utilised by addresses with assigned roles.

#### User

##### *requestPayout()*
`function requestPayout(uint256 amount, bytes memory data)`

Sends a certain `amount` of tokens to the masterContract. The `data` input can be utilised to include the reason for a payout in order to trigger responses from Company.  "0x0" is standard input. Emits a {Payout} event.

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| amount          | uint256       | amount to send expressed in wei units |
| data            | bytes         | additional data field         |

#### defaultOperator

##### *mintTokensToVault()*
`function mintTokensToVault(uint256 amount)`

This function is called by a defaultOperator in order to mint tokens to the masterContract. Emits a {Payout} event.

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| amount          | uint256       | amount to mint expressed in wei units |


##### *operatorBurn()*
`function operatorBurn(address account, uint256 amount, bytes memory data, bytes memory operatorData)`

This is an overridden ERC777 function and is called by a defaultOperator in order to burn tokens. It can only burn tokens in the masterContract.

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| account         | address       | address from which to burn tokens |
| amount          | uint256       | amount to burn expressed in wei units |
| data            | bytes         | additional data field         |
| operatorData    | bytes         | additional operator data field |

##### *operatorSend()*
`function operatorSend(address sender, addresss recipient, uint256 amount, bytes memory data, bytes memory operatorData)`

This is an overridden ERC777 function and is called by a defaultOperator in order to remove tokens from individuals. It can only send tokens to the masterContract.

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| sender          | address       | address from which to send tokens |
| recipient       | address       | address to receive tokens |
| amount          | uint256       | amount to send expressed in wei units |
| data            | bytes         | additional data field         |
| operatorData    | bytes         | additional operator data field |

##### *whitelistUsers()*
`function whitelistUsers(address[] memory arr)`

This function is called by a defaultOperator in order to whitelist all listed addresses. It works by changing the isWhitelistedAddress flag -> true. It only changes the boolean flag for addresses in the listed input.

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| arr             | address[]     | addresses to whitelist        |

##### *removeFromWhitelist()*
`function removeFromWhitelist(address[] memory arr)`

This function is called by a defaultOperator in order to un-whitelist all listed addresses. It works by changing the isWhitelistedAddress flag -> false. It only changes the boolean flag for addresses in the listed input.

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| arr             | address[]     | addresses to un-whitelist        |

#### administrator

##### *pauseContract()*
`function pauseContract()`

This function is called by the administrator to initiate the Paused contract setting. It can be used to prevent all transfer style functions. It is to be used in the case the vested token contract needs to be terminated and replaced by a new one.
##### *unpauseContract()*
`function unpauseontract()`

This function is called by the administrator to disable the Paused contract setting. It can be used to reactivate transfer style functions. 

##### *activateWhitelist()*
`function activateWhitelist()`

This function is called by the administrator to initiate the whitelistEnabled contract setting. It enables transfers between whitelisted addresses.

##### *deactivateWhitelist()*
`function deactivateWhitelist()`

This function is called by the administrator to disable the whitelistEnabled contract setting. It disables transfers between whitelisted addresses.

#### administrator and masterContract

##### *authorizeOperator()*
`authorizeOperator(address operator)`

This function is called by the masterContract or administrator in order to add an address as a defaultOperator.

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| operator        | address       | address to add as defaultOperator |

##### *revokeOperator()*
`revokeOperator(address operator)`

This function is called by the masterContract or administrator in order to remove an address as a defaultOperator.

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| operator        | address       | address to remove as defaultOperator |

##### *sendTokensToIndividualAddress()*
`function sendTokensToIndividualAddress(address recipient, uint256 amount, bytes memory data)`

This function is called by the masterContract or administrator in order to send tokens to an individual address. This function does not require the whitelistEnabled contract setting to be activated.

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| recipient       | address       | address to receive tokens |
| amount          | uint256       | amount to send expressed in wei units |
| data            | bytes         | additional data field         |

##### *sendTokensToMutipleAddresses()*
`function sendTokensToMultipleAddresses(address[] memory listOfAddresses_ToSend_To, uint256 amountToSend, bytes memory data)`

This function is called by the masterContract or administrator in order to airdrop tokens via batch transfer. The amount must be the same for each recipient listed.

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| listOfAddresses_ToSend_To | address[]       | addresses to receive tokens |
| amountToSend          | uint256       | amount to send expressed in wei units |
| data            | bytes         | additional data field         |

#### masterContract

##### *setAdministrator()*
`function setAdministrator(address administrator_to_set)`

This function is called by the masterContract in order to remove the current adminitrator and add a new one. It also removes the old administrator as a defaultOperator and adds the new administrator as a defaultOperator. 

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| administrator_to_set        | address       | address to set as new administrator |

##### *setMaster()*
`function setMaster(address master_to_set)`

This function is called by the masterContract in order to remove the current masterContract and add a new one. It also removes the old masterContract as a defaultOperator and adds the new masterContract as a defaultOperator. 

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| master_to_set              | address       | address to set as new masterContract |


### Read Methods

[ERC20](https://ethereum.org/en/developers/docs/standards/tokens/erc-20/) read functions can be found in its token standard documentation. They include name(), symbol(), decimals(), totalSupply() and balanceOf().

##### defaultOperators()
`function defaultOperators()`
###### Return Values

| Type          | Description                   |
| ------------- | ----------------------------- |
| address[]     | addresses of defaultOperators |

##### masterContract()
`address public masterContract`
###### Return Values

| Type          | Description                   |
| ------------- | ----------------------------- |
| address       | addresses of the masterContract |

##### administrator()
`address public administrator`
###### Return Values

| Type          | Description                   |
| ------------- | ----------------------------- |
| address       | addresses of the administrator |

##### whitelistEnabled()
`bool public whitelistEnabled`
###### Return Values

| Type          | Description                   |
| ------------- | ----------------------------- |
| bool          | flag to show if the whitelistEnabled control setting is active |

##### isWhitelistedAddress()
`mapping(address => bool) public isWhitelistedAddress`

| Type          | Description                   |
| ------------- | ----------------------------- |
| address       | address to check              |
###### Return Values

| Type          | Description                   |
| ------------- | ----------------------------- |
| bool          | flag to show if address is whitelisted |

### Events

`event Payout (uint256 date, address indexed from, uint256 amount);`

Event can be consumed by APIs in order to trigger responses by Company eg. emails.
Date output is emitted as a timestamp and can be converted to a date using python's datetime.date.fromtimestamp()

### Deployment
Deployment of the smart contract follows the guidelines set in [Brownie](https://eth-brownie.readthedocs.io/en/stable/index.html). The scripts/deploy.py file can deploy the smart contract and initialises the parameters of deployment. Running the following code in the terminal will deploy the smart contract.

`brownie run scripts/deploy.py main(<fromWallet>) --network <network>`

| Parameter Name  | Type          | Description                   |
| --------------- | ------------- | ----------------------------- |
| initial_supply  | uint256       | initial supply of tokens to be minted to the masterContract expressed in wei units |
| max_fee         | uint256       | maximum gas fee for deployment expressed in wei units |
| priority_fee    | uint 256      | gas fee added for transaction priority expressed in wei units |
| defaultOperators[0] | address      | companyName Vault to be set to masterContract |
| defaultOperators[1] | address      | company CFO to be set to administrator |


### Tests

Unit tests of the smart contract are held in the tests/test_unit.py file. They test major functionality of the smart contract. Tests were run on a local fork of the Rinkeby testnet. Running the following code in the terminal will fork your local ganache chain.

`ganache-cli --fork https://rinkeby.infura.io/v3/<ProjectID>`

Running the folllowing code in the terminal will run the unit test file.

`brownie test`




































 
