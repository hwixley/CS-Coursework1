import os
import sys
from common import *
from const import *

args = sys.argv

if len(args) != 2:
    print("You must provide exactly one of these tags as an argument upon execution: --relay --break-heart --custom")
    exit(0)
else:

    #1) Connect to Alice and get her key

    #2) Connect to Bob and get his key

    #3) Communication cases:
    #3.1) Relay - decrypt, re-encrypt and send each message using respective keys
    #3.2) Break Heart - encrypt and send messages (-> Alice: "I hate you!", -> Bob "You broke my heart...")
    #3.3) Custom - prompt user to add message upon message receival from Bob/Alice, encrypt and send it

    dialog = Dialog('print')
    player = os.path.basename(sys.argv[0]).split('.', 1)[0]
    socket, aes = setup(player, BUFFER_DIR, BUFFER_FILE_NAME)

    if CUSTOM_CHAT:
        dialog.prompt('Please input message...')
        to_send = input()
    else:
        to_send = NICE_MSG[player]
    encrypt_and_send(to_send, aes, socket)
    dialog.info('Message sent! Waiting for reply...')
    received = receive_and_decrypt(aes, socket)
    dialog.chat('Alice said: "{}"'.format(received))

    tear_down(socket, BUFFER_DIR, BUFFER_FILE_NAME)


    if args[1] == "--relay":
        print(1)
    elif args[1] == "--break-heart":
        print(2)
    elif args[1] == "--custom":
        print(3)

    exit(0)
