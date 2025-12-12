from EnigmaModel import EnigmaModel

def encrypt(rotors: str, message: str) -> str: # both rotors and message must be given in all caps
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    model = EnigmaModel() # assigns EnigmaModel() to a variable so that it doesn't get called at every instance

    model.rotor1.offset = alphabet.index(rotors[0])
    model.rotor2.offset = alphabet.index(rotors[1]) # initializes the offset based on the given str "rotors"
    model.rotor3.offset = alphabet.index(rotors[2])

    """This version of encrypt() should work despite the "version" of EnigmaModel.py file,
    only changes that need to be made is the naming of the rotors, in this case,
    rotor1, rotor2, rotor3 refer to the leftmost, middle and rightmost rotors respectivelly
    
    if a different version of EnigmaModel.py is used, the naming needs to be changed
    accordingly to match the rotor names in the EnigmaModel.py file"""

    result = []

    for i in message:
        model.key_pressed(i)

        for j in alphabet:
            if model.is_lamp_on(j):
                result.append(j)

        model.key_released(i)

    return "".join(result)

#print(encrypt("ABC", "HELLO")) -> "EIMKS"
