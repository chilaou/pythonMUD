#!/usr/bin/python

# Things for making multiuser forum/game
# 1) User accounts
#    To start, probably just plaintext names and passwords
#    a)  Should each player be a class with currentLocation, stats, etc that save regularly and upon
#        log out
# 2) The chat interface
#    To do a web interface...how do I make it auto update?

#!/usr/bin/python

import pickle

# Key elements of an account?
# Need a user name, and a password (plaintext now, hash later, roll someone else's crypto WAY LATER)
# We can add key value pairs as we need them later, but things that may be relevant
# Health, Power, Stamina, Currency, Inventory list
try:
    file_object = open('accounts.pydata', 'rb')
    accounts = pickle.load(file_object)
    file_object.close()
except:
    accounts = {}

def listAccounts():
    for player in accounts:
        print(player)
        
        
def save_accounts():
    try:
        file_object = open('accounts.pydata', 'wb')
        pickle.dump(accounts, file_object)
        file_object.close()
    except Exception as e:
        print(e)
        print("\nSave error.\n")
        
def print_help():
    print('\nCurrent commands are: quit, save, help, list\n')
    
def deleteUser(username):
    password = raw_input('Please enter your password. ')
    if accounts[username]['password'] == password:
        print('\nWARNING! This will permanently remove your account.')
        confirmation = raw_input('Are you sure? Enter "delete" to confirm. ')
        if confirmation == 'delete':
            del accounts[username]
            print('Account "{}" deleted!'.format(username))
            save_accounts()
    else:
        print('\nIncorrect password.\n')
        
def changePassword(username):
    password = raw_input('Please enter your password: ')
    if accounts[username]['password'] == password:
        newPassword = raw_input('Please enter a new password: ')
        confirmation = raw_input('Confirm your new password: ')
        if newPassword == confirmation:
            accounts[username]['password'] = newPassword
            print('Success! Password changed.')
            save_accounts()
        else:
            print('\nPasswords do not match.\n')
    else:
        print('\nIncorrect password.\n')


# Main run loop
user_input = None
while user_input != 'quit':
    existingUser = False
    user_input = raw_input("Please enter your character name, 'help', or 'quit': ").strip()
    user_input = user_input.lower()
    for name in accounts:
        if user_input == name:
            existingUser = True
    if user_input == 'quit':
        print('\nThank you for visiting. See you later!')
    elif user_input == 'save':
        save_accounts()
        print('Accounts saved: ')
        listAccounts()
    elif user_input == 'help':
        print_help()
    elif user_input == 'list':
        listAccounts()
    elif len(user_input) < 17:
        if existingUser:
            userPassword = raw_input("\nEnter your password, or type 'delete' or 'change'): ")
            if userPassword == 'delete':
                deleteUser(user_input)
            elif userPassword == 'change':
                changePassword(user_input)
            else:
                if accounts[user_input]['password'] == userPassword:
                    print('\nCorrect password supplied.')
                    print('Logging in...\n')
                else:
                    print('\nIncorrect password.\n')
        else:
            print("\nWelcome, {}.".format(user_input.title()))
            passwordMatch = False
            while not passwordMatch:
                password = raw_input("\nPlease choose a password for your account: ")
                passwordCheck = raw_input("Confirm your password: ")
                if password != 'delete' and password != 'change':
                    passwordMatch = password == passwordCheck
                if passwordMatch:
                    accounts[user_input] = {'password': password}
                    print('\nAccount created.')
                    save_accounts()
                    print("Let's make your character!")
                    #createNewCharacter
                else:
                    print("\nPasswords do not match, or invalid password. Please try again.")
    else:
        print('\nError: Name over 16 characters. Please try again.\n')
