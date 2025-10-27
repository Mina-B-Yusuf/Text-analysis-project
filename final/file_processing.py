
import json

#========================================================================================================================
# VARIABLE FUNCTIONS
#========================================================================================================================

#=============================== CHARACTER VARIBALES ==============================================

def character_variables_function(sentence, data):
    for char in sentence:
        if char.isalpha():
            if char.isupper():
                if char not in data["characters_dic"]["letters"]["uppercase"]:
                    data["characters_dic"]["letters"]["uppercase"][char] = 1
                else:
                    data["characters_dic"]["letters"]["uppercase"][char] += 1
            elif char.islower():
                if char not in data["characters_dic"]["letters"]["lowercase"]:
                    data["characters_dic"]["letters"]["lowercase"][char] = 1
                else:
                    data["characters_dic"]["letters"]["lowercase"][char] += 1

        elif char in ".,!?;:-—()[]\"'":
            if char not in data["characters_dic"]["punctuation"]:
                data["characters_dic"]["punctuation"][char] = 1
            else:
                data["characters_dic"]["punctuation"][char] += 1

        elif char == " ":
            data["characters_dic"]["spaces"] += 1

        elif char.isdigit():
            data["characters_dic"]["digits"] += 1

    return data



#=============================== WORD VARIBALES ==============================================

def word_var_function(words, data):
    words_per_line = 0
    for word in words:
        word = word.lower().strip(".,!?;:-—()[]\"'")
        if not word:
            continue
        words_per_line += 1
        data["words_dic_all"]["word_lengths"].append(len(word))
        if word in data["words_dic_all"]["words_dic"]:
            data["words_dic_all"]["words_dic"][word] += 1
        else:
            data["words_dic_all"]["words_dic"][word] = 1
    data["words_dic_all"]["words_per_lines_list"].append(words_per_line)
    return data



#=============================== SENTENCE VARIBALES ==============================================

def sentence_var_function(sentence, data):
    data["sentence_lengths"].append(len(sentence.split()))
    return data

def shortest_and_longest_sentence(sentence, data):
    words = sentence.split()
    if data["shortest_sentence"] is None or len(words) < len(data["shortest_sentence"].split()):
        data["shortest_sentence"] = sentence
    if data["longest_sentence"] is None or len(words) > len(data["longest_sentence"].split()):
        data["longest_sentence"] = sentence
    return data


#========================================================================================================================
# SHORT NAMES
#========================================================================================================================

def analyze_sentence(sentence, data):
    data = sentence_var_function(sentence, data)
    data = shortest_and_longest_sentence(sentence, data)
    data = character_variables_function(sentence, data)
    data = word_var_function(sentence.split(), data)
    return data





#========================================================================================================================
# FILE PROCESSING FUNCTION
#========================================================================================================================



def process_file(text):

    #=============================== Initialize global counters and storage ==============================================

    data = {
        "sentence_lengths": [],
        "shortest_sentence": None,
        "longest_sentence": None,
        "characters_dic": {
            "letters": {"uppercase": {}, "lowercase": {}},
            "punctuation": {},
            "spaces": 0,
            "digits": 0
        },
        "words_dic_all": {
            "words_dic": {},
            "word_lengths": [],
            "words_per_lines_list": []
        }
    }

    # List of known abbreviations (lowercase)
    ABBREVIATIONS = ["mr.", "mrs.", "dr.", "ms.", "prof.", "sr.", "jr.", "st.", "vs.", "etc.", "u.s.", "e.g.", "i.e."]


 #=============================== MAIN LOOP — Read each line and detect sentences ==============================================
    sentence_from_prev_line = ""

    for line in text:
        line = line.strip()
        if not line:
            continue

        # Combine with any leftover from previous line
        if sentence_from_prev_line:
            line = sentence_from_prev_line + " " + line
            sentence_from_prev_line = ""

        start_i = 0
        i = 0
        while i < len(line):
            # === Handle ellipses (skip splitting here) ===
            if line[i:i+3] == "...":
                i += 3
                continue

            # === Check if this is a sentence-ending punctuation ===
            if line[i] in ".!?":
                # Check the character after punctuation
                next_char_ok = (i + 1 == len(line)) or (line[i + 1] in ' "”’')

                if next_char_ok:
                    # Get the text up to this point
                    sentence_candidate = line[start_i:i+1].strip()
                    words = sentence_candidate.split()

                    if words:
                        last_word = words[-1].lower()

                        # === Check if it's an abbreviation (e.g., "Mr.") ===
                        if last_word in ABBREVIATIONS:
                            i += 1
                            continue

                        # === Check for initials like "U. S." ===
                        if len(words) >= 2 and all(len(w) == 2 and w[1] == '.' for w in words[-2:]):
                            i += 1
                            continue

                        # All checks passed — treat as end of sentence
                        sentence = line[start_i:i+1].strip()
                        data = analyze_sentence(sentence, data)
                        start_i = i + 1

            i += 1

        # If there is text remaining after the last punctuation, save it for next line
        if start_i < len(line):
            sentence_from_prev_line = line[start_i:].strip()

    # After all lines, if something is left, treat it as the final sentence
    if sentence_from_prev_line:
        data = analyze_sentence(sentence_from_prev_line, data)

    return data


#========================================================================================================================
# SAVING PROCESSED DATA
#========================================================================================================================

def run_processing_from_main(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.readlines()

    processed_text_data = process_file(text)

    with open("processed_data.json", "w", encoding="utf-8") as json_file:
        json.dump(processed_text_data, json_file, indent=4, ensure_ascii=False)

    print(f"Processing complete. Results saved to processed_data.json from {filename}")