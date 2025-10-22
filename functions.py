import json

# 🔹 Load the saved data
with open("processed_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)



##================================Basic statistics =================================
def basic_statistics(data): 
    # Total number of words (sum of frequencies)
    number_of_words = sum(data["words_dic"].values())

    # Total characters = all letters + punctuation
    # if you only have characters_dic with letters and punctuation counts
    if isinstance(data["characters_dic"], dict):
        total_characters = sum(data["characters_dic"].values()) + data["number_of_punctuation"]
    else:
        total_characters = data["number_of_punctuation"]

    # Average words per line
    average_words_per_line = round(sum(data["words_per_lines_list"]) / data["number_of_lines"], 2)

    # Average characters per word
    average_characters_per_word = round(total_characters / number_of_words, 2)

    return number_of_words, total_characters, average_words_per_line, average_characters_per_word


#=================display =======================
print("---- Basic Statistics ----")
print("Number of lines: ", data["number_of_lines"])
print("Number of words: ", number_of_words)
print("Number of characters: ", total_characters)
print("Average words per line: ", average_words_per_line)
print("Average characters per word: ", average_characters_per_word)

##===========================Word analysis ==============================================

def top_10_most_common_words(data):
    wordCounts = data["words_dic"]
    pairs = list(wordCounts.items())
    items = [[count, word] for (word, count) in pairs]
    items.sort(reverse=True)


    # optional: return them as a list of tuples
    return [(word, count) for count, word in items[:10]]






#==================display =======================
print("---- Top 10 Most Common Words ----")
for count, word in items[:10]:
    print(word, count, sep="\t")