#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re

# In[2]:

def count_syllables(word):
    vowels = "aeiouáéíóú"
    word = word.lower().strip()
    if word.endswith('e') or word.endswith('s'):
        word = word[:-1]
    
    syllable_count = 0
    previous_char_was_vowel = False
    
    for char in word:
        if char in vowels:
            if not previous_char_was_vowel: # Si ahora tengo una vocal y la anterior no fue vocal, me agrega una sílaba
                syllable_count += 1
            previous_char_was_vowel = True # Seteo que la previa fue vocal
        else:
            previous_char_was_vowel = False 

    return syllable_count

# In[3]:

def difficult_word(word):
    n_syllabes = count_syllables(word)
    if n_syllabes > 2:
        difficult_word = 1
    else:
        difficult_word = 0
    return difficult_word


# In[4]:

# Una función para encontrar el titulo usando regex
def find_title(filecontent):
    match = re.search(r'Title:\s*(.+?)\n', filecontent)
    if match:
        return match.group(1).strip()
    else:
        return "Title not found."


# In[5]:


def measure_complexity(filepath):
    if filepath.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()
            title = find_title(file_content)
            replaced_text = file_content.replace('!', '.').replace('?', '.').replace('\n', ' ')
            sentences = [s.strip() for s in replaced_text.split('.') if s.strip()] # Filtra oraciones vacías
            sentence_count = len(sentences)
            if sentence_count == 0:
                return "The file does not contain any sentences."
            #words = replaced_text.split(' ')
            words = re.findall(r'\b\w+\b', replaced_text) # Usa regex para definir palabras
            word_count = len(words)
            if word_count == 0:
                return "The file does not contain any words."
            character_count = 0
            syllable_count = 0
            difficult_word_count = 0
            for word in words:
                character_count += len(word)
                syllable_count += count_syllables(word)
                difficult_word_count += difficult_word(word)
            cpw = character_count/word_count
            wps = word_count/sentence_count
            spw = syllable_count/word_count
            diff_words = difficult_word_count/word_count
            ars = 4.71*cpw + 0.5*wps - 21.43
            fki = 0.39*wps + 11.8*spw - 15.59
            d_c = 15.79*diff_words + 0.0496*wps
    #return title, ars, fki, d_c
    return (f"Title: {title} - Automated Readability Score: {ars:.3f} - "
                f"Flesch-Kincaid Index: {fki:.3f} - "
                f"Dale-Chall Readability Score: {d_c:.3f}")
    

