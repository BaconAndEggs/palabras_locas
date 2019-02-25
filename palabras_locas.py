import sys
# Make sure it is running under at least a 3.x python
if sys.version_info[0] < 3:
    print('Only compatible with python 3.x versions.')
    sys.exit(1)

from PyDictionary import PyDictionary
dictionary = PyDictionary()
# PyDictionary invokes BeutifulSoup in a way that causes a default parser selection warning.
# It looks like a fix was put in during December of 2017 (https://github.com/ckreibich/scholar.py/issues/49),
# but the latest release on PyPI for download is from 2015 (https://pypi.org/project/PyDictionary/#history).
# For now, just hiding the bs4 warning...
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='PyDictionary')

import time
import re
import os
import platform
from random import randrange
import json
import io
from contextlib import redirect_stdout

class WordLookupException(Exception):
    pass

file_to_read = sys.argv[1]

output_filename = os.path.basename(file_to_read)

# Check if it is a Mac, if so, we will use the say command to
# so lazy people like me don't need to read the new text out loud.
try:
    platform.mac_ver()
    is_osx = True
except:
    is_osx = False

loco_sentences = []

def find_word_and_replace_it(sentence):
    word_list = sentence.split()
    random_word_index = randrange(len(word_list))
    random_word = word_list[random_word_index].lower()
    # keep the last character in case it is punctuation
    last_word_char = random_word[-1:]
    word_end_char = ''
    # let's not lookup commas and stuff
    letters_only_regex = re.compile('[^a-zA-Z]')
    if not last_word_char.isalpha():
        word_no_end_punction = random_word[:-1]
        word_end_punctuation = random_word[-1]
        cleaned_word = letters_only_regex.sub('', word_no_end_punction)
    else:
        word_end_punctuation = ''
        cleaned_word = letters_only_regex.sub('', random_word)

    # look up the type of word

    # If PyDictionary fails to lookup a word, it does not throw an exception,
    # but rather returns a None.
    # Also, it spits out error text to stdout, that we will suppress, and hope the
    # retry finds a known word.
    f = io.StringIO()
    with redirect_stdout(f):
        lookup_result = dictionary.meaning(cleaned_word)
    lookup_stdout = f.getvalue()
    if 'The Following Error occured' in lookup_stdout:
        raise(WordLookupException)

    type_of_word = list(lookup_result.keys())[0]

    # check if we should say "A noun/verb", or "AN adjective/adverb"
    if type_of_word.lower()[0] == 'a':
        type_of_word_article = 'an'
    else:
        type_of_word_article = 'a'

    # ask for our new word
    if is_osx:
        os.system('say "give me {} {}"'.format(type_of_word_article, type_of_word))
    new_word = input('Give me {} {}: '.format(type_of_word_article, type_of_word))
    time.sleep(1)

    word_list[random_word_index] = '{}{}'.format(new_word, word_end_punctuation)
    new_sentence = ' '.join(word_list)
    return new_sentence

with open(file_to_read) as f:
    original_text = f.read()

original_sentences = re.split(r' *[\.\?!][\'"\)\]]* *', original_text)

print('')

for idx,orig_sentence in enumerate(original_sentences):
    stripped_sentence = orig_sentence.strip()
    if len(stripped_sentence) < 1:
        # skipping empty sentence/line
        continue

    # make 3 attempts, because Russell Wilson's number is 3
    replace_attempts = 0
    while replace_attempts < 3:
        try:
            new_sentence = find_word_and_replace_it(stripped_sentence)
            loco_sentences.append(new_sentence)
            break
        except WordLookupException:
            replace_attempts += 1
            if replace_attempts == 3:
                # give up, like Cam Newton reaching for a fumble, and use original sentence
                loco_sentences.append(stripped_sentence)

print('')
try:
    input("Press any key for your Palabras Locas...")
except:
    pass

print('')
print('###### {} ######'.format(output_filename))

for loco_sentence in loco_sentences:
    print(loco_sentence)
    if is_osx:
        sentence_without_quotes_for_say = loco_sentence.replace('"', "")
        sentence_without_quotes_for_say = sentence_without_quotes_for_say.replace("'", "")
        os.system('say "{}"'.format(sentence_without_quotes_for_say))

print('########################################')
print('')
