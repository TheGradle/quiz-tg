import data
from random import randint

class Definition:
    def __init__(self, word, definition):
        self.word = word
        self.definition = definition

def GetRandomWord():
    return data.words[randint(0, len(data.words))]

def GetHashWord(word):
    code = ""
    
    while (len(code) != len(word)):
        code += "#"

    return code

def hasLetter(letter, word):
    for i in word:
        if letter == i:
            return True

    return False

def hasHash(code):
    for i in code:
        if i == "#":
            return True

    return False

def EditHashWord(letter, code, word):
    newcode = list(code)
    
    i = 0
    while i < len(word):
        if letter == word[i]:
            newcode[i] = letter
        i += 1
    
    str = ''.join(newcode)
    return str