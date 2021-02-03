#!/usr/bin/env python3
import sys,os,json
assert sys.version_info >= (3,9), "This script requires at least Python 3.9"

def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j

def find_passage(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p
    return {}


def parselink(text, number):
    msg = "(" + str(number) + ") " + text[2:-2]
    if "->" in msg:
        return msg.split("->")[0]
    elif "<-" in msg:
        return msg.split("<-")[1]
    else:
        return msg
# ------------------------------------------------------

def render(current):
    text = current["text"]
    inbracket = 0
    delimiterstart = 0
    linknumber = 0
    msg = ""
    for x in range(0, len(text)):
        msg = msg + text[x]
        if x > 0 and text[x] == "[" and text[x-1] == "[" and not inbracket:
            delimiterstart = len(msg) - 2
            inbracket = True
        if x > 0 and text[x] == "]" and text[x-1] == "]" and inbracket:
            inbracket = False
            linknumber += 1
            msg = msg[:delimiterstart] + parselink(msg[delimiterstart:],linknumber)
    print(msg)

def update(current, game_desc, choice):
    links = current["links"]
    selection = None
    #input validation, is int
    try:
        selection = int(choice)
    except ValueError:
        selection = None
    #input validation; exists/nonzero, and within bounds
    if (selection) and (selection > 0) and (selection <= len(links)):
        dest = links[selection - 1]["pid"]
        return find_passage(game_desc, dest)
    return current

def get_input(current):
    return input("> ")

# ------------------------------------------------------

def main():
    game_desc = load("adventure.json")
    current = find_passage(game_desc, game_desc["startnode"])
    choice = ""

    while choice != "quit" and current != {}:
        current = update(current, game_desc, choice)
        render(current)
        choice = get_input(current)

    print("Thanks for playing!")




if __name__ == "__main__":
    main()