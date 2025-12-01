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
    """Compute basic text statistics and return them as a dictionary."""

    #---------------------- number of words ----------------------
    number_of_words = sum(data["words_dic_all"]["words_dic"].values())

    #---------------------- number of characters ----------------------
    num_upper = sum(data["characters_dic"]["letters"]["uppercase"].values())
    num_lower = sum(data["characters_dic"]["letters"]["lowercase"].values())
    num_punct = sum(data["characters_dic"]["punctuation"].values())
    total_characters = num_upper + num_lower + num_punct

    #---------------------- average words per sentence ----------------------
    average_words_per_sentence = round(sum(data["words_dic_all"]["words_per_sentence_list"]) / len(data["sentence_lengths"]), 2)

    #---------------------- average characters per word ----------------------
    average_characters_per_word = round(total_characters / number_of_words, 2)

    #---------------------- average characters per word ----------------------
    num_of_paragraph = data['paragraph_count']

    #---------------------- return results instead of printing ----------------------
    return {
        "num_sentences": len(data["sentence_lengths"]),
        "num_words": number_of_words,
        "num_characters": total_characters,
        "avg_words_per_sentence": average_words_per_sentence,
        "avg_chars_per_word": average_characters_per_word,
        "num_of_paragraph": num_of_paragraph 
    }

def display_basic_statistics(stats):
    print("---- Basic Statistics ----")
    for label, value in stats.items():
        if isinstance(value, float):
            print(f"{label:35} {value:.2f}")
        else:
            print(f"{label:35} {value}")

#========================================================================================================================
# WORD ANALYSIS
#========================================================================================================================

def word_analysis(data):
    """Compute word-based statistics and return them as a dictionary."""

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
    words_appearing_once = sum(1 for w in word_dic if word_dic[w] == 1)

    #---------------------- return computed data ----------------------
    return {
        "top_words": items[:10],
        "shortest_word_length": shortest_word_length,
        "longest_word_length": longest_word_length,
        "average_word_length": average_word_length,
        "unique_word_count": unique_word_count,
        "words_appearing_once": words_appearing_once,
        "total_words": total_words
    }

def display_word_analysis(stats):
    """Display formatted word analysis results."""
    print("----- Word Analysis -----")
    print(" Top 10 most common words:")

    rank = 1
    for pair in stats["top_words"]:
        frequency = pair[0]
        word = pair[1]
        percentage = round((frequency / stats["total_words"]) * 100, 1)
        print("", rank, ".", word, "-", frequency, "times (", str(percentage) + "%)", sep=" ")
        rank += 1

    print(" Shortest word:", stats["shortest_word_length"], "characters")
    print(" Longest word:", stats["longest_word_length"], "characters")
    print(" Average word length:", stats["average_word_length"], "characters")
    print(" Unique words:", stats["unique_word_count"])
    print(" Words appearing only once:", stats["words_appearing_once"])

#========================================================================================================================
# SENTENCE ANALYSIS
def sentence_analysis(data):
    """Compute sentence-based statistics and return them as a dictionary."""

    #---------------------- sentence counts and lengths ----------------------
    number_of_sentences = len(data["sentence_lengths"])

    if number_of_sentences > 0:
        average_words_per_sentence = round(sum(data["sentence_lengths"]) / number_of_sentences, 2)
    else:
        average_words_per_sentence = 0

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

    #---------------------- return computed data ----------------------
    return {
        "num_sentences": number_of_sentences,
        "avg_words_per_sentence": average_words_per_sentence,
        "shortest_sentence_text": shortest_sentence_text,
        "longest_sentence_text": longest_sentence_text,
        "shortest_sentence_length": shortest_sentence_length,
        "longest_sentence_length": longest_sentence_length,
        "paragraph_count": data["paragraph_count"],
        "length_distribution": items[:5] 
    }

def display_sentence_analysis(stats):
    """Display sentence analysis results in a formatted way."""
    print("------ Sentence Analysis -----")
    print(f"{'Total sentences:':35} {stats['num_sentences']}")
    print(f"{'Average words per sentence:':35} {stats['avg_words_per_sentence']}")
    print(f"{'Shortest sentence:':35} {stats['shortest_sentence_length']} words")
    print(f"{'Longest sentence:':35} {stats['longest_sentence_length']} words")
    print(f"{'Shortest sentence text:':35} {stats['shortest_sentence_text']}")
    print(f"{'Longest sentence text:':35} {stats['longest_sentence_text'][:100]} ...")
    print(f"{'Total number of paragraphs:':35} {stats['paragraph_count']}")
    print()
    print("Sentence length distribution (top 5):")
    for freq, length in stats["length_distribution"]:
        print(f" {length} words: {freq} sentences")



#========================================================================================================================
# CHARACTER ANALYSIS
#========================================================================================================================
def character_analysis(data):
    """Compute character-based statistics and return them as a dictionary."""

    #---------------------- merge uppercase and lowercase letters ----------------------
    letters_upper = data["characters_dic"]["letters"]["uppercase"]
    letters_lower = data["characters_dic"]["letters"]["lowercase"]

    for letter, freq in letters_upper.items():
        letter_lower = letter.lower()
        if letter_lower in letters_lower:
            letters_lower[letter_lower] += freq
        else:
            letters_lower[letter_lower] = freq

    #---------------------- prepare and sort by frequency ----------------------
    pairs = list(letters_lower.items())
    items = [[freq, letter] for (letter, freq) in pairs]
    items.sort(reverse=True)

    #---------------------- basic counts ----------------------
    letters_count = sum(letters_lower.values())
    digits = data["characters_dic"]["digits"]
    spaces = data["characters_dic"]["spaces"]
    punctuation = sum(data["characters_dic"]["punctuation"].values())
    total_characters = letters_count + digits + spaces + punctuation

    #---------------------- return results as dictionary ----------------------
    return {
        "letters_count": letters_count,
        "digits": digits,
        "spaces": spaces,
        "punctuation": punctuation,
        "total_characters": total_characters,
        "top_letters": items[:10]  # only keep top 10 most common
    }


def display_character_analysis(stats):
    """Display character analysis results in a formatted way."""
    print(" ------- Character Analysis -------")
    print(f" Letters: {stats['letters_count']} ({round((stats['letters_count'] / stats['total_characters']) * 100, 1)}%)")
    print(f" Digits: {stats['digits']} ({round((stats['digits'] / stats['total_characters']) * 100, 1)}%)")
    print(f" Spaces: {stats['spaces']} ({round((stats['spaces'] / stats['total_characters']) * 100, 1)}%)")
    print(f" Punctuation: {stats['punctuation']} ({round((stats['punctuation'] / stats['total_characters']) * 100, 1)}%)")
    print()
    print(" Most common letters:")
    rank = 1
    for freq, letter in stats["top_letters"]:
        percentage = round((freq / stats["letters_count"]) * 100, 1)
        print(f"  {rank}. \"{letter}\" - {freq} times ({percentage}%)")
        rank += 1