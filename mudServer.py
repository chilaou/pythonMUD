#!/usr/bin/python

import json

# XAE: To do
#  - Roll crypto on passwords
#  - Separate out account information into sections: modifiable stats, core info
#  - Status Effects might be something to add to account information.
#  - Modify to be part of state machine.

try:
    with open("accounts.txt", "r") as f:
        accounts = json.loads(f.read())
except:
    accounts = {}
    
try:
    with open("races.txt", "r") as f:
        availableRaces = json.loads(f.read())
except:
    availableRaces = {
        'human': {'desc':'The basic starter race.','statMod':{'cha':'1'}},
        'alien': {'desc':'The not-so-basic starter race.','statMod':{'vit':'1'}}
    }
    
try:
    with open("classes.txt", "r") as f:
        availableClasses = json.loads(f.read())
except:
    availableClasses = {
        'developer': {'desc':'The basic starter class!', 'skill':'deadline'},
        'engineer': {'desc':'The not-so-basic starter class.', 'skill':'betaTest'},
        'teamlead': {'desc':"The 'I think I'm special' class. :P", 'skill':'encourage'}
    }
    
try:
    with open("rooms.txt", "r") as f:
        roomDB = json.loads(f.read())
except:
    roomDB = {}
    roomDB['Sanctuary'] = {'name': 'The Sanctuary', 'desc': '\
The marble walls glisten with golden tones as a never-setting sun beams \n\
through the skymark. A light breeze wafts through the room. Everything is safe \n\
and warm, and the world is at peace.', 
        'item': ['sanctuary/nexus', 'altar/eternalScroll'],
        'path': 
        {'north':'Altar', 'east':'', 'south':'', 'west':'', 'up':'Sanctuary', 'down':''}
    }
    roomDB['Altar'] = {'name': 'The Altar', 'desc': '\
A golden staircase leads to a podium, adorned with ornate scrolls and chains.', 
        'item': ['altar/eternalScroll'],
        'path': 
    {'north':'', 'east':'', 'south':'Sanctuary', 'west':'', 'up':'', 'down':''}
    }
    
try:
    with open("items.txt", "r") as f:
        itemDB = json.loads(f.read())
except:
    itemDB = {}
    itemDB['sanctuary/nexus'] = {'name': "a traveler's nexus", 'desc': '\
The nexus glows blue and gold, allowing passage to wherever one might desire.', 
        'pickUp': False,
        'weight': 0,
        'despawn': False,
        'keywords': ['traveler', 'nexus']
    }
    itemDB['altar/eternalScroll'] = {'name': 'a Scroll of Eternity', 'desc': '\
An ornate golden scroll with black text.', 
        'pickUp': True,
        'weight': 1,
        'despawn': False,
        'keywords': ['scroll', 'eternity']
    }    
    itemDB['general/foobar'] = {'name': 'a FOOBAR', 'desc': '\
A basic foobar(C). It is used to FUYS.', 
        'pickUp': True,
        'weight': 5,
        'despawn': True,
        'keywords': ['foo', 'bar', 'foobar']
    }
    
DIRECTIONS = ('north', 'east', 'south', 'west', 'up', 'down')

def inputHandler(prompt = ''):
    return raw_input(prompt)
    
def outputHandler(prompt = ''):
    print(prompt)
    
def listAccounts():
    for player in accounts:
        outputHandler(player)

# create a plain character
def initializeCharacter(player):
    accounts[player]['name'] = player
    accounts[player]['desc'] = "It's {}.".format(player.title())
    accounts[player]['race'] = 'human'
    accounts[player]['playerClass'] = 'developer'
    accounts[player]['stamina'] = 10
    accounts[player]['cur_stamina'] = 10
    accounts[player]['health'] = 10
    accounts[player]['cur_health'] = 10
    accounts[player]['power'] = 10
    accounts[player]['cur_power'] = 10
    accounts[player]['influence'] = 10
    accounts[player]['cur_influence'] = 10
    accounts[player]['level'] = 1
    accounts[player]['exp'] = 0
    accounts[player]['gold'] = 0
    accounts[player]['currentRoom'] = 'Sanctuary'
    accounts[player]['recallRoom'] = 'Sanctuary'
    accounts[player]['inventory'] = ['general/foobar']
    accounts[player]['str'] = 8
    accounts[player]['dex'] = 8
    accounts[player]['vit'] = 8
    accounts[player]['con'] = 8
    accounts[player]['int'] = 8
    accounts[player]['wis'] = 8
    accounts[player]['cha'] = 8
    accounts[player]['foc'] = 8
    accounts[player]['guild'] = 'Unaligned'
    accounts[player]['title'] = 'the Newbie'
    accounts[player]['customized'] = False
    accounts[player]['online'] = False
    
def createNewCharacter(player):
    selectionComplete = False
    initializeCharacter(player)
    outputHandler("\nWe're going to start customizing your character.")
    outputHandler("Any any point, you can learn more about an option by typing:")
    outputHandler("    help <option>")
    outputHandler("Where <option> is the word you want more information about.")
    while not selectionComplete:
        outputHandler("\nPlease choose a race from the following options: ")
        for race in availableRaces:
            outputHandler(race)
        user_input = inputHandler("Which race would you like to be? ")
        if user_input in availableRaces:
            accounts[player]['race'] = user_input
            selectionComplete = True
        elif user_input[0:4] == 'help':
            if user_input[5:] in availableRaces:
                outputHandler("{}".format(availableRaces[user_input[5:]]['desc']))
            else:
                outputHandler("I'm sorry, I can't identify that race. Try again.")
        else:
            outputHandler("I'm sorry, I can't identify that race. Try again.")
    selectionComplete = False
    while not selectionComplete:
        outputHandler("\nPlease choose a class from the following options: ")
        for gameClass in availableClasses:
            outputHandler(gameClass)
        user_input = inputHandler("Which class would you like to be? ")
        if user_input in availableClasses:
            accounts[player]['playerClass'] = user_input
            selectionComplete = True
        elif user_input[0:4] == 'help':
            if user_input[5:] in availableClasses:
                outputHandler("{}".format(availableClasses[user_input[5:]]['desc']))
            else:
                outputHandler("I'm sorry, I can't identify that class. Try again.")
        else:
            outputHandler("I'm sorry, I can't identify that class. Try again.")
    selectionComplete = False
    outputHandler('New character initialized as follows: ')
    characterStats(player)
    outputHandler('To enter the game, please log in again.')
    return True # confirms character customization complete
            
def characterStats(player):
    # this is not sorted, but later i will format this to be pretty
    # and make specific requests in particular places of the sheet
    for key in accounts[player]:
        if key != 'password':
            outputHandler('{} = {}'.format(key, accounts[player][key]))
        else:
            #BE SURE TO OBFUSCATE THIS
            outputHandler('{} = {}'.format(key, accounts[player][key]))

        
def save_accounts():
    try:
        with open("accounts.txt", "w", 0) as fileData:
            fileData.write(json.dumps(accounts))
    except Exception as e:
        outputHandler(e)
        outputHandler("\nSave error.\n")
        
def saveEverything():
    try:
        with open("accounts.txt", "w", 0) as fileData:
            fileData.write(json.dumps(accounts))
    except Exception as e:
        outputHandler(e)
        outputHandler("\nError saving accounts.\n")
    try:
        with open("races.txt", "w", 0) as fileData:
            fileData.write(json.dumps(availableRaces))
    except Exception as e:
        outputHandler(e)
        outputHandler("\nError saving races.\n")
    try:
        with open("classes.txt", "w", 0) as fileData:
            fileData.write(json.dumps(availableClasses))
    except Exception as e:
        outputHandler(e)
        outputHandler("\nError saving classes.\n")
    try:
        with open("rooms.txt", "w", 0) as fileData:
            fileData.write(json.dumps(roomDB))
    except Exception as e:
        outputHandler(e)
        outputHandler("\nError saving rooms.\n")
    try:
        with open("items.txt", "w", 0) as fileData:
            fileData.write(json.dumps(itemDB))
    except Exception as e:
        outputHandler(e)
        outputHandler("\nError saving items.\n")

    
        
def outputHandler_help():
    outputHandler('\nCurrent commands are: quit, save, help, list\n')
    
def deleteUser(username):
    password = inputHandler('Please enter your password. ')
    if accounts[username]['password'] == password:
        outputHandler('\nWARNING! This will permanently remove your account.')
        confirmation = inputHandler('Are you sure? Enter "delete" to confirm. ')
        if confirmation == 'delete':
            del accounts[username]
            outputHandler('Account "{}" deleted!'.format(username))
            save_accounts()
    else:
        outputHandler('\nIncorrect password.\n')
        
def changePassword(username):
    password = inputHandler('Please enter your password: ')
    if accounts[username]['password'] == password:
        newPassword = inputHandler('Please enter a new password: ')
        confirmation = inputHandler('Confirm your new password: ')
        if newPassword == confirmation:
            accounts[username]['password'] = newPassword
            outputHandler('Success! Password changed.')
            save_accounts()
        else:
            outputHandler('\nPasswords do not match.\n')
    else:
        outputHandler('\nIncorrect password.\n')
        
def announce(msg = ''):
    print(msg)

def roomLook(pName):
    outputHandler('')
    outputHandler(roomDB[accounts[pName]['currentRoom']]['name'])
    outputHandler(roomDB[accounts[pName]['currentRoom']]['desc'])
    exits = 'Exits:'
    for key in roomDB[accounts[pName]['currentRoom']]['path']:
        if roomDB[accounts[pName]['currentRoom']]['path'][key] != '':
            exits = exits + ' ' + key
    outputHandler(exits)
    items = roomDB[accounts[pName]['currentRoom']]['item']
    for item in items:
        outputHandler('There is {} here.'.format(itemDB[item]['name']))
    
def enterGame(pName):
    accounts[pName]['online'] = True
    user_input = ''
    announce('{} has entered the game.\n'.format(pName.title()))
    roomLook(pName)
    while user_input != '/logout':
        user_input = inputHandler('\n{} <HEA {}/{}> <POW {}/{}> <STA {}/{}> <INF {}/{}> '.format(pName.title(), 
            accounts[pName]['cur_health'], accounts[pName]['health'], accounts[pName]['cur_power'], accounts[pName]['power'],
            accounts[pName]['cur_stamina'], accounts[pName]['stamina'], accounts[pName]['cur_influence'], accounts[pName]['influence']))
        if user_input != '':
            split_input = user_input.split(' ')
            if split_input[0] == '/help':
                outputHandler('The following / commands are currently in the game:\n')
                outputHandler('help *look *desc save logout recall setrecall')
                outputHandler('\nCommands with an asterisk * can take an argument.\n')
            if split_input[0] == '/look':
                if len(split_input) == 1:
                    roomLook(pName)
                else:
                    target = split_input[1].lower()
                    if target in accounts:
                        if accounts[target]['online'] and accounts[target]['currentRoom'] == accounts[pName]['currentRoom']:
                            outputHandler('You look at {}.'.format(target.title()))
                            outputHandler(accounts[target]['desc'])
                        else:
                            outputHandler("{} isn't here.".format(target.title()))
                    else:
                        totalKeywords = {}
                        for item in roomDB[accounts[pName]['currentRoom']]['item']:
                            for keyword in itemDB[item]['keywords']:
                                totalKeywords[keyword] = item
                        if target in totalKeywords:
                            outputHandler(itemDB[totalKeywords[target]]['desc'])
                        else:
                            outputHandler("{} isn't here.".format(target))
            if split_input[0] == '/desc':
                if len(split_input) > 1:
                    accounts[pName]['desc'] = user_input[6:]
                else:
                    accounts[pName]['desc'] = inputHandler('Enter a new, brief description for yourself: ')
                save_accounts()
            if split_input[0] == '/save':
                save_accounts()
                outputHandler('Accounts saved.')
            if split_input[0] == '/recall':
                # Consider ableToRecall(pName), to set cooldown, prevent while in combat.
                outputHandler('Returning...')
                accounts[pName]['currentRoom'] = accounts[pName]['recallRoom']
                roomLook(pName)
            if split_input[0] == '/setrecall':
                outputHandler('You have made this room your new recall point.')
                accounts[pName]['recallRoom'] = accounts[pName]['currentRoom']
            if split_input[0] in DIRECTIONS:
                if roomDB[accounts[pName]['currentRoom']]['path'][split_input[0]] != '':
                    accounts[pName]['currentRoom'] = roomDB[accounts[pName]['currentRoom']]['path'][split_input[0]]
                    roomLook(pName)
                else:
                    outputHandler('Silly goose, you can not go that way!')
                    
                
    outputHandler('\nLogging out...')
    accounts[pName]['online'] = False
    save_accounts()
    

        

# Main Log-in Loop
user_input = None
while user_input != 'quit':
    existingUser = False
    user_input = inputHandler("Please enter your character name, 'help', or 'quit': ").strip()
    user_input = user_input.lower()
    for name in accounts:
        if user_input == name:
            existingUser = True
    if user_input == 'quit':
        outputHandler('\nThank you for visiting. See you later!')
    elif user_input == 'save':
        saveEverything()
        outputHandler('Accounts saved: ')
        listAccounts()
        outputHandler('Saved everything else, too.')
    elif user_input == 'help':
        outputHandler_help()
    elif user_input == 'list':
        listAccounts()
    elif len(user_input) < 17:
        if existingUser:
            userPassword = inputHandler("\nEnter your password, 'delete', 'change', or 'stats': ")
            if userPassword == 'delete':
                deleteUser(user_input)
            elif userPassword == 'change':
                changePassword(user_input)
            elif userPassword == 'stats':
                characterStats(user_input)
            else:
                if accounts[user_input]['password'] == userPassword:
                    outputHandler('\nCorrect password supplied.')
                    if accounts[user_input]['customized']:
                        outputHandler('Logging in...\n')
                        enterGame(user_input) 
                    else:
                        outputHandler('It looks like your character has yet to be customized.')
                        outputHandler('Commencing character customization...')
                        accounts[user_input]['customized'] = createNewCharacter(user_input)
                        save_accounts()
                else:
                    outputHandler('\nIncorrect password.\n')
        else:
            outputHandler("\nWelcome, {}.".format(user_input.title()))
            passwordMatch = False
            while not passwordMatch:
                password = inputHandler("\nPlease choose a password for your account: ")
                passwordCheck = inputHandler("Confirm your password: ")
                if password != 'delete' and password != 'change' and password != 'stats':
                    passwordMatch = password == passwordCheck
                if passwordMatch:
                    accounts[user_input] = {'password': password}
                    outputHandler('\nAccount created.')
                    outputHandler("Let's make your character!")
                    accounts[user_input]['customized'] = createNewCharacter(user_input)
                    save_accounts()
                else:
                    outputHandler("\nPasswords do not match, or invalid password. Please try again.")
    else:
        outputHandler('\nError: Name over 16 characters. Please try again.\n')
