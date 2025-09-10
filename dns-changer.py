
import sys

def change_dns(argumants):
    pass

def clear_dns(argumants):
    pass

def add_dns(argumants):
    pass


argumants = sys.argv


if argumants:
    if '-set' in argumants:
        change_dns(argumants)

    elif '-clear' in argumants:
        clear_dns(argumants)
    
    elif '-add' in argumants:
        add_dns(argumants)