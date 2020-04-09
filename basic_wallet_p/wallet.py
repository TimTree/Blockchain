import hashlib
import requests

import sys
import json

# What is the server address? IE `python3 miner.py https://server.com/api/`
if len(sys.argv) > 1:
    node = sys.argv[1]
else:
    node = "http://localhost:5000"


# Load ID
f = open("my_id.txt", "r")
id = f.read()


def changeID():
    global id
    id = input('Enter new ID: ')
    print(f'Changed ID to {id}')
    print('')


def showBalance():
    totalBalance = 0
    r = requests.get(url=node + "/chain")
    data = r.json()
    allTransactions = [transactions['transactions'] for transactions in data['chain'] if transactions['transactions'] != []]
    # print(allTransactions)
    for block in allTransactions:
        for transaction in block:
            if transaction['recipient'] == id:
                totalBalance += int(transaction['amount'])
            elif transaction['sender'] == id:
                totalBalance -= int(transaction['amount'])
    print(f'{id} has {totalBalance} coins')
    print('')


def sendCoins():
    theRecipient = input('Enter the recipient: ')
    theCoins = int(input('Enter number of coins to give (whole number only): '))
    
    if theRecipient == id:
        print('Error: Cannot send coins to yourself')
    else:
        post_data = {"sender": id, "recipient": theRecipient, "amount": theCoins}
        r = requests.post(url=node + "/transactions/new", json=post_data)
        data = r.json()
        print(data['message'])
    print('')


def displayTransactions():
    usersTransactions = []
    r = requests.get(url=node + "/chain")
    data = r.json()
    allTransactions = [transactions['transactions'] for transactions in data['chain'] if transactions['transactions'] != []]
    for block in allTransactions:
        for transaction in block:
            if transaction['recipient'] == id:
                usersTransactions.append(transaction)
            elif transaction['sender'] == id:
                usersTransactions.append(transaction)
    print(usersTransactions)
    print('')


if __name__ == '__main__':
    print("ID is", id)
    f.close()
    print('')
    print('OPTIONS')
    print('I: Change ID')
    print('B: Show balance of user')
    print('S: Send coins to user')
    print('D: Display all transactions of user')
    print('')
    # Run forever until interrupted
    while True:
        prompt = input("Select action (I, B, S, D): ")
        if prompt == "I":
            changeID()
        elif prompt == "B":
            showBalance()
        elif prompt == "S":
            sendCoins()
        elif prompt == "D":
            displayTransactions()

