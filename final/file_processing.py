import json
import string
import re


#========================================================================================================================
# VARIABLE FUNCTIONS
#========================================================================================================================

#=============================== CHARACTER VARIBALES ==============================================

def character_variables_function(sentence, data):

    letters_upper = data["characters_dic"]["letters"]["uppercase"]
    letters_lower = data["characters_dic"]["letters"]["lowercase"]
    punctuation = data["characters_dic"]["punctuation"]

    spaces = data["characters_dic"]["spaces"]
    digits = data["characters_dic"]["digits"]

    punct_set = ".,!?;:-—()[]\"'"

    for char in sentence:

        if char.isalpha():
            if char.isupper():
                letters_upper[char] = letters_upper.get(char, 0) + 1
            else: 
                letters_lower[char] = letters_lower.get(char, 0) + 1

        elif char in punct_set:
            punctuation[char] = punctuation.get(char, 0) + 1

        elif char == " ":
            spaces += 1

        elif char.isdigit():
            digits += 1

    data["characters_dic"]["spaces"] = spaces
    data["characters_dic"]["digits"] = digits

    return data



#=============================== WORD VARIBALES ==============================================

def word_var_function(words, data):

    words_dic = data["words_dic_all"]["words_dic"]
    word_lengths = data["words_dic_all"]["word_lengths"]
    wps_list = data["words_dic_all"]["words_per_sentence_list"]
    names = data["words_dic_all"]["names"]

    words_per_line = 0

    allowed = string.ascii_letters + "'"
    roman_pattern = r"^(m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3}))$"

    count = 1

    for word in words:
        if word[0].isupper() and count != 1: #detecting names 
            names.append(word.strip(".,;:!?\"'"))

        count += 1

        # --- clean word  ---
        clean_chars = []
        for ch in word:
            if ch in allowed:
                clean_chars.append(ch)
            else:
                clean_chars.append(" ")
        word = "".join(clean_chars)
        word = word.strip().lower()

        if not word:
            continue

        if word.startswith("www"):
            continue

        if re.fullmatch(roman_pattern, word):
            continue 

        # Skip numeric-only words
        if word.isdigit():
            continue

        # Skip single-letter junk
        if len(word) == 1 and word not in ("a", "i"):
            continue

        # Count word
        words_per_line += 1
        word_lengths.append(len(word))
        words_dic[word] = words_dic.get(word, 0) + 1

    # Add total word count for the line
    wps_list.append(words_per_line)
    return data


#=============================== SENTENCE VARIBALES ==============================================

def sentence_var_function(words, data):
    data["sentence_lengths"].append(len(words))
    return data

def shortest_and_longest_sentence(sentence, words, data):
    if data["shortest_sentence"] is None or len(words) < len(data["shortest_sentence"].split()):
        data["shortest_sentence"] = sentence
    if data["longest_sentence"] is None or len(words) > len(data["longest_sentence"].split()):
        data["longest_sentence"] = sentence
    return data


#========================================================================================================================
# Filtering out invalid sententeces  
#========================================================================================================================

def is_valid_sentence(sentence, words, abbreviations): #Returns True if this sentence should be analyzed.
    if len(words) < 2: #skipping sentences less than 2 characters, e.g. "a?"
        return False
    if sentence.isupper(): #skipping sentences with all capital letters, e.g. "ALLCOT."
        return False
    if sentence.strip() in ['"', '”', '“', "’", "‘"]: #skipping quoates  
        return False
    if sentence.strip().startswith(("“", '"')) and len(words) <= 2: 
        return False

    last_word = words[-1].lower() 
    if last_word in abbreviations: # skipping dots used for abbreviations, e.g. "DR."
        return False

    if len(words) >= 2:
        last_two = words[-2:]
        if all(len(w) == 2 and w[1] == '.' for w in last_two):
            return False

    return True


#========================================================================================================================
# SHORT NAMES
#========================================================================================================================

def analyze_sentence(sentence, words, data):
    data = sentence_var_function(words, data)
    data = shortest_and_longest_sentence(sentence, words, data)
    data = character_variables_function(sentence, data)
    data = word_var_function(words, data)
    return data


#========================================================================================================================
# FILE PROCESSING FUNCTION
#========================================================================================================================


def process_file(file_object):

    #=============================== Initialize global counters and storage ==============================================
    data = {
        "sentence_lengths": [],
        "shortest_sentence": None,
        "longest_sentence": None,
        "paragraph_count" : 0, 
        "characters_dic": {
            "letters": {"uppercase": {}, "lowercase": {}},
            "punctuation": {},
            "spaces": 0,
            "digits": 0
        },
        "words_dic_all": {
            "words_dic": {},
            "word_lengths": [],
            "words_per_sentence_list": [],
            "names": []
        }
    }

    # possible abbreviations to skip 
    abbreviations = {
        "mr.", "mrs.", "dr.", "ms.", "prof.", "sr.", "jr.", "st.",
        "vs.", "etc.", "u.s.", "e.g.", "i.e."
    }
    previous_line_blank = False
    sentence_from_prev_line = ""


    #============================================= Main loop  ==============================================

    paragraph_started = False

    for line in file_object:
        
        raw = line
        if raw.strip() == "":
            paragraph_started = False
            line = raw.strip()
        else:
            if not paragraph_started:
                data["paragraph_count"] += 1
            paragraph_started = True
            line = raw.strip()


        if sentence_from_prev_line: # Combine with leftover sentence from previous line
            line = sentence_from_prev_line + " " + line
            sentence_from_prev_line = ""
            
        line_len = len(line)
        i = 0
        start_i = 0
        line_chars = line  # local reference for speed

        while i < line_len:

            # check ellipses
            if i + 2 < line_len and line_chars[i] == '.' and line_chars[i+1] == '.' and line_chars[i+2] == '.':
                i += 3
                continue

            ch = line_chars[i]

            # check sentence-ending punctuation
            if ch == '.' or ch == '!' or ch == '?':

                # next char check (same logic, faster)
                if i + 1 == line_len:
                    next_char_ok = True
                else:
                    next_char_ok = line_chars[i+1] in (' ', '"', '”', '’')

                if next_char_ok:
                    sentence = line_chars[start_i:i+1].strip()
                    words = sentence.split()

                    if is_valid_sentence(sentence, words, abbreviations):
                        data = analyze_sentence(sentence, words, data)
                    start_i = i + 1

            i += 1

        # leftover text for next line
        if start_i < line_len:
            sentence_from_prev_line = line_chars[start_i:].strip()
        else:
            sentence_from_prev_line = ""


    if sentence_from_prev_line: # If leftover sentence remains at end of file, process it
        words = sentence_from_prev_line.split()
        data = analyze_sentence(sentence_from_prev_line, words, data)
    return data


#========================================================================================================================
# SAVING PROCESSED DATA
#========================================================================================================================

def run_processing_from_main(filename):
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            processed_text_data = process_file(f)
    except FileNotFoundError:
        print("Error: File not found. Please check the filename and try again.")
        return None

    with open("processed_data.json", "w", encoding="utf-8") as json_file:
        json.dump(processed_text_data, json_file, indent=4, ensure_ascii=False)

    print(f"Processing complete. Results saved to processed_data.json from {filename}")
    return processed_text_data