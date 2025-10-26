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

def top_10_most_common_words(data):
    wordCounts = data["words_dic_all"]["words_dic"]
    pairs = list(wordCounts.items())
    items = [[count, word] for (word, count) in pairs]
    items.sort(reverse=True)
    return [(word, count) for count, word in items[:10]]


top_words = top_10_most_common_words(data)


#---------------------- display ----------------------
print("---- Top 10 Most Common Words ----")
for word, count in top_words:
    print(word, count, sep="\t")