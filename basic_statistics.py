 
#importing data from processing the text 

number_of_words = sum(data[words_dic].values()) #getting the number of word from th dictionary
total_characters = data[number_of_letters] + data[number_of_punctuation]  #adding all the characters together
average_words_per_line = round((sum(data[words_per_lines_list])) // (data[number_of_lines]), 2)
average_character_per_word = round(data[total_characters]/data[number_of_words], 2)


print ('----Basic Statistics----') # Headline
print ('Number of lines: ', data[number_of_lines])
print ('Number of words: ', number_of_words)
print ('Number of characters: ', total_characters)
print ('Average word per line: ', average_words_per_line )
print ('Average characters per word: ' (sum(sum(number_of_letters, number_of_punctuation)))//(number_of_words), )
