import json


#========================================= functions =============================================

##character varaibles 
def character_variables_function(sentence, characters_dic):
    for char in sentence:
        if char.isupper():
            # uppercase letters
            if char not in characters_dic["letters"]["uppercase"]:
                characters_dic["letters"]["uppercase"][char] = 1
            else:
                characters_dic["letters"]["uppercase"][char] += 1

        elif char.islower():
            # lowercase letters
            if char not in characters_dic["letters"]["lowercase"]:
                characters_dic["letters"]["lowercase"][char] = 1
            else:
                characters_dic["letters"]["lowercase"][char] += 1

        elif char in ".,!?;:-—()[]\"'":
            # punctuation marks
            if char not in characters_dic["punctuation"]:
                characters_dic["punctuation"][char] = 1
            else:
                characters_dic["punctuation"][char] += 1

    return characters_dic


##sentence length 
def shortest_and_longest_sentence(words, sentence, shortest_sentence, longest_sentence):
    if shortest_sentence == None or len(words) < len(shortest_sentence.split()):
        shortest_sentence = sentence
    if longest_sentence == None or len(words) > len(longest_sentence.split()):
        longest_sentence = sentence  
    return shortest_sentence, longest_sentence

## word variable 
def word_var_function(words, words_dic_all):
    words_per_line = 0

    for word in words:
        word = word.lower().strip(".,!?;:-—()[]\"'")
        words_per_line += 1
        words_dic_all["word_lengths"].append(len(word))

        if word in words_dic_all["words_dic"]:
            words_dic_all["words_dic"][word] += 1
        else:
            words_dic_all["words_dic"][word] = 1

    words_dic_all["words_per_lines_list"].append(words_per_line)
    return words_dic_all

##sentence variables
def sentence_var_function(sentence, number_of_lines, sentence_lengths):
    number_of_lines += 1
    sentence_lengths.apppend(len(sentence)) 
    return number_of_lines, sentence_lengths




#========================================= processing file =============================================


def process_file(text):
    # ==================================================================
    # Initialize global counters and storage
    # ==================================================================
    #word 
    words = sentence.split()
    words_dic_all = {
        "words_dic": {},
        "word_lengths": [],
        "words_per_lines_list": []
    }

    #sentence 
    shortest_sentence = None
    longest_sentence = None
    number_of_lines = 0
    sentence_lengths = []

    #char 
    characters_dic = {
        "letters": {
            "uppercase": {},
            "lowercase": {}
        },
        "punctuation": {}
    }
    number_of_letters = 0

    # =================================================================
    # MAIN LOOP — Read each line and detect sentences
    # =================================================================

    sentence_from_prev_line = ""  # ✅ only once, before the loop starts

    for line in text:
        line = line.strip()
        if line == "":
            continue

        # Combine previous leftover if there is one
        if sentence_from_prev_line != "":
            line = sentence_from_prev_line + " " + line
            sentence_from_prev_line = ""  # now we clear it after merging

        start_i = 0
        i = 0




        #====================detect sentence-ending punctuation ===================
        while i < len(line):
            if line[i] in ".!?":  # found sentence end
                sentence = line[start_i:i+1].strip()
                start_i = i + 1   # next sentence starts after punctuation

                # Now treat the sentence like you treated each line before ↓↓↓
                number_of_lines, sentence_lengths = sentence_var_function(sentence, number_of_lines, sentence_lengths)
                words_per_line = 0
                words = sentence.split()

                # shortest and longest sentence
                shortest_sentence, longest_sentence = shortest_and_longest_sentence(words, sentence, shortest_sentence, longest_sentence)

                # character variables
                characters_dic = character_variables_function(sentence, characters_dic)

                # word variables
                words_dic_all = word_var_function(words, words_dic_all)



            i += 1

        # 🔹 if line ended with no punctuation, save the leftover
        if start_i < len(line):
            sentence_from_prev_line = line[start_i:].strip()

    # 🔹 If text ended but there’s still leftover sentence
    if sentence_from_prev_line != "":
        words = sentence_from_prev_line.split()
        number_of_lines += 1
        sentence_lengths.append(len(words))
        if shortest_sentence == None or len(words) < len(shortest_sentence.split()):
            shortest_sentence = sentence_from_prev_line
        if longest_sentence == None or len(words) > len(longest_sentence.split()):
            longest_sentence = sentence_from_prev_line

    # return like before
    return {
        "number_of_lines": number_of_lines,
        "characters_dic": characters_dic,
        "words_dic_all": words_dic_all,
        "sentence_lengths": sentence_lengths,
        "shortest_sentence": shortest_sentence,
        "longest_sentence": longest_sentence
    }

with open("sample.txt", "r", encoding="utf-8") as f:
    text = f.readlines()

processed_text_data = process_file(text)

with open("processed_data.json", "w", encoding="utf-8") as json_file:
    json.dump(processed_text_data, json_file, indent=4, ensure_ascii=False)

print("✅ Processing complete. Results saved to processed_data.json")