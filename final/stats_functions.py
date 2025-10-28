import json

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

def basic_statistics(data):

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


    #---------------------- display ----------------------
    print("---- Basic Statistics ----")
    print(" Number of sentences: ", len(data["sentence_lengths"]))
    print(" Number of words: ", number_of_words)
    print(" Number of characters: ", total_characters)
    print(" Average words per sentence: ", average_words_per_sentence)
    print(" Average characters per word: ", average_characters_per_word)



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

    #---------------------- unique words and words appearing once ----------------------
    unique_word_count = len(word_dic)

    words_appearing_once = 0
    for word in word_dic:
        if word_dic[word] == 1:
            words_appearing_once += 1

    #---------------------- display ----------------------
    print('----- Word Analysis -----')
    print(" Top 10 most common words: ")

    rank = 1
    for pair in items[:10]:
        frequency = pair[0]
        word = pair[1]
        percentage = round((frequency / total_words) * 100, 1)
        print("", rank, ".", word, "-", frequency, "times (", str(percentage) + "%)", sep=" ")
        rank = rank + 1

    print(" Shortest word: ", shortest_word_length, "characters")
    print(" Longest word: ", longest_word_length, "characters")
    print(" Average word length: ", average_word_length, "characters")
    print(" Unique words: ", unique_word_count)
    print(" Words appearing only once: ", words_appearing_once)

#========================================================================================================================
# SENTENCE ANALYSIS
#========================================================================================================================
def sentence_analysis(data):

    #---------------------- sentence counts and lengths ----------------------
    number_of_sentences = len(data["sentence_lengths"])

    if number_of_sentences > 0:
        average_word_per_sentence = round((sum(data["sentence_lengths"]) / number_of_sentences), 2)
    else:
        average_word_per_sentence = 0

    #---------------------- shortest and longest sentence ----------------------
    shortest_sentence_text = data["shortest_sentence"]
    longest_sentence_text = data["longest_sentence"]

    shortest_sentence_length = len(shortest_sentence_text.split())
    longest_sentence_length = len(longest_sentence_text.split())

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

    #---------------------- display ----------------------
    print('------ Sentence Analysis -----')
    print(" Total sentences: ", number_of_sentences)
    print(" Average words per sentence: ", average_word_per_sentence)
    print(" Shortest sentence: ", shortest_sentence_length, "words")
    print(" Longest sentence: ", longest_sentence_length, "words")
    print(" Shortest sentence text: ", shortest_sentence_text)
    print(" Longest sentence text: ", longest_sentence_text[0:100], "...")
    print(" Total number of Paragraphs: ", data[paragraph_count])

    print(" Sentence length distribution (top 5): ")
    count = 0
    for pair in items:
        freq = pair[0]
        length = pair[1]
        print("", length, "words:", freq, "sentences")
        count = count + 1
        if count == 5:
            break

    return

#========================================================================================================================
# CHARACTER ANALYSIS
#========================================================================================================================
def character_analysis(data):
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

    letters_count = sum(letters_lower.values())
    digits = data["characters_dic"]["digits"]
    spaces = data["characters_dic"]["spaces"]
    punctuation = sum(data["characters_dic"]["punctuation"].values())
    total_characters = letters_count + digits + spaces + punctuation

    print(" ------- Character Analysis -------")
    print(" Letters: ", letters_count, "(", round((letters_count / total_characters) * 100, 1), "%)")
    print(" Digits: ", digits, "(", round((digits / total_characters) * 100, 1), "%)")
    print(" Spaces: ", spaces, "(", round((spaces / total_characters) * 100, 1), "%)")
    print(" Punctuation: ", punctuation, "(", round((punctuation / total_characters) * 100, 1), "%)")

    print("Most common letters:")
    rank = 1
    for pair in items[:10]:
        freq = pair[0]
        letter = pair[1]
        percentage = round((freq / letters_count) * 100, 1)
        print("", rank, ".", '"'+letter+'"', "-", freq, "times (", str(percentage) + "%)", sep=" ")
        rank = rank + 1

