import os

# -----------------------------------------------------------
# Simple key-value exporter for stats
# -----------------------------------------------------------
def export_simple_fields(stats, file_object, skip_keys):
    for key, value in stats.items():
        if key not in skip_keys:
            file_object.write(f"{key}: {value}\n")


# -----------------------------------------------------------
def export_top_words(top_words, file_object):
    file_object.write("top_words:\n")
    for rank, (count, word) in enumerate(top_words, start=1):
        file_object.write(f"  {rank}. {word} – {count} times\n")
    file_object.write("\n")


# -----------------------------------------------------------
def export_length_distribution(dist_list, file_object):
    file_object.write("length_distribution:\n")
    for freq, length in dist_list:
        file_object.write(f"  {length} words : {freq} sentences\n")
    file_object.write("\n")


# -----------------------------------------------------------
def export_top_letters(top_letters, file_object):
    file_object.write("top_letters:\n")
    for rank, (freq, letter) in enumerate(top_letters, start=1):
        file_object.write(f"  {rank}. {letter} – {freq} times\n")
    file_object.write("\n")


# -----------------------------------------------------------
def create_export_folder(text_filename):
    name = os.path.basename(text_filename)
    name_no_ext = os.path.splitext(name)[0]
    safe = name_no_ext.replace(" ", "_")

    foldername = f"{safe}_stats"

    if not os.path.exists(foldername):
        os.makedirs(foldername)

    return foldername


# -----------------------------------------------------------
def export_results(all_stats, foldername):

    filepath = os.path.join(foldername, "summary_of_statistics.txt")

    try:
        with open(filepath, "w", encoding="utf-8") as file:

            # ================= BASIC STATISTICS =================
            file.write("=== BASIC STATISTICS ===\n")
            export_simple_fields(all_stats["basic"], file, skip_keys=[])
            file.write("\n")

            # ================= WORD STATISTICS =================
            file.write("=== WORD STATISTICS ===\n")
            export_simple_fields(all_stats["word"], file, skip_keys=["top_words"])
            export_top_words(all_stats["word"]["top_words"], file)
            file.write("\n")

            # ================= SENTENCE STATISTICS =============
            file.write("=== SENTENCE STATISTICS ===\n")
            export_simple_fields(all_stats["sentence"], file, skip_keys=["length_distribution"])
            export_length_distribution(all_stats["sentence"]["length_distribution"], file)
            file.write("\n")

            # ================= CHARACTER STATISTICS ============
            file.write("=== CHARACTER STATISTICS ===\n")
            export_simple_fields(all_stats["character"], file, skip_keys=["top_letters"])
            export_top_letters(all_stats["character"]["top_letters"], file)
            file.write("\n")

            # ================= VISUALISATIONS ==================
            file.write("=== VISUALISATIONS SAVED ===\n")
            file.write("Basic_text_composition.png\n")
            file.write("basic_character_type_distribution.png\n")
            file.write("word_length_distribution.png\n")
            file.write("top_10_most_common_words.png\n")
            file.write("histogram_of_word_lengths.png\n")
            file.write("sentence_length_distribution.png\n")
            file.write("sentence_length_histogram.png\n")
            file.write("top_10_most_common_letters.png\n")
            file.write("\n")

        print("Export completed successfully.")

    except IOError:
        print("Error writing summary_of_statistics.txt.")