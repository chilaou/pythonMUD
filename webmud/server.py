import BaseHTTPServer
import json
import time
import threading
import Queue

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

commandQueue = Queue.Queue(20)
outputQueue = Queue.Queue(20)

def inputHandler(requestHandler, userID = '', prompt = ''):
    while commandQueue.empty():
        requestHandler.handle_request()
    return commandQueue.get()
    
#firstEntry = True
def outputHandler(prompt = ''):
    outputQueue.put(prompt)
#    if firstEntry:
#        outputQueue.get()
#        firstEntry = False

class WebMUDRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
#    def do_GET(self):
#        # Eventually be picky about the endpoint, but right now accept any request.
#        # (This is because eventually the mud can serve the client HTML/CSS/JS too!)
#        self.send_response(200)
#        self.send_header('Content-type', 'application/json')
#        self.send_header('Access-Control-Allow-Origin', '*')
#        self.end_headers()
#        if self.path == "/playerCommand":
#            print('self.path = {}'.format(self.path))
#            print('self.command = {}'.format(self.command))
#            print('self.client_address = {}'.format(self.client_address))
#            print('self.server = {}'.format(self.server))
#            print('self.request_version = {}'.format(self.request_version))
#            print('self.query = {}'.format(self.query))
#        response = []
#        response.append(self._console_out("Ok @ {}".format(self.date_time_string(time.time()))))
#        response.append(self._console_in_flash(200, [["#F00", "#0F0", "#00F"][int(time.time())%3], "#FFF"]))
#        self.wfile.write(json.dumps(response))

    def do_POST(self):
        # Eventually be picky about the endpoint, but right now accept any request.
        # (This is because eventually the mud can serve the client HTML/CSS/JS too!)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        if self.path == "/playerCommand":
#            for key, value in self.__dict__.items():
#                print('Key = {}  Value = {}'.format(key, value))
            userID = self.client_address[0]
            content_len = int(self.headers.getheader('content-length', 0))
            command = self.rfile.read(content_len)
            print('{}: {}'.format(userID,command))
            commandQueue.put(command)
        response = []
#        response.append(self._console_out("Ok @ {}".format(self.date_time_string(time.time()))))
        while not outputQueue.empty():
            response.append(self._console_out(outputQueue.get()))
        response.append(self._console_in_flash(200, [["#F00", "#0F0", "#00F"][int(time.time())%3], "#FFF"]))
        self.wfile.write(json.dumps(response))
        

    def _console_out(self, msg):
        result = {}
        result['time'] = time.time()
        result['type'] = 'console-out'
        result['data'] = {'msg': msg}
        return result

    def _console_in_flash(self, speed, seq):
        result = {}
        result['time'] = time.time()
        result['type'] = 'console-in-flash'
        result['data'] = {"speed": speed, "seq": seq}
        return result

    
    

        

# Main Log-in Loop
def mainGameLoop(httpd):
    user_input = ''
    while user_input != 'quit':
        existingUser = False
        outputHandler("Please enter your character name, 'help', or 'quit': ")
       # user_input = inputHandler(httpd)
        user_input = inputHandler(httpd).strip()
        user_input = user_input.lower()
        outputHandler(user_input)
#        for name in accounts:
#            if user_input == name:
#                existingUser = True
#        if user_input == 'quit':
#            outputHandler('\nThank you for visiting. See you later!')
#        elif user_input == 'save':
#            saveEverything()
#            outputHandler('Accounts saved: ')
#            listAccounts()
#            outputHandler('Saved everything else, too.')
#        elif user_input == 'help':
#            outputHandler_help()
#        elif user_input == 'list':
#            listAccounts()
#        elif len(user_input) < 17:
#            if existingUser:
#                userPassword = inputHandler("\nEnter your password, 'delete', 'change', or 'stats': ")
#                if userPassword == 'delete':
#                    deleteUser(user_input)
#                elif userPassword == 'change':
#                    changePassword(user_input)
#                elif userPassword == 'stats':
#                    characterStats(user_input)
#                else:
#                    if accounts[user_input]['password'] == userPassword:
#                        outputHandler('\nCorrect password supplied.')
#                        if accounts[user_input]['customized']:
#                            outputHandler('Logging in...\n')
#                            enterGame(user_input) 
#                        else:
#                            outputHandler('It looks like your character has yet to be customized.')
#                            outputHandler('Commencing character customization...')
#                            accounts[user_input]['customized'] = createNewCharacter(user_input)
#                            save_accounts()
#                    else:
#                        outputHandler('\nIncorrect password.\n')
#            else:
#                outputHandler("\nWelcome, {}.".format(user_input.title()))
#                passwordMatch = False
#                while not passwordMatch:
#                    password = inputHandler("\nPlease choose a password for your account: ")
#                    passwordCheck = inputHandler("Confirm your password: ")
#                    if password != 'delete' and password != 'change' and password != 'stats':
#                        passwordMatch = password == passwordCheck
#                    if passwordMatch:
#                        accounts[user_input] = {'password': password}
#                        outputHandler('\nAccount created.')
#                        outputHandler("Let's make your character!")
#                        accounts[user_input]['customized'] = createNewCharacter(user_input)
#                        save_accounts()
#                    else:
#                        outputHandler("\nPasswords do not match, or invalid password. Please try again.")
#        else:
#            outputHandler('\nError: Name over 16 characters. Please try again.\n')


def start_mud():
    server_address = ('', 7777)
    httpd = BaseHTTPServer.HTTPServer(server_address, WebMUDRequestHandler)
    #httpd.timeout = 1
    # Use httpd.handle_request() to handle one request 
    # This allows checks in-between, like for shutdown.
    while True: # "True" makes this equivalent to httpd.serve_forever()
        mainGameLoop(httpd)


if __name__ == '__main__':
    start_mud()

