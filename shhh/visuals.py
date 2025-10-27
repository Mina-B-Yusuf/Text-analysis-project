import json
import numpy as np
import matplotlib.pyplot as plt


#========================================================================================================================
# LOAD DATA
#========================================================================================================================

def load_data():
    with open("processed_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


#========================================================================================================================
# BASIC STATISTICS
#========================================================================================================================

def basic_statistics_visuals(data):

    #---------------------- number of words ----------------------
    number_of_words = sum(data["words_dic_all"]["words_dic"].values())

    #---------------------- number of characters ----------------------
    num_upper = sum(data["characters_dic"]["letters"]["uppercase"].values())
    num_lower = sum(data["characters_dic"]["letters"]["lowercase"].values())
    num_punct = sum(data["characters_dic"]["punctuation"].values())
    total_characters = num_upper + num_lower + num_punct

    #---------------------- average words per sentence ----------------------
    average_words_per_sentence = round(sum(data["words_dic_all"]["words_per_lines_list"]) /len(data["sentence_lengths"]), 2)

    #---------------------- average characters per word ----------------------
    average_characters_per_word = round(total_characters / number_of_words, 2)

    basic_statistics_dic = {
        "Sentences": len(data["sentence_lengths"]),
        "unique words": data["words_dic_all"]["words_dic"]
    }


    #---------------------- display ----------------------
    print("---- Basic Statistics ----")
    plt.figure(9, 6)
    plt.bar( x =  basic_statistics_dic
            )
    plt.xticks(rotation = 45, fontsize = 13)
    plt.ysticks(fontsize = 13)
    plt.title("---- Basic Statistics ----")


    



#========================================================================================================================
# WORD ANALYSIS
#========================================================================================================================

import matplotlib.pyplot as plt

def word_analysis_visuals(data):

    #---------------------- getting data ----------------------------------------------
    word_dic = data["words_dic_all"]["words_dic"]
    word_lengths = data["words_dic_all"]["word_lengths"]

    #======================================== visualization ============================================

    #---------------------- word length statistics --------------------------------
    length_count_dic = {}
    for length in word_lengths:
        if length not in length_count_dic:
            length_count_dic[length] = 1
        else:
            length_count_dic[length] += 1

    pairs_1 = list(length_count_dic.items())
    items_1 = [[count, length] for (length, count) in pairs_1]
    items_1.sort(reverse=True)

    length_visual_dic = {}
    for pair in items_1[:10]:
        frequency = pair[0]
        length = pair[1]
        length_visual_dic[length] = frequency

    plt.figure(figsize=(9, 6))
    plt.bar(length_visual_dic.keys(), length_visual_dic.values(), color='skyblue', edgecolor='black')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.title("Word length distribution (Top 10)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

    #---------------------- Top 10 word statistics --------------------------------
    pairs = list(word_dic.items())
    items = [[count, word] for (word, count) in pairs]
    items.sort(reverse=True)

    word_visual_dic = {}
    for pair in items[:10]:
        frequency = pair[0]
        word = pair[1]
        word_visual_dic[word] = frequency

    plt.figure(figsize=(9, 6))
    plt.bar(word_visual_dic.keys(), word_visual_dic.values(), color='skyblue', edgecolor='black')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.title("Top 10 Most Common Words", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

    




#========================================================================================================================
# SENTENCE ANALYSIS
#========================================================================================================================
import matplotlib.pyplot as plt

def sentence_analysis_visuals(data):

    #---------------------- sentence length distribution ----------------------
    sentence_lengths = data["sentence_lengths"]
    length_counts = {}

    for length in sentence_lengths:
        if length not in length_counts:
            length_counts[length] = 1
        else:
            length_counts[length] += 1

    pairs = list(length_counts.items())
    items = [[count, length] for (length, count) in pairs]
    items.sort(reverse=True)

    sentence_lengths_visualisation = {}
    shown = 0
    for pair in items:
        freq = pair[0]
        length = pair[1]
        sentence_lengths_visualisation[length] = freq
        shown += 1
        if shown == 5:    # only keep top 5 like in your project description
            break

    #======================================== visualization ============================================

    plt.figure(figsize=(9, 6))
    plt.bar(sentence_lengths_visualisation.keys(), sentence_lengths_visualisation.values(), color='skyblue', edgecolor='black')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.title("Sentence length distribution (Top 5)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

    

#========================================================================================================================
# CHARACTER ANALYSIS
#========================================================================================================================
def character_analysis_visuals(data):
    #---------------------- merge uppercase and lowercase ----------------------
    letters_upper = data["characters_dic"]["letters"]["uppercase"]
    letters_lower = data["characters_dic"]["letters"]["lowercase"]

    for letter, freq in letters_upper.items():
        letter_lower = letter.lower()
        if letter_lower in letters_lower:
            letters_lower[letter_lower] += freq
        else:
            letters_lower[letter_lower] = freq

    pairs = list(letters_lower.items())
    items = [[freq, letter] for (letter, freq) in pairs]
    items.sort(reverse=True)

    characters_visuals_dic = {}
    for pair in items[:10]:
        freq = pair[0]
        letter = pair[1]
        characters_visuals_dic[letter] = freq

    #---------------------- character type distribution ----------------------
   # letters_count = sum(letters_lower.values())
    #digits = data["characters_dic"]["digits"]
    #spaces = data["characters_dic"]["spaces"]
    #punctuation = sum(data["characters_dic"]["punctuation"].values())
    #total_characters = letters_count + digits + spaces + punctuation

    #type_distribution = {
       #"Letters": letters_count,
        #"Digits": digits,
        #"Spaces": spaces,
        #"Punctuation": punctuation}

    #======================================== visualization ============================================

    # --- Character type distribution ---
    #plt.figure(figsize=(8, 6))
    #plt.bar(type_distribution.keys(), type_distribution.values(), color='lightcoral', edgecolor='black')
    #plt.title("Character Type Distribution", fontsize=14, fontweight='bold')
    #plt.xticks(rotation=30, fontsize=12)
    #plt.yticks(fontsize=12)
    #plt.tight_layout()
   # plt.show()

    # --- Top 10 most common letters ---
    plt.figure(figsize=(9, 6))
    plt.bar(characters_visuals_dic.keys(), characters_visuals_dic.values(), color='skyblue', edgecolor='black')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.title("Top 10 Most Common Letters", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
 