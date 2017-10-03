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
import json

# Key elements of an account?
# Need a user name, and a password (plaintext now, hash later, roll someone else's crypto WAY LATER)
# We can add key value pairs as we need them later, but things that may be relevant
# Health, Power, Stamina, Currency, Inventory list, Current Room, Status Effects

# I should change character data to a JSON library
try:
    file_object = open('accounts.pydata', 'rb')
    accounts = pickle.load(file_object)
    file_object.close()
except:
    accounts = {}

availableRaces = {
    'human': 'The basic starter race.',
    'alien': 'The not-so-basic starter race.'
    }
    
availableClasses = {
    'developer': 'The basic starter class!',
    'engineer': 'The not-so-basic starter class.',
    'teamlead': "The 'I think I'm special' class. :P"
    }
    
roomDB = {}
roomDB['Sanctuary'] = {'name': 'The Sanctuary', 'desc': '\
The marble walls glisten with golden tones as a never-setting sun beams \n\
through the skymark. A light breeze wafts through the room. Everything is safe \n\
and warm, and the world is at peace.', 
    'item': [], #['i0000001', 'i0000002'], 
    'path': 
    {'north':'Altar', 'east':'', 'south':'', 'west':'', 'up':'Sanctuary', 'down':''}}
roomDB['Altar'] = {'name': 'The Altar', 'desc': '\
A golden staircase leads to a podium, adorned with ornate scrolls and chains.', 
    'item': [],
    'path': 
    {'north':'', 'east':'', 'south':'Sanctuary', 'west':'', 'up':'', 'down':''}}
    
DIRECTIONS = ('north', 'east', 'south', 'west', 'up', 'down')

#with open("roomData.txt", "r") as f:
#    for line in f.readlines():
#        line = line.strip('\n')
#       # print('line = {}'.format(line))
#        if line[0] == 'r':
#            if line[0:8] in roomDB:
#                roomDB[line[0:8]][line[8:12]] = line[13:]
#            else:
#                roomDB[line[0:8]] = {}
#                roomDB[line[0:8]][line[8:12]] = line[13:]
#          #  print('line[0:8] = {}'.format(line[0:8]))
#          #  print('line[8:12] = {}'.format(line[8:12]))
#          #  print('line[13:] = {}'.format(line[13:]))
#print('roomDB = {}'.format(roomDB))
#with open("roomData2.txt", "w", 0) as fileData:
#    fileData.write(json.dumps(roomDB))

#Take the following string containing JSON data:
#
#json_string = '{"first_name": "Guido", "last_name":"Rossum"}'
#It can be parsed like this:
#
#import json
#parsed_json = json.loads(json_string)
#and can now be used as a normal dictionary:
#
#print(parsed_json['first_name'])
#"Guido"
#You can also convert the following to JSON:
#
#d = {
#    'first_name': 'Guido',
#    'second_name': 'Rossum',
#    'titles': ['BDFL', 'Developer'],
#}


        
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
    # It occurs to me that this would be where to define gender but SCREW THAT.
    # Let's make everything genderless and use neutral pronouns, I've always
    # wanted to try that.
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
    accounts[player]['inventory'] = ['i0000001', 'i0000002']
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
                outputHandler("{}".format(availableRaces[user_input[5:]]))
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
                outputHandler("{}".format(availableClasses[user_input[5:]]))
            else:
                outputHandler("I'm sorry, I can't identify that class. Try again.")
        else:
            outputHandler("I'm sorry, I can't identify that class. Try again.")
    selectionComplete = False
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
        file_object = open('accounts.pydata', 'wb')
        pickle.dump(accounts, file_object)
        file_object.close()
    except Exception as e:
        outputHandler(e)
        outputHandler("\nSave error.\n")
        
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

class pChar():
    def __init__(self, pData = {}):
        self.pData = pData
#        self.name = pStats['name']
#        self.race = pStats['race']
#        self.playerClass = pStats['playerClass']
#        self.stamina = pStats['stamina']
#        self.cur_stamina = pStats['cur_stamina']
#        self.health = pStats['health']
#        self.cur_health = pStats['cur_health']
#        self.power = pStats['power']
#        self.cur_power = pStats['cur_power']
#        self.influence = pStats['influence']
#        self.cur_influence = pStats['cur_influence']
#        self.level = pStats['level']
#        self.exp = pStats['exp']
#        self.gold = pStats['gold']
#        self.currentRoom = pStats['currentRoom']
#        self.recallRoom = pStats['recallRoom']
#        self.inventory = pStats['inventory']
#        self.str = pStats['str']
#        self.dex = pStats['dex']
#        self.vit = pStats['vit']
#        self.con = pStats['con']
#        self.int = pStats['int']
#        self.wis = pStats['wis']
#        self.cha = pStats['cha']
#        self.foc = pStats['foc']
#        self.guild = pStats['guild']
#        self.title = pStats['title']
        # consider just passing in the dictionary and requesting specific keys
        # like playerChar.get('currentRoom') = pStats['currentRoom']
        
def get(key = ''):
    return self.pData['key']
  #  def move(direction):
        # look at currentRoom's paths, see if direction is one of them, then change currentRoom
        # to the room listed
        
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
        outputHandler('There is {} here.'.format(item))
    
def enterGame(pName):
    accounts[pName]['online'] = True
    user_input = ''
    announce('{} has entered the game.\n'.format(pName.title()))
    roomLook(pName)
    while user_input != '/logout':
        user_input = inputHandler('\nWhat would you like to do, {}? '.format(pName.title()))
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
                    if split_input[1].lower() in accounts:
                        if accounts[target]['online'] and accounts[target]['currentRoom'] == accounts[pName]['currentRoom']:
                            outputHandler('You look at {}.'.format(target.title()))
                            outputHandler(accounts[target]['desc'])
                        else:
                            outputHandler("{} isn't here.".format(target.title()))
                    # next, check if it's an item.
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
            if user_input in DIRECTIONS:
                if roomDB[accounts[pName]['currentRoom']]['path'][user_input] != '':
                    accounts[pName]['currentRoom'] = roomDB[accounts[pName]['currentRoom']]['path'][user_input]
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
        save_accounts()
        outputHandler('Accounts saved: ')
        listAccounts()
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
                    outputHandler('Logging in...\n')
                    enterGame(user_input) 
                    # I feel like *this* is the point at which I would make a class from
                    # the player information that is used in the game environment.
                    # Each player would have an instance id that lets to control the class
                    # that is their character in the world.
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
                    outputHandler('New character initialized as follows: ')
                    characterStats(user_input)
                    outputHandler('To enter the game, please log in again.')
                else:
                    outputHandler("\nPasswords do not match, or invalid password. Please try again.")
    else:
        outputHandler('\nError: Name over 16 characters. Please try again.\n')
