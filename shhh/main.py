from stats_functions import basic_statistics, word_analysis, sentence_analysis, character_analysis, data

while True: #keep looping forever — until I manually tell it to stop
    print ('''--- Menu ---
    1. Load text file
    2. display basic statistics
    3. word frequency analysis
    5. character analysis
    6. export resultat
    7. exit''')
    choice = int(input('enter your choice: '))

    if choice == 1 : # load text file
        print (1) 
    elif choice == 2: # display basic statistics
        print("--------- Basic Statistics---------")
        basic_statistics(data)
        print()

    elif choice == 3: # word frequency analysis
        print ("--------- Word Analysis ---------")
        word_analysis(data)
        print()

    elif choice == 4:
        print ("--------- Sentence Analysis ---------")
        sentence_analysis(data)
        print()

    elif choice == 5:
        print ("--------- Character Analysis ---------")
        character_analysis(data)
        print()

    elif choice == 6:
        print (6)   # export resultat


    else: 
        break      #break the loop
        print (7)   # exit
    print('press enter to continue...')
