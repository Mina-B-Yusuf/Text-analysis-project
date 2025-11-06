
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

        word = word.lower().strip(".,!?;:-—()[]\"'") # lowering all letters and striping of quotation marks
        if not word:
            continue

        if word.isdigit(): # Skip numeric-only words (e.g., "2001", "50") 
            continue

        # --- Skip single-letter words (like "z") ---
        # (You can remove this check if you want to keep "a" or "I")
        if len(word) == 1 and word not in ("a", "i"):
            continue

        # --- Skip junk words that are mostly punctuation ---
        if all(ch in ".,!?;:-—()[]\"'" for ch in word):
            continue

        # Count the word
        words_per_line += 1
        data["words_dic_all"]["word_lengths"].append(len(word))
        if word in data["words_dic_all"]["words_dic"]:
            data["words_dic_all"]["words_dic"][word] += 1
        else:
            data["words_dic_all"]["words_dic"][word] = 1

    # Add total word count for the line
    data["words_dic_all"]["words_per_sentence_list"].append(words_per_line)
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

    if len(words) >= 2 and all(len(w) == 2 and w[1] == '.' for w in words[-2:]): #skipping character with only 2 character "U.", and where the second cahracter is a "." for two last characters of sentence, e.g. U.S.
        return False

    return True


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
            "words_per_sentence_list": []
        }
    }

    # possible abbreviations to skip 
    abbreviations = [
        "mr.", "mrs.", "dr.", "ms.", "prof.", "sr.", "jr.", "st.",
        "vs.", "etc.", "u.s.", "e.g.", "i.e."
    ]
    previous_line_blank = False
    sentence_from_prev_line = ""


    #============================================= Main loop  ==============================================


    for line in text:
        line = line.strip()
        
        #counting paragraphs 
        if line == "":
            if not previous_line_blank: #for empty lines, = start of a paragraph or end of a paragraph
                data["paragraph_count"] += 1
            previous_line_blank = True
            continue 
        previous_line_blank = False

        if sentence_from_prev_line: # Combine with leftover sentence from previous line
            line = sentence_from_prev_line + " " + line
            sentence_from_prev_line = ""

        start_i = 0
        i = 0
        while i < len(line):
    
            if line[i:i+3] == "...": # skipping ellipses, e.g. "what..."
                i += 3
                continue 

        
            if line[i] in ".!?": # detecting sentence with punctuation
                next_char_ok = (i + 1 == len(line)) or (line[i + 1] in ' "”’') # to check if its end of line or if there is a e,g, - road." marking or a space

                if next_char_ok: # Get the sentence
                    sentence = line[start_i:i+1].strip()
                    words = sentence.split()

                    if is_valid_sentence(sentence, words, abbreviations):
                        data = analyze_sentence(sentence, data) #deriving needed data
                    start_i = i + 1 #restarting starting index

            i += 1

        if start_i < len(line): # If text remains after punctuation, carry it to next line
            sentence_from_prev_line = line[start_i:].strip()


    if sentence_from_prev_line: # If leftover sentence remains at end of file, process it
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