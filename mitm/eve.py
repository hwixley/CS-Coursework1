import os
import sys
from common import *
from const import *

args = sys.argv

tags = ["--custom", "--relay", "--break-heart"]

if len(args) != 2 or not (args[1] in tags):
    print("You must provide exactly one of these tags as an argument upon execution: --relay --break-heart --custom")
    exit(0)
else:
    dialog = Dialog('print')

    # Connect to Alice and get her key
    socket1, aes1 = setup("bob", BUFFER_DIR, BUFFER_FILE_NAME)

    # Connect to Bob and get his key
    # os.rename(BUFFER_DIR + BUFFER_FILE_NAME, BUFFER_DIR + BUFFER_FILE_NAME + "2")
    socket2, aes2 = setup("alice", BUFFER_DIR, BUFFER_FILE_NAME)

    # Receive bob's message
    dialog.info("Waiting for message...")
    received = receive_and_decrypt(aes2, socket2)
    dialog.chat('Bob wanted to say: "{}"'.format(received))

    # Formulate message to send to alice
    if args[1] == "--custom":
        dialog.prompt('Please input message...')
        to_send = input()
    elif args[1] == "--relay":
        to_send = NICE_MSG["bob"]
    elif args[1] == "--break-heart":
        to_send = BAD_MSG["bob"]
    else:
        print("ERROR: you have an entered an invalid argument")

    # Send message to alice
    encrypt_and_send(to_send, aes1, socket1)
    dialog.info('Message sent! Waiting for reply...')

    # Receive alice's message
    received = receive_and_decrypt(aes1, socket1)
    dialog.chat('Alice wanted to say: "{}"'.format(received))

    # Formulate message to send to bob
    if args[1] == "--custom":
        dialog.prompt('Please input message...')
        to_send = input()
    elif args[1] == "--relay":
        to_send = NICE_MSG["alice"]
    elif args[1] == "--break-heart":
        to_send = BAD_MSG["alice"]

    # Send message to bob
    encrypt_and_send(to_send, aes2, socket2)

    # Close chat
    #tear_down(socket1, BUFFER_DIR, BUFFER_FILE_NAME)


    #3) Communication cases:
    #3.1) Relay - decrypt, re-encrypt and send each message using respective keys
    #3.2) Break Heart - encrypt and send messages (-> Alice: "I hate you!", -> Bob "You broke my heart...")
    #3.3) Custom - prompt user to add message upon message receival from Bob/Alice, encrypt and send it

    exit(0)
