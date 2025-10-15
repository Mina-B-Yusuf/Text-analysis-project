with open("sample.txt", "r") as f:
    print(f.readline())
    Once upon a time there was a flower.
The flower was yellow and bright.
It grew beside a calm river.

def number_of_lines_f(text):
    number_of_lines = 0
    for line in text:
        number_of_lines += 1
    return number_of_lines

def number_of_words_f(text):
    number_of_words = 0
    for line in text:
        words = line.split()
        for word in words:
            number_of_words += 1
    return number_of_words

def number_of_characters_f(text):
    number_of_character = 0
    for line in text:
        for char in line:
            if char != ' ':
                number_of_character += 1
    return number_of_character

def average_words_per_line_f(text):
    number_of_lines = 0
    number_of_words = 0
    average_words_per_lines = []

    for line in text:
        number_of_lines += 1
        words = line.split()
        for word in words:
            number_of_words += 1
        average_words_per_lines.append(number_of_words)

    average_words_per_line = (sum(average_words_per_lines))/(number_of_lines)
    return average_words_per_line

def average_character_per_word_f(text):
    average_character_per_words = []
    char = 0
    number_of_words = 0
    for line in text:
        words = line.split()
        for word in words:
            number_of_words += 1
            char = len(word)
            average_character_per_words.append(char)
    average_character_per_word = (sum(average_character_per_words))/(number_of_words)
    return average_character_per_word

def top_10_most_common_words(text):
    list_of_words = []
    for line in text:
        words = line.split()
        for word in words:
            list_of_words.append(word.lower())
    
    frequencies = []
    for word in list_of_words :
        frequencies.append(list_of_words.count(word))
    frequencies.sort(reverse=True)
    
    list_of_words_in_order = []
    for word in list_of_words:
        if list_of_words.count(word) == frequencies[0]:
            frequencies.pop(0)
            list_of_words_in_order.append(word)
    return list_of_words_in_order[ : :10]


            
def distribution_of_words(text):
    average_word_length_per_line = []
    for line in text:
        words = line.split()
        words = 0
        number of character
        for word in words:
            number_of_characters = len(word)


def unique_words(text):
    list_of_words = []
    for line in text:
        words = line.split()
        for word in words:
            list_of_words.append(word.lower())
    
    frequencies = []
    for word in list_of_words :
        frequencies.append(list_of_words.count(word))
    frequencies.sort(reverse=True)
    
    list_of_words_in_order = []
    for word in list_of_words:
        if list_of_words.count(word) == frequencies[0]:
            frequencies.pop(0)
            list_of_words_in_order.append(word)
    return list_of_words_in_order[ : :-10]


def words_that_appear_once(text):
        list_of_words = []
    for line in text:
        words = line.split()
        for word in words:
            list_of_words.append(word.lower())
    
    frequencies = []
    for word in list_of_words :
        frequencies.append(list_of_words.count(word))
    frequencies.sort(reverse=True)
    
    list_of_words_in_order = []
    for word in list_of_words:
        if list_of_words.count(word) == frequencies[0]:
            frequencies.pop(0)
            list_of_words_in_order.append(word)
    return list_of_words_in_order[ : :-10]




