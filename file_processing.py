##file processing
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
    upper_case_letters_number = 0 
    number_of_lines = 0
    number_of_spaces = 0
    shortest_sentence = None
    longest_sentence = None

    #-------------line variables ---------
    for line in text:
        number_of_lines += 1
        words_per_line = 0
        words = line.split()
        sentence_lengths.append(len(words))

        #--------------short and long sentence -----------
        if len(words) < len(shortest_sentence) or shortest_sentence == None :
            shortest_sentence = line.strip()
        elif len(words) > len(longest_sentence) or longest_sentence == None:
            longest_sentence = line.strip()

        #----------Character variables----------
        for char in line:
            if char == ' ':
                number_of_spaces += 1
            elif char.isalpha():
                if char not in characters_dic:
                    characters_dic[char] = 1
                else:
                    characters_dic[char] += 1
                if char.isupper():
                    upper_case_letters_number += 1

            #-------Punctuation Varaibles  ----------
            elif char in ".,!?;:-—()[]\"'" and not in :
                number_of_punctuation += 1 
    

        #--------------word variables ----------
        for word in words:
            word = word.lower().strip(".,!?;:-—()[]\"'")
            words_per_line += 1
            word_lengths.append(len(word))
            if word in words_dic:
                words_dic[word] += 1
            elif word not in words_dic:
                words_dic[word] = 1

        words_per_lines_list.append(words_per_line)

            
    return number_of_lines, number_of_spaces, words_list, number_of_letters, number_of_punctuation, word_lengths, sentence_lengths, shortest_sentence, longest_sentence, words_per_lines_list, upper_case_letters_number

number_of_lines, number_of_spaces, words_list, number_of_letters, number_of_punctuation, word_lengths, sentence_lengths, shortest_sentence, longest_sentence, words_per_lines_list, upper_case_letters_number = process_file(text)
