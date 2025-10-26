import json

# 🔹 Load the saved data
with open("processed_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

def top_10_most_common_words(data):
    word_freq = data["words_dic"]
    pairs = list(word_freq.items())
    items = [[count, word] for (word, count) in pairs]
    items.sort(reverse=True)


    # optional: return them as a list of tuples
    return [(word, count) for count, word in items[:10]]

def distitbution_of_words_lengths(data):

#display 
print("---- Top 10 Most Common Words ----")
for count, word in items[:10]:
    print(word, count, sep="\t")