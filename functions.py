import json

#========================================================================================================================
# LOAD DATA
#========================================================================================================================

with open("processed_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)


#========================================================================================================================
# BASIC STATISTICS
#========================================================================================================================

def basic_statistics(data):

    #---------------------- number of words ----------------------
    number_of_words = sum(data["words_dic_all"]["words_dic"].values())

    #---------------------- number of characters ----------------------
    num_upper = sum(data["characters_dic"]["letters"]["uppercase"].values())
    num_lower = sum(data["characters_dic"]["letters"]["lowercase"].values())
    num_punct = sum(data["characters_dic"]["punctuation"].values())
    total_characters = num_upper + num_lower + num_punct

    #---------------------- average words per sentence ----------------------
    average_words_per_sentence = round(sum(data["words_dic_all"]["words_per_lines_list"]) / data["number_of_lines"], 2)

    #---------------------- average characters per word ----------------------
    average_characters_per_word = round(total_characters / number_of_words, 2)

    return number_of_words, total_characters, average_words_per_sentence, average_characters_per_word


number_of_words, total_characters, average_words_per_sentence, average_characters_per_word = basic_statistics(data)


#---------------------- display ----------------------
print("---- Basic Statistics ----")
print("Number of sentences: ", data["number_of_lines"])
print("Number of words: ", number_of_words)
print("Number of characters: ", total_characters)
print("Average words per sentence: ", average_words_per_sentence)
print("Average characters per word: ", average_characters_per_word)



#========================================================================================================================
# WORD ANALYSIS
#========================================================================================================================
def word_analysis(data):

    #---------------------- getting data ----------------------------------------------
    word_dic = data["words_dic_all"]["words_dic"]
    word_lengths = data["words_dic_all"]["word_lengths"]

    #---------------------- sorting according to their frequency ----------------------
    pairs = list(word_dic.items())
    items = [[count, word] for (word, count) in pairs]
    items.sort(reverse=True)

    total_words = sum(word_dic.values())

    #---------------------- word length statistics --------------------------------
    if len(word_lengths) > 0:
        shortest_word_length = min(word_lengths)
        longest_word_length = max(word_lengths)
        average_word_length = round(sum(word_lengths) / len(word_lengths), 1)
    else:
        shortest_word_length = 0
        longest_word_length = 0
        average_word_length = 0

    #---------------------- unique words ----------------------
    unique_word_count = len(word_dic)

    #---------------------- words appearing once ----------------------
    words_appearing_once = []
    for word in word_dic:
        if word_dic[word] == 1:
            words_appearing_once.append(word)

    words_appearing_once_count = len(words_appearing_once)

    #---------------------- display ----------------------
    print('--- Word Analysis for "sample.txt" ---')
    print("Top 10 most common words:")

    rank = 1
    for pair in items[:10]:
        count = pair[0]
        word = pair[1]
        percentage = round((count / total_words) * 100, 1)
        print("", rank, ".", word, count, "times (", str(percentage) + "%)", sep=" ")
        rank = rank + 1

    print("Word length statistics:")
    print(" Shortest word:", shortest_word_length, "characters")
    print(" Longest word:", longest_word_length, "characters")
    print(" Average word length:", average_word_length, "characters")
    print("Unique words:", unique_word_count)
    print("Words appearing only once:", words_appearing_once_count)

#========================================================================================================================
# Sentence ANALYSIS
#========================================================================================================================

def sentence_analysis(data):
    number_of_sentences = len(data["sentence_lengths"])
    average_word_per_sentence = round((sum(data["sentence_lengths"]) / len(data["sentence_lengths"])), 2)