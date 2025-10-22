with open("sample.txt", "w") as f:
    f.write("""
Once upon a time there was a flower.
The flower was yellow and bright.
It grew beside a calm river.
""")
with open("sample.txt", "r", encoding="utf-8") as file:
    text = file.readlines() 
    
import matplotlib.pyplot as plt

`##file processing

def process_file(text):
    words_list = {}
    words_per_lines_list = []
    number_of_letters = 0
    word_lengths = []
    sentence_lengths = []
    number_of_punctuation = 0
    upper_case_letters_number = 0 
    number_of_lines = 0
    number_of_spaces = 0
    shortest_sentence = 'a'
    longest_sentence = 'a'

    for line in text:
        number_of_lines += 1
        words_per_line = 0
        words = line.split()
        sentence_lengths.append(len(words))

        if len(words) < len(shortest_sentence) :
            shortest_sentence = line.strip()
        elif len(words) > len(longest_sentence):
            longest_sentence = line.strip()


        for char in line:
            if char == ' ':
                number_of_spaces += 1
            elif char.isalpha():
                number_of_letters += 1
                if char.isupper():
                    upper_case_letters_number += 1


            elif char in ".,!?;:-—()[]\"'":
                number_of_punctuation += 1 
    
        for word in words:
            words_per_line += 1
            word_lengths.append(len(word.lower().strip(".,!?;:-—()[]\"'")))
            if word.lower().strip(".,!?;:-—()[]\"'") in words_list:
                words_list[word] += 1
            elif word.lower().strip(".,!?;:-—()[]\"'") not in words_list:
                words_list[word] = 1

        words_per_lines_list.append(words_per_line)

            
    return number_of_lines, number_of_spaces, words_list, number_of_letters, number_of_punctuation, word_lengths, sentence_lengths, shortest_sentence, longest_sentence, words_per_lines_list, upper_case_letters_number

number_of_lines, number_of_spaces, words_list, number_of_letters, number_of_punctuation, word_lengths, sentence_lengths, shortest_sentence, longest_sentence, words_per_lines_list, upper_case_letters_number = process_file(text)

##functions - word analysis
def top_10_most_common_words(text):
    top_10 = sorted(words_list.items(), key=lambda x: x[1], reverse=True)[:10]
    return top_10

##functions - sentence analysis

##functions - character analysis


##Display 

while True: #keep looping forever — until I manually tell it to stop
    print ('''--- Menu ---
    1. Load text file
    2. display basic statistics
    3. word frequency analysis
    4. sentence analysis
    5. character analysis
    6. export resultat
    7. exit''')
    choice = int(input('enter your choice'))
    if choice == 1 : # load text file
        print (1) 
    elif choice == 2: # display basic statistics
        

    elif choice == 3: # word frequency analysis
        print ('The top 10 most common words are: ', top_10)   
    elif choice == 4:
        print (4)   # sentence analysis
    elif choice == 5:
        print (5)   # character analysis
    elif choice == 6:
        print (6)   # export resultat
    else: 
        break      #break the loop
        print (7)   # exit
    print('press enter to continue...')



