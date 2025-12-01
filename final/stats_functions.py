import json
import numpy as np


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
    average_words_per_sentence = round(sum(data["words_dic_all"]["words_per_sentence_list"]) / len(data["sentence_lengths"]), 2)

    #---------------------- average characters per word ----------------------
    average_characters_per_word = round(total_characters / number_of_words, 2)

    #---------------------- average characters per word ----------------------
    num_of_paragraph = data['paragraph_count']

    #---------------------- LIX ----------------------
    word_lengths = data["words_dic_all"]["word_lengths"]
    long_word_count = 0
    for L in word_lengths:
        if L > 6:
            long_word_count += 1
        # total words

    total_words = sum(data["words_dic_all"]["words_dic"].values())

    # total sentences
    total_sentences = len(data["sentence_lengths"])

    Lix = round((total_words / total_sentences) + (long_word_count * 100 / total_words), 2)


    #---------------------- return results instead of printing ----------------------
    return {
        "num_sentences": len(data["sentence_lengths"]),
        "num_words": number_of_words,
        "num_characters": total_characters,
        "avg_words_per_sentence": average_words_per_sentence,
        "avg_chars_per_word": average_characters_per_word,
        "num_of_paragraph": num_of_paragraph,
        "lix_index": Lix
    }





def display_basic_statistics(stats):
    print("\n========== Basic Statistics ==========\n")

    labels = {
        "num_sentences": "Number of sentences",
        "num_words": "Number of words",
        "num_characters": "Number of characters",
        "avg_words_per_sentence": "Average words per sentence",
        "avg_chars_per_word": "Average characters per word",
        "num_of_paragraph": "Number of paragraphs",
        "lix_index": "LIX index of text"
    }

    for key, label in labels.items():
        value = stats[key]
        if isinstance(value, float):
            print(f"{label:<30} : {value:.2f}")
        else:
            print(f"{label:<30} : {value:,}")

    print("\n======================================\n")

#========================================================================================================================
# WORD ANALYSIS
#========================================================================================================================
def word_analysis(data):
    word_dic = data["words_dic_all"]["words_dic"]
    word_lengths = data["words_dic_all"]["word_lengths"]

    # ---------------------- total words ----------------------
    total_words = sum(word_dic.values())

    # ---------------------- word length statistics ----------------------
    if len(word_lengths) > 0:
        shortest_word_length = min(word_lengths)
        longest_word_length = max(word_lengths)
        average_word_length = round(sum(word_lengths) / len(word_lengths), 2)
        long_word_count = sum(1 for length in data["words_dic_all"]["word_lengths"] if length > 6)
    else:
        shortest_word_length = 0
        longest_word_length = 0
        average_word_length = 0

    # ---------------------- dictionary to numpy array ----------------------
    pairs = []
    for w, c in word_dic.items():
        pairs.append([c, w])     # [count, word]

    #dtype=object ---> Type of the data (integer, float, Python object, etc.)
    pairs = np.array(pairs, dtype=object)

    # sort by count (descending)
    idx = np.argsort(pairs[:, 0].astype(int))[::-1]
    top10 = pairs[idx][:10]

    # convert a given array to an ordinary list with the same items, elements, or values
    top10_list = top10.tolist()

    # ---------------------- unique words and words appearing once ----------------------
    unique_word_count = len(word_dic)

    words_appearing_once = 0
    for w in word_dic:
        if word_dic[w] == 1:
            words_appearing_once += 1

    return {
        "top_words": top10_list,
        "shortest_word_length": shortest_word_length,
        "longest_word_length": longest_word_length,
        "average_word_length": average_word_length,
        "unique_word_count": unique_word_count,
        "words_appearing_once": words_appearing_once,
        "total_words": total_words,
       "long_word_coun": long_word_count
    }

def display_word_analysis(stats):
    print("\n============== Word Analysis ==============\n")

    print("Top 10 Most Common Words:")
    print("------------------------------------------")

    total = stats["total_words"]

    # stats["top_words"] = list of [count, word]
    rank = 1
    for item in stats["top_words"]:
        count = item[0]
        word = item[1]

        if total > 0:
            pct = round((count / total) * 100, 1)
        else:
            pct = 0

        print(f"{rank:>2}. {word:<15} {count:>7,} times  ({pct:>4}%)")
        rank += 1

    print("\nWord Statistics:")
    print("------------------------------------------")
    print(f"{'Shortest word length':30} : {stats['shortest_word_length']} characters")
    print(f"{'Longest word length':30} : {stats['longest_word_length']} characters")
    print(f"{'Average word length':30} : {stats['average_word_length']:.2f} characters")
    print(f"{'Unique words':30} : {stats['unique_word_count']:,}")
    print(f"{'Words appearing only once':30} : {stats['words_appearing_once']:,}")

    print("\n===========================================\n")



#========================================================================================================================
# SENTENCE ANALYSIS
#========================================================================================================================
def sentence_analysis(data):
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
    print("\n========== Sentence Analysis ==========\n")

    labels = {
        "num_sentences": "Total sentences",
        "avg_words_per_sentence": "Average words per sentence",
        "shortest_sentence_length": "Shortest sentence (words)",
        "longest_sentence_length": "Longest sentence (words)",
        "paragraph_count": "Total number of paragraphs"
    }

    for key, label in labels.items():
        value = stats[key]
        if isinstance(value, float):
            print(f"{label:<32} : {value:.2f}")
        else:
            print(f"{label:<32} : {value:,}")

    print(f"\n{'Shortest sentence text':<32} : {stats['shortest_sentence_text']}")
    print(f"{'Longest sentence text':<32} : {stats['longest_sentence_text'][:100]} ...")

    print("\nSentence length distribution (top 5):")
    print("--------------------------------------")
    for freq, length in stats["length_distribution"]:
        print(f"{length:>3} words : {freq:,} sentences")

    print("\n=======================================\n")


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
    print("\n=========== Character Analysis ===========\n")

    # --- Character Type Distribution ---
    print("Character Distribution:")
    print("------------------------------------------")

    print(f"{'Letters':25} : {stats['letters_count']:>10,} "
          f"({(stats['letters_count'] / stats['total_characters'] * 100):>5.1f}%)")

    print(f"{'Digits':25} : {stats['digits']:>10,} "
          f"({(stats['digits'] / stats['total_characters'] * 100):>5.1f}%)")

    print(f"{'Spaces':25} : {stats['spaces']:>10,} "
          f"({(stats['spaces'] / stats['total_characters'] * 100):>5.1f}%)")

    print(f"{'Punctuation':25} : {stats['punctuation']:>10,} "
          f"({(stats['punctuation'] / stats['total_characters'] * 100):>5.1f}%)")

    print("\nMost Common Letters:")
    print("------------------------------------------")

    for rank, (freq, letter) in enumerate(stats["top_letters"], start=1):
        pct = round((freq / stats['letters_count']) * 100, 1)
        print(f"{rank:>2}. {letter:<5} {freq:>10,} times   ({pct:>4}%)")

    print("\n===========================================\n")