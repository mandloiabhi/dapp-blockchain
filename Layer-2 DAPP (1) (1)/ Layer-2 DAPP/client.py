import json
import random
import sys
import networkx as nx
import random
import secrets
import matplotlib.pyplot as plt
# import check_deg_seq as cds
import numpy as np
import build1 
from scipy.stats import expon
from web3 import Web3
from scipy.sparse import csr_matrix
from powerlaw import Power_Law as powerlaw
from collections import deque


def dfs(node, adj_list, visited):
    # Add the current node to the set of visited nodes
    visited.add(node)
    # Recursively visit all neighbors of the current node
    for neighbor in adj_list[node]:
        if neighbor not in visited:
            dfs(neighbor, adj_list, visited)

def bfs(graph, start, end):
    queue = deque([[start]])
    visited = set()
    path = []
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == end:
            return path
        elif node not in visited:
            visited.add(node)
            for adjacent_node, connected in enumerate(graph[node]):
                if connected and adjacent_node not in visited:
                    new_path = path + [adjacent_node]
                    queue.append(new_path)

def is_connected(adj_list):
    # Initialize a set to keep track of visited nodes
    visited = set()
    # Perform depth-first search from an arbitrary node
    dfs(0, adj_list, visited)
    # Check if all nodes were visited
    return len(visited) == len(adj_list)
#connect to the local ethereum blockchain
provider = Web3.HTTPProvider('http://127.0.0.1:8545')
w3 = Web3(provider)
#check if ethereum is connected
print(w3.is_connected())

#replace the address with your contract address (!very important)
deployed_contract_address = '0x1789Fa30eb9B1b807C4202d1B618aaA0aC7E46Fc'
deployed_contract_address = sys.argv[1]
#path of the contract json file. edit it with your contract json file
compiled_contract_path ="build/contracts/Payment.json"
#compiled_contract_path="/home/abhijeet/Desktop/HW3/2_deploy_contracts.js"
with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']
contract = w3.eth.contract(address = deployed_contract_address, abi = contract_abi)



'''
#Calling a contract function createAcc(uint,uint,uint)
txn_receipt = contract.functions.createAcc(1, 2, 5).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':24096380000000})
txn_receipt_json = json.loads(w3.to_json(txn_receipt))
print(txn_receipt_json) # print transaction hash

# print block info that has the transaction)
print(w3.eth.get_transaction(txn_receipt_json)) 

#Call a read only contract function by replacing transact() with call()

'''
y="abhiakjflja"





#-----------------------code to generate graph according to power law degree distribution--------------------------

alpha = 2.5 # parameter of the power-law dist
participants = 100  # no. of nodes in the network
dist = []  # degree distribution from powerlaw


# generate a valid power law distribution, valid means the degree of each node belongs to [1, participants)
while True:
    dist = powerlaw(xmin=1, parameters=[alpha]).generate_random(
        participants)  # generate the distribution
    dist = [round(val) for val in dist]

    if all([val > 0 and val < participants for val in dist]):
        break  # valid dist

adj_list = []

print(dist)
# generate the adjacency list
while True:
    adj_list = [[] for _ in range(participants)]

    for node in range(participants):
        possible_neigh = [_ for _ in range(participants)]

        while len(adj_list[node]) < dist[node]:
            random_node = secrets.choice(possible_neigh)

            if random_node != node and random_node not in adj_list[node]:
                adj_list[node].append(random_node)
                adj_list[random_node].append(node)
            else:
                possible_neigh.remove(random_node)

    if is_connected(adj_list):
        break

A1=[]
for i in range(100):
    temp_list=[]
    for j in range(100):
        if j in adj_list[i]:
            temp_list.append(1)
        else:
            temp_list.append(0)
    A1.append(temp_list)            

#---------------------------code for regestering user -----------------------------------------
for i in range(100): # registering 100 user starting id 0 to ending id is 99
    x=contract.functions.registerUser(i,"abhijeet").transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
    # print("user creation ",i)
m=0

joint_matrix=[] # matrix to store join_account information
for i in range(100):
    temp_list1=[]
    for j in range(100):
        temp_list1.append(0)
    joint_matrix.append(temp_list1)    
#--------------------------------------code to create account _---------------------------------------------------       
for i in range(100):
    temp_list=[]
    for j in range(100):
        #temp_list.append(0)
        if A1[i][j]==1 and i<=j:
            
            
            k=np.random.exponential(10, 1)
            # k=int(k[0])
            k1=int(k[0]/2)
            x=contract.functions.createAcc(i,j,k1).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
            joint_matrix[i][j]=k1
            joint_matrix[j][i]=k1
            
           
        
     
n=0 # number of txn that are unsuccessfull

#----------------------------------------------code to generate 1000 transaction--------------------------------
count=0            
noOfTxn = []
ratioOfTxn = []

for i in range(1000):
    #  code to find two distinct users x and y from 0 to 99  randomly
    path=[]
    x=random.randint(0,99)
    y=random.randint(0,99)   
    # x=0
    # y=1 
    while(y==x):
        y=random.randint(0,99)
    #-----------------------------code to finding the path-----------------------------------    
    bfs_matrix=[]
    for j in range(100):
        temp_list=[]
        for k in range(100):
            
            if joint_matrix[j][k]>=1:
                temp_list.append(1)
            else:
                temp_list.append(0)
        bfs_matrix.append(temp_list)
    path = bfs(bfs_matrix, x, y)
    # print(type(path))
    # print(path)
   
    if path is not None:
        
        a=int(0)
        b=int(1)
        
        p=path[a]
        q=path[b]
 
        while b<len(path):
            p=path[a]
            q=path[b]
            
            joint_matrix[p][q]=joint_matrix[p][q]-1
            joint_matrix[q][p]=joint_matrix[q][p]+1
            
            a=b
            b=b+1
            
          
        
          
        q=contract.functions.sendAmount(x,y,path).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409680})
        # print("after transaction",i)
        m=contract.caller.check_account(x,y)
        l=contract.caller.check_account(y,x)
        if m!=joint_matrix[x][y] or l!=joint_matrix[y][x]:
            print("not updated")
        count=count+1
    else:
        path=[]
        q=contract.functions.sendAmount(x,y,path).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':240968})
#---------------------------code to print the graph----------------------------------        
    if (i+1)%100==0:
        m=contract.caller.txn_fail()-n
        
        n=contract.caller.txn_fail()
        ratio_txn=(100-m)/100
        print(i+1,ratio_txn,count)
        noOfTxn.append(i+1)
        ratioOfTxn.append(ratio_txn)
        count=0
      
# print(joint_matrix[5])
# x=int(input("enter the nm"))
# print(contract.caller.check_account(5,x))
# print(contract.caller.check_account(x,5))    
# print(contract.functions.closeAccount(5,x).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':240968}))
# print(contract.caller.check_account(5,x),contract.caller.check_account(x,5))    





build1.draw_graph(noOfTxn,ratioOfTxn)

