import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

import pygame
from card import Card
from SplendorClasses import *

pygame.font.init()
pygame.init()

game_surface = pygame.display.set_mode((1440,900)) 

# This example uses Python threads to manage async input from sys.stdin.
# This is so that I can receive input from the console whilst running the server.
# Don't ever do this - it's slow and ugly. (I'm doing it for simplicity's sake)
from _thread import *

class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        print("Chat client started")
        print("Ctrl-C to exit")
        # get a nickname from the user before starting
        self.nickname = str(input("Enter your nickname: "))
        connection.Send({"action": "nickname", "nickname": self.nickname})
        # launch our threaded input loop
        t = start_new_thread(self.InputLoop, ())

    def Loop(self):
        connection.Pump()
        self.Pump()
    
    def InputLoop(self):
        # horrid threaded input loop
        # continually reads from stdin and sends whatever is typed to the server
        while 1:
            connection.Send({"action": "message", "message": stdin.readline().rstrip("\n")})
    
    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_player_addr(self, data):
        # Gets the player's address and stores it in a variable
        if data['action'] == 'player_addr':
            self.addr = data['player_addr']
    
    def Network_players(self, data):
        print("*** players: " + ", ".join([p for p in data['players']]))
    
    def Network_message(self, data):
        # Print's players' messages
        if data['action'] == 'message':
            print(data['who'] + ": " + data['message'])
            
    def Network_table_cards(self, data):
        # Prints the cards based on the given data
        if data['action'] == "table_cards":
            for details in data["table_cards"][self.addr]:
                c = Card(game_surface,details[0],details[1],details[2],details[3],details[4],details[5],details[6])
                c.draw()
    
    def Network_table_tokens(self, data):
        # Prints the tokens based on the given data
        if data['action'] == "table_cards":
            for details in data["table_cards"]:
                t = Token(game_surface,details[0],details[1],details[2],details[3],details[4],details[5],details[6],details[7])
                t.draw()

    # built in stuff

    def Network_connected(self, data):
        print("You are now connected to the server")
    
    def Network_error(self, data):
        print('error:', data['error'])
        connection.Close()
    
    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    c = Client(host, int(port))
    while 1:
        c.Loop()
        sleep(0.001)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.flip()
