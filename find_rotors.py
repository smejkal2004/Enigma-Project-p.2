
from EnigmaModel import EnigmaModel
from EnigmaConstants import ALPHABET
from encrypt import encrypt # The encrypt funtion is defined in encrypt.py. It will exist when repository is merged.

def find_rotors(message:str, cipher:str) -> str:
    for a in ALPHABET:
        for b in ALPHABET:
            for c in ALPHABET:
                rotors = a + b + c
                if encrypt(rotors, message)==cipher:
                    return rotors
    return "Not found"

