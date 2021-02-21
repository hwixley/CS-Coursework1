import os
import sys

args = sys.argv

if len(args) != 2:
    print("You must provide exactly one of these tags as an argument upon execution: --relay --break-heart --custom")
    exit(0)
else:
    if args[1] == "--relay":
        print(1)
    elif args[1] == "--break-heart":
        print(2)
    elif args[1] == "--custom":
        print(3)
