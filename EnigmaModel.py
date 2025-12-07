# File: EnigmaModel.py

""" This is the starter file for the Enigma project. """

from EnigmaView import EnigmaView

def apply_permutation(index: int, permutation: str, offset: int) -> int:
    """Applies the rotor permutation with the current offset: shift -> permute -> unshift"""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    index_after_shifting = (index + offset)%26
    shifted_char = permutation[index_after_shifting]
    permuted_index = alphabet.index(shifted_char)
    return (permuted_index - offset)%26

def invert_key(permutation: str) -> str:
    """Constructs the reverse permutation used in the backwards signal through the rotor"""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    inverted_str = []
    for i in range(0, len(alphabet)):
        wanted_letter = alphabet[i]
        letter_in_perm = permutation.index(wanted_letter)
        belongs_to_new_str = alphabet[letter_in_perm]
        inverted_str.append(belongs_to_new_str)
    return "".join(inverted_str)

class EnigmaRotor:

    def __init__(self, permutations: str):
        self.permutations = permutations
        self.inverted_key = invert_key(permutations)
        self.offset = 0

    def get_offset(self):
        return self.offset
    
    def get_permutation(self):
        return self.permutations
    
    def advance(self) -> bool:
        """Steps the rotor by one position, returns True on turnover to signal the next rotor"""
        value = False
        self.offset = (self.offset + 1) % 26
        if self.offset == 0:
            value = True
        return value

    def get_inverted_key(self):
        return self.inverted_key

class EnigmaModel:

    def __init__(self):
        
        self.keyboard = {"A": False, "B": False, "C": False, "D": False, "E": False,
            "F": False,"G": False, "H": False, "I": False, "J": False,"K": False,
            "L": False,"M": False, "N": False, "O": False, "P": False, "Q": False,
            "R": False,"S": False, "T": False, "U": False, "V": False, "W": False,
            "X": False,"Y": False, "Z": False} # Tracks the on/off state of all keys
        
        self.lamps = {"A": False, "B": False, "C": False, "D": False, "E": False,
            "F": False,"G": False, "H": False, "I": False, "J": False,"K": False,
            "L": False,"M": False, "N": False, "O": False, "P": False, "Q": False,
            "R": False,"S": False, "T": False, "U": False, "V": False, "W": False,
            "X": False,"Y": False, "Z": False} # Tracks the on/off state of all lamps
        
        self.rotor1 = EnigmaRotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ") # rotor1 = leftmost
        self.rotor2 = EnigmaRotor("AJDKSIRUXBLHWTMCQGZNPYFVOE") # rotor2 = middle
        self.rotor3 = EnigmaRotor("BDFHJLCPRTXVZNYEIWGAKMUSQO") # rotor3 = rightmost

        self._views = [ ]

    def add_view(self, view):
        self._views.append(view)

    def update(self):
        for view in self._views:
            view.update()

    def is_key_down(self, letter: str) -> bool:
        """Returns the current state of the given key"""
        return self.keyboard[letter]

    def is_lamp_on(self, letter: str) -> bool:
        """Returns the current state of the given lamp"""
        return self.lamps[letter]

    def key_pressed(self, letter: str):
        """
        Handles one full encryption cycle:
        1. Step the fast rotor
        2. Map the input letter through rotor3 -> rotor2 -> rotor1
        3. Reflect the signal
        4. Map back through inverse rotor1 -> rotor2 -> rotor3
        5. Light the resulting output letter
        """
        self.rotor_clicked(2) # Step rotor3 before encryption
        self.keyboard[letter] = True
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
        index = alphabet.index(letter)

        index = apply_permutation(
            index,
            self.rotor3.get_permutation(),
            self.rotor3.get_offset()
        )
        index = apply_permutation(
            index,
            self.rotor2.get_permutation(),     # Forward pass through rotors
            self.rotor2.get_offset()
        )
        index = apply_permutation(
            index,
            self.rotor1.get_permutation(),
            self.rotor1.get_offset()
        )

        reflector_permutation = "IXUHFEZDAOMTKQJWNSRLCYPBVG"
        index = alphabet.index(reflector_permutation[index]) # Reflection step

        index = apply_permutation(
            index,
            self.rotor1.get_inverted_key(),
            self.rotor1.get_offset()
        )
        index = apply_permutation(
            index,
            self.rotor2.get_inverted_key(),     # Backwards pass through inverse rotor mappings
            self.rotor2.get_offset()
        )
        index = apply_permutation(
            index,
            self.rotor3.get_inverted_key(),
            self.rotor3.get_offset()
        )

        output_letter = alphabet[index]
        self.lamps[output_letter] = True
        self.update()

    def key_released(self, letter: str):
        """Resets the key state and clears all lamps (only one key can be active at a time)"""
        self.keyboard[letter] = False
        for k in self.lamps:
            self.lamps[k] = False
        self.update()

    def get_rotor_letter(self, index: int) -> str:
        """Returns the letter currently showing in the rotor window (determined by its offset)"""
        rotor_list = [self.rotor1, self.rotor2, self.rotor3]
        rotor = rotor_list[index]
        offset = rotor.get_offset()
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[offset]

    def rotor_clicked(self, index: int):
        """Manually rotates a rotor, includes turnover propagation to the left."""
        rotor_list = [self.rotor1, self.rotor2, self.rotor3]
        carry = rotor_list[index].advance()
        if carry and index > 0:
            carry = rotor_list[index - 1].advance()
            if carry and index - 1 > 0:
                rotor_list[index - 2].advance()
        self.update()

def enigma():
    model = EnigmaModel()
    view = EnigmaView(model)
    model.add_view(view)

# Startup code

if __name__ == "__main__":
    enigma()
