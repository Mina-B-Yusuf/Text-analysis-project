##file processing


def process_file(text):


    words_per_lines_list = []
    number_of_letters = 0
    word_lengths = []
    number_of_punctuation = 0


    #-------------line variables ----------
    sentence_lengths = []
    number_of_lines = 0
    for line in text:
        number_of_lines += 1
        words_per_line = 0
        words = line.split()
        sentence_lengths.append(len(words))

    #--------------short and long sentence -----------
    shortest_sentence = None
    longest_sentence = None
        if shortest_sentence == None or len(words) < len(shortest_sentence.split()):
            shortest_sentence = line.strip()
        if longest_sentence == None or len(words) > len(longest_sentence.split()):
            longest_sentence = line.strip()

    #----------Character variables----------
    number_of_spaces = 0
    characters_dic = {
    "letters": {
        "uppercase_letters": {},
        "lowercase_letters": {}
    },
    "punctuation_number": {}
    }
        for char in line:
            if char == ' ':
                number_of_spaces += 1
            elif char.isupper():
                if char not in uppercase_letters:
                    uppercase_letters[char] = 1
                else:
                    uppercase_letters[char] += 1
            elif char.islower():
                if char not in lowercase_letters :
                    lowercase_letters[char] = 1
                else:
                    lowercase_letters[char] += 1

            #-------Punctuation Varaibles  ----------
            elif char in ".,!?;:-—()[]\"'" :
                if char not in punctuation_number:
                    punctuation_number[char] = 1
                else:
                    punctuation_number[char] += 1 
     
    words_dic = {}
        #--------------word variables ----------
        for word in words:
            word = word.lower().strip(".,!?;:-—()[]\"'")
            words_per_line += 1
            word_lengths.append(len(word))
            if word in words_dic:
                words_dic[word] += 1
            else:
                words_dic[word] = 1

        words_per_lines_list.append(words_per_line)

            
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

proccesed_text_data = process_file(text)

def _(text):
    sentence_from_prev_line =
    for line in text:
        
        sentece_from_prev_line = ''
        prev_i = 0 
        i = 0
        sentences_in_line = [] 
        while i < len(line):
            index = i
            if i in "!.?":
                sentence = [prev_i : i + 1]
                sentences_in_line.append(sentence)
                prev_i = i
                if prev_i == 0 and sentence_from_prev_line != '':
                    whole_sentence = sentence_from_prev_line
                    whole_sentence += line[prev_i : i + 1]
                    sentence_from_prev_line = ''
                    sentences_in_line.append(whole_sentence)
            elif prev_i != index and i == len(line) :
                sentence_from_prev_line += [prev_i : len(line)+1] 
            i += 1
        for sentnece in sentences_in_line:
            #functions 
