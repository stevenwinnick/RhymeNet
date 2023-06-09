# Imports
from os import path
from sys import argv
from json import load, dumps
from collections import defaultdict
from phonemes import *
import re

def addPlainWords(dictionary: dict, cmu_dict_path: str):
    if path.isfile(cmu_dict_path):
        pass

def addPronouncedSyllables(dictionary: dict, cmu_dict_path: str, add_new: bool):
    if path.isfile(cmu_dict_path):
        if add_new:
            with open(cmu_dict_path) as file:
                
                # Skip to first line of dictionary
                cur_line = file.readline()
                while cur_line[0] != 'A' and cur_line[1] != ' ':
                    cur_line = file.readline()
                
                # Parse the rest of the dictionary
                while cur_line != '':
                    split_line = cur_line.split()
                    cur_word = split_line[0]
                    if cur_word not in dictionary:
                        dictionary[cur_word] = defaultdict(dict)
                    dictionary[cur_word]['phonemes'] = [split_line[1:]]
                    dictionary[cur_word]['phoneme_syllables'] = phonemeSyllabize(split_line[1:])
                    # Go to next line
                    cur_line = file.readline()

        else:
            pass

def addWrittenSyllables(dictionary: dict, written_dict_path: str, add_new: bool):
    
    mismatches = []
    number_added = 0
    number_not_in_dict = 0
    
    if path.isfile(written_dict_path):
        with open(written_dict_path) as file:

            # Skip to first line of dictionary
            cur_line = file.readline()
            while cur_line != 'A\n':
                cur_line = file.readline()
            
            while cur_line != '*** END OF THIS PROJECT GUTENBERG EBOOK WEBSTER\'S UNABRIDGED DICTIONARY ***\n':
                # Add current word's written syllables
                if cur_line.isupper():
                    word = cur_line[:-1]

                    if add_new:
                        next_line = file.readline()
                        # Check if right format
                        split_line = next_line.split() # Might have to do the special (regex?) version of this to split at specific characters
                        if len(split_line) > 0:
                            if len(split_line[0]) > 0:
                                if split_line[0][-1] == ',':
                                    syllables = re.split(r'[*"`]', split_line[0][:-1].upper())
                                    if syllables[-1] == '':
                                        syllables = syllables[:-1]

                                    # Add to dictionary
                                    if word in dictionary:

                                        if not 'written_syllables' in dictionary[word]:
                                            dictionary[word]['written_syllables'] = syllables
                                            number_added += 1
                                        
                                    else:
                                        dictionary[word]['written_syllables'] = syllables
                                        number_added += 1

                    # Not add new
                    else:
                        if word in dictionary:
                            next_line = file.readline()
                            # Check if right format
                            split_line = next_line.split() # Might have to do the special (regex?) version of this to split at specific characters
                            if len(split_line) > 0:
                                if len(split_line[0]) > 0:
                                    if split_line[0][-1] == ',':
                                        syllables = re.split(r'[*"`]', split_line[0][:-1].upper())
                                        if syllables[-1] == '':
                                            syllables = syllables[:-1]
                                        # Add to dictionary
                                        if (len(syllables) == len(dictionary[word]['phoneme_syllables'])) and (not 'written_syllables' in dictionary[word]):
                                            dictionary[word]['written_syllables'] = syllables
                                            number_added += 1
                                        elif len(syllables) != len(dictionary[word]['phoneme_syllables']): 
                                            mismatches.append([word, dictionary[word]['phoneme_syllables'], syllables])
                        else:
                            number_not_in_dict += 1
                            print("Not in dict:", word)
                            pass
                    # Move to next line
                    cur_line = file.readline()

                # Find next word
                else:
                    cur_line = file.readline()

def makePhonemeSylList(dictionary):
    
    phoneme_syl_list = {}

    for word in dictionary:
        if 'phoneme_syllables' in dictionary[word]:
            for syllable in dictionary[word]['phoneme_syllables']:
                sylstring = ''
                for phoneme in syllable:
                    sylstring += phoneme
                    sylstring += '_'
                sylstring = re.sub(r'[0-9]', '', sylstring)
                if sylstring in phoneme_syl_list:
                    phoneme_syl_list[sylstring].append(word)
                else:
                    phoneme_syl_list[sylstring] = [word]
        else:
            pass

    return phoneme_syl_list

def makeVowelSoundsList(dictionary):
    
    vowel_sound_list = {}

    for word in dictionary:
        if 'phonemes' in dictionary[word]:
            for phoneme in dictionary[word]['phonemes'][0]:
                no_number = re.sub(r'[0-9]', '', phoneme)
                if (no_number in vowel_sound_list) and (PHONEMES_LIST[no_number] == VOWEL):
                    if word not in vowel_sound_list[no_number]:
                        vowel_sound_list[no_number].add(word)
                elif PHONEMES_LIST[no_number] == VOWEL:
                    vowel_sound_list[no_number] = set()
                    vowel_sound_list[no_number].add(word)
        else:
            pass
    
    for vowel_sound in vowel_sound_list:
        vowel_sound_list[vowel_sound] = list(vowel_sound_list[vowel_sound])

    return vowel_sound_list

def makeStressRhymeList(dictionary):
    
    stress_rhyme_list = {}

    for word in dictionary:
        if 'phonemes' in dictionary[word]:
            primary_stress_idx = -1
            for idx, phoneme in enumerate(dictionary[word]['phonemes'][0]):
                if phoneme[-1] == '1':
                    primary_stress_idx = idx
            rhyme_string = ''
            for idx in range(primary_stress_idx, len(dictionary[word]['phonemes'][0])):
                rhyme_string += dictionary[word]['phonemes'][0][idx]
                rhyme_string += '_'
            rhyme_string = rhyme_string[:-1]
            rhyme_string = re.sub(r'[0-9]', '', rhyme_string)
            dictionary[word]['after_stress_rhyme'] = rhyme_string
            if rhyme_string in stress_rhyme_list:
                    stress_rhyme_list[rhyme_string].append(word)
            else:
                stress_rhyme_list[rhyme_string] = [word]

    return stress_rhyme_list

def makeLastSylRhymeList(dictionary):
    
    syl_rhyme_list = {}

    for word in dictionary:
        if 'phoneme_syllables' in dictionary[word]:
            last_syllable = dictionary[word]['phoneme_syllables'][-1]
            last_vowel_sound_idx = -1
            for idx, phoneme in enumerate(last_syllable):
                if (PHONEMES_LIST[phoneme] == VOWEL):
                    last_vowel_sound_idx = idx
            rhyme_string = ''
            for idx in range(last_vowel_sound_idx, len(last_syllable)):
                rhyme_string += last_syllable[idx]
                rhyme_string += '_'
            rhyme_string = rhyme_string[:-1]
            rhyme_string = re.sub(r'[0-9]', '', rhyme_string)
            dictionary[word]['last_syl_rhyme'] = rhyme_string
            if rhyme_string in syl_rhyme_list:
                    syl_rhyme_list[rhyme_string].append(word)
            else:
                syl_rhyme_list[rhyme_string] = [word]

    return syl_rhyme_list

def phonemeSyllabize(phonemes: list):

    syllables = []
    phoneme_count = len(phonemes)
    cur_syl_start_idx = 0
    next_syl_start_idx = -1

    # Everything up to first VOWEL sound is in the first syllable
    cur_vowel_idx = 0
    first_vowel_found = False
    while (not first_vowel_found) and (cur_vowel_idx < phoneme_count):
        if PHONEMES_LIST[phonemes[cur_vowel_idx]] != VOWEL:
            cur_vowel_idx += 1
        else:
            first_vowel_found = True

    # Parse
    end_reached = False
    next_vowel_idx = cur_vowel_idx + 1
    while not end_reached:

        # Find the next vowel sound
        next_vowel_found = False
        while (next_vowel_idx < phoneme_count) and (not next_vowel_found):
            if PHONEMES_LIST[phonemes[next_vowel_idx]] != VOWEL:
                next_vowel_idx += 1
            else:
                next_vowel_found = True

        # Determine break point
        if next_vowel_found:
            consonants_between = next_vowel_idx - cur_vowel_idx - 1
            if consonants_between == 0:
                next_syl_start_idx = next_vowel_idx
            elif consonants_between == 1:
                next_syl_start_idx = next_vowel_idx - 1
            elif consonants_between == 2:
                if (phonemes[next_vowel_idx - 2], phonemes[next_vowel_idx - 1]) in TWO_ONSET_CLUSTERS:
                    next_syl_start_idx = next_vowel_idx - 2
                else:
                    next_syl_start_idx = next_vowel_idx - 1
            else:
                if (phonemes[next_vowel_idx - 3], phonemes[next_vowel_idx - 2], phonemes[next_vowel_idx - 1]) in THREE_ONSET_CLUSTERS:
                    next_syl_start_idx = next_vowel_idx - 3
                elif (phonemes[next_vowel_idx - 2], phonemes[next_vowel_idx - 1]) in TWO_ONSET_CLUSTERS:
                    next_syl_start_idx = next_vowel_idx - 2
                else:
                    next_syl_start_idx = next_vowel_idx - 1
            syllables.append(phonemes[cur_syl_start_idx: next_syl_start_idx])
            cur_syl_start_idx = next_syl_start_idx
            # Move to next
            cur_vowel_idx = next_vowel_idx
            next_vowel_idx = cur_vowel_idx + 1
        else:
            end_reached = True
            syllables.append(phonemes[cur_syl_start_idx:])

    # Return
    return syllables


if __name__ == '__main__':

    if len(argv) != 3:
        print("Usage: [old db filepath] [output db filepath]") # python3 RhymeNetCreator.py none RhymeNetV1.0
        exit()

    english = defaultdict(dict)

    # Load previous version if not creating from scratch
    if path.isfile(argv[1]):
        print("Input file found")
        english = load(open(argv[1]))

    addPronouncedSyllables(english, 'cmudict-0.7b.txt', True) # cmudict file should be in this directory
    addWrittenSyllables(english, 'websters.txt', True) # websters too
    phoneme_syllables = makePhonemeSylList(english)
    vowel_sounds = makeVowelSoundsList(english)
    after_stress_rhymes = makeStressRhymeList(english)
    last_syl_rhymes = makeLastSylRhymeList(english)

    dataset = {
        'words': english,
        'syllables': phoneme_syllables,
        'vowel_sounds': vowel_sounds,
        'after_stress_rhymes': after_stress_rhymes,
        'last_syllable_rhymes': last_syl_rhymes
    }

    # Save 
    json_object = dumps(dataset)
    with open(argv[2], "w") as outfile:
        outfile.write(json_object)