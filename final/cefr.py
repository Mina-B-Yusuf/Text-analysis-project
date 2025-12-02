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

def cefr_levels(words_dic, cefr_dict):

    level_count = {
        "A1":0, 
        "A2":0,
        "B1":0, 
        "B2":0,
        "C1":0, 
        "C2":0,
        "others": 0
    }

    for word, freq in words_dic.items():
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

