import json


def load_cefr_json(json_path="cefr_words.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        cefr_dict = json.load(f)
    return cefr_dict

def load_reverse_verb_dict(path="verbs_reverse.json"):
    """Load the reverse verb dictionary: inflected → base form."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            reverse_dict = json.load(f)
        return reverse_dict
    except FileNotFoundError:
        print(f"[ERROR] Verb dictionary not found: {path}")
        return {}


def cefr_levels(data, cefr_dict, reverse_verb_dict):
    normalized = {}

    for word, freq in data["words_dic_all"]["words_dic"].items():
        w = word.lower()

        # If verb variant exists → convert to base form
        if w in reverse_verb_dict:
            base = reverse_verb_dict[w]   # e.g. "abandoned" → "abandon"
        else:
            base = w

        # Add to normalized dictionary
        if base in normalized:
            normalized[base] += freq
        else:
            normalized[base] = freq

    level_count = {
        "A1":0, 
        "A2":0,
        "B1":0, 
        "B2":0,
        "C1":0, 
        "C2":0,
        "others": 0
    }

    for word, freq in normalized.items():
        word_clean = word.lower()

        if word_clean in cefr_dict:
            level = cefr_dict[word_clean]
            level_count[level] += 1
        else:
            level_count["others"] += 1

    return level_count



def display_cefr_stats(cefr_result):
    total = sum(cefr_result.values())

    # Determine which CEFR level (A1–C2) dominates
    core_levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    core_only = {lvl: cefr_result.get(lvl, 0) for lvl in core_levels}
    dominant_level = max(core_only, key=core_only.get)
    dominant_count = core_only[dominant_level]

    print("\n======= CEFR Vocabulary Profile =======\n")
    print(f"{'Level':<7} {'Count':>10}   {'Percent':>8}")
    print("-" * 35)

    for level, count in cefr_result.items():
        pct = (count / total * 100) if total > 0 else 0
        print(f"{level:<7} {count:>10,}   {pct:>7.2f}%")

    print(
        f"From A1 to C2, the level with the most unique words is {dominant_level} "
        f"with {dominant_count:,} occurrences."
    )
    print("=======================================\n")

def running_cefr_excelsheet():
    excel_file = "ENGLISH_CERF_WORDS.xlsx"     # CHANGE this to your filename
    output_json = "cefr_words.json"

    print("Loading Excel file...")
    cefr_dict = load_cefr_dictionary(excel_file)

    print(f"Loaded {len(cefr_dict)} CEFR entries.")
    print("Saving dictionary as JSON...")

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(cefr_dict, f, indent=4, ensure_ascii=False)

    print(f"Saved CEFR dictionary to {output_json}")

