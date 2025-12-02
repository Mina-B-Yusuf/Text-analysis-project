import pandas as pd
import json

def load_cefr_dictionary(filepath):
    df = pd.read_excel(filepath)

    # Ensure we skip the first header rows
    df = df.iloc[2:, :]    # skip header rows (since your real data starts at row 3)

    cefr_dict = {}

    for _, row in df.iterrows():
        word = str(row[0]).strip().lower()
        level = str(row[1]).strip().upper()

        # Handle cases like "tranquilize/ tranquillise"
        if "/" in word:
            variants = [w.strip() for w in word.split("/")]
            for variant in variants:
                cefr_dict[variant] = level
        else:
            cefr_dict[word] = level

    return cefr_dict


def create_verb_dictionary(excel_path, output_json):
    # Load Excel file
    df = pd.read_excel(excel_path)

    # Skip header row if needed — adjust based on your sheet layout
    df = df.iloc[1:, :]

    verb_dict = {}

    for _, row in df.iterrows():
        base = str(row[0]).strip().lower()

        if base == "" or base == "nan":
            continue

        variants = set()

        # Gather all forms in all columns
        for col in row.index:
            val = str(row[col]).strip().lower()
            if val != "" and val != "nan":
                variants.add(val)

        # Always include base form
        variants.add(base)

        # Convert set → sorted list
        verb_dict[base] = sorted(variants)

    # Save dictionary to JSON file
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(verb_dict, f, ensure_ascii=False, indent=4)

    print(f"Verb dictionary created successfully and saved as {output_json}.")


# Run it directly
if __name__ == "__main__":
    create_verb_dictionary(
        excel_path="Verbs.xlsx",   # change if needed
        output_json="verb_forms.json"
    )





def load_cefr_json(json_path="cefr_words.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        cefr_dict = json.load(f)
    return cefr_dict


def cefr_levels(data, cefr_dict, reverse_verb_dict):
    normalized_dict = {}

    for word, freq in word_dic.items():
        w = word.lower()

        if w in reverse_verb_dict:      # it’s a verb form
            base = reverse_verb_dict[w]
        else:
            base = w

        # accumulate counts
        normalized_dict[base] = normalized_dict.get(base, 0) + freq

    level_count = {
        "A1":0, 
        "A2":0,
        "B1":0, 
        "B2":0,
        "C1":0, 
        "C2":0,
        "others": 0
    }

    for word, freq in data["words_dic_all"]["words_dic"].items():
        word_clean = word.lower()

        if word_clean in cefr_dict:
            level = cefr_dict[word_clean]
            level_count[level] += freq
        else:
            level_count["others"] += freq

    return level_count



def display_cefr_stats(cefr_result):
    print("\n======= CEFR Vocabulary Profile =======\n")
    for level, count in cefr_result.items():
        print(f"{level:<7} : {count}")
    print("\n=======================================\n")


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

