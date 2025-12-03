from utils.math_utils import mean

int_num = 5
float_num = 6.5
string_string = "Adiza"
list_list = ['a', 32, 'Bola']
tuple_tuple = ('a', 35, 'Bola')
dictionary_dictionary = {'a': 32, 12:45, 'Bola':78}
set_set = set({1, 2, 3, 4})
boolean_boolean = True
bytearray_bytearray = (b'\x36\x44')# bytearray(5)
decoded_string = bytearray_bytearray.decode('utf-8')
data_mutable = bytearray(b'Python')

    
class Entry:
    def __init__(self, word: str, pos: str, meaning: list[str]):
        """
        A class that immitates a dictionary as it return object/string 
        Args:
            word (str): The specific word
            pos (str): The part of speech of the word
            meaning (str): Listist of meanings or definitions of the word
        """
        self.word = word
        self.pos = pos
        self.meaning = meaning
        
    def __repr__(self) -> str:
        return f"Entry(word={self.word!r}, pos={self.pos!r}, meanings={self.meaning!r})"
    

if __name__ == "__main__":
    try:
        calculate = mean([1.0, 2.0, 3.0, 5.0])
        print(f"{calculate}")
    except TypeError as e:
        print(f"Error: {e}")
        
    entry = Entry("go", "verb", ["to proceed in a direcion", "to move towards something"])
    print(entry)
