def export_simple_fields(stats, file_object, skip_keys):
    for key, value in stats.items():
        if key not in skip_keys:
            file_object.write(f"{key}: {value}\n")

def export_top_words(top_words, file_object):
    file_object.write("top_words:\n")
    rank = 1
    for pair in top_words:
        count = pair[0]
        word = pair[1]
        file_object.write(f"  {rank}. {word} - {count} times\n")
        rank += 1
    file_object.write("\n")

def export_length_distribution(dist_list, file_object):
    file_object.write("length_distribution:\n")
    for pair in dist_list:
        freq = pair[0]
        length = pair[1]
        file_object.write(f"  {length} words : {freq} sentences\n")
    file_object.write("\n")

def export_top_letters(top_letters, file_object):
    file_object.write("top_letters:\n")
    for rank, pair in enumerate(top_letters, start=1):
        freq = pair[0]
        letter = pair[1]
        file_object.write(f"  {rank}. {letter} - {freq} times\n")
    file_object.write("\n")

# ================================================================
def export_results(all_stats, filename="results.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as file:

            # BASIC STATISTICS
            file.write("=== BASIC STATISTICS ===\n")
            export_simple_fields(all_stats["basic"], file, skip_keys=[])
            file.write("\n")

            # WORD ANALYSIS
            file.write("=== WORD STATISTICS ===\n")
            export_simple_fields(all_stats["word"], file, skip_keys=["top_words"])
            export_top_words(all_stats["word"]["top_words"], file)
            file.write("\n")

            # SENTENCE ANALYSIS
            file.write("=== SENTENCE STATISTICS ===\n")
            export_simple_fields(all_stats["sentence"], file, skip_keys=["length_distribution"])
            export_length_distribution(all_stats["sentence"]["length_distribution"], file)
            file.write("\n")

            # CHARACTER ANALYSIS
            file.write("=== CHARACTER STATISTICS ===\n")
            export_simple_fields(all_stats["character"], file, skip_keys=["top_letters"])
            export_top_letters(all_stats["character"]["top_letters"], file)
            file.write("\n")

        print("Export completed.")

    except IOError:
        print("Error writing file.")