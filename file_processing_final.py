with open("sample.txt", "r", encoding="utf-8") as file:
    text = file.readlines() 
 


def process_file(text):
    words_dic = {}
    characters_dic = {}
    words_per_lines_list = []
    number_of_letters = 0
    word_lengths = []
    sentence_lengths = []
    number_of_punctuation = 0
    number_of_lines = 0
    number_of_spaces = 0
    shortest_sentence = None
    longest_sentence = None
    upper_case_letters_number = 0

    #unfinishes sentence from previous line
    sentence_from_prev_line = ""

    #-------------line variables ----------
    for line in text:
        line = line.strip()
        if line == "":
            continue

        # 🔹 Combine previous leftover if there is one
        if sentence_from_prev_line != "":
            line = sentence_from_prev_line + " " + line
            sentence_from_prev_line = ""

        start_i = 0
        i = 0

        # ---------- detect sentence-ending punctuation ----------
        while i < len(line):
            if line[i] in ".!?":  # found sentence end
                sentence = line[start_i:i+1].strip()
                start_i = i + 1   # next sentence starts after punctuation

                # Now treat the sentence like you treated each line before ↓↓↓
                number_of_lines += 1
                words_per_line = 0
                words = sentence.split()
                sentence_lengths.append(len(words))

                # shortest and longest sentence
                if shortest_sentence == None or len(words) < len(shortest_sentence.split()):
                    shortest_sentence = sentence
                if longest_sentence == None or len(words) > len(longest_sentence.split()):
                    longest_sentence = sentence

                # character variables
                for char in sentence:
                    if char == ' ':
                        number_of_spaces += 1
                    elif char.isalpha():
                        number_of_letters += 1
                        if char not in characters_dic:
                            characters_dic[char] = 1
                        else:
                            characters_dic[char] += 1
                        if char.isupper():
                            upper_case_letters_number += 1
                    elif char in ".,!?;:-—()[]\"'":
                        number_of_punctuation += 1 

                # word variables
                for word in words:
                    word = word.lower().strip(".,!?;:-—()[]\"'")
                    words_per_line += 1
                    word_lengths.append(len(word))
                    if word in words_dic:
                        words_dic[word] += 1
                    else:
                        words_dic[word] = 1

                words_per_lines_list.append(words_per_line)

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
        'number_of_lines'            : number_of_lines           , 
        'number_of_spaces'           : number_of_spaces          , 
        'words_dic'                  : words_dic                 ,
        'characters_dic'             : characters_dic            , 
        'number_of_punctuation'      : number_of_punctuation     , 
        'word_lengths'               : word_lengths              ,
        'sentence_lengths'           : sentence_lengths          ,
        'shortest_sentence'          : shortest_sentence         ,
        'longest_sentence'           : longest_sentence          ,
        'words_per_lines_list'       : words_per_lines_list      ,
        'upper_case_letters_number'  : upper_case_letters_number
    }