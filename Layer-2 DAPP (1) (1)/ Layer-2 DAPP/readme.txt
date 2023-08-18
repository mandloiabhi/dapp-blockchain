CS765: Introduction of Blockchains, Cryptocurrencies, and Smart Contracts 

Project part 3: Building a layer-2 DAPP on top of Blockchain

Group Members:
Darshit Gandhi (22M0824)
Abhijeet Singh (22M0749)
Niteen Pawar (22M0800)



1. Compiling and running the code :
	i) ganache-cli
	ii) start new terminal
	iii) truffle compile
	iv) truffle migrate
	v) python3 client.py <contract_address>


2. The program will simulate for 100 nodes and 1000 transactions and for each 100 transactions number of successfull txn's will be calculated. At the end of simulation graph of successfull txn vs total txn will be printed.


Files:
1. client.py: Contains the code for making a scale-free network for 100 nodes using power-law distribution and barbarsi-albert algoirthm. It also contains the code to fire transactions, with balance between 2 nodes calculated using exponential distribution. It also contains the code to draw the final graph between total number of transactions and the ratio of successful transactions by total transactions.

2. payment.sol: Contains the whole logic in solidity for creating account, transferring money between these accounts and also for deletion of account.

