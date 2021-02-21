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
    dialog.info("Waiting for Bob's message...")
    received = receive_and_decrypt(aes2, socket2)
    dialog.chat('Bob wanted to say: "{}"'.format(received))

    # Formulate message to send to alice
    if args[1] == tags[0]:
        dialog.prompt('Input what you would like Bob to say to Alice:')
        to_send = input()
    elif args[1] == tags[1]:
        to_send = NICE_MSG["bob"]
    elif args[1] == tags[2]:
        to_send = BAD_MSG["bob"]

    dialog.chat('What Bob actually said: "{}"'.format(to_send))

    # Send message to alice
    encrypt_and_send(to_send, aes1, socket1)
    dialog.info('Message sent to Alice! Waiting for reply...')

    # Receive alice's message
    received = receive_and_decrypt(aes1, socket1)
    dialog.chat('Alice wanted to say: "{}"'.format(received))

    # Formulate message to send to bob
    if args[1] == tags[0]:
        dialog.prompt('Input what you would like Alice to say to Bob:')
        to_send = input()
    elif args[1] == tags[1]:
        to_send = NICE_MSG["alice"]
    elif args[1] == tags[2]:
        to_send = BAD_MSG["alice"]

    dialog.chat('What Alice actually said: "{}"'.format(to_send))

    # Send message to bob
    encrypt_and_send(to_send, aes2, socket2)
    dialog.info("Message sent to Bob!")

    # Close chat with alice
    #tear_down(socket1, BUFFER_DIR, BUFFER_FILE_NAME)

    exit(0)
