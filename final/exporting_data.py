def export_results(all_stats, filename="results.txt"):
    """
    Save all computed statistics to a text file in a clean, readable format.
    Uses ONLY the analysis dictionaries. No prints are captured.
    """

    try:
        with open(filename, "w", encoding="utf-8") as file:

            # ============================
            # BASIC STATISTICS
            # ============================
            b = all_stats["basic"]
            file.write("========== BASIC STATISTICS ==========\n")
            file.write(f"Number of sentences          : {b['num_sentences']}\n")
            file.write(f"Number of words              : {b['num_words']}\n")
            file.write(f"Number of characters         : {b['num_characters']}\n")
            file.write(f"Average words per sentence   : {b['avg_words_per_sentence']:.2f}\n")
            file.write(f"Average characters per word  : {b['avg_chars_per_word']:.2f}\n")
            file.write(f"Number of paragraphs         : {b['num_of_paragraph']}\n\n\n")

            # ============================
            # WORD ANALYSIS
            # ============================
            w = all_stats["word"]
            file.write("============== WORD ANALYSIS ==============\n")
            file.write("Top 10 Most Common Words:\n")
            file.write("-------------------------------------------\n")

            total = w["total_words"]
            rank = 1
            for count, word in w["top_words"]:
                pct = (count / total * 100) if total > 0 else 0
                file.write(f"{rank:>2}. {word:<15} {count:>7} times ({pct:.1f}%)\n")
                rank += 1

            file.write("\nWord Statistics:\n")
            file.write("-------------------------------------------\n")
            file.write(f"Shortest word length        : {w['shortest_word_length']} characters\n")
            file.write(f"Longest word length         : {w['longest_word_length']} characters\n")
            file.write(f"Average word length         : {w['average_word_length']:.2f} characters\n")
            file.write(f"Unique words                : {w['unique_word_count']}\n")
            file.write(f"Words appearing only once   : {w['words_appearing_once']}\n\n\n")

            # ============================
            # SENTENCE ANALYSIS
            # ============================
            s = all_stats["sentence"]
            file.write("========== SENTENCE ANALYSIS ==========\n")
            file.write(f"Total sentences              : {s['num_sentences']}\n")
            file.write(f"Average words per sentence   : {s['avg_words_per_sentence']:.2f}\n")
            file.write(f"Shortest sentence length     : {s['shortest_sentence_length']} words\n")
            file.write(f"Longest sentence length      : {s['longest_sentence_length']} words\n")
            file.write(f"Shortest sentence text       : {s['shortest_sentence_text']}\n")
            file.write(f"Longest sentence text        : {s['longest_sentence_text'][:100]} ...\n")
            file.write(f"Paragraph count              : {s['paragraph_count']}\n\n")

            file.write("Sentence length distribution (top 5):\n")
            for freq, length in s["length_distribution"]:
                file.write(f"{length:>3} words : {freq} sentences\n")
            file.write("\n\n")

            # ============================
            # CHARACTER ANALYSIS
            # ============================
            c = all_stats["character"]
            file.write("=========== CHARACTER ANALYSIS ===========\n")
            file.write(f"Letters                       : {c['letters_count']} ({(c['letters_count']/c['total_characters']*100):.1f}%)\n")
            file.write(f"Digits                        : {c['digits']} ({(c['digits']/c['total_characters']*100):.1f}%)\n")
            file.write(f"Spaces                        : {c['spaces']} ({(c['spaces']/c['total_characters']*100):.1f}%)\n")
            file.write(f"Punctuation                   : {c['punctuation']} ({(c['punctuation']/c['total_characters']*100):.1f}%)\n\n")

            file.write("Most Common Letters:\n")
            rank = 1
            for freq, letter in c["top_letters"]:
                pct = round((freq / c["letters_count"]) * 100, 1)
                file.write(f"{rank:>2}. {letter:<5} {freq:>10} times ({pct:.1f}%)\n")
                rank += 1

            file.write("\n==========================================\n")

        print(f"Results successfully saved to {filename}")

    except IOError:
        print("Error: Could not write to file.")