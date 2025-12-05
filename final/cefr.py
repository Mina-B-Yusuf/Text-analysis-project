import json

#Loading data
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


#main cateorizing function
def cefr_levels(data, cefr_dict, reverse_verb_dict):
    normalized = {}

    # --- normalize words (verbs → base form) ---
    for word, freq in data["words_dic_all"]["words_dic"].items():
        w = word.lower()

        if w in reverse_verb_dict:
            base = reverse_verb_dict[w]
        else:
            base = w

        normalized[base] = normalized.get(base, 0) + freq

    level_count = {
        "A1": 0,
        "A2": 0,
        "B1": 0,
        "B2": 0,
        "C1": 0,
        "C2": 0,
        "names": 0,
        "others": 0
    }

    # ← add this block
    morphology = [
        (" s", ""),
        ("ies", "y"),
        ("es", ""),
        ("s", ""),
        ("ed", ""),
        ("ing", ""),
        ("eth", ""),
        ("est", ""),
        ("en", ""),
    ]

    unknown_words = set()
    names_lower = set(n.lower() for n in data["words_dic_all"]["names"])


    for word, freq in normalized.items():
        word_clean = word.lower()

        # 1. Direct CEFR match
        if word_clean in cefr_dict:
            level_count[cefr_dict[word_clean]] += 1
            continue

        # 2. Multi-word expressions (e.g. "able to")
        if " " in word_clean:
            parts = word_clean.split()
            classified_any = False
            for p in parts:
                p_clean = p.lower()
                if p_clean in cefr_dict:
                    level_count[cefr_dict[p_clean]] += 1
                    classified_any = True
            if classified_any:
                continue

        # 3. Morphological stripping using suffix table
        matched = False
        for suf, repl in morphology:
            if word_clean.endswith(suf) and len(word_clean) > len(suf):
                base = word_clean[:-len(suf)] + repl
                if base in cefr_dict:
                    level_count[cefr_dict[base]] += 1
                    matched = True
                    break

        if matched:
            continue

        # 4. Names
        if word_clean in names_lower:
            level_count["names"] += 1
            continue


        # 5. Others + collect unknown
        unknown_words.add(word_clean)
        level_count["others"] += 1

    # write unknown words once
    with open("unknown_words.txt", "w", encoding="utf-8") as f:
        for w in sorted(unknown_words):
            f.write(w + "\n")

    return level_count



#Display stats
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
        f"From A1 to C2, the level with the most words is {dominant_level} "
        f"with {dominant_count:,} occurrences."
    )
    print("=======================================\n")




