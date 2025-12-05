import os 
import matplotlib.pyplot as plt



#========================================================================================================================
# BASIC STATISTICS
#========================================================================================================================

def basic_statistics_visuals(data, foldername):

    # ---------------------- compute basic stats ----------------------
    num_sentences = len(data["sentence_lengths"])
    num_words = sum(data["words_dic_all"]["words_dic"].values())

    num_upper = sum(data["characters_dic"]["letters"]["uppercase"].values())
    num_lower = sum(data["characters_dic"]["letters"]["lowercase"].values())
    num_punct = sum(data["characters_dic"]["punctuation"].values())
    num_spaces = data["characters_dic"]["spaces"]
    num_digits = data["characters_dic"]["digits"]

    num_paragraphs = data["paragraph_count"]
    total_characters = num_upper + num_lower + num_punct

    # BAR CHART 
    labels = ["Sentences", "Words", "Characters", "Paragraphs"]
    values = [num_sentences, num_words, total_characters, num_paragraphs]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.title("Basic Text Composition")
    plt.ylabel("Count")
    plt.xlabel("Statistic")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(foldername, "Basic_text_compostion.png"))
    plt.show()
    plt.close()

    # PIE CHART
    char_labels = ["Letters", "Digits", "Spaces", "Punctuation"]
    char_values = [num_upper + num_lower, num_digits, num_spaces, num_punct]

    explode = [0.05] * 4  

    plt.figure(figsize=(7, 7))
    plt.pie(char_values, labels=char_labels, autopct="%1.1f%%",
            startangle=140, explode=explode)
    plt.title("Character Type Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(foldername, "character_type_distribution.png"))
    plt.show()
    plt.close()


#========================================================================================================================
# WORD ANALYSIS
#========================================================================================================================

def word_analysis_visuals(data, foldername):

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
    plt.savefig(os.path.join(foldername,"word_length_distribution.png"))
    plt.show()
    plt.close()

    
    #---------------------- Top 10 word statistics --------------------------------
    length_count_dic = {}
    for length in word_lengths:
        length_count_dic[length] = length_count_dic.get(length, 0) + 1

    items_1 = sorted([[count, length] for length, count in length_count_dic.items()],
                    reverse=True)

    top_lengths = [length for count, length in items_1[:10]]
    top_freqs = [count for count, length in items_1[:10]]

    plt.figure(figsize=(9, 6))
    plt.bar(top_lengths, top_freqs, edgecolor="black")
    plt.xticks(top_lengths)
    plt.title("Word Length Distribution (Top 10)")
    plt.tight_layout()
    plt.savefig(os.path.join(foldername, "word_length_distribution.png"))
    plt.show()
    plt.close()

    
    #---------------------- HISTOGRAM --------------------------------
    plt.figure(figsize=(10, 6))
    lengths = word_lengths
    max_len = max(lengths) if lengths else 0
    step = max_len / 25 if max_len > 0 else 1
    bins = [i * step for i in range(26)]

    plt.hist(lengths, bins=bins, edgecolor="black")
    plt.title("Histogram of Word Lengths", fontsize=14, fontweight='bold')
    plt.xlabel("Word Length", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(foldername,"histogram_of_word_lengths.png"))
    plt.show()
    plt.close()



#========================================================================================================================
# SENTENCE ANALYSIS
#========================================================================================================================

def sentence_analysis_visuals(data, foldername):

    # ---------------------- sentence length distribution ----------------------
    arr = data["sentence_lengths"]
    max_len = max(arr) if arr else 0
    bins = list(range(0, max_len + 5, 5))

    # ---------------------- bar chart (top 5 sentence lengths) ----------------------
    freq = {}
    for length in arr:
        freq[length] = freq.get(length, 0) + 1

    # Sort by count (largest first)
    sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    # Extract top 5
    top5 = sorted_items[:5]

    # Convert to dict for plotting
    top5_dict = {length: count for length, count in top5}


    plt.figure(figsize=(9, 6))
    plt.bar(top5_dict.keys(), top5_dict.values(), edgecolor="black")
    plt.title("Top 5 Most Common Sentence Lengths")
    plt.xlabel("Sentence length (words)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(foldername, "sentence_length_distribution.png"))
    plt.show()
    plt.close()

    # ---------------------- histogram of all sentence lengths ----------------------
    plt.figure(figsize=(9, 6))
    plt.hist(arr, bins=bins, edgecolor="black")
    plt.title("Sentence Length Histogram")
    plt.xlabel("Sentence length (words)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(foldername, "sentence_length_histogram.png"))
    plt.show()
    plt.close()

    

#========================================================================================================================
# CHARACTER ANALYSIS
#========================================================================================================================
def character_analysis_visuals(data, foldername):

    # ---------------------- merge uppercase + lowercase ----------------------
    letters_upper = data["characters_dic"]["letters"]["uppercase"]
    letters_lower = data["characters_dic"]["letters"]["lowercase"]

    for letter, freq in letters_upper.items():
        small = letter.lower()
        letters_lower[small] = letters_lower.get(small, 0) + freq

    # ---------------------- Top 10 letters ----------------------
    pairs = []
    for letter, freq in letters_lower.items():
        pairs.append([freq, letter])

    pairs.sort(reverse=True)

    top_letters_dic = {}
    for freq, letter in pairs[:10]:
        top_letters_dic[letter] = freq

    # ---------------------- Character type distribution ----------------------
    letters_count = sum(letters_lower.values())
    digits = data["characters_dic"]["digits"]
    spaces = data["characters_dic"]["spaces"]
    punctuation = sum(data["characters_dic"]["punctuation"].values())

    type_distribution = {
        "letters": letters_count,
        "digits": digits,
        "spaces": spaces,
        "punctuation": punctuation
    }

    # ---------------------- Visualization ----------------------

    # --- Top 10 letters (bar chart) ---
    plt.figure(figsize=(9, 6))
    plt.bar(top_letters_dic.keys(), top_letters_dic.values(), edgecolor="black")
    plt.xticks(rotation=45)
    plt.title("Top 10 Most Common Letters")
    plt.tight_layout()
    plt.savefig(os.path.join(foldername, "top_10_most_common_letters.png"))
    plt.show()
    plt.close()

    # --- Character types (pie chart) ---
    plt.figure(figsize=(8, 6))
    vals = list(type_distribution.values())
    labels = list(type_distribution.keys())
    plt.pie(vals, labels=labels, autopct="%1.1f%%")
    plt.title("Character Type Distribution")
    plt.tight_layout()
    plt.show()
    plt.close()
 