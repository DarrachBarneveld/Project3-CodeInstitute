import os
import sys
import time
import colorama


colorama.init()

G = colorama.Fore.LIGHTGREEN_EX
R = colorama.Fore.RED
B = colorama.Fore.CYAN
Y = colorama.Fore.YELLOW
W = colorama.Fore.WHITE
M = colorama.Fore.MAGENTA


def display_welcome():
    """
    Display ASCII welcome Log logo on the terminal.
    """
    print(G + ' _    _            _   _____ _   _____       _  ')
    print(G + '| |  | |          | | |_   _| | |  _  |     | |  ')
    print(G + '| |  | | ___  _ __| | __| | | |_| | | |_   _| |_ ')
    print(B + "| |/\| |/ _ \| '__| |/ /| | | __| | | | | | | __|")
    print(B + '\  /\  / (_) | |  |   <_| |_| |_\ \_/ / |_| | |_ ')
    print(B + ' \/  \/ \___/|_|  |_|\_\___/ \__|\___/ \__,_|\__|')
    print(' ')
    print(R + '                             By Darrach Barneveld')
    print(W)


def type_text(string, speed=.03):
    """
    Displays a string in a typed out animation by printing text periodically
    
    Args:
        string (str): The string to print to the console
        speed (int): A number to configure speed of animation 
    """
    for character in string:
        time.sleep(speed)
        sys.stdout.write(character)
        sys.stdout.flush()

def display_text(text_array, speed):
    """
    Loops through an array of strings and prints them to the console in an animated manner
    
    Args:
        text_array (Arr[str]): An array of strings
        speed (int): A number to configure speed of animation 
    """
    for text in text_array:
        print(text[0])
        type_text(text[1], speed)
        time.sleep(.1)
    print(W + '\n')

def clear_screen():
    os.system('cls' if os.name == 'nt' else "printf '\033c'")