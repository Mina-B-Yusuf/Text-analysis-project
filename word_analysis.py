def top_10_most_common_words(text):
    top_10 = sorted(words_list.items(), key=lambda x: x[1], reverse=True)[:10]
    return top_10


