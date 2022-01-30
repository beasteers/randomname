
import os
from pathlib import Path
from posixpath import basename

def get_wordlist(filepath):
    """Read all words from a file and return them as a list"""
    with open(filepath, 'r') as f:
        return [
            l for l in (l.strip() for l in f.readlines())
            if l and l[0] not in ';#']

def get_key(filepath):
    """Get key for the dictionary from a given file path. Returns e.g. 
    'nouns/storage' for '/path/to/wordlists/nouns/storage.txt'"""
    # the path of the parent directory of the file
    parent =  os.path.abspath(os.path.join(filepath, os.pardir))
    filename_without_ext = Path(filepath).stem # e.g. 'storage'
    basename = os.path.basename(parent) # the name of the parent directory (e.g. 'nouns')
    key = '{}/{}'.format(basename, filename_without_ext) # the key for the entry in the dict (e.g. 'nouns/storage')
    return key

def generate_dict_begin():
    """Generates the beginning of a dictionary called wordlists"""
    return 'wordlists = {\n'

def generate_dict_end():
    """Generates the end of the dictionary (yes, its trivial)"""
    return '}'

def generate_dict_entry(key, wordlist):
    """Generate one entry of the python dictionary"""
    entry = "    '{}': {},\n".format(key, wordlist)
    return entry

def main():
    """
    This program is a helper tool. It reads all txt files in the (subfolders of the) 
    folder 'wordlists'.The 'wordlists' folder must be relative to this source file. 
    The program creates a new python file called 'wordlists.py' and writes all words 
    and their their categories into a dictionary.
    """

    # The absolute path tothe wordlists folder   
    wordlists_folder = os.path.abspath('wordlists').lower()
    print('Reading words from {}'.format(wordlists_folder))
    with open('wordlists.py', 'w') as wordlists_py:
        begin = generate_dict_begin() # create the start of the dictionary
        wordlists_py.write(begin) # write it the py file
        for subdir, dirs, files in os.walk(wordlists_folder):
            for file in files: # iterate over all files in the wordlists folder
                if file.endswith('.txt'): # make sure it is a .txt file
                    # create the absolute path to the text file
                    filepath = os.path.join(subdir, file) 
                    key = get_key(filepath) # create the key (e.g. 'nouns/writing') for the dict
                    wordlist = get_wordlist(filepath) # create the wordlist by reading the file
                    entry = generate_dict_entry(key, wordlist) # create the dict entry (one line)
                    wordlists_py.write(entry) # write the entry into the py file
            
        end = generate_dict_end() # create the end of the dictionary
        wordlists_py.write(end) # and write it into the py file as well
    print('Dictionary was written to {}'.format(os.path.abspath('wordlists.py')))
                
if __name__ == '__main__':
    main()